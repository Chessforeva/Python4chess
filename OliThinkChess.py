#--
#-- OliThink5 Java(c) Oliver Brausch 28.Jan.2010, ob112@web.de, http://home.arcor.de/dreamlike
#-- python port by http://chessforeva.blogspot.com

import time
import random

if(True):

      global VER, PAWN, KNIGHT, KING, ENP, BISHOP, ROOK, QUEEN, CNODES, HEUR, pval, cap_val, pawnrun
      global HSIZEB, HMASKB, HINVB, HSIZEP, HMASKP, HINVP, hashDB, hashDP, hashb, stack, stack
      global hashxor, rays, pmoves, pcaps, nmoves, kmoves, _knight, _king, BITi, LSB, BITC, crevoke, nmobil, kmobil
      global pawnprg, pawnfree, pawnfile, pawnhelp, movelist, movenum, p_v, pvlength, kvalue, iter, pieceChar
      global searchtime, maxtime, starttime, sabort, noabort, sd, count, flags
      global mat_, onmove, engine, kingpos, pieceb, colorb, irbuf, sfen
      global r_x, r_y, r_z, r_w, r_carry, bmask45, bmask135, killer, history, eval1, nodes_, q_nodes, Nonevar
      global tm, mps, base, inc, post_
      global movemade

      def woutput(txt):

        print(txt)

      woutput("Loading")

      #-- it takes time to prepare this python based chess engine for a game  

      VER = "OliThink 5.3.0 Java port to python"
      #depth
      sd = 8
      #time in seconds
      tm = 20
      
      movemade = ""

      PAWN = 1
      KNIGHT = 2
      KING = 3
      ENP = 4
      BISHOP = 5
      ROOK = 6
      QUEEN = 7

      CNODES = 0xFFFF
      HEUR = 9900000
      pval = [ 0, 100, 290, 0, 100, 310, 500, 950 ]

      cap_val = [ 0, HEUR+1, HEUR+2, 0, HEUR+1, HEUR+2, HEUR+3, HEUR+4 ]

      pawnrun = [ 0, 0, 1, 8, 16, 32, 64, 128 ]

      HSIZEB = 0x200000
      HMASKB = HSIZEB - 1
      HINVB = 0xFFFFFFFF00000000 | (0xFFFFFFFF & ~HMASKB)

      HSIZEP = 0x400000
      HMASKP = HSIZEP - 1
      HINVP = 0xFFFFFFFF00000000 | (0xFFFFFFFF & ~HMASKP)

      hashDB = [0 for x in range(HSIZEB)]
      hashDP = [0 for x in range(HSIZEP)]
      hashb = 0
      hstack = [0 for x in range(0x800)]
      mstack = [0 for x in range(0x800)]

      hashxor = [0 for x in range(0x4096)]
      rays = [0 for x in range(0x10000)]
      pmoves = [[0 for x in range(64)] for x in range(2)]
      pcaps = [[0 for x in range(192)] for x in range(2)]
      nmoves = [0 for x in range(64)]
      kmoves = [0 for x in range(64)]
      _knight = [ -17,-10,6,15,17,10,-6,-15 ]

      _king = [ -9,-1,7,8,9,1,-7,-8 ]

      BITi = [0 for x in range(64)]
      LSB = [0 for x in range(0x10000)]
      BITC = [0 for x in range(0x10000)]
      crevoke = [0x3FF for x in range(64)]
      nmobil = [0 for x in range(64)]
      kmobil = [0 for x in range(64)]
      pawnprg = [[0 for x in range(64)] for x in range(2)]
      pawnfree = [[0 for x in range(64)] for x in range(2)]
      pawnfile = [[0 for x in range(64)] for x in range(2)]
      pawnhelp = [[0 for x in range(64)] for x in range(2)]
      movelist = [[0 for x in range(256)] for x in range(64)]
      movenum = [0 for x in range(64)]
      p_v = [[0 for x in range(64)] for x in range(64)]
      pvlength = [0 for x in range(64)]
      kvalue = [0 for x in range(64)]
      iter = 0
      pieceChar = "*PNK.BRQ"
      searchtime = 0
      maxtime = 0
      starttime = 0
      sabort = False
      noabort = False

      count = 0
      flags = 0
      mat_ = 0
      onmove = 0
      engine = -1
      kingpos = [0 for x in range(2)]
      pieceb = [0 for x in range(8)]
      colorb = [0 for x in range(2)]
      irbuf = ""

      sfen = "rnbqkbnr/pppppppp/////PPPPPPPP/RNBQKBNR w KQkq - 0 1"

      r_x = 30903
      r_y = 30903
      r_z = 30903
      r_w = 30903
      r_carry = 0

      bmask45 = [0 for x in range(64)]
      bmask135 = [0 for x in range(64)]
      killer = [0 for x in range(128)]
      history = [0 for x in range(0x1000)]

      eval1 = 0

      nodes_ = 0
      q_nodes = 0

      Nonevar = [ 13, 43, 149, 519, 1809, 6311, 22027 ]

      mps = 0
      base = 5
      inc = 0
      post_ = True

      def iif(ask, onTrue, onFalse):
        retval = onFalse
        if( ask ):
          retval = onTrue

        return retval

      def ISRANK(c):

        return (c >= "1"  and  c <= "8")

      def ISFILE(c):

        return (c >= "a"  and  c <= "h")

      def FROM(x):

        return ((x) & 63)

      def TO(x):

        return (((x) >> 6) & 63)

      def PROM(x):

        return (((x) >> 12) & 7)

      def PIECE(x):

        return (((x) >> 15) & 7)

      def ONMV(x):

        return (((x) >> 18) & 1)

      def CAP(x):

        return (((x) >> 19) & 7)

      def _TO(x):

        return ((x) << 6)

      def _PROM(x):

        return ((x) << 12)

      def _PIECE(x):

        return ((x) << 15)

      def _ONMV(x):

        return ((x) << 18)

      def _CAP(x):

        return ((x) << 19)

      def PREMOVE(f, p, c):

        return ((f) | _ONMV(c) | _PIECE(p))

      def RATT1(f):

        global  rays

        return rays[((f) << 7) | key000(BOARD(), f)]

      def RATT2(f):

        global  rays

        return rays[((f) << 7) | key090(BOARD(), f) | 0x2000]

      def BATT3(f):

        global  rays

        return rays[((f) << 7) | key045(BOARD(), f) | 0x4000]

      def BATT4(f):

        global  rays

        return rays[((f) << 7) | key135(BOARD(), f) | 0x6000]

      def RXRAY1(f):

        global  rays

        return rays[((f) << 7) | key000(BOARD(), f) | 0x8000]

      def RXRAY2(f):

        global  rays

        return rays[((f) << 7) | key090(BOARD(), f) | 0xA000]

      def BXRAY3(f):

        global  rays

        return rays[((f) << 7) | key045(BOARD(), f) | 0xC000]

      def BXRAY4(f):

        global  rays

        return rays[((f) << 7) | key135(BOARD(), f) | 0xE000]

      def ROCC1(f):

        return (RATT1(f) & BOARD())

      def ROCC2(f):

        return (RATT2(f) & BOARD())

      def BOCC3(f):

        return (BATT3(f) & BOARD())

      def BOCC4(f):

        return (BATT4(f) & BOARD())

      def RMOVE1(f):

        return (RATT1(f) & (~BOARD()))

      def RMOVE2(f):

        return (RATT2(f) & (~BOARD()))

      def BMOVE3(f):

        return (BATT3(f) & (~BOARD()))

      def BMOVE4(f):

        return (BATT4(f) & (~BOARD()))

      def RCAP1(f,c):

        global  colorb

        return (RATT1(f) & colorb[(c)^1])

      def RCAP2(f,c):

        global  colorb

        return (RATT2(f) & colorb[(c)^1])

      def BCAP3(f,c):

        global  colorb

        return (BATT3(f) & colorb[(c)^1])

      def BCAP4(f,c):

        global  colorb

        return (BATT4(f) & colorb[(c)^1])

      def ROCC(f):

        return (ROCC1(f) | ROCC2(f))

      def BOCC(f):

        return (BOCC3(f) | BOCC4(f))

      def RMOVE(f):

        return (RMOVE1(f) | RMOVE2(f))

      def BMOVE(f):

        return (BMOVE3(f) | BMOVE4(f))

      def RCAP(f,c):

        global  colorb

        return (ROCC(f) & colorb[(c)^1])

      def BCAP(f,c):

        global  colorb

        return (BOCC(f) & colorb[(c)^1])

      def SHORTMOVE(x):

        return ((x) & ((x)^BOARD()))

      def SHORTOCC(x):

        return ((x) & BOARD())

      def SHORTCAP(x,c):

        global  colorb

        return ((x) & colorb[(c)^1])

      def NMOVE(x):

        global  nmoves

        return (SHORTMOVE(nmoves[x]))

      def KMOVE(x):

        global  kmoves

        return (SHORTMOVE(kmoves[x]))

      def PMOVE(x,c):

        global  pmoves

        return (pmoves[(c)][(x)] & (~BOARD()))

      def NOCC(x):

        global  nmoves

        return (SHORTOCC(nmoves[x]))

      def KOCC(x):

        global  kmoves

        return (SHORTOCC(kmoves[x]))

      def POCC(x,c):

        global  pcaps

        return (pcaps[(c)][(x)] & BOARD())

      def NCAP(x,c):

        global  nmoves

        return (SHORTCAP(nmoves[x], (c)))

      def KCAP(x,c):

        global  kmoves

        return (SHORTCAP(kmoves[x], (c)))

      def PCAP(x,c):

        global  pcaps, colorb

        return (pcaps[(c)][(x)] & colorb[(c)^1])

      def PCA3(x,c):

        global  ENP, pcaps, BITi, colorb

        return (pcaps[(c)][(x) | 64] & (colorb[(c)^1] | ((BITi[ENPASS()]) & iif(c == 1, 0xFF0000, 0xFF0000000000))))

      def PCA4(x,c):

        global  ENP, pcaps, BITi, colorb

        return (pcaps[(c)][(x) | 128] & (colorb[(c)^1] | ((BITi[ENPASS()]) & iif(c == 1, 0xFF0000, 0xFF0000000000))))

      def RANK(x,y):

        return (((x) & 0x38) == (y))

      def TEST(f,b):

        global  BITi

        return (BITi[f] & (b)) != 0

      def ENPASS():

        global  flags

        return (flags & 63)

      def CASTLE():

        global  flags

        return (flags & 960)

      def COUNT():

        global  count

        return (count & 0x3FF)

      def BOARD():

        global  colorb

        return (colorb[0] | colorb[1])

      def RQU():

        global  ROOK, QUEEN, pieceb

        return (pieceb[QUEEN] | pieceb[ROOK])

      def BQU():

        global  BISHOP, QUEEN, pieceb

        return (pieceb[QUEEN] | pieceb[BISHOP])

      def getLowestBit(bb):

        return bb & (-bb)

      def _getpiece(s,c):

        global  pieceChar

        i = 1
        while (i < 8):

          if (pieceChar[i] == s):

            c[0] = 0
            return i

          else:

            if (pieceChar[i] == chr(ord(s)-32)):

              c[0] = 1
              return i

          i += 1

        return 0

      def parseInt(s):

        if(len(s)==0 or ("0123456789-.").find(s[0],0)<0):

          return 0

        else:

          return int(s)

      def nextToken(str,tok):

        j = 0
        s = str
        r = ""
        while(j<=tok):

          i = s.find(" ",0)
          if(i<0):

            r = s
            break

          r = s[0:i];
          s = s[i+1:];

          j += 1

        return r

      def printboard():

        b = ""
        s = ""
        i = 0
        while(i < 64):

          c = "."
          k = 0
          while(k < 8):

            if( pieceb[k] & BITi[i] > 0 ):
              if( colorb[0] & BITi[i] == 0 ):
                c = chr(ord(pieceChar[k])+32)
              else:
                c = pieceChar[k]

            k += 1

          s += c

          i += 1

          if( i % 8 == 0 ):
            b = s + "\n" + b
            s = ""

        print(b)

      def _parse_fen(fen):

        global  KING, pval, hashb, hstack, hashxor, BITi, count, flags
        global  mat_, onmove, kingpos, pieceb, colorb

        col = 0
        row = 7

        pieceb = [ 0, 0, 0, 0, 0, 0, 0, 0 ]

        colorb[0] = 0
        colorb[1] = 0
        hashb = 0

        mat_ = 0

        pos = nextToken(fen,0);
        mv = (nextToken(fen,1))[0];
        cas = nextToken(fen,2);
        enps = nextToken(fen,3);
        halfm = parseInt(nextToken(fen,4));
        fullm = parseInt(nextToken(fen,5));

        i = 0
        while(i < len(pos)):

          s = pos[i]
          if (s == "/"):

            row -= 1
            col = 0

          else:

            if (s >= "1"  and  s <= "8"):

              col += (ord(s) - ord("0"))

            else:

              cp = [0]
              p = _getpiece(s, cp)
              c = cp[0]

              if (p == KING):

                kingpos[c] = (row*8) + col

              else:

                mat_ += iif(c == 1, -pval[p], pval[p])

              hashb ^= hashxor[col | row << 3 | i << 6 | iif(c == 1, 512, 0)]
              pieceb[p] |= BITi[row*8 + col]
              colorb[c] |= BITi[row*8 + col]
              col += 1

          i += 1

        onmove = iif( mv == "b", 1, 0 )

        flags = 0
        i = 0
        while(i < len(cas)):

          s = cas[i]
          if (s == "K"):
            flags |= BITi[6]
          if (s == "k"):
            flags |= BITi[7]
          if (s == "Q"):
            flags |= BITi[8]
          if (s == "q"):
            flags |= BITi[9]
          i += 1

        if (enps[0] >= "a"  and  enps[0] <= "h"  and  enps[1] >= "1"  and  enps[1] <= "8"):

          flags |= 8*(ord(enps[1]) - ord("1")) + ord(enps[0]) - ord("a")

        count = (fullm - 1)*2 + onmove + (halfm << 10)

        i = 0
        while( i < COUNT() ):

          hstack[i] = 0
          i += 1

      def _startpos():

        global  sd, count, engine, sfen

        _parse_fen(sfen)

        engine = 1

      def LOW16(x):

        return ((x) & 0xFFFF)

      def LOW32(x):

        return ((x) & 0xFFFFFFFF)

      def L32(x):

        return ((x) & 0xFFFFFFFF)

      def _rand_32():

        global  r_x, r_y, r_z, r_w, r_carry

        r_x = L32(r_x * 69069 + 1)
        r_y ^= L32(r_y << 13)
        r_y ^= L32(r_y >> 17)
        r_y ^= L32(r_y << 5)
        r_y = L32(r_y)

        t = L32((r_w << 1)) + r_z + r_carry
        r_carry = (L32(r_z >> 2) + L32(r_w >> 3) + L32(r_carry >> 2)) >> 30
        r_z = r_w
        r_w = L32(t)
        return L32(r_x + r_y + r_w)

      def _rand_64():

        c = _rand_32()
        return _rand_32() | (c << 32)

      def getLsb(bm):

        global  LSB

        n = LOW32(bm)

        if (n != 0):

          if (LOW16(n) != 0):

            return LSB[LOW16(n)]

          else:

            return (16 | LSB[LOW16(n >> 16)])

        else:

          n = (bm >> 32)
          if (LOW16(n) != 0):

            return (32 | LSB[LOW16(n)])

          else:

            return (48 | LSB[LOW16(n >> 16)])

      def _slow_lsb(bm):

        k = -1
        while (bm != 0):

          k += 1
          if ((bm & 1) != 0):
            break

          bm >>= 1

        return k

      def _BITCnt(bit):

        c = 0
        while (bit != 0):

          bit &= (bit - 1)
          c += 1

        return c

      def BITCnt (n):

        global  BITC

        return (BITC[LOW16(n)] + BITC[LOW16(n >> 16)] + BITC[LOW16(n >> 32)] + BITC[LOW16(n >> 48)])

      def identPiece(f):

        global  PAWN, KNIGHT, KING, ENP, BISHOP, ROOK, QUEEN, pieceb

        if (TEST(f, pieceb[PAWN])):
          return PAWN
        if (TEST(f, pieceb[KNIGHT])):
          return KNIGHT
        if (TEST(f, pieceb[BISHOP])):
          return BISHOP
        if (TEST(f, pieceb[ROOK])):
          return ROOK
        if (TEST(f, pieceb[QUEEN])):
          return QUEEN
        if (TEST(f, pieceb[KING])):
          return KING
        return ENP

      def key000(b,f):

        return ((b >> (f & 56)) & 0x7E)

      def key090(b,f):

        b = b >> (f&7)
        h = ((b & 0x1010101) | ((b >> 31) & 0x2020202))
        h = (h & 0x303) | ((h >> 14) & 0xC0C)
        return (h & 0xE) | ((h >> 4) & 0x70)

      def keyDiag(_b):

        h = (_b | _b >> 32)
        h |= h >> 16
        h |= h >>  8
        return h & 0x7E

      def key045(b,f):

        global  bmask45

        return keyDiag(b & bmask45[f])

      def key135(b,f):

        global  bmask135

        return keyDiag(b & bmask135[f])

      def DUALATT(x,y,c):

        return (battacked(x, c)  or  battacked(y, c))

      def battacked(f,c):

        global  PAWN, KNIGHT, KING, pieceb

        if ((PCAP(f, c) & pieceb[PAWN]) != 0):
          return True
        if ((NCAP(f, c) & pieceb[KNIGHT]) != 0):
          return True
        if ((KCAP(f, c) & pieceb[KING]) != 0):
          return True
        if ((RCAP1(f, c) & RQU()) != 0):
          return True
        if ((RCAP2(f, c) & RQU()) != 0):
          return True
        if ((BCAP3(f, c) & BQU()) != 0):
          return True
        if ((BCAP4(f, c) & BQU()) != 0):
          return True

        return False

      def reach(f,c):

        global  KNIGHT, pieceb

        return (NCAP(f, c) & pieceb[KNIGHT]) | (RCAP1(f, c) & RQU()) | (RCAP2(f, c) & RQU()) | (BCAP3(f, c) & BQU()) | (BCAP4(f, c) & BQU())

      def  attacked(f,c):

        global  PAWN, pieceb

        return (PCAP(f, c) & pieceb[PAWN]) | reach(f, c)

      def _init_pawns(moves,caps,freep,filep,helpp,c):

        global  pawnrun, BITi, pawnprg

        i = -1
        while(i < 63):

          i += 1

          rank = int(i/8)
          file = i&7
          m = i + iif(c == 1, -8, 8)
          pawnprg[c][i] = pawnrun[ iif(c == 1, 7-rank, rank ) ]

          j = -1
          while(j < 63):

            j += 1

            jrank = int(j/8)
            jfile = j&7
            dfile = (jfile - file)*(jfile - file)

            if (dfile > 1):
              continue

            if ((c == 1  and  jrank < rank)  or  (c == 0  and  jrank > rank)):

              #--The not touched half of the pawn

              if (dfile == 0):
                filep[i] |= BITi[j]

              freep[i] |= BITi[j]

            else:

              if (dfile != 0  and  (jrank - rank)*(jrank - rank) <= 1):

                helpp[i] |= BITi[j]

          if (m < 0  or  m > 63):
            continue

          moves[i] |= BITi[m]

          if (file > 0):

            m = i + iif(c == 1, -9, 7)
            if (m < 0  or  m > 63):
              continue

            caps[i] |= BITi[m]
            caps[i + (64*(2 - c))] |= BITi[m]

          if (file < 7):

            m = i + iif(c == 1, -7, 9)
            if (m < 0  or  m > 63):
              continue

            caps[i] |= BITi[m]
            caps[i + (64*(c + 1))] |= BITi[m]
 
      def _init_shorts(moves,m):

        global  BITi

        i = 0
        while( i < 64 ):

          j = 0
          while( j < 8 ):

            n = i + m[j]
            if (n < 64  and  n >= 0  and  ((n & 7)-(i & 7))*((n & 7)-(i & 7)) <= 4):

              moves[i] |= BITi[n]

            j += 1

          i += 1

      def _occ_free_board(bc,dl,fr):

        perm = fr
        i = 0
        while( i < bc ):

          low = getLowestBit(fr)
          fr &= (~low)

          if (not TEST(i, dl)):
            perm &= (~low)

          i += 1

        return perm

      def _init_rays1():

        global  rays, BITi, BITC

        f = 0
        while( f < 64 ):

          mmask = _rook0(f, 0, 0) | BITi[f]
          bc = BITCnt(mmask)
          iperm = 1 << bc

          i = 0
          while( i < iperm ):

            board = _occ_free_board(bc, i, mmask)
            move = _rook0(f, board, 1)
            occ = _rook0(f, board, 2)
            xray = _rook0(f, board, 3)
            index = key000(board, f)
            rays[(f << 7) + index] = occ | move
            rays[(f << 7) + index + 0x8000] = xray
            i += 1

          f += 1

      def _init_rays2():

        global  rays, BITi, BITC

        f = 0
        while( f < 64 ):

          mmask = _rook90(f, 0, 0) | BITi[f]
          bc = BITCnt(mmask)
          iperm = 1 << bc

          i = 0
          while( i < iperm ):

            board = _occ_free_board(bc, i, mmask)
            move = _rook90(f, board, 1)
            occ = _rook90(f, board, 2)
            xray = _rook90(f, board, 3)
            index = key090(board, f)
            rays[(f << 7) + index + 0x2000] = occ | move
            rays[(f << 7) + index + 0x8000 + 0x2000] = xray
            i += 1

          f += 1

      def _init_rays3():

        global  rays, BITi, BITC

        f = 0
        while( f < 64 ):

          mmask = _bishop45(f, 0, 0) | BITi[f]
          bc = BITCnt(mmask)
          iperm = 1 << bc

          i = 0
          while( i < iperm ):

            board = _occ_free_board(bc, i, mmask)
            move = _bishop45(f, board, 1)
            occ = _bishop45(f, board, 2)
            xray = _bishop45(f, board, 3)
            index = key045(board, f)
            rays[(f << 7) + index + 0x4000] = occ | move
            rays[(f << 7) + index + 0x8000 + 0x4000] = xray
            i += 1

          f += 1

      def _init_rays4():

        global  rays, BITi, BITC

        f = 0
        while( f < 64 ):

          mmask = _bishop135(f, 0, 0) | BITi[f]
          bc = BITCnt(mmask)
          iperm = 1 << bc

          i = 0
          while( i < iperm ):

            board = _occ_free_board(bc, i, mmask)
            move = _bishop135(f, board, 1)
            occ = _bishop135(f, board, 2)
            xray = _bishop135(f, board, 3)
            index = key135(board, f)
            rays[(f << 7) + index + 0x6000] = occ | move
            rays[(f << 7) + index + 0x8000 + 0x6000] = xray

            i += 1

          f += 1

      def _rook0(f, board, t):

        global  BITi

        fr = 0
        occ = 0
        xray = 0

        b = 0
        i = f+1
        while( i < 64  and  i%8 != 0 ):

          if (TEST(i, board)):

            if (b != 0):

              xray |= BITi[i]
              break

            else:

              occ |= BITi[i]
              b = 1

          if (b == 0):
            fr |= BITi[i]

          i += 1

        b = 0
        i = f-1
        while( i >= 0  and  i%8 != 7 ):

          if (TEST(i, board)):

            if (b != 0):

              xray |= BITi[i]
              break

            else:

              occ |= BITi[i]
              b = 1

          if (b == 0):
            fr |= BITi[i]

          i -= 1

        return iif( (t < 2), fr, iif(t == 2, occ, xray) )

      def _rook90(f,board,t):

        global  BITi

        fr = 0
        occ = 0
        xray = 0

        b = 0
        i = f-8
        while( i >= 0 ):

          if (TEST(i, board)):

            if (b != 0):

              xray |= BITi[i]
              break

            else:

              occ |= BITi[i]
              b = 1

          if (b == 0):
            fr |= BITi[i]

          i -= 8

        b = 0
        i = f+8
        while( i < 64 ):

          if (TEST(i, board)):

            if (b != 0):

              xray |= BITi[i]
              break

            else:

              occ |= BITi[i]
              b = 1

          if (b == 0):
            fr |= BITi[i]

          i += 8

        return iif( (t < 2), fr, iif(t == 2, occ, xray) )

      def _bishop45(f,board,t):

        global  BITi

        fr = 0
        occ = 0
        xray = 0

        b = 0
        i = f+9
        while( i < 64  and  (i%8 != 0) ):

          if (TEST(i, board)):

            if (b != 0):

              xray |= BITi[i]
              break

            else:

              occ |= BITi[i]
              b = 1

          if (b == 0):
            fr |= BITi[i]

          i += 9

        b = 0
        i = f-9
        while( i >= 0  and  (i%8 != 7) ):

          if (TEST(i, board)):

            if (b != 0):

              xray |= BITi[i]
              break

            else:

              occ |= BITi[i]
              b = 1

          if (b == 0):
            fr |= BITi[i]

          i -= 9

        return iif( (t < 2), fr, iif(t == 2, occ, xray) )

      def _bishop135(f,board,t):

        global  BITi

        fr = 0
        occ = 0
        xray = 0

        b = 0
        i = f-7
        while( i >= 0  and  (i%8 != 0) ):

          if (TEST(i, board)):

            if (b != 0):

              xray |= BITi[i]
              break

            else:

              occ |= BITi[i]
              b = 1

          if (b == 0):
            fr |= BITi[i]

          i -= 7

        b = 0
        i = f+7
        while( i < 64  and  (i%8 != 7) ):

          if (TEST(i, board)):

            if (b != 0):

              xray |= BITi[i]
              break

            else:

              occ |= BITi[i]
              b = 1

          if (b == 0):
            fr |= BITi[i]

          i += 7

        return iif( (t < 2), fr, iif(t == 2, occ, xray) )

      def displaym(m):

        print(mvstr(m))

      def mvstr(m):

        global  pieceChar

        s = chr(ord("a") + (FROM(m) % 8)) + chr(ord("1") + int(FROM(m)/8))
        s += chr(ord("a") + (TO(m) % 8)) + chr(ord("1") + int(TO(m)/8))
        s += iif(PROM(m) != 0,  chr( ord( pieceChar[PROM(m)] ) +32 ), "" )
        return s

      def errprint(s):

        print("error: "+s)

      def displaypv():

        global  p_v, pvlength

        s = ""
        i = 0
        while( i < pvlength[0] ): 

          s += mvstr(p_v[0][i]) + " "
          i += 1

        print(s)

      def isDraw(hp,nrep):

        global  PAWN, hstack, BITC, count, pieceb, colorb

        if (count > 0xFFF):

          #--fifty > 3
          #--100 plies

          if (count >= 0x400*100):
            return 2
          c = 0
          n = COUNT() - (count >> 10)
          i = COUNT() - 2
          while (i >= n):
            c += 1
            if (hstack[i] == hp  and  c == nrep):
              return 1
            i -= 1

        else:
          if ((pieceb[PAWN] | RQU()) == 0):

            #--Check for mating material
            if (_BITCnt(colorb[0]) <= 2  and  _BITCnt(colorb[1]) <= 2):
              return 3

        return 0

      def pinnedPieces(f,oc):

        global  BITi, colorb

        pin = 0
        b = ((RXRAY1(f) | RXRAY2(f)) & colorb[oc]) & RQU()
        while (b != 0):

          t = getLsb(b)
          b ^= BITi[t]
          pin |= RCAP(t, oc) & ROCC(f)

        b = ((BXRAY3(f) | BXRAY4(f)) & colorb[oc]) & BQU()
        while (b != 0):

          t = getLsb(b)
          b ^= BITi[t]
          pin |= BCAP(t, oc) & BOCC(f)

        return pin

      def getDir(f,t):

        global  count, flags

        if (((f ^ t) & 56) == 0):
          return 8
        if (((f ^ t) & 7) == 0):
          return 16
        return iif(((f - t) % 7) != 0, 32, 64)

      #-- move is both makeMove and unmakeMove,
      #-- only for unmakeMove the flags have to be restored (counter, castle, enpass...)

      def move(m,c):

        global  PAWN, KING, ENP, ROOK, pval, hashb, hashxor, BITi, crevoke, count
        global  flags, mat_, kingpos, pieceb, colorb

        f = FROM(m)
        t = TO(m)
        p = PIECE(m)
        a = CAP(m)

        colorb[c] ^= BITi[f]
        pieceb[p] ^= BITi[f]

        colorb[c] ^= BITi[t]
        pieceb[p] ^= BITi[t]
        hashb ^= hashxor[(f) | (p) << 6 | (c) << 9]
        hashb ^= hashxor[(t) | (p) << 6 | (c) << 9]

        flags &= 960
        count += 0x401
        if (a != 0):

          if (a == ENP):

            #-- Enpassant Capture
            t = (t&7) | (f&56)
            a = PAWN

          else:
            if (a == ROOK  and  CASTLE() != 0):

               #--Revoke castling rights.
               flags &= crevoke[t]

          pieceb[a] ^= BITi[t]
          colorb[c^1] ^= BITi[t]
          hashb ^= hashxor[(t) | (a) << 6 | (c^1) << 9]

          #--Reset Fifty Counter
          count &= 0x3FF

          mat_ += iif(c == 1, -pval[a], +pval[a])

        if (p == PAWN):

          if (((f^t)&8) == 0):
            flags |= f^24
            #--Enpassant
          else:
            if ((t&56) == 0  or  (t&56) == 56):

              pieceb[PAWN] ^= BITi[t]
              pieceb[PROM(m)] ^= BITi[t]
              hashb ^= hashxor[(t) | (PAWN) << 6 | (c) << 9]
              hashb ^= hashxor[(t) | (PROM(m)) << 6 | (c) << 9]
              mat_ += iif( c == 1, pval[PAWN] - pval[PROM(m)], -pval[PAWN] + pval[PROM(m)] )

          #--Reset Fifty Counter
          count &= 0x3FF

        else:
          if (p == KING):

            if (kingpos[c] == f):
              kingpos[c] = t
            else:
              kingpos[c] = f

            #-- Lose castling rights
            flags &= ~(320 << c)
            if (((f^t)&3) == 2):

                  #-- Castle
              if (t == 6):

                f = 7
                t = 5

              else:
                if (t == 2):

                  f = 0
                  t = 3

                else:
                  if (t == 62):

                    f = 63
                    t = 61

                  else:

                    f = 56
                    t = 59

              colorb[c] ^= BITi[f]
              pieceb[ROOK] ^= BITi[f]
              colorb[c] ^= BITi[t]
              pieceb[ROOK] ^= BITi[t]
              hashb ^= hashxor[(f) | (ROOK) << 6 | (c) << 9]
              hashb ^= hashxor[(t) | (ROOK) << 6 | (c) << 9]

          else:
            if (p == ROOK  and  CASTLE() != 0):
              flags &= crevoke[f]

      def doMove(m,c):

        global  mstack, count, flags, mat_

        mstack[COUNT()] = count | (flags << 17) | ((mat_ + 0x4000) << 27) | (m << 42)
        move(m, c)

      def undoMove(m,c):

        global  mstack, count, flags, mat_

        u = mstack[COUNT() - 1]
        move(m, c)
        count = (u & 0x1FFFF)
        flags = ((u >> 17) & 0x3FF)
        mat_ = (((u >> 27) & 0x7FFF) - 0x4000)

      def registerCaps(m,bc,mlist,mn):

        global  BITi

        while (bc != 0):

          t = getLsb(bc)
          bc ^= BITi[t]
          mlist[ mn[0] ] = m | _TO(t) | _CAP(identPiece(t))
          mn[0] += 1

      def registerMoves(m,bc,bm,mlist,mn):

        global  BITi

        while (bc != 0):

          t = getLsb(bc)
          bc ^= BITi[t]
          mlist[ mn[0] ] = m | _TO(t) | _CAP(identPiece(t))
          mn[0] += 1

        while (bm != 0):

          t = getLsb(bm)
          bm ^= BITi[t]
          mlist[ mn[0] ] = m | _TO(t)
          mn[0] += 1

      def registerProms(f,c,bc,bm,mlist,mn):

        global  PAWN, KNIGHT, BISHOP, ROOK, QUEEN, BITi

        while (bc != 0):

          t = getLsb(bc)
          bc ^= BITi[t]
          m = f | _ONMV(c) | _PIECE(PAWN) | _TO(t) | _CAP(identPiece(t))
          mlist[ mn[0] ] = m | _PROM(QUEEN)
          mn[0] += 1
          mlist[ mn[0] ] = m | _PROM(KNIGHT)
          mn[0] += 1
          mlist[ mn[0] ] = m | _PROM(ROOK)
          mn[0] += 1
          mlist[ mn[0] ] = m | _PROM(BISHOP)
          mn[0] += 1

        while (bm != 0):

          t = getLsb(bm)
          bm ^= BITi[t]
          m = f | _ONMV(c) | _PIECE(PAWN) | _TO(t)
          mlist[ mn[0] ] = m | _PROM(QUEEN)
          mn[0] += 1
          mlist[ mn[0] ] = m | _PROM(KNIGHT)
          mn[0] += 1
          mlist[ mn[0] ] = m | _PROM(ROOK)
          mn[0] += 1
          mlist[ mn[0] ] = m | _PROM(BISHOP)
          mn[0] += 1

      def registerKing(m,bc,bm,mlist,mn,c):

        global  BITi

        while (bc != 0):

          t = getLsb(bc)
          bc ^= BITi[t]
          if (battacked(t, c)):
            continue
          mlist[ mn[0] ] = m | _TO(t) | _CAP(identPiece(t))
          mn[0] += 1

        while (bm != 0):

          t = getLsb(bm)
          bm ^= BITi[t]
          if (battacked(t, c)):
            continue
          mlist[ mn[0] ] = m | _TO(t)
          mn[0] += 1

      def generateCheckEsc(ch,apin,c,k,ml,mn):

        global  PAWN, KING, ENP, nmoves, kmoves, BITi, BITC, pieceb, colorb

        bf = _BITCnt(ch)
        colorb[c] ^= BITi[k]
        registerKing(PREMOVE(k, KING, c), KCAP(k, c), KMOVE(k), ml, mn, c)
        colorb[c] ^= BITi[k]

        #--Doublecheck:
        if (bf > 1):
          return bf

        bf = getLsb(ch)

        #--Can we capture the checker?
        cc = attacked(bf, c^1) & apin
        while (cc != 0):

          cf = getLsb(cc)
          cc ^= BITi[cf]
          p = identPiece(cf)
          if (p == PAWN  and  RANK(cf, iif(c != 0, 0x08, 0x30) )):

            registerProms(cf, c, ch, 0, ml, mn)

          else:

            registerMoves(PREMOVE(cf, p, c), ch, 0, ml, mn)

        if (ENPASS() != 0  and  (ch & pieceb[PAWN]) != 0):

          #--Enpassant capture of attacking Pawn
          cc = PCAP(ENPASS(), c^1) & pieceb[PAWN] & apin
          while (cc != 0):

            cf = getLsb(cc)
            cc ^= BITi[cf]
            registerMoves(PREMOVE(cf, PAWN, c), BITi[ENPASS()], 0, ml, mn)

        if ((ch & (nmoves[k] | kmoves[k])) != 0):
          #--We can not move anything between!
          return 1

        d = getDir(bf, k)
        if ((d & 8) != 0):
          fl = RMOVE1(bf) & RMOVE1(k)
        else:
          if ((d & 16) != 0):
            fl = RMOVE2(bf) & RMOVE2(k)
          else:
            if ((d & 32) != 0):
              fl = BMOVE3(bf) & BMOVE3(k)
            else:
              fl = BMOVE4(bf) & BMOVE4(k)

        while (fl != 0):

          f = getLsb(fl)
          fl ^= BITi[f]
          cc = reach(f, c^1) & apin
          while (cc != 0):

            cf = getLsb(cc)
            cc ^= BITi[cf]
            p = identPiece(cf)
            registerMoves(PREMOVE(cf, p, c), 0, BITi[f], ml, mn)

          bf = iif(c != 0, f+8, f-8)
          if (bf < 0  or  bf > 63):
            continue

          if ((BITi[bf] & pieceb[PAWN] & colorb[c] & apin) != 0):

            if (RANK(bf, iif(c != 0, 0x08, 0x30) )):
              registerProms(bf, c, 0, BITi[f], ml, mn)
            else:
              registerMoves(PREMOVE(bf, PAWN, c), 0, BITi[f], ml, mn)

          if (RANK(f, iif(c != 0, 0x20, 0x18) )  and  (BOARD() & BITi[bf]) == 0  and  (BITi[ iif(c != 0, f+16, f-16) ] & pieceb[PAWN] & colorb[c] & apin) != 0):
            registerMoves(PREMOVE( iif(c != 0, f+16, f-16 ), PAWN, c), 0, BITi[f], ml, mn)

        return 1

      def generateMoves(ch,c,ply):

        global  PAWN, KNIGHT, KING, ENP, BISHOP, ROOK, QUEEN, pcaps, BITi, movelist, movenum
        global  flags, kingpos, pieceb, colorb

        f = kingpos[c]
        cb = colorb[c]
        pin = pinnedPieces(f, c^1)
        ml = movelist[ply]
        mn = [0]

        if (ch != 0):

          ret = generateCheckEsc(ch, ~pin, c, f, ml, mn)
          movenum[ply] = mn[0]
          return ret

        registerKing(PREMOVE(f, KING, c), KCAP(f, c), KMOVE(f), ml, mn, c)

        cb = colorb[c] & (~pin)
        b = pieceb[PAWN] & cb
        while (b != 0):

          f = getLsb(b)
          b ^= BITi[f]
          m = PMOVE(f, c)
          a = PCAP(f, c)

          if (m != 0  and  RANK(f, iif( c != 0, 0x30, 0x08) )):
            m |= PMOVE( iif(c != 0, f-8, f+8), c)

          if (RANK(f, iif(c != 0, 0x08, 0x30) )):

            registerProms(f, c, a, m, ml, mn)

          else:

            if (ENPASS() != 0  and  (BITi[ENPASS()] & pcaps[(c)][(f)]) != 0):

              clbd = ENPASS()^8
              colorb[c] ^= BITi[clbd]
              hh = ROCC1(f)
              if ((hh & BITi[kingpos[c]]) == 0  or  (hh & colorb[c^1] & RQU()) == 0):

                a = a | BITi[ENPASS()]

              colorb[c] ^= BITi[clbd]

            registerMoves(PREMOVE(f, PAWN, c), a, m, ml, mn)

        b = pin & pieceb[PAWN]
        while (b != 0):

          f = getLsb(b)
          b ^= BITi[f]
          t = getDir(f, kingpos[c])
          if ((t & 8) != 0):
            continue

          m = 0
          a = 0
          if ((t & 16) != 0):

            m = PMOVE(f, c)

            if (m != 0  and  RANK(f, iif( c != 0, 0x30, 0x08) )):
              m |= PMOVE( iif(c != 0, f-8, f+8 ), c)

          else:
            if ((t & 32) != 0):

              a = PCA3(f, c)

            else:

              a = PCA4(f, c)

            if (RANK(f, iif(c != 0, 0x08, 0x30) )):

              registerProms(f, c, a, m, ml, mn)

            else:

              registerMoves(PREMOVE(f, PAWN, c), a, m, ml, mn)

        b = pieceb[KNIGHT] & cb
        while (b != 0):

          f = getLsb(b)
          b ^= BITi[f]
          registerMoves(PREMOVE(f, KNIGHT, c), NCAP(f, c), NMOVE(f), ml, mn)

        b = pieceb[ROOK] & cb
        while (b != 0):

          f = getLsb(b)
          b ^= BITi[f]
          registerMoves(PREMOVE(f, ROOK, c), RCAP(f, c), RMOVE(f), ml, mn)
          if (CASTLE() != 0  and  ch == 0):

            if (c != 0):

              if ((flags & 128) != 0  and  (f == 63)  and  (RMOVE1(63) & BITi[61]) != 0):
                if (not DUALATT(61, 62, c)):
                  registerMoves(PREMOVE(60, KING, c), 0, BITi[62], ml, mn)

              if ((flags & 512) != 0  and  (f == 56)  and  (RMOVE1(56) & BITi[59]) != 0):
                if (not DUALATT(59, 58, c)):
                  registerMoves(PREMOVE(60, KING, c), 0, BITi[58], ml, mn)

            else:

              if ((flags & 64) != 0  and  (f == 7)  and  (RMOVE1(7) & BITi[5]) != 0):
                if (not DUALATT(5, 6, c)):
                  registerMoves(PREMOVE(4, KING, c), 0, BITi[6], ml, mn)

              if ((flags & 256) != 0  and  (f == 0)  and  (RMOVE1(0) & BITi[3]) != 0):
                if (not DUALATT(3, 2, c)):
                  registerMoves(PREMOVE(4, KING, c), 0, BITi[2], ml, mn)

        b = pieceb[BISHOP] & cb
        while (b != 0):

          f = getLsb(b)
          b ^= BITi[f]
          registerMoves(PREMOVE(f, BISHOP, c), BCAP(f, c), BMOVE(f), ml, mn)

        b = pieceb[QUEEN] & cb
        while (b != 0):

          f = getLsb(b)
          b ^= BITi[f]
          registerMoves(PREMOVE(f, QUEEN, c), RCAP(f, c) | BCAP(f,c), RMOVE(f) | BMOVE(f), ml, mn)

        b = pin & (pieceb[ROOK] | pieceb[BISHOP] | pieceb[QUEEN])
        while (b != 0):

          f = getLsb(b)
          b ^= BITi[f]
          p = identPiece(f)
          t = p | getDir(f, kingpos[c])

          if ((t & 10) == 10):
            registerMoves(PREMOVE(f, p, c), RCAP1(f, c), RMOVE1(f), ml, mn)

          if ((t & 18) == 18):
            registerMoves(PREMOVE(f, p, c), RCAP2(f, c), RMOVE2(f), ml, mn)

          if ((t & 33) == 33):
            registerMoves(PREMOVE(f, p, c), BCAP3(f, c), BMOVE3(f), ml, mn)

          if ((t & 65) == 65):
            registerMoves(PREMOVE(f, p, c), BCAP4(f, c), BMOVE4(f), ml, mn)

        movenum[ply] = mn[0]
        return 0

      def generateCaps(ch,c,ply):

        global  PAWN, KNIGHT, KING, ENP, BISHOP, ROOK, QUEEN
        global  pcaps, BITi, movelist, movenum, kingpos, pieceb, colorb

        f = kingpos[c]
        cb = colorb[c]
        pin = pinnedPieces(f, c^1)
        ml = movelist[ply]
        mn = [0]

        if (ch != 0):

          ret = generateCheckEsc(ch, ~pin, c, f, ml, mn)
          movenum[ply] = mn[0]
          return ret

        registerKing(PREMOVE(f, KING, c), KCAP(f, c), 0, ml, mn, c)

        cb = colorb[c] & (~pin)

        b = pieceb[PAWN] & cb
        while (b != 0):

          f = getLsb(b)
          b ^= BITi[f]
          a = PCAP(f, c)
          if (RANK(f, iif(c != 0, 0x08, 0x30) )):

            registerMoves(PREMOVE(f, PAWN, c) | _PROM(QUEEN), a, PMOVE(f, c), ml, mn)

          else:

            if (ENPASS() != 0  and  (BITi[ENPASS()] & pcaps[(c)][(f)]) != 0):

              clbd = ENPASS()^8
              colorb[c] ^= BITi[clbd]
              hh = ROCC1(f)
              if ((hh & BITi[kingpos[c]]) == 0  or  (hh & colorb[c^1] & RQU()) == 0):

                a = a | BITi[ENPASS()]

              colorb[c] ^= BITi[clbd]

            registerCaps(PREMOVE(f, PAWN, c), a, ml, mn)

        b = pin & pieceb[PAWN]
        while (b != 0):

          f = getLsb(b)
          b ^= BITi[f]
          t = getDir(f, kingpos[c])
          if ((t & 8) != 0):
            continue

          m = 0
          a = 0

          if ((t & 16) != 0):

            m = PMOVE(f, c)

          else:
            if ((t & 32) != 0):

              a = PCA3(f, c)

            else:

              a = PCA4(f, c)

          if (RANK(f, iif(c != 0, 0x08, 0x30) )):

            registerMoves(PREMOVE(f, PAWN, c) | _PROM(QUEEN), a, m, ml, mn)

          else:

            registerCaps(PREMOVE(f, PAWN, c), a, ml, mn)

        b = pieceb[KNIGHT] & cb
        while (b != 0):

          f = getLsb(b)
          b ^= BITi[f]
          registerCaps(PREMOVE(f, KNIGHT, c), NCAP(f, c), ml, mn)

        b = pieceb[BISHOP] & cb
        while (b != 0):

          f = getLsb(b)
          b ^= BITi[f]
          registerCaps(PREMOVE(f, BISHOP, c), BCAP(f, c), ml, mn)

        b = pieceb[ROOK] & cb
        while (b != 0):

          f = getLsb(b)
          b ^= BITi[f]
          registerCaps(PREMOVE(f, ROOK, c), RCAP(f, c), ml, mn)

        b = pieceb[QUEEN] & cb
        while (b != 0):

          f = getLsb(b)
          b ^= BITi[f]
          registerCaps(PREMOVE(f, QUEEN, c), RCAP(f, c) | BCAP(f,c), ml, mn)

        b = pin & (pieceb[ROOK] | pieceb[BISHOP] | pieceb[QUEEN])
        while (b != 0):

          f = getLsb(b)
          b ^= BITi[f]
          p = identPiece(f)
          t = p | getDir(f, kingpos[c])

          if ((t & 10) == 10):
            registerCaps(PREMOVE(f, p, c), RCAP1(f, c), ml, mn)

          if ((t & 18) == 18):
            registerCaps(PREMOVE(f, p, c), RCAP2(f, c), ml, mn)

          if ((t & 33) == 33):
            registerCaps(PREMOVE(f, p, c), BCAP3(f, c), ml, mn)

          if ((t & 65) == 65):
            registerCaps(PREMOVE(f, p, c), BCAP4(f, c), ml, mn)

        movenum[ply] = mn[0]
        return 0

      #--SEE Stuff
      def swap(m):

        global  PAWN, KNIGHT, KING, BISHOP, ROOK, QUEEN, pval, BITi, pieceb, colorb

        k_list = [0 for x in range(32)]

        f = FROM(m)
        t = TO(m)
        onmv = ONMV(m)
        a_piece = pval[CAP(m)]
        piece = PIECE(m)
        c = onmv^1
        nc = 1
        temp = 0
        colstore0 = colorb[0]
        colstore1 = colorb[1]

        attacks = attacked(t, 0) | attacked(t, 1)
        k_list[0] = a_piece
        a_piece = pval[piece]
        colorb[onmv] ^= BITi[f]
        if ((piece & 4) != 0  or  piece == 1):

          d = getDir(f, t)
          if (d == 32  or  d == 64):
            attacks |= BOCC(t) & BQU()
          if (d == 8  or  d == 16):
            attacks |= ROCC(t) & RQU()

        attacks &= BOARD()

        while (attacks != 0):

          temp = pieceb[PAWN] & colorb[c] & attacks
          if (temp != 0):
            piece = PAWN
          else:
            temp = pieceb[KNIGHT] & colorb[c] & attacks
            if (temp != 0):
              piece = KNIGHT
            else:
              temp = pieceb[BISHOP] & colorb[c] & attacks
              if (temp != 0):
                piece = BISHOP
              else:
                temp = pieceb[ROOK] & colorb[c] & attacks
                if (temp != 0):
                  piece = ROOK
                else:
                  temp = pieceb[QUEEN] & colorb[c] & attacks
                  if (temp != 0):
                    piece = QUEEN
                  else:
                    temp = pieceb[KING] & colorb[c] & attacks
                    if (temp != 0):
                      piece = KING
                    else:
                      break

          temp &= -temp
          colorb[c] ^= temp
          if ((piece & 4) != 0  or  piece == 1):

            if ((piece & 1) != 0):
              attacks |= BOCC(t) & BQU()
            if ((piece & 2) != 0):
              attacks |= ROCC(t) & RQU()

          attacks &= BOARD()

          k_list[nc] = -k_list[nc - 1] + a_piece
          a_piece = pval[piece]
          nc += 1
          c ^= 1

        while (nc != 1):
           nc -= 1
           if (k_list[nc] > -k_list[nc - 1]):
             k_list[nc - 1] = -k_list[nc]

        colorb[0] = colstore0
        colorb[1] = colstore1
        return k_list[0]

      #-- In quiesce the moves are ordered just for the value of the captured piece
      def qpick(ml,mn,s):

        global  HEUR, cap_val, p_v

        pi = 0
        vmax = -HEUR
        i = s
        while(i < mn):

          m = ml[i]
          t = cap_val[CAP(m)]
          if (t > vmax):

            vmax = t
            pi = i

          i += 1

        m = ml[pi]
        if (pi != s):
          ml[pi] = ml[s]

        return m

      #-- In normal search some basic move ordering heuristics are used

      def spick(ml,mn,s,ply):

        global  HEUR, cap_val, p_v, killer, history

        pi = 0
        vmax = -HEUR
        i = s
        while(i < mn):

          m = ml[i]
          cap = CAP(m)
          if (cap != 0):

            t = cap_val[cap]
            if (t > vmax):

              vmax = t
              pi = i

          if (vmax < HEUR  and  m == killer[ply]):

            vmax = HEUR
            pi = i

          if (vmax < history[m & 0xFFF]):

            vmax = history[m & 0xFFF]
            pi = i

          i += 1

        m = ml[pi]
        if (pi != s):
          ml[pi] = ml[s]

        return m

      #-- The evaluation for Color c. It's only mobility stuff.
      #-- Pinned pieces are still awarded for limiting opposite's king

      def evalc(c,sf):

        global  PAWN, KNIGHT, BISHOP, ROOK, QUEEN, nmoves, kmoves, BITi, BITC
        global  nmobil, pawnprg, pawnfree, pawnfile, pawnhelp, kingpos, pieceb, colorb

        mn = 0
        katt = 0
        oc = c^1
        ocb = colorb[oc]
        kn = kmoves[kingpos[oc]]
        pin = pinnedPieces(kingpos[c], oc)

        b = pieceb[PAWN] & colorb[c]
        while (b != 0):

          ppos = 0
          f = getLsb(b)
          b ^= BITi[f]
          ppos = pawnprg[c][f]
          m = PMOVE(f, c)
          a = POCC(f, c)

          if ((a & kn) != 0):
            katt += _BITCnt(a & kn) << 4

          if ((BITi[f] & pin) != 0):

            if ((getDir(f, kingpos[c]) & 16) == 0):
              m = 0

          else:

            ppos += _BITCnt(a & pieceb[PAWN] & colorb[c]) << 2

          ppos += iif( m != 0, 8, -8 )

          if ((pawnfile[c][f] & pieceb[PAWN] & ocb) == 0):

                  #--Free file?
            if ((pawnfree[c][f] & pieceb[PAWN] & ocb) == 0):
              #--Free run?:
              ppos *= 2

            if ((pawnhelp[c][f] & pieceb[PAWN] & colorb[c]) == 0):
              #--Hanging backpawn?
              ppos -= 33

          mn += ppos

        cb = colorb[c] & (~pin)
        b = pieceb[KNIGHT] & cb
        while (b != 0):

          sf[0] += 1
          f = getLsb(b)
          b ^= BITi[f]
          a = nmoves[f]

          if ((a & kn) != 0):
            katt += _BITCnt(a & kn) << 4

          mn += nmobil[f]

        b = pieceb[KNIGHT] & pin
        while (b != 0):

          sf[0] += 1
          f = getLsb(b)
          b ^= BITi[f]
          a = nmoves[f]

          if ((a & kn) != 0):
            katt += _BITCnt(a & kn) << 4

        #--Opposite King does not block mobility at all
        colorb[oc] ^= BITi[kingpos[oc]]
        b = pieceb[QUEEN] & cb
        while (b != 0):

          sf[0] += 4
          f = getLsb(b)
          b ^= BITi[f]
          a = RATT1(f) | RATT2(f) | BATT3(f) | BATT4(f)

          if ((a & kn) != 0):
            katt += _BITCnt(a & kn) << 4

          mn += BITCnt(a)

        #--Opposite Queen & Rook does not block mobility for bishop
        colorb[oc] ^= RQU() & ocb
        b = pieceb[BISHOP] & cb
        while (b != 0):

          sf[0] += 1
          f = getLsb(b)
          b ^= BITi[f]
          a = BATT3(f) | BATT4(f)

          if ((a & kn) != 0):
            katt += _BITCnt(a & kn) << 4

          mn += BITCnt(a) << 3

        #--Opposite Queen does not block mobility for rook.
        colorb[oc] ^= pieceb[ROOK] & ocb
        #--Own non-pinned Rook does not block mobility for rook.
        colorb[c] ^= pieceb[ROOK] & cb
        b = pieceb[ROOK] & cb
        while (b != 0):

          sf[0] += 2
          f = getLsb(b)
          b ^= BITi[f]
          a = RATT1(f) | RATT2(f)

          if ((a & kn) != 0):
            katt += _BITCnt(a & kn) << 4

          mn += BITCnt(a) << 2

        #-- Back
        colorb[c] ^= pieceb[ROOK] & cb
        b = pin & (pieceb[ROOK] | pieceb[BISHOP] | pieceb[QUEEN])
        while (b != 0):

          f = getLsb(b)
          b ^= BITi[f]
          p = identPiece(f)
          if (p == BISHOP):

            sf[0] += 1
            a = BATT3(f) | BATT4(f)

            if ((a & kn) != 0):
              katt += _BITCnt(a & kn) << 4

          else:
            if (p == ROOK):

              sf[0] += 2
              a = RATT1(f) | RATT2(f)

              if ((a & kn) != 0):
                katt += _BITCnt(a & kn) << 4

            else:

              sf[0] += 4
              a = RATT1(f) | RATT2(f) | BATT3(f) | BATT4(f)

              if ((a & kn) != 0):
                katt += _BITCnt(a & kn) << 4

          t = p | getDir(f, kingpos[c])

          if ((t & 10) == 10):
            mn += _BITCnt(RATT1(f))
          if ((t & 18) == 18):
            mn += _BITCnt(RATT2(f))
          if ((t & 33) == 33):
            mn += _BITCnt(BATT3(f))
          if ((t & 65) == 65):
            mn += _BITCnt(BATT4(f))

        #--Back
        colorb[oc] ^= pieceb[QUEEN] & ocb
        #--Back
        colorb[oc] ^= BITi[kingpos[oc]]
        if (sf[0] == 1  and  (pieceb[PAWN] & colorb[c]) == 0):
          #--No mating material:
          mn =- 200

        if (sf[0] < 7):
          #--Reduce the bonus for attacking king squares
          katt = int(katt * sf[0]/7)

        if (sf[0] < 2):
          sf[0] = 2

        return mn + katt

      def eval0(c):

        global  kmobil, kingpos, eval1

        sf0 = 0
        sf1 = 0
        sfp = [sf0]

        ev0 = evalc(0, sfp)
        sf0 = sfp[0]
        sfp[0] = sf1
        ev1 = evalc(1, sfp)
        sf1 = sfp[0]
        eval1 += 1

        if (sf1 < 6):
          ev0 += kmobil[kingpos[0]]*(6-sf1)

        if (sf0 < 6):
          ev1 += kmobil[kingpos[1]]*(6-sf0)

        return iif(c != 0, (ev1 - ev0), (ev0 - ev1))

      def quiesce(ch,c,ply,alpha,beta):

        global  pval, movelist, movenum, mat_, kingpos, q_nodes, sd

        best = -32000
        cmat = iif( c == 1, -mat_, mat_ )

        if (ply>=sd):
          return eval0(c) + cmat

        if (ch == 0):

          if (cmat - 200 >= beta):
            return beta

          if (cmat + 200 > alpha):

            best = eval0(c) + cmat
            if (best > alpha):

              alpha = best
              if (best >= beta):
                return beta

        generateCaps(ch, c, ply)

        if (ch != 0  and  movenum[ply] == 0):
          return -32000 + ply

        i = -1
        while( (i+1) < movenum[ply]):

          i += 1

          m = qpick(movelist[ply], movenum[ply], i)

          if (ch == 0  and  PROM(m) == 0  and  pval[PIECE(m)] > pval[CAP(m)]  and  swap(m) < 0):
            continue

          doMove(m, c)
          q_nodes += 1

          w = -quiesce(attacked(kingpos[c^1], c^1), c^1, ply+1, -beta, -alpha)

          undoMove(m, c)

          if (w > best):

            best = w
            if (w > alpha):

              alpha = w
              if (w >= beta):
                return beta


        return iif( best >= alpha, best, eval0(c) + cmat )

      def retPVMove(c,ply):

        global  movelist, movenum, p_v, kingpos

        generateMoves(attacked(kingpos[c], c), c, 0)

        i = 0
        while(i < movenum[0]):

          m = movelist[0][i]

          if (m == p_v[0][ply]):
            return m

          i += 1

        return 0

      def Nonevariance(delta):

        global  Nonevar

        r = 0
        if (delta >= 4):
          r = 1
          while(r <= len(Nonevar)):

            if (delta < Nonevar[r - 1]):
              break
            r += 1

        return r

      def HASHP(c):

        global  hashb, hashxor, flags

        return (hashb ^ hashxor[flags | 1024 | (c << 11)])

      def HASHB(c,d):

        global  hashb, hashxor, flags

        return ((hashb ^ hashxor[flags | 1024]) ^ hashxor[c | (d << 1) | 2048])

      def search(ch,c,d,ply,alpha,beta,pvnode,isNone):

        global  PAWN, CNODES, HMASKB, HINVB, HMASKP, HINVP, hashDB, hashDP, hstack, BITC
        global  pawnfree, movelist, movenum, p_v, pvlength, kvalue, iter
        global  searchtime, maxtime, starttime, sabort, noabort, count, flags
        global  mat_, kingpos, pieceb, colorb, killer, history, nodes_, Nonevar, sd

        pvlength[ply] = ply

        if (ply>=sd):
          return eval0(c) + iif(c != 0, -mat_, mat_)

        nodes_ += 1
        if ((nodes_ & CNODES) == 0):

          consumed = time.clock() - starttime
          if ( consumed > maxtime  or  (consumed > searchtime  and  (not noabort))):
            sabort = True

        if (sabort):
          return eval0(c) + iif(c != 0, -mat_, mat_)

        hp = HASHP(c)
        if (ply != 0  and  isDraw(hp, 1) != 0):
          return 0

        if (d == 0):
          return quiesce(ch, c, ply, alpha, beta)
        hstack[COUNT()] = hp

        hb = HASHB(c, d)

        he = hashDB[(hb & HMASKB)]
        if (((he^hb) & HINVB) == 0):

          w = LOW16(he) - 32768
          if ((he & 0x10000) != 0):

            isNone = 0
            if (w <= alpha):
              return alpha

          else:

            if (w >= beta):
              return beta

        else:

          w = iif( c != 0, -mat_, mat_ )

        if (pvnode == 0  and  ch == 0  and  isNone != 0  and  d > 1  and  BITCnt(colorb[c] & (~pieceb[PAWN]) & (~pinnedPieces(kingpos[c], c^1))) > 2):

          flagstore = flags
          R = int( (10 + d + Nonevariance(w - beta))/4 )
          if (R > d):
            R = d

          flags &= 960
          count += 0x401

          #--Null Move Search
          w = -search(0, c^1, d-R, ply+1, -beta, -alpha, 0, 0)
          flags = flagstore
          count -= 0x401
          if (not sabort  and  w >= beta):

            hashDB[(hb & HMASKB)] = (hb & HINVB) | (w + 32768)
            return beta

        hsave = 0
        hmove = 0

        if (ply > 0):

          he = hashDP[(hp & HMASKP)]
          if (((he^hp) & HINVP) == 0):
            hsave = (he & HMASKP)
            hmove = hsave

          if (d >= 4  and  hmove == 0):

            #-- Simple version of Internal Iterative Deepening
            w = search(ch, c, d-3, ply, alpha, beta, pvnode, 0)
            he = hashDP[(hp & HMASKP)]
            if (((he^hp) & HINVP) == 0):
              hsave = (he & HMASKP)
              hmove = hsave

        else:

          hmove = retPVMove(c, ply)

        n = -1
        i = 0
        best = iif(pvnode != 0, alpha, -32001 )
        asave = alpha
        first = 1

        while (i != n):

          i += 1
          ext = 0
          if (hmove != 0):

            m = hmove
            hmove = 0
            i -= 1

          else:

            if (n == -1):

              generateMoves(ch, c, ply)
              n = movenum[ply]
              if (n == 0):
                return iif( ch != 0, -32000+ply, 0 )

            m = spick(movelist[ply], n, i, ply)

            if (hsave != 0  and  m == hsave):
              continue

          doMove(m, c)

          nch = attacked(kingpos[c^1], c^1)
          #-- Check Extension:
          if (nch != 0):
            ext += 1

          else:
            #--LMR
            if (d >= 3  and  i >= 4  and  pvnode == 0):

              if (CAP(m) == 0  and  PROM(m) == 0):

                if (PIECE(m) != PAWN  or  (pawnfree[c][TO(m)] & pieceb[PAWN] & colorb[c^1]) != 0):

                  ext -= 1

          if (first != 0  and  pvnode != 0):

            w = -search(nch, c^1, d-1+ext, ply+1, -beta, -alpha, 1, 1)
            if (ply == 0):
              noabort = (iter > 1  and  w < kvalue[iter-1] - 40)

          else:

            w = -search(nch, c^1, d-1+ext, ply+1, -alpha-1, -alpha, 0, 1)

            if (w > alpha  and  ext < 0):
              w = -search(nch, c^1, d-1, ply+1, -alpha-1, -alpha, 0, 1)

            if (w > alpha  and  w < beta  and  pvnode != 0):
              w = -search(nch, c^1, d-1+ext, ply+1, -beta, -alpha, 1, 1)

          undoMove(m, c)

          if (not sabort  and  w > best):

            if (w > alpha):

              hashDP[(hp & HMASKP)] = (hp & HINVP) | m
              alpha = w

            if (w >= beta):

              if (CAP(m) == 0):

                killer[ply] = m
                history[m & 0xFFF] += 1

              hashDB[(hb & HMASKB)] = (hb & HINVB) | (w + 32768)
              return beta

            if (pvnode != 0  and  w >= alpha):

              p_v[ply][ply] = m
              j = ply +1
              while(j < pvlength[ply +1]):
                p_v[ply][j] = p_v[ply +1][j]
                j += 1

              pvlength[ply] = pvlength[ply +1]
              if (ply == 0  and  iter > 1  and  w > kvalue[iter-1] - 20):
                noabort = False

              if (w == 31999 - ply):
                return w

            best = w

          first = 0

        if (not sabort  and  (pvnode != 0  or  asave == alpha)):
          hashDB[(hb & HMASKB)] = (hb & HINVB) | 0x10000 | (best + 32768)

        return alpha

      def execMove(m):

        global  hstack, movenum, count, onmove, kingpos, killer, history

        doMove(m, onmove)
        onmove ^= 1
        c = onmove

        hstack[COUNT()] = HASHP(c)
        i = 0
        while(i < 127):
          killer[i] = killer[i+1]
          i += 1

        i = 0
        while(i < 0x1000):
          history[i] = 0
          i += 1

        i = generateMoves(attacked(kingpos[c], c), c, 0)

        if (movenum[0] == 0):

          if (i == 0):

            print("1/2-1/2 Stalemate");
            return 4

          else:

            print(  iif(c == 1, "1-0 White mates", "0-1 Black mates") )
            return 5 + c

        c = isDraw(HASHP(c), 2)

        if( c==1 ):
          print("1/2-1/2 Draw by Repetition")
        else:
          if( c==2 ):
            print("1/2-1/2 Draw by Fifty Move Rule")
          else:
            if( c==3 ):
              print("1/2-1/2 Insufficient material")
            else:
              c = 0

        return c

      def ismove(m,to,fr,piece,prom,h):

        if (TO(m) != to):
          return False

        if (fr < 0  and  PIECE(m) != piece):
          return False

        if (fr >= 0  and  FROM(m) != fr):
          return False

        if (ISFILE(chr(h))  and  (FROM(m) & 7) != h - ord("a")):
          return False

        if (ISRANK(chr(h))  and  (FROM(m) & 56) != 8*(h - ord("1"))):
          return False

        if (prom != 0 and  PROM(m) != prom):
          return False

        return True

      def parseMove(s,c,p):

        global  PAWN, movelist, movenum, kingpos

        fr = -1
        piece = PAWN
        prom = 0
        h = 0
        ip = [1]

        if (s[0:5]=="O-O-O"):
          s = iif(c != 0, "Kc8", "Kc1")

        else:
          if (s[0:3]=="O-O"):
            s = iif(c != 0, "Kg8", "Kg1")

        sp = 0

        if(True):

          if (s[sp] >= "A"  and  s[sp] <= "Z"):
            piece = _getpiece(s[sp], ip)
            sp += 1
            if (piece< 1):
              return -1

          if (s[sp] == "x"):
            sp += 1

          if (ISRANK(s[sp])):
            h = s[sp]
            sp += 1
            if (s[sp] == "x"):
              sp += 1

          if (not ISFILE(s[sp])):
            return -1

          c1 = s[sp]
          sp += 1

          if (s[sp] == "x"):
            sp += 1

          if (ISFILE(s[sp])):
            h = c1
            c1 = s[sp]
            sp += 1

          c2 = s[sp]
          sp += 1

          if (not ISRANK(c2)):
            return -1

          if (len(s) > sp):

            if (s[sp] == "="):
              prom = _getpiece(s[sp + 1], ip)

            else:
              if (s[sp] != "+"):

                #-- Algebraic Notation
                fr = ord(c1) - ord("a") + 8*(ord(c2) - ord("1"))
                c1 = s[sp]
                sp += 1
                c2 = s[sp]
                sp += 1
                if (not ISFILE(c1)  or  not ISRANK(c2)):
                  return -1

                if (len(s) > sp):
                  prom = _getpiece(s[sp], ip)

          to = ord(c1) - ord("a") + 8*(ord(c2) - ord("1"))
          if (p != 0):

            if (ismove(p, to, fr, piece, prom, h)):
              return p

            return 0

          generateMoves(attacked(kingpos[c], c), c, 0)
          i = 0
          while(i < movenum[0]):

            if (ismove(movelist[0][i], to, fr, piece, prom, h)):
              return movelist[0][i]

            i += 1

        return 0

      def parseMoveNExec(s,c,m):

        m[0] = parseMove(s, c, 0)
        if (m[0] == -1):
          print("UNKNOWN COMMAND: " + s)

        else:
          if (m[0] == 0):
            errprint("Illegal move: " + s)

          else:
            return execMove(m[0])

        return -1

      def undo():

        global  mstack, onmove

        cnt = COUNT() - 1
        onmove ^= 1
        undoMove((mstack[cnt] >> 42), onmove)

      def calc():

        global  p_v, pvlength, kvalue, iter, searchtime, maxtime, starttime
        global  sabort, noabort, count, onmove, engine, kingpos
        global  eval1, nodes_, q_nodes, mps, inc, post_, sd,tm
        global  movemade

        movemade = ""
        t1 = 0
        m2go = 32
        ch = attacked(kingpos[onmove], onmove)
        eval1 = 0
        iter = 0
        kvalue[0] = 0
        sabort = False
        q_nodes = 0
        nodes_ = 0
        if (mps > 0):
          m2go = 1 + mps - ( int(COUNT()/2) % mps)

        searchtime = int( (tm*10)/m2go ) + inc
        maxtime = iif(inc != 0, tm*3, tm*2)

        starttime = time.clock()

        iter = 1
        while(iter <= sd):

          noabort = False
          kvalue[iter] = search(ch, onmove, iter, 0, -32000, 32000, 1, 0)
          t1 = (time.clock() - starttime)
          if (sabort  and  pvlength[0] == 0):
            iter -= 1
            if(iter != 0):
              break


          if (post_  and  pvlength[0] > 0):

            print(str(iter) + ". " + str(kvalue[iter]) + " " + str(int(t1)) + "s " + str(nodes_ + q_nodes) + " nodes ")
            displaypv()

          if (iter >= 32000-kvalue[iter]  or  sabort  or  t1 > searchtime/2):
            break

          iter += 1

        if (post_):
          s = ""
          s += "kibitz W: " + str(kvalue[  iif(iter > sd, sd, iter) ])
          s += " Nodes: " + str(nodes_)
          s += " QNodes: " + str(q_nodes)
          s += " Evals: " + str(eval1)
          s += " Secs: " + str( int(t1) )
          s += " knps: "+ str( int( (nodes_+q_nodes)/(t1+1) ) )
          print(s)

        movemade = mvstr(p_v[0][0])
        print( "move " + movemade )

        return execMove(p_v[0][0])

      def gomove():

        global  onmove, engine, sd, tm

        engine = onmove
        ex = calc()

      def entermove(buf):

        global  onmove

        m = [1]
        ex = parseMoveNExec(buf, onmove, m)

      def autogame():

        global  onmove, engine, sd, tm

        engine = onmove

        while(True):
          ex = calc()
          printboard()
          if( ex != 0 ):
            break

      def init():

        global  HSIZEB, HSIZEP, hashDB, hashDP, hashxor, rays, pmoves, pcaps, nmoves, kmoves
        global  _knight, _king, BITi, LSB, BITC, crevoke, nmobil, kmobil, pawnfree, pawnfile, pawnhelp
        global  bmask45, bmask135

        woutput("Arrays")

        i = 0
        while(i < 0x10000):
          LSB[i] = _slow_lsb(i)
          i += 1

        i = 0
        while(i < 0x10000):
          BITC[i] = _BITCnt(i)
          i += 1

        woutput("Zobrists")

        i = 0
        while(i < 4096):
          hashxor[i] = _rand_64()
          i += 1

        i = 0
        while(i < 64):
          BITi[i] = 1 << i
          i += 1

        woutput("Bitmasks")

        i = 0
        while(i < 64):
          bmask45[i] = _bishop45(i, 0, 0) | BITi[i]
          i += 1
        i = 0
        while(i < 64):
          bmask135[i] = _bishop135(i, 0, 0) | BITi[i]
          i += 1

        crevoke[7] ^= BITi[6]
        crevoke[63] ^= BITi[7]
        crevoke[0] ^= BITi[8]
        crevoke[56] ^= BITi[9]

        woutput("Rays")

        _init_rays1()
        _init_rays2()
        _init_rays3()
        _init_rays4()

        woutput("Shorts")

        _init_shorts(nmoves, _knight)
        _init_shorts(kmoves, _king)

        woutput("Pawns")

        _init_pawns(pmoves[0], pcaps[0], pawnfree[0], pawnfile[0], pawnhelp[0], 0)
        _init_pawns(pmoves[1], pcaps[1], pawnfree[1], pawnfile[1], pawnhelp[1], 1)

        _startpos()

        woutput("Board")

        i = 0
        while(i < 64):
          nmobil[i] = (BITCnt( nmoves[i])-1 )*6
          kmobil[i] = (BITCnt( int(nmoves[i]/2) ))*2
          i += 1

        woutput("Ready")

      #-- starting

      init()

      #--entermove("e2e4")
      #--gomove()
      #--printboard()

      autogame()



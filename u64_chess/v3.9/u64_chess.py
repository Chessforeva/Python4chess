# ---------------------------------------------
#
#   PYTHON 3.9 version
#
#   u64_chess python script by Chessforeva, mar.2022
#
#   Magic numbers MoveGen based (uint64) chess logic in python.
#   Setup position, perform  move generation with magics, make & unmake move.
#   May be improved by anyone in any project.
#   Does not count moves nor keeps notation history.
#
# ---------------------------------------------
#

#or class...
if True:

    # performance options 
    CHECK_FLAG = 1;         # to obtain check+ flags or not (0 = faster++)
    CKMATE_FLAG = 1;        # to obtain checkmate# flags or not (0 = faster+)
        
    # types U64,U32,U16,U8 as (unsigned bits)

    # white pieces
    WQ = 0; WR = 1; WB = 2; WN = 3; WP = 4; WK = 5; 
    # black pieces
    BQ = 6; BR = 7; BB = 8; BN = 9; BP = 10; BK = 11;  
    
    pieces = list("QRBNPKqrbnpk");
    
    MLIST = [0 for x in range(4<<8)];       # a buffer to store generated chess moves list
    ML2 = [0 for x in range(4<<6)];         # a small buffer to store possible checkmate evading moves list
    
    # a workaround "global variables" as object
    class u64_chess_vars:
        def __init__(self):

            self.B = [0 for x in range(12)];     # Board variables as array

            self.ENPSQ = 0;    # U64 en-passant square
            self.CASTLES = 0;  # U64 castles
            self.ToMove = 0;    # to move 0-white,1-black
            
            #oninit variables
            self.Bo1 = 0;      # boards U64
            self.Bo2 = 0;
            self.SqI = 0;       # U8 square to prepare
            self.b_r = 0;       # U8 1-bishops, 0-rooks
            self.b_w = 0;       # U8 1-black, 0-white (for pawns)
            self.legalck = 0;       # U8 Calculate: 0-allmoves-rays, 1-legalmoves

            # occupancy, only when calculating MoveGen
            self.WOCC = 0; self.BOCC = 0; self.OCC = 0; self.NOCC = 0;
            self.NWOCC = 0; self.NBOCC = 0; self.EOCC = 0; self.EWOCC = 0; self.EBOCC = 0;

            # U8
            self.sq = 0;    # current square
            self.ty = 0;    # piece type 0-12
            self.mv1 = 0;   # is it first move (to evade) we are searching (checkmate case)
            self.sqA = 0;   # king square
            
            # undo list counter
            self.uCnt = 0;
  
    #endclass u64_chess_vars
    
    # Object is accessible
    C = u64_chess_vars();

    class u64_undo:
        def __init__(self):
            
            self.B = [0 for x in range(12)];
            self.ENPSQ = 0;
            self.CASTLES = 0;
    #endclass u64_undo

    Undo = [ u64_undo() for x in range(256)];       # fast chess undo moves
    
    B2G7 = 0x007E7E7E7E7E7E00;     # inner squares constant

    # Magics for bishops
    BishopMagics = [
        0x6CFFD8B9D37E06BB, 0x7C178C7BF7F57CAE, 0xBD98AC81272FB5B8, 0xEDFAE51870C9F19F, 0x87F47FB1C074593A, 0xD7C16D85CA270CF5, 0x5BA782D5B7C17BB3, 0x3A4C9A5ACF80510D,
        0x6D57FAB6246EF2B3, 0x0BD74D62FC617A7B, 0x9584DA4D20B959BD, 0x6F723DEBECA069F4, 0xF4ACC795CB2D5CB5, 0x43C4F193D04AD6A9, 0x612085F344704B15, 0xE1A9E4CF7060D21F,
        0x596BEA7F05C0FE36, 0x6214025A7E63AD2F, 0x15912315DA5016A0, 0xBB3A96FA5092215F, 0x51C771E8BDF392C0, 0x7AEB8FC497D0BC32, 0x36FB5CF010EC579E, 0x34EB7C64AE28C243,
        0x4212BD8C83A6E4C0, 0xE0412592D1C1C3FF, 0x7751B104DA2A81FB, 0xF730B59B8571381C, 0x634900EA035C3400, 0xC840D3F3B6F9B929, 0x39C239F3FC93CB76, 0x66C5D96788357B03,
        0xD9824BEFC9415C11, 0xCD7DF0EFE183E6E3, 0xD79C76F086E33E64, 0x4DBA5F8501CE2400, 0xCBAF744A8043F100, 0x617DBA463E646CFF, 0x61B7B064856AD941, 0x5E682D8D0B916E5D,
        0xFD9CACF9DA01803E, 0xF6779696FF3E7EE0, 0x6FE2E5338E0C1248, 0x72165A308C570B6E, 0xAF7756B732E846E2, 0x6B1A5D734E172568, 0x2197A3345514B9D9, 0x678DBC7501FB2C50,
        0x78612467DABD1F04, 0x33966792F76720D1, 0x96C66374DDFB3360, 0x53860F0EE0C8CD45, 0x534290A02B766B2C, 0x5595C747518329FB, 0x4370788E0145B955, 0xFD35BBAF299013D9,
        0x6E266965ADAF646C, 0xA1DEEFF0A585674F, 0xD262607972DD3A36, 0xD46BC2B72BF218A5, 0x562CDC3F02EC43F5, 0x2AA80F72248BE656, 0x91F23AC46A1EE715, 0x013FB443B15EB41A
        ];

    # Magics for rooks
    RookMagics = [
        0xFF260527D2CAC700, 0x4CF0F24E7D5A5800, 0x829576FC130A3080, 0x5CFB475FC91E1100, 0x1C6E08D3004F2600, 0xF1B1998208AC1078, 0x06FCBDB2CB1BC4A8, 0x938C7FC1E07D6298,
        0x4E2D37B8F9E42E39, 0x45719CD9ACBBEB00, 0x29FBB48EFBF98AC0, 0xBBE3DBB8542C8C80, 0x1B0CBBC889E0A010, 0x784844442DBFABB8, 0x08320F627EE206D0, 0xE651EECBDD946AE0,
        0xBD8AEA197A509A03, 0x6412AE5F67893D00, 0x4CD4742FDEAA6A00, 0x324FDAC71DBAE100, 0x0D6F612384FF4DB0, 0xC0322570866933F0, 0xFE527633BA19DCCC, 0x65DD6D0E8C0A245C,
        0xCCD36B245D1A34BF, 0x301B25F9D1808F00, 0xCDD5B0E696401E00, 0xAA567462A1BFE7C0, 0xCB8D9FFE2B0A4540, 0xB002D050508A8808, 0x90DBCB9AA74E5DEC, 0x52BD607AD16823CE,
        0x6789D8D2F2B06E12, 0x84DBDAD1C0C9E180, 0xECA9A368B64154C0, 0xCB663F3098641DE0, 0x900DB76EA2B3CE30, 0x09A70669D4010E20, 0xC512D6EE770DE5A0, 0x797423BE8627BC94,
        0x8A3D575077F24F63, 0x0EC9B8F218AB9D00, 0x0C8587D6C0DD33C0, 0x60AF95CADD982560, 0xACC5169EB71CA590, 0x160D1C32B7BC6398, 0x88B6F3A8886C2D2A, 0x4C5BC7A588A0AB5C,
        0x0A2F0CEF3B7D0C39, 0xEF4D5C4858599E00, 0x1B041BF13B674200, 0xFB6B678E03BAAE00, 0xC277382FB0280FE0, 0x5C8971741F006128, 0x8A909A7AC999AAAC, 0x5405CD9DAE7D3E08,
        0x9D4D6B7CC2DAD786, 0xCE3D0AD07A35766A, 0xC0EA25A977591592, 0xC5C9BB5E7D8EF022, 0xB1552E04EC9C49E9, 0x9C16B80885B53F9E, 0xDE285EF1DAC7D27A, 0x441830E566CDF37A
        ];

    # pre-generated constants, pawnMagicGen created

    # Pawn Magics for white
    PawnMagicsWhite = [
        0x6CFFD877D338779F, 0x2D0386CD9AF51A16, 0xDCB0008790284C44, 0x333C8EF2E5D906EF, 0x1E6DA07F86EC13EE, 0x94D11367A0FD5CAD, 0x9709B0EB6FCD810F, 0x3D8E90C4BB4005AD,
        0xA6A7BE94DA1F1137, 0x1B8630C2852BB09F, 0x9340708591EE1E37, 0xE91CBC5191A3A197, 0xAC4EE4310657296B, 0xDEE4E205AA98C729, 0xA8ABD5055AF4DB4E, 0x46BA9C7AE7242EB6,
        0x6252531829102CD7, 0xB176F36A437EFFBC, 0xE238975A85BBD30E, 0x0F4879719F5BBD48, 0x391BABD74587079B, 0x9AA959C5C38475F9, 0x47EEF42CFD4B9CBE, 0xDD2625A6DEB18CF0,
        0x64D008AB74486795, 0xA549FB872086711C, 0xF78E16E50D1B5A89, 0x62652CC3E7B2F26C, 0xE6FF22805DA4DE30, 0x7461A0774C4AA2EB, 0xA313AE58FE92BF56, 0xBAB572F8AD1F9EB5,
        0x94294BB147BB4DD1, 0x8FE9F782F3628071, 0x502A4DFC65BB2CD7, 0x0B17D7D020C71381, 0xDE1BC1108396147C, 0x0A30E5A50BD76BF5, 0xCFB908AD73376570, 0xFA7695CF29EC6255,
        0x52098B6D5758118B, 0xBDEF4CCC69BEE6ED, 0xCCAA2F891E29F084, 0x82E975DC643571B7, 0xB3AE62F29104E480, 0xC0D3E6819B2CD37B, 0xCAEA117F7672BB6D, 0x429332B81C18CA21,
        0x9CB017BC75E21E8B, 0x0EF099078FCFACA1, 0x4F53FDFEEA51FFD8, 0x72786340CF25CF09, 0xE42C34931F0857D6, 0x5F7333B802F85437, 0x857BC8DD1CCE839D, 0x2F78D25830845451,
        0xFAB2742802D61FD6, 0xF209C3C525FC4C59, 0xBA341C4C9C969AFC, 0x463FC1E7ADD33298, 0x8CF30B7B3FCD7B03, 0xEDB6E8803AB36382, 0xA7FC85869CE3A9BF, 0xB3874247C2457A49
        ];

    # Pawn Magics for black
    PawnMagicsBlack = [
        0x34B5385467B0144E, 0x681F851A088CC9B4, 0x7B89F324FE8CF26A, 0x5BF0C6B8DE51A4A0, 0x01AA7F90EA79B9BE, 0x56E5D76FD603F447, 0x753FD6C0F78E9120, 0x07BD569FEE94CB02,
        0xBE258FF73E57AC8F, 0x5E4E68981294BC7A, 0x5A062E1BF8D08922, 0xC80D9383740DEA61, 0x23695C2D0F721BDB, 0x0977D01E826FC653, 0x90E511DF9A108B39, 0x41A803CDB5471786,
        0x335AE3B15F5240DE, 0x561F57E2309575B9, 0x3B11DC8FEB1ACF22, 0xAEAF00C7EF4D0E39, 0x81D6D3B4AEF63ABF, 0xBF115E265089C862, 0x4FC3107939FE3E66, 0x1798603F58B091DF,
        0x6E27B57B81A9D2C3, 0x37AB512383E9DB9F, 0xBBF8B5BD094F8341, 0xC207384103D41905, 0xF995FA59DC45BA79, 0x50295899DBB069C6, 0x04C2C62280E54351, 0xC7940130BD5768EB,
        0x337C373FBEE06777, 0xFB43A615E3F737A6, 0xA7B268D08CDFF0C2, 0xD71F68F86D96D418, 0x77EBB0A6233650BE, 0x75B14A4A00012E94, 0x5AA5ECD91FD515C3, 0x4A931E83788D4547,
        0xFF25A7A3640D3D1D, 0xCEE6E5AF3A655B1E, 0x4FA319769DB79349, 0x433A9EBBCEE081AA, 0x97417A5A444776A4, 0x577170E23E38E6D8, 0x1FC0E04A1D272ECF, 0xAF7433E56B8CAE83,
        0xE1B6AFBA7C1824A7, 0xA453ACBE41B15D47, 0xB4618E85E118C676, 0x0F100C3916985A57, 0xA0E42AA06F344462, 0x5DC8C067518E1929, 0xE8BB6960D5C30AE2, 0x53D67A580A7EDC08,
        0x5FBDF0D194E122DA, 0x592BEB15A5348A40, 0xF7E6A95D44B5559E, 0x198D8621B1AE3F9A, 0x17C09FEFDFEDC9A9, 0xCF90010F623D1DAE, 0x5AD8FDAA5A792633, 0x05C71892C521DFCB
        ];
    # BitCount=4  >>60

    # MoveGen arrays U64

    BishopMask = [0 for x in range(64)];
    RookMask = [0 for x in range(64)];
    
    BishopLegalsTable = [[0 for x in range(1<<16)] for x in range(64)];
    RookLegalsTable = [[0 for x in range(1<<16)] for x in range(64)];

    KnightLegals = [0 for x in range(64)];
    KingLegals = [0 for x in range(64)];

    PawnMaskWhite = [0 for x in range(64)];
    PawnMaskBlack = [0 for x in range(64)];

    PawnWhiteLegalsTable = [[0 for x in range(1<<4)] for x in range(64)];
    PawnBlackLegalsTable = [[0 for x in range(1<<4)] for x in range(64)];

    # Square attacked by opposite pawns
    PawnWhiteAtck = [0 for x in range(64)];     
    PawnBlackAtck = [0 for x in range(64)];
    
    # U64 castling constants
    cs_E1H1 = 144;
    cs_E1A1 = 17;
    cs_E8H8 = (9<<60);
    cs_E8A8 = (17<<56);
    N_cs_WH = int( ~(145) );
    N_cs_BL = int( ~(145<<56) );
    cs_ALL = (145<<56) | (145);
    F1G1 = 96;
    D1B1 = 14;
    F8G8 = (6<<60);
    D8B8 = (14<<56);
    
    # Count of 0s func.
    trailingZerosTable = [
        63, 0,  58, 1,  59, 47, 53, 2,
        60, 39, 48, 27, 54, 33, 42, 3,
        61, 51, 37, 40, 49, 18, 28, 20,
        55, 30, 34, 11, 43, 14, 22, 4,
        62, 57, 46, 52, 38, 26, 32, 41,
        50, 36, 17, 19, 29, 10, 13, 21,
        56, 45, 25, 31, 35, 16, 9,  12,
        44, 24, 15, 8,  23, 7,  6,  5
        ];

    def trail0(mask):
        m = int(mask & (-mask));
        n = int(m * 0x07EDD5E59A4E28C2);       # magic constant
        i = int( (n >> 58) & 63 );
        return trailingZerosTable[i];

    # dv,dh=-1,0,1   loop=1,0
    def gdir(dv, dh, loop):

        V = C.SqI>>3;
        H = C.SqI&7;
        V+=dv; H+=dh;
        while( (V>=0 and V<8) and (H>=0 and H<8) ):
            sq = (V<<3)|H;      #U8
            b = int(1<<sq);   #U64
            if(C.legalck):
                C.Bo2 |= b;
                if( C.Bo1 & b ):
                    return;
            else:
                C.Bo1 |= b;
    
            if(not loop):
                return;
            V+=dv; H+=dh;

        return;
        
    def gen2dir():

        if(C.b_r):  # bishops
            gdir(-1,-1,1); gdir(+1,-1,1); gdir(-1,+1,1); gdir(+1,+1,1);
        else:       # rooks
            gdir(-1,0,1); gdir(+1,0,1); gdir(0,+1,1); gdir(0,-1,1);
        return;

    # U8 sq=0-63 , U8 capt=1,0 capturing case
    def BoSet(sq,capt):
        
        u = 0;
        b = int(1<<sq);   #U64
        if(C.legalck):
            if(C.Bo1 & b):
                u = 1;
            if(capt==u):
                C.Bo2 |= b;
        else:
            C.Bo1 |= b;
        return u;

    def gen_pawnmoves():

        V = (C.SqI>>3);
        H = (C.SqI&7);
        if(V>0 and V<7):
            if(C.b_w):
                V-=1;
            else:
                V+=1;

            sq = (V<<3)|H;      #U8
            f = BoSet(sq,0);    #U8
            if(H>0):
                BoSet(sq-1,1);
            if(H<7):
                BoSet(sq+1,1);
            if(not f):
                if(C.b_w):
                    if(V==5):
                        BoSet(sq-8,0);
                else:
                    if(V==2):
                        BoSet(sq+8,0);
        return;

    def gen_pawn_atck():
    
        V = (C.SqI>>3);
        H = (C.SqI&7);
        if(C.b_w):
            V+=1;
        else:
            V-=1;
        
        if(V>0 and V<7):
            sq = (V<<3)|H;      # U8
            if(H>0):
                BoSet(sq-1,1);
            if(H<7):
                BoSet(sq+1,1);
        return;

    # Scan occupancy cases pawncase=0,1
    def Permutate(pawncase):
        
        bits = [0 for x in range(64)];      #U8
    
        n = 0;    #U8
        for sq in range(64):
            b = int(1<<sq);
            if( C.Bo1 & b ):
                bits[n]=sq;
                n+=1;


        Ln = int(1<<n);    #U16
        for i in range(Ln):

            C.Bo1 = 0;

            for j in range(n):	# scan as bits
    
                if(i & int(1<<j)):
                    b = int(1<<bits[j]);
                    C.Bo1 |= b;
		
        
            C.Bo2 = 0;       # find legal moves for square, put in Bo2

            if(pawncase):

                if(C.b_w):
                    m = PawnMagicsBlack[C.SqI];
                else:
                    m = PawnMagicsWhite[C.SqI];

                mult = int( C.Bo1 * m );
        
                i = int( (mult >> 60) & 15 );       # U8

                gen_pawnmoves();

                if(C.b_w):
                    PawnBlackLegalsTable[C.SqI][i] = C.Bo2;
                else:
                    PawnWhiteLegalsTable[C.SqI][i] = C.Bo2;
        
            else:
        
                if(C.b_r):
                    m = BishopMagics[C.SqI]
                else:
                    m = RookMagics[C.SqI];
        
                mult = int( C.Bo1 * m );

                i = int( (mult >> 48) & 0xFFFF);    # U16
        
                gen2dir();

                if(C.b_r):
                    BishopLegalsTable[C.SqI][i] = C.Bo2;
                else:
                    RookLegalsTable[C.SqI][i] = C.Bo2;
        return;

    def prepare_tables():

        for C.SqI in range(64):
            # print(C.SqI);        
            for C.b_r in range(2):
        
                C.legalck = 0;
                C.Bo1 = 0;
                gen2dir();
                b = int(1<<C.SqI);      # U64
                if( b & B2G7 ):
                    C.Bo1 &= B2G7;
                if(C.b_r):
                    BishopMask[C.SqI] = C.Bo1;
                else:
                    RookMask[C.SqI] = C.Bo1;
                C.legalck = 1;
                Permutate(0);

            for C.b_w in range(2):

                C.legalck = 0;
                C.Bo1 = 0;
                gen_pawnmoves();
                if(C.b_w):
                    PawnMaskBlack[C.SqI] = C.Bo1;
                else:
                    PawnMaskWhite[C.SqI] = C.Bo1;
                C.legalck = 1;
                Permutate(1);

                C.legalck = 0;
                C.Bo1 = 0;
                gen_pawn_atck();
                if(C.b_w):
                    PawnBlackAtck[C.SqI] = C.Bo1;
                else:
                    PawnWhiteAtck[C.SqI] = C.Bo1;
        return;
                    
    def prepare_knights():

        for C.SqI in range(64):
            C.Bo1 = 0;
            C.legalck=0;
            gdir(-1,-2,0); gdir(+1,-2,0); gdir(-2,+1,0); gdir(+2,-1,0);
            gdir(-1,+2,0); gdir(+1,+2,0); gdir(-2,-1,0); gdir(+2,+1,0);
            KnightLegals[C.SqI] = C.Bo1;

        return;

    def prepare_kings():
    
        for C.SqI in range(64):
            C.Bo1 = 0;
            C.legalck=0;
            gdir(-1,-1,0); gdir(-1,0,0); gdir(-1,+1,0); gdir(0,-1,0);
            gdir(+1,-1,0); gdir(+1,0,0); gdir(+1,+1,0); gdir(0,+1,0);
            KingLegals[C.SqI] = C.Bo1;

        return;

    #
    # chess logic
    #

    # rays of moves combined with occupancy mask
    # square 0-63, U64 occupancy, returns U64 moves as to-square-bits
    
    def getBishopMove(sq, occ):

        o = int( occ & BishopMask[sq] );       # U64
        m = int( o * BishopMagics[sq] );       # U64
        i = int( (m >> 48) & 0xFFFF );          # U16
        return BishopLegalsTable[sq][i];        # U64

    def getRookMove(sq, occ):
        
        o = int( occ & RookMask[sq] );         # U64
        m = int( o * RookMagics[sq] );         # U64
        i = int( (m >> 48) & 0xFFFF );          # U16
        return RookLegalsTable[sq][i];          # U64
        
    def getWhitePawnMove(sq, occ):

        o = int( occ & PawnMaskWhite[sq] );         # U64
        m = int( o * PawnMagicsWhite[sq] );         # U64
        i = int( (m >> 60) & 15 );                   # U8
        return PawnWhiteLegalsTable[sq][i];          # U64

    def getBlackPawnMove(sq, occ):

        o = int( occ & PawnMaskBlack[sq] );         # U64
        m = int( o * PawnMagicsBlack[sq] );         # U64
        i = int( (m >> 60) & 15 );                   # U8
        return PawnBlackLegalsTable[sq][i];          # U64

    # is check+
    def sqAttackedByWhites():

        if(KingLegals[C.sqA] & C.B[WK]):
            return 1;
        else:
            if(KnightLegals[C.sqA] & C.B[WN]):
                return 1;
            else:
                if(getRookMove(C.sqA,C.OCC) & (C.B[WR] | C.B[WQ])):
                    return 1;
                else:
                    if(getBishopMove(C.sqA,C.OCC) & (C.B[WB] | C.B[WQ])):
                        return 1;
                    else:
                        if(PawnWhiteAtck[C.sqA] & C.B[WP]):
                            return 1;
        return 0;

    def sqAttackedByBlacks():

        if(KingLegals[C.sqA] & C.B[BK]):
            return 1;
        else:
            if(KnightLegals[C.sqA] & C.B[BN]):
                return 1;
            else:
                if(getRookMove(C.sqA,C.OCC) & (C.B[BR] | C.B[BQ])):
                    return 1;
                else:
                    if(getBishopMove(C.sqA,C.OCC) & (C.B[BB] | C.B[BQ])):
                        return 1;
                    else:
                        if(PawnBlackAtck[C.sqA] & C.B[BP]):
                            return 1;
        return 0;
    
    #
    # Is check+?
    #
    def isCheck():

        C.WOCC = C.B[0]|C.B[1]|C.B[2]|C.B[3]|C.B[4]|C.B[5];
        C.BOCC = C.B[6]|C.B[7]|C.B[8]|C.B[9]|C.B[10]|C.B[11];
        C.OCC = C.WOCC | C.BOCC;
        if(C.ToMove):
            C.sqA = trail0(C.B[BK]);
            return sqAttackedByWhites();
        else:
            C.sqA = trail0(C.B[WK]);
            return sqAttackedByBlacks();

        return 0;

    #
    # Make a chess move on board
    #   L[i] is a move in the list

    def DoMove( L, i ):
    
        U = Undo[ C.uCnt ];
        U.B = list( C.B );
        U.CASTLES = C.CASTLES;
        U.ENPSQ = C.ENPSQ;
        C.uCnt += 1;

        p = 1 + (i<<2);
        ty = L[ p ];
        sq = L[ p+1 ];
        sqTo = L[ p+2 ];
        fr = int(1<<sq);
        to = int(1<<sqTo);
        fl = L[ p+3 ];

        if(fl&1):   # capture
            tc = (ty>>4)&15;
            ty &= 15;
            C.B[tc] &= int(~to);     # remove captured piece

        C.B[ty] &= int(~fr);         # move from
        if(fl&2):                   # promotion
            j = ((fl>>2)&3);
            if(C.ToMove):
                j += 6;
            C.B[j] |= to;
        else:
            C.B[ty] |= to;            # move to

        if(fl&16):                  # en-passant
            if(C.ToMove):
                C.B[WP] &= int( ~(1<<(sqTo+8)));
            else:
                C.B[BP] &= int( ~(1<<(sqTo-8)));
  
        if(C.CASTLES):
            C.CASTLES &= int( ~(fr | to) );


        if(fl&32):      # castling
            if(C.ToMove):
                if(sqTo>sq):
                    C.B[BK] = (1<<62);
                    C.B[BR] ^= (1<<63);
                    C.B[BR] |= (1<<61);
                else:
                    C.B[BK] = (1<<58);
                    C.B[BR] ^= (1<<56);
                    C.B[BR] |= (1<<59);
                    
                C.CASTLES &= N_cs_BL;
            else:
                if(sqTo>sq):
                    C.B[WK] = 64;
                    C.B[WR] ^= 128;
                    C.B[WR] |= 32;
                else:
                    C.B[WK] = 4;
                    C.B[WR] ^= 1;
                    C.B[WR] |= 8;
                    
                C.CASTLES &= N_cs_WH;
                
        # if pawn, set en-passant square
        C.ENPSQ = 0;
        if(ty==WP or ty==BP):
            if(C.ToMove):
                if(sq>47 and sqTo<40):
                    C.ENPSQ = int(1<<(sq-8));
            else:
                if(sq<16 and sqTo>23):
                    C.ENPSQ = int(1<<(sq+8));
        C.ToMove ^= 1;
        return;

    #  UnMake a chess move (fast)

    def UnDoMove():

        C.uCnt -= 1;
        U = Undo[ C.uCnt ];
        C.B = list( U.B );
        C.ENPSQ = U.ENPSQ;
        C.CASTLES = U.CASTLES;
        C.ToMove ^= 1;
        return;

    #
    # Sets Check+ flags
    #

    def getFlags( L, p ):

        if(C.mv1):
            return;

        if(C.ToMove):
            C.sqA = trail0(C.B[WK]);
            if( sqAttackedByBlacks() ):         # is opposite king checked+?
                L[ p+3 ] |= 64;
        else:
            C.sqA = trail0(C.B[BK]);
            if( sqAttackedByWhites() ):         # is opposite king checked+?
                L[ p+3 ] |= 64;
        return;

    #
    # Verifies checkmate cases, if check+ flag is set.
    #

    def getCheckMateFlags( L ):

        p = 1;        
        for i in range(L[0]):
            fl = L[ p+3 ];

            if(fl&64):          # is check+

                DoMove( L, i );
                C.mv1 = 1;

                MoveGen( ML2 );

                if( not ML2[0] ):
                    L[ p+3 ] |= 128;      # add checkmate flag, if could not escape check
    
                C.mv1 = 0;
                
                UnDoMove();

            p += 4;

        return;

    #
    # Tries to move the piece to all mo squares,
    # verifies if king left under attack,
    # saves in the list, if ok.
    #

    # U64 mo   moves to bits
    def addMove( L, mo ):

        fr = int(1<<C.sq);
        
        s = list( C.B );        # save
        sOCC = C.OCC;
        
        p = 1 + (L[0]<<2);
        
        while(mo):

            nf = int(~fr);
            C.B[C.ty] &= nf;           # moved from remove piece
            C.OCC &= nf;
            sqTo = trail0(mo);
            to = int(1<<sqTo);
            nt = int(~to);
            fC = fP = fE = tc = 0;

            # try move piece, verify attacks to our king
            C.B[C.ty] |= to;
            C.OCC |= to;

            if(C.ToMove):               # black
                C.sqA = trail0(C.B[BK]);
                if(C.EWOCC & to):
                    fC = 1;
                    for x in range(0,5):
                        if(C.B[x] & to):
                            tc = x;
                            C.B[x] &= nt;
                if((to==C.ENPSQ) and (C.ty==BP)):
                    C.B[WP] &= int( ~(C.ENPSQ<<8) );
                    fE = 16;

                # is black king ok?
                if(not sqAttackedByWhites()):
                    if((C.ty==BP) and (sqTo<8)):   # pawn promoted to
                        fP = 2;
                        C.B[BP] &= nt;
                        ss = C.B[BQ];
                        C.B[BQ] |= to;        # put a Queen

                    L[ p ] = C.ty | (tc<<4);
                    L[ p+1 ] = C.sq;
                    L[ p+2 ] = sqTo;
                    L[ p+3 ] = (fC | fP | fE);
                    L[0] += 1;
                    if CHECK_FLAG:
                        if(not C.mv1):
                            getFlags(L,p);

                    p += 4;

                    if(fP):                 # promoted
                        C.B[BQ] = ss;

                        ss = C.B[BR];
                        C.B[BR] |= to;      # put a Rook
                        L[ p ] = C.ty | (tc<<4);
                        L[ p+1 ] = C.sq;
                        L[ p+2 ] = sqTo;
                        L[ p+3 ] = (fC | (fP|4) | fE);
                        L[0] += 1;
                
                        if CHECK_FLAG:
                            if(not C.mv1):
                                getFlags(L,p);

                        p += 4;
                        C.B[BR] = ss;

                        ss = C.B[BB];
                        C.B[BB] |= to;      # put a Bishop
                        L[ p ] = C.ty | (tc<<4);
                        L[ p+1 ] = C.sq;
                        L[ p+2 ] = sqTo;
                        L[ p+3 ] = (fC | (fP|8) | fE);
                        L[0] += 1;
                
                        if CHECK_FLAG:
                            if(not C.mv1):
                                getFlags(L,p);

                        p += 4;
                        C.B[BB] = ss;

                        ss = C.B[BN];
                        C.B[BN] |= to;      # put a Knight
                        L[ p ] = C.ty | (tc<<4);
                        L[ p+1 ] = C.sq;
                        L[ p+2 ] = sqTo;
                        L[ p+3 ] = (fC | (fP|12) | fE);
                        L[0] += 1;
                
                        if CHECK_FLAG:
                            if(not C.mv1):
                                getFlags(L,p);

                        p += 4;
                        C.B[BN] = ss;

            else:                       # white
            
                C.sqA = trail0(C.B[WK]);
                if(C.EBOCC & to):
                    fC = 1;
                    for x in range(6,11):
                        if(C.B[x] & to):
                            tc = x;
                            C.B[x] &= nt;
                if((to==C.ENPSQ) and (C.ty==WP)):
                    C.B[WP] &= int( ~(C.ENPSQ>>8) );
                    fE = 16;
                    
                # is white king ok?
                if(not sqAttackedByBlacks()):
                    
                    if((C.ty==WP) and (sqTo>55)):   # pawn promoted to
                        fP = 2;
                        C.B[WP] &= nt;
                        ss = C.B[WQ];
                        C.B[WQ] |= to;        # put a Queen

                    L[ p ] = C.ty | (tc<<4);
                    L[ p+1 ] = C.sq;
                    L[ p+2 ] = sqTo;
                    L[ p+3 ] = (fC | fP | fE);
                    L[0] += 1;

                    if CHECK_FLAG:
                        if(not C.mv1):
                            getFlags(L,p);

                    p += 4;

                    if(fP):                 # promoted
                        C.B[WQ] = ss;

                        ss = C.B[WR];
                        C.B[WR] |= to;      # put a Rook
                        L[ p ] = C.ty | (tc<<4);
                        L[ p+1 ] = C.sq;
                        L[ p+2 ] = sqTo;
                        L[ p+3 ] = (fC | (fP|4) | fE);
                        L[0] += 1;
                
                        if CHECK_FLAG:
                            if(not C.mv1):
                                getFlags(L,p);

                        p += 4;
                        C.B[WR] = ss;

                        ss = C.B[WB];
                        C.B[WB] |= to;      # put a Bishop
                        L[ p ] = C.ty | (tc<<4);
                        L[ p+1 ] = C.sq;
                        L[ p+2 ] = sqTo;
                        L[ p+3 ] = (fC | (fP|8) | fE);
                        L[0] += 1;
                
                        if CHECK_FLAG:
                            if(not C.mv1):
                                getFlags(L,p);

                        p += 4;
                        C.B[WB] = ss;

                        ss = C.B[WN];
                        C.B[WN] |= to;      # put a Knight
                        L[ p ] = C.ty | (tc<<4);
                        L[ p+1 ] = C.sq;
                        L[ p+2 ] = sqTo;
                        L[ p+3 ] = (fC | (fP|12) | fE);
                        L[0] += 1;
                
                        if CHECK_FLAG:
                            if(not C.mv1):
                                getFlags(L,p);

                        p += 4;
                        C.B[WN] = ss;

            C.B = list(s);       # restore
            C.OCC = sOCC;

            mo &= mo-1;

        return;

    #  Castlings case

    def addCastleMove( L ):

        if(C.ToMove):
            r = C.B[BR];
            k = C.B[BK];
            if(C.sqA > C.sq):
                C.B[BK] = (1<<62);
                C.B[BR] ^= (1<<63);
                C.B[BR] |= (1<<61);
            else:
                C.B[BK] = (1<<58);
                C.B[BR] ^= (1<<56);
                C.B[BR] |= (1<<59);
        else:
            r = C.B[WR];
            k = C.B[WK];
            if(C.sqA > C.sq):
                C.B[WK] = 64;
                C.B[WR] ^= 128;
                C.B[WR] |= 32;
            else:
                C.B[WK] = 4;
                C.B[WR] ^= 1;
                C.B[WR] |= 8;

        p = 1 + (L[0]<<2);  
        L[ p ] = C.ty;
        L[ p+1 ] = C.sq;
        L[ p+2 ] = C.sqA;
        L[ p+3 ] = 32;
        L[0] += 1;

        if CHECK_FLAG:
            if(not C.mv1):
                getFlags(L,p);
        
        if(C.ToMove):
            C.B[BK] = k;
            C.B[BR] = r;
        else:
            C.B[WK] = k;
            C.B[WR] = r;

        return;
            
    # Cenerates the list of legal chess moves on current board
    # L[0] = count of moves, L[1-4] move0, L[5-8] move1,...
    def MoveGen( L ):

        C.WOCC = C.B[0]|C.B[1]|C.B[2]|C.B[3]|C.B[4]|C.B[5];
        C.BOCC = C.B[6]|C.B[7]|C.B[8]|C.B[9]|C.B[10]|C.B[11];
        C.OCC = C.WOCC | C.BOCC;
        C.NOCC = int( ~C.OCC );
        C.NWOCC = int( ~C.WOCC );
        C.NBOCC = int( ~C.BOCC );
        C.EOCC = C.OCC | C.ENPSQ;
        C.EWOCC = C.WOCC | C.ENPSQ;
        C.EBOCC = C.BOCC | C.ENPSQ;
    
        L[0] = 0;
    
        if(C.ToMove):       # Black to move

            # King moves
            P = C.B[BK]; C.ty = BK;
            C.sq = trail0(P);
            addMove(L,KingLegals[C.sq] & C.NBOCC);
            if(C.mv1 and L[0]):
                return;

            if(C.CASTLES and (not C.mv1)):
                if(((C.NOCC & F8G8)== F8G8) and ((C.CASTLES & cs_E8H8)==cs_E8H8)):
                    C.sqA = C.sq;
                    # is E8 under check+?
                    if(not sqAttackedByWhites()):
                        C.sqA += 1;
                        # is F8 check+?
                        if(not sqAttackedByWhites()):
                            C.sqA += 1;
                            # is G8 check+?
                            if(not sqAttackedByWhites()):
                                addCastleMove(L);   # add castling

                if(((C.NOCC & D8B8)== D8B8) and ((C.CASTLES & cs_E8A8)==cs_E8A8)):
                    C.sqA = C.sq;
                    # is E8 under check+?
                    if(not sqAttackedByWhites()):
                        C.sqA -= 1;
                        # is D8 check+?
                        if(not sqAttackedByWhites()):
                            C.sqA -= 1;
                            # is C8 check+?
                            if(not sqAttackedByWhites()):
                                addCastleMove(L);   # add castling
            C.sqA = C.sq;
            P = C.B[BR]; C.ty = BR;
            while(P):
                # Rook moves
                C.sq = trail0(P);
                addMove(L,getRookMove(C.sq,C.OCC) & C.NBOCC);
                P &= (P-1);

            P = C.B[BB]; C.ty = BB;
            while(P):
                # Bishop moves
                C.sq = trail0(P);
                addMove(L,getBishopMove(C.sq,C.OCC) & C.NBOCC);
                P &= (P-1);

            P = C.B[BQ]; C.ty = BQ;
            while(P):
                # Queen moves
                C.sq = trail0(P);
                addMove(L,getRookMove(C.sq,C.OCC) & C.NBOCC);
                addMove(L,getBishopMove(C.sq,C.OCC) & C.NBOCC);
                P &= (P-1);
                
            if(C.mv1 and L[0]):
                return;

            P = C.B[BN]; C.ty = BN;
            while(P):
                # Knight moves
                C.sq = trail0(P);
                addMove(L,KnightLegals[C.sq] & C.NBOCC);
                P &= (P-1);

            P = C.B[BP]; C.ty = BP;
            while(P):
                # Pawn moves
                C.sq = trail0(P);
                addMove(L,getBlackPawnMove(C.sq,C.EOCC) & C.NBOCC);
                P &= (P-1);

        else:               # White to move

            # King moves
            P = C.B[WK]; C.ty = WK;
            C.sq = trail0(P);
            addMove(L,KingLegals[C.sq] & C.NWOCC);
            if(C.mv1 and L[0]):
                return;

            if(C.CASTLES and (not C.mv1)):
                if(((C.NOCC & F1G1)== F1G1) and ((C.CASTLES & cs_E1H1)==cs_E1H1)):
                    C.sqA = C.sq;
                    # is E1 under check+?
                    if(not sqAttackedByBlacks()):
                        C.sqA += 1;
                        # is F1 check+?
                        if(not sqAttackedByBlacks()):
                            C.sqA += 1;
                            # is G1 check+?
                            if(not sqAttackedByBlacks()):
                                addCastleMove(L);   # add castling

                if(((C.NOCC & D1B1)== D1B1) and ((C.CASTLES & cs_E1A1)==cs_E1A1)):
                    C.sqA = C.sq;
                    # is E1 under check+?
                    if(not sqAttackedByBlacks()):
                        C.sqA -= 1;
                        # is D1 check+?
                        if(not sqAttackedByBlacks()):
                            C.sqA -= 1;
                            # is C1 check+?
                            if(not sqAttackedByBlacks()):
                                addCastleMove(L);   # add castling
            C.sqA = C.sq;
            P = C.B[WR]; C.ty = WR;
            while(P):
                # Rook moves
                C.sq = trail0(P);
                addMove(L,getRookMove(C.sq,C.OCC) & C.NWOCC);
                P &= (P-1);

            P = C.B[WB]; C.ty = WB;
            while(P):
                # Bishop moves
                C.sq = trail0(P);
                addMove(L,getBishopMove(C.sq,C.OCC) & C.NWOCC);
                P &= (P-1);

            P = C.B[WQ]; C.ty = WQ;
            while(P):
                # Queen moves
                C.sq = trail0(P);
                addMove(L,getRookMove(C.sq,C.OCC) & C.NWOCC);
                addMove(L,getBishopMove(C.sq,C.OCC) & C.NWOCC);
                P &= (P-1);

                if(C.mv1 and L[0]):
                    return;

            P = C.B[WN]; C.ty = WN;
            while(P):
                # Knight moves
                C.sq = trail0(P);
                addMove(L,KnightLegals[C.sq] & C.NWOCC);
                P &= (P-1);

            P = C.B[WP]; C.ty = WP;
            while(P):
                # Pawn moves
                C.sq = trail0(P);
                addMove(L,getWhitePawnMove(C.sq,C.EOCC) & C.NWOCC);
                P &= (P-1);

        if(CHECK_FLAG and CKMATE_FLAG):
            if(not C.mv1):
                getCheckMateFlags(L);

        return;

    #---------------------------------------------
                
    # Sets the initial chess position

    def SetStartPos():
    
        C.B[WK] = 16; C.B[WQ] = 8; C.B[WR] = 129; C.B[WB] = 36; C.B[WN] = 66; C.B[WP] = 65280;
        C.B[BK] = (1<<60); C.B[BQ] = (1<<59);
        C.B[BR] = (1<<56) | (1<<63);
        C.B[BB] = (1<<58) | (1<<61);
        C.B[BN] = (1<<57) | (1<<62);
        C.B[BP] = (255<<48);
        C.ENPSQ = 0;
        C.CASTLES = cs_ALL;
        C.ToMove = 0;
        C.uCnt = 0;
        return;

    # Board to char[64]
    # returns pieces a1-h7

    def sBoard():

        S = ["." for x in range(64)];
        for i in range(12):
            c = pieces[i];
            P = C.B[i];
            while(P):
                sq = trail0(P);
                if(S[sq]=='.'):
                    S[sq] = c;
                else:
                    S[sq] = '?';      # wtf cases
                P &= (P-1);

        return (''.join(S));

    # Prints Chess Board

    def printBoard():

        s = sBoard();
        for i in range(64,0,-8):
            print( s[i-8:i] );
        
        c = "";
        if(C.ToMove):
            c += 'b';
        else:
            c += 'w';
        
        if(isCheckMate()):
            c += '#';
        else:
            if(isCheck()):
                c += '+';

        print(c);

        return;

    # Legal moves to String

    def sLegalMoves( L ):

        s = "";
        
        for p in range(1, 1+(L[0]<<2), 4):
            ty = L[ p ] & 15;
            fr = L[ p+1 ];
            to = L[ p+2 ];
            fl = L[ p+3 ];

            Ck = " ";
            if(fl&128):
                Ck = "# ";       # checkmate
            else:
                if(fl&64):
                    Ck = '+ ';   # check+
 
            if(fl&32):              # castlings
                if(fr>to):
                    s += "O-O-O" + Ck;
                else:
                    s += "O-O" + Ck;
            else:

                Pc = "";
                if( not((ty==WP) or (ty==BP))):
                    if(ty>5):
                        ty -= 6;
                    Pc = pieces[ty];
                
                Cp = "-";
                if(fl&1):
                    Cp = "x";
                
                Ep = "";
                if(fl&16):
                    Ep = "ep";
                
                Pr = "";
                if(fl&2):
                    Pr = "=" + pieces[ (fl>>2)&3 ];
                
                s += Pc + chr(97+(fr&7))+chr(49+(fr>>3)) + Cp + chr(97+(to&7))+chr(49+(to>>3)) + Ep + Pr + Ck;
            
        return s;

    #
    # Put pieces directly on board - testing capabilities
    #   "pa2", "Ne3", "ng8", or clear " a3"
    #
    def PutPiece( s ):
    
        pc = s[0];
        sq = ((ord( s[2] )-49)<<3) | ((ord( s[1] )-97)&7);
        b = int(1<<sq);
        for i in range(12):
            if(pc==' '):
                C.B[i] &= int(~b);
            else:
                if(pieces[i]==pc):
                    C.B[i] |= b;
        return;

    #
    # Is checkmate#?
    #
    def isCheckMate():

        if(isCheck()):
            C.mv1 = 1;
            MoveGen( ML2 );
            C.mv1 = 0;
            
            return (ML2[0]==0);
        
        return 0;
        
    #
    # perform uci move
    # "e2e4", "b7a8q", "e1g1",...
    #
    # Returns 1 if made or 0 if error

    def uciMove( s ):

        f = ((ord( s[1] )-49)<<3) | ((ord( s[0] )-97)&7);
        t = ((ord( s[3] )-49)<<3) | ((ord( s[2] )-97)&7);
        pr = 0;
        if( len(s)>4 ):
            pr = "qrbn".find( s[4] );
            if(pr<0):
                pr = 0;

        MoveGen( MLIST );
        L = MLIST;
        
        p = 1;        
        for i in range(L[0]):
            fr = L[ p+1 ];
            to = L[ p+2 ];
            fl = L[ p+3 ];
            j = 0;
            if(fl&2):                   # promotion
                j = ((fl>>2)&3);
            
            if(fr==f and to==t and (pr==0 or j==pr)):
                DoMove(L,i);
                return 1;

            p += 4;

        return 0;


    #
    # Set position by uci FEN, but it is slow style
    #
    def SetByFEN( pos ):

        C.B = [0 for x in range(12)];     # clear board
        C.ToMove = 0;
        C.CASTLES = 0;
        C.ENPSQ = 0;
        enSq = 0;
    
        pcs = (''.join(pieces));
        y = 7; x = 0;
        w = 0;
        for c in pos:
            if(w==0):               # position
                if(c==" "):
                    w = 1;
                    continue;
                else:
                    if( c.isdigit() ):
                        x += ord(c)-49;
                    else:
                        if( c.isalpha() ):
                            i = pcs.find(c);
                            if(i>=0):
                                sq = ((y<<3)+x);
                                b = int( 1<<sq );
                                C.B[i] |= b;
                    if(x>6):
                        x = 0;
                        y -= 1;
                    else:
                        if(not(c=="/")):
                            x += 1;

            if(w==1):
                if(c==" "):
                    w = 2;
                    continue;
                if(c=="b"):
                    C.ToMove = 1;
            
            if(w==2):
                if(c==" "):
                    w = 3;
                    continue;
                if(c=="K"):
                    C.CASTLES |= cs_E1H1;
                if(c=="Q"):
                    C.CASTLES |= cs_E1A1;
                if(c=="k"):
                    C.CASTLES |= cs_E8H8;
                if(c=="q"):
                    C.CASTLES |= cs_E8A8;
                    
            if(w==3):
                if(c==" "):
                    w = 4;
                    if(enSq):
                        C.ENPSQ = (1<<enSq);
                    continue;
                    
                if( c.isdigit() ):
                    enSq += ((ord(c)-49)<<3);
                else:
                    if( c.isalpha() ):
                        enSq += ((ord(c)-97)&7);
                        
        C.uCnt = 0;
        return;

    #
    # Gets current uci FEN of position, slow too
    #

    def sGetFEN():
    
        s = sBoard();
        o = "";
        for i in range(64,0,-8):
            x = 0;
            for c in s[i-8:i]:
                if( c=="." ):
                    x += 1;
                else:
                    if(x>0):
                        o += chr( 48+x );
                        x = 0;
                    o += c;
            if(x>0):
                o += chr( 48+x );    
            if(i>8):
                o += "/";

        o += " ";
        if(C.ToMove):
            o += "b";
        else:
            o += "w";
        o += " ";
        if(not C.CASTLES):
            o += "-";
        else:
            if((C.CASTLES & cs_E1H1)==cs_E1H1):
                o += "K";
            if((C.CASTLES & cs_E1A1)==cs_E1A1):
                o += "Q";
            if((C.CASTLES & cs_E8H8)==cs_E8H8):
                o += "k";
            if((C.CASTLES & cs_E8A8)==cs_E8A8):
                o += "q";
        o += " ";
        if(not C.ENPSQ):
            o += "-";
        else:
            enSq = trail0(C.ENPSQ);
            o += chr( 97+(enSq&7) ) + chr( 49+(enSq>>3) );            
        
        o += " 0 1";

        return o;

    #
    # -------------------- Usage samples
    #
    #    Sample 1    Fast MoveGen with checkmate flag sample
    #

    def Sample1():          # fool's mate

        mv = [0 for x in range(4<<8)];
        
        uciMove("f2f3");
        uciMove("e7e5");
        uciMove("g2g4");

        printBoard();
        MoveGen( mv );
        print( sLegalMoves( mv ) );
        print( sGetFEN() );
        return;


    #
    #    Sample 2    The Puzzle.
    #

    def samp2_seek_2w():
        
        mv = [0 for x in range(4<<8)];
        MoveGen( mv );
        for p in range(1, 1+(mv[0]<<2), 4):            
            if( mv[ p+3 ] & 128 ):
                return 1;               # if checkmate flag,
        return 0;        # nope, no checkmate at all


    def samp2_seek_1b():

        mv = [0 for x in range(4<<8)];
        can = 0;            # can escape or not?
        MoveGen( mv );
        if( not mv[0]):
             return 0;      # stalemate?

        for i in range( mv[0] ):
            DoMove( mv, i );
            # can I avoid checkmate?
            can = samp2_seek_2w() ^ 1;      # opposite to opponent can checkmate
            UnDoMove();
            if(can):
                return 0;       # no checkmate here

        return 1;   # checkmate here

    def samp2_seek_1w():

        mv = [0 for x in range(4<<8)];
        MoveGen( mv );
        for i in range( mv[0] ):
            DoMove( mv, i );
            # if black can't escape checkmate and here it is
            if(samp2_seek_1b()):
                p = 1+(i<<2);
                fr = mv[ p+1 ];
                to = mv[ p+2 ];
                print("Go");
                print( chr( 97+(fr&7) ) + chr( 49+(fr>>3) ) + chr( 97+(to&7) ) + chr( 49+(to>>3) ) );
                print("to checkmate in 2 moves");
            UnDoMove();

        return;

    def Sample2():          # Set position and simple search

        # Solve 2 move checkmate puzzle.
        # This puzzle was created by Frank Healey,
        # and published in 5 Family Herald on 7/17/1858.
        # 7R/1B1N4/8/3r4/1K2k3/8/5Q2/8 w
        #   1.Rd8 Kd3 2.Nc5#

        SetByFEN("7R/1B1N4/8/3r4/1K2k3/8/5Q2/8 w");
        printBoard();
        samp2_seek_1w();
        return;

    #------------------------------------
    # init and run...
        
    print("init u64_chess...");
    prepare_tables();
    prepare_knights();
    prepare_kings();
    print("init done ok");

    SetStartPos();

    Sample1();
    Sample2();    
    
    # end of program



# ---------------------------------------------
#
#   PYTHON 2.7 version
#
#   u64_chess python script by Chessforeva, mar.2022
#
#   Magic numbers MoveGen based (uint64) chess logic in python.
#   Setup position, perform  move generation with magics, make & unmake move.
#   May be improved by anyone in any project.
#   Does not count moves nor keeps notation history.
#
#  Tested on pypy-2.0 JIT
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

            self.ENPSQ = 0L;    # U64 en-passant square
            self.CASTLES = 0L;  # U64 castles
            self.ToMove = 0;    # to move 0-white,1-black
            
            #oninit variables
            self.Bo1 = 0L;      # boards U64
            self.Bo2 = 0L;
            self.SqI = 0;       # U8 square to prepare
            self.b_r = 0;       # U8 1-bishops, 0-rooks
            self.b_w = 0;       # U8 1-black, 0-white (for pawns)
            self.legalck = 0;       # U8 Calculate: 0-allmoves-rays, 1-legalmoves

            # occupancy, only when calculating MoveGen
            self.WOCC = 0L; self.BOCC = 0L; self.OCC = 0L; self.NOCC = 0L;
            self.NWOCC = 0L; self.NBOCC = 0L; self.EOCC = 0L; self.EWOCC = 0L; self.EBOCC = 0L;

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
    
    B2G7 = 0x007E7E7E7E7E7E00L;     # inner squares constant

    # Magics for bishops
    BishopMagics = [
        0x6CFFD8B9D37E06BBL, 0x7C178C7BF7F57CAEL, 0xBD98AC81272FB5B8L, 0xEDFAE51870C9F19FL, 0x87F47FB1C074593AL, 0xD7C16D85CA270CF5L, 0x5BA782D5B7C17BB3L, 0x3A4C9A5ACF80510DL,
        0x6D57FAB6246EF2B3L, 0x0BD74D62FC617A7BL, 0x9584DA4D20B959BDL, 0x6F723DEBECA069F4L, 0xF4ACC795CB2D5CB5L, 0x43C4F193D04AD6A9L, 0x612085F344704B15L, 0xE1A9E4CF7060D21FL,
        0x596BEA7F05C0FE36L, 0x6214025A7E63AD2FL, 0x15912315DA5016A0L, 0xBB3A96FA5092215FL, 0x51C771E8BDF392C0L, 0x7AEB8FC497D0BC32L, 0x36FB5CF010EC579EL, 0x34EB7C64AE28C243L,
        0x4212BD8C83A6E4C0L, 0xE0412592D1C1C3FFL, 0x7751B104DA2A81FBL, 0xF730B59B8571381CL, 0x634900EA035C3400L, 0xC840D3F3B6F9B929L, 0x39C239F3FC93CB76L, 0x66C5D96788357B03L,
        0xD9824BEFC9415C11L, 0xCD7DF0EFE183E6E3L, 0xD79C76F086E33E64L, 0x4DBA5F8501CE2400L, 0xCBAF744A8043F100L, 0x617DBA463E646CFFL, 0x61B7B064856AD941L, 0x5E682D8D0B916E5DL,
        0xFD9CACF9DA01803EL, 0xF6779696FF3E7EE0L, 0x6FE2E5338E0C1248L, 0x72165A308C570B6EL, 0xAF7756B732E846E2L, 0x6B1A5D734E172568L, 0x2197A3345514B9D9L, 0x678DBC7501FB2C50L,
        0x78612467DABD1F04L, 0x33966792F76720D1L, 0x96C66374DDFB3360L, 0x53860F0EE0C8CD45L, 0x534290A02B766B2CL, 0x5595C747518329FBL, 0x4370788E0145B955L, 0xFD35BBAF299013D9L,
        0x6E266965ADAF646CL, 0xA1DEEFF0A585674FL, 0xD262607972DD3A36L, 0xD46BC2B72BF218A5L, 0x562CDC3F02EC43F5L, 0x2AA80F72248BE656L, 0x91F23AC46A1EE715L, 0x013FB443B15EB41AL
        ];

    # Magics for rooks
    RookMagics = [
        0xFF260527D2CAC700L, 0x4CF0F24E7D5A5800L, 0x829576FC130A3080L, 0x5CFB475FC91E1100L, 0x1C6E08D3004F2600L, 0xF1B1998208AC1078L, 0x06FCBDB2CB1BC4A8L, 0x938C7FC1E07D6298L,
        0x4E2D37B8F9E42E39L, 0x45719CD9ACBBEB00L, 0x29FBB48EFBF98AC0L, 0xBBE3DBB8542C8C80L, 0x1B0CBBC889E0A010L, 0x784844442DBFABB8L, 0x08320F627EE206D0L, 0xE651EECBDD946AE0L,
        0xBD8AEA197A509A03L, 0x6412AE5F67893D00L, 0x4CD4742FDEAA6A00L, 0x324FDAC71DBAE100L, 0x0D6F612384FF4DB0L, 0xC0322570866933F0L, 0xFE527633BA19DCCCL, 0x65DD6D0E8C0A245CL,
        0xCCD36B245D1A34BFL, 0x301B25F9D1808F00L, 0xCDD5B0E696401E00L, 0xAA567462A1BFE7C0L, 0xCB8D9FFE2B0A4540L, 0xB002D050508A8808L, 0x90DBCB9AA74E5DECL, 0x52BD607AD16823CEL,
        0x6789D8D2F2B06E12L, 0x84DBDAD1C0C9E180L, 0xECA9A368B64154C0L, 0xCB663F3098641DE0L, 0x900DB76EA2B3CE30L, 0x09A70669D4010E20L, 0xC512D6EE770DE5A0L, 0x797423BE8627BC94L,
        0x8A3D575077F24F63L, 0x0EC9B8F218AB9D00L, 0x0C8587D6C0DD33C0L, 0x60AF95CADD982560L, 0xACC5169EB71CA590L, 0x160D1C32B7BC6398L, 0x88B6F3A8886C2D2AL, 0x4C5BC7A588A0AB5CL,
        0x0A2F0CEF3B7D0C39L, 0xEF4D5C4858599E00L, 0x1B041BF13B674200L, 0xFB6B678E03BAAE00L, 0xC277382FB0280FE0L, 0x5C8971741F006128L, 0x8A909A7AC999AAACL, 0x5405CD9DAE7D3E08L,
        0x9D4D6B7CC2DAD786L, 0xCE3D0AD07A35766AL, 0xC0EA25A977591592L, 0xC5C9BB5E7D8EF022L, 0xB1552E04EC9C49E9L, 0x9C16B80885B53F9EL, 0xDE285EF1DAC7D27AL, 0x441830E566CDF37AL
        ];

    # pre-generated constants, pawnMagicGen created

    # Pawn Magics for white
    PawnMagicsWhite = [
        0x6CFFD8BCD3813025L, 0xD124186042012412L, 0x47D1CB98DC98C626L, 0x9960A3319A0370A7L, 0xF57AA11C65FA8AECL, 0x666F4312B4C037E1L, 0x2A68DDD475354CE9L, 0xA2E0E09B5C0EE01DL,
        0xE2791197D71749EFL, 0x8041E0F89AAFD8F1L, 0xC4E86860077C1E6BL, 0xF21CA852246F6593L, 0x2494C41F7D900347L, 0x6674B60D9A900A65L, 0xBF709C4103B32D43L, 0x7E7C73602722894BL,
        0x753A0BE05B7409DEL, 0xFAD801465CEBC598L, 0x75491B383EB986CEL, 0x160836D6E157ADEFL, 0x4293770388AFED51L, 0xFC00457C53A7A8CCL, 0x933A416F7FA1BEFBL, 0x3A6DD28A944A89A4L,
        0x2B32C9EDE5D36625L, 0x598807C071807290L, 0x51F67A2B4FCD94BEL, 0x30468DEB19182555L, 0x52502DB0AE2A8854L, 0xC766DFDBFA0EE2B9L, 0x138F57656ADC76B5L, 0x096D4FAF27875385L,
        0xF6C08BB990BB080DL, 0xEA57DFA529A2C4FEL, 0x5159A8BE8414092BL, 0x2F7650DCB9C84A47L, 0xCB9D650D37ED81BDL, 0xC98D4D7C35F95288L, 0x9AFC4746431B8281L, 0xAC7E6366E9AEC902L,
        0xE50204A876F2910CL, 0xDCDA62861C5E9DF2L, 0xB3E7DCF35BC01861L, 0xDF5BC8E4CB5AC47DL, 0x985E5D3573EE5DA0L, 0x3F622C3D95F8D13FL, 0x9CE96D4D9B47C5E4L, 0x47C859E4A93F3B86L,
        0x8B9EE7CFD60C44A9L, 0x48CD5724C7FD3EF1L, 0xEBE321BE5396A4C7L, 0x781EF3D4A0CBADCFL, 0x74B6985859DD0E89L, 0xAB099F864255121AL, 0x4B32732AFF896361L, 0x3C4755EB59E83C65L,
        0x0D08957E08521372L, 0xFDF19B39AD6BC6B2L, 0xF4D721133D240DA9L, 0x8C3481A7C4E3D2BFL, 0x06CFF88D337EFF50L, 0x1D7AC438742547ACL, 0xCDDBF6FB9AA9832DL, 0x6B9E69C6883FA50BL
        ];

    # Pawn Magics for black
    PawnMagicsBlack = [
        0x3BE7FC46927CF82FL, 0x4AAC763FA470CE98L, 0x0FF62BEE8FBD5F76L, 0xB2589E054CC0E43CL, 0x0D88BB0FD4C3F231L, 0x20F213C013DD9FEAL, 0xD0B2B77848F0A66DL, 0xEB14C34F54F2D57AL,
        0x19D7C8BAC44A9A6FL, 0x9E090BB094DEE86DL, 0xBA473B4EB44158E8L, 0xA844702091EB8067L, 0x23EC2A26EF0BE169L, 0x4EF88CEE76CE3FC9L, 0x0F17C5CCB32A834DL, 0xC4D1814E4C75D21BL,
        0x03976178DFD226F3L, 0xB117C3E4260AEE44L, 0xD9A5F62FFCC2D7EEL, 0x4391D38271B166B8L, 0xE843C4FF9888ABA1L, 0x121B595647031BBDL, 0x2D28D420366E2A36L, 0xC932750F8F70B654L,
        0x021A35782B70B577L, 0x22484DC1D25713C4L, 0x0E921CE58FA7D771L, 0xA4454E470A24AC31L, 0xA1A0D233233A1672L, 0xECBB9B320FD66DD3L, 0xFF52D3BAFC80874BL, 0x016A9AD5C6274070L,
        0x6761EA34FECAFF77L, 0xCB99473867611CA4L, 0x93E2A89D1DAF3327L, 0xB0C4D93293A295C1L, 0xC80CF6EC257F7312L, 0x5AFA753D0ACD0130L, 0x96AF80A64DEF717DL, 0xF8ACCB6A2FE5196FL,
        0xDD0A4D5B5C1D215EL, 0xC34300BB46EB9347L, 0x5411B3BE16DA5F92L, 0x684585F768A7CE1BL, 0x941465C6672E1F57L, 0x2D7C51046B0EAA08L, 0x648D13FAED26DA3EL, 0xA4EC588D84466058L,
        0x49130F7B82174554L, 0xAAA5518D3961B481L, 0xB27780EAA746F79FL, 0xD1D092A030E42126L, 0x7C0C9FF0C8720D80L, 0x38B93FAD85A2150DL, 0x1E7F6AF95FC31136L, 0x1CFB3E0C75045016L,
        0x05A7788C6DC71739L, 0x0C32324921486AA6L, 0xFDB67D5B6271DEF2L, 0x76711792B83C3F48L, 0xA57A37C961F4B050L, 0x24AB64AD89927642L, 0x8140B8DA4374A11FL, 0x01D5067165EACDA4L
        ];
    # BitCount=4  >>60

    # MoveGen arrays U64

    BishopMask = [0L for x in range(64)];
    RookMask = [0L for x in range(64)];
    
    BishopLegalsTable = [[0L for x in range(1<<16)] for x in range(64)];
    RookLegalsTable = [[0L for x in range(1<<16)] for x in range(64)];

    KnightLegals = [0L for x in range(64)];
    KingLegals = [0L for x in range(64)];

    PawnMaskWhite = [0L for x in range(64)];
    PawnMaskBlack = [0L for x in range(64)];

    PawnWhiteLegalsTable = [[0L for x in range(1<<4)] for x in range(64)];
    PawnBlackLegalsTable = [[0L for x in range(1<<4)] for x in range(64)];

    # Square attacked by opposite pawns
    PawnWhiteAtck = [0L for x in range(64)];     
    PawnBlackAtck = [0L for x in range(64)];
    
    # U64 castling constants
    cs_E1H1 = 144L;
    cs_E1A1 = 17L;
    cs_E8H8 = (9L<<60);
    cs_E8A8 = (17L<<56);
    N_cs_WH = long( ~(145L) );
    N_cs_BL = long( ~(145L<<56) );
    cs_ALL = (145L<<56) | (145L);
    F1G1 = 96L;
    D1B1 = 14L;
    F8G8 = (6L<<60);
    D8B8 = (14L<<56);
    
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
        m = long(mask & (-mask));
        n = long(m * 0x07EDD5E59A4E28C2L);       # magic constant
        i = int( (n >> 58) & 63 );
        return trailingZerosTable[i];

    # dv,dh=-1,0,1   loop=1,0
    def gdir(dv, dh, loop):

        V = C.SqI>>3;
        H = C.SqI&7;
        V+=dv; H+=dh;
        while( (V>=0 and V<8) and (H>=0 and H<8) ):
            sq = (V<<3)|H;      #U8
            b = long(1L<<sq);   #U64
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
        b = long(1L<<sq);   #U64
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
            b = long(1L<<sq);
            if( C.Bo1 & b ):
                bits[n]=sq;
                n+=1;


        Ln = int(1<<n);    #U16
        for i in range(Ln):

            C.Bo1 = 0L;

            for j in range(n):	# scan as bits
    
                if(i & int(1<<j)):
                    b = long(1L<<bits[j]);
                    C.Bo1 |= b;
		
        
            C.Bo2 = 0L;       # find legal moves for square, put in Bo2

            if(pawncase):

                if(C.b_w):
                    m = PawnMagicsBlack[C.SqI];
                else:
                    m = PawnMagicsWhite[C.SqI];

                mult = long( C.Bo1 * m );
        
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
        
                mult = long( C.Bo1 * m );

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
                C.Bo1 = 0L;
                gen2dir();
                b = long(1L<<C.SqI);      # U64
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
                C.Bo1 = 0L;
                gen_pawnmoves();
                if(C.b_w):
                    PawnMaskBlack[C.SqI] = C.Bo1;
                else:
                    PawnMaskWhite[C.SqI] = C.Bo1;
                C.legalck = 1;
                Permutate(1);

                C.legalck = 0;
                C.Bo1 = 0L;
                gen_pawn_atck();
                if(C.b_w):
                    PawnBlackAtck[C.SqI] = C.Bo1;
                else:
                    PawnWhiteAtck[C.SqI] = C.Bo1;
        return;
                    
    def prepare_knights():

        for C.SqI in range(64):
            C.Bo1 = 0L;
            C.legalck=0;
            gdir(-1,-2,0); gdir(+1,-2,0); gdir(-2,+1,0); gdir(+2,-1,0);
            gdir(-1,+2,0); gdir(+1,+2,0); gdir(-2,-1,0); gdir(+2,+1,0);
            KnightLegals[C.SqI] = C.Bo1;

        return;

    def prepare_kings():
    
        for C.SqI in range(64):
            C.Bo1 = 0L;
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

        o = long( occ & BishopMask[sq] );       # U64
        m = long( o * BishopMagics[sq] );       # U64
        i = int( (m >> 48) & 0xFFFF );          # U16
        return BishopLegalsTable[sq][i];        # U64

    def getRookMove(sq, occ):
        
        o = long( occ & RookMask[sq] );         # U64
        m = long( o * RookMagics[sq] );         # U64
        i = int( (m >> 48) & 0xFFFF );          # U16
        return RookLegalsTable[sq][i];          # U64
        
    def getWhitePawnMove(sq, occ):

        o = long( occ & PawnMaskWhite[sq] );         # U64
        m = long( o * PawnMagicsWhite[sq] );         # U64
        i = int( (m >> 60) & 15 );                   # U8
        return PawnWhiteLegalsTable[sq][i];          # U64

    def getBlackPawnMove(sq, occ):

        o = long( occ & PawnMaskBlack[sq] );         # U64
        m = long( o * PawnMagicsBlack[sq] );         # U64
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
        fr = long(1L<<sq);
        to = long(1L<<sqTo);
        fl = L[ p+3 ];

        if(fl&1):   # capture
            tc = (ty>>4)&15;
            ty &= 15;
            C.B[tc] &= long(~to);     # remove captured piece

        C.B[ty] &= long(~fr);         # move from
        if(fl&2):                   # promotion
            j = ((fl>>2)&3);
            if(C.ToMove):
                j += 6;
            C.B[j] |= to;
        else:
            C.B[ty] |= to;            # move to

        if(fl&16):                  # en-passant
            if(C.ToMove):
                C.B[WP] &= long( ~(1L<<(sqTo+8)));
            else:
                C.B[BP] &= long( ~(1L<<(sqTo-8)));
  
        if(C.CASTLES):
            C.CASTLES &= long( ~(fr | to) );


        if(fl&32):      # castling
            if(C.ToMove):
                if(sqTo>sq):
                    C.B[BK] = (1L<<62);
                    C.B[BR] ^= (1L<<63);
                    C.B[BR] |= (1L<<61);
                else:
                    C.B[BK] = (1L<<58);
                    C.B[BR] ^= (1L<<56);
                    C.B[BR] |= (1L<<59);
                    
                C.CASTLES &= N_cs_BL;
            else:
                if(sqTo>sq):
                    C.B[WK] = 64L;
                    C.B[WR] ^= 128L;
                    C.B[WR] |= 32L;
                else:
                    C.B[WK] = 4L;
                    C.B[WR] ^= 1L;
                    C.B[WR] |= 8L;
                    
                C.CASTLES &= N_cs_WH;
                
        # if pawn, set en-passant square
        C.ENPSQ = 0L;
        if(ty==WP or ty==BP):
            if(C.ToMove):
                if(sq>47 and sqTo<40):
                    C.ENPSQ = long(1L<<(sq-8));
            else:
                if(sq<16 and sqTo>23):
                    C.ENPSQ = long(1L<<(sq+8));
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

        fr = long(1L<<C.sq);
        
        s = list( C.B );        # save
        sOCC = C.OCC;
        
        p = 1 + (L[0]<<2);
        
        while(mo):

            nf = long(~fr);
            C.B[C.ty] &= nf;           # moved from remove piece
            C.OCC &= nf;
            sqTo = trail0(mo);
            to = long(1L<<sqTo);
            nt = long(~to);
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
                    C.B[WP] &= long( ~(C.ENPSQ<<8) );
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
                    C.B[WP] &= long( ~(C.ENPSQ>>8) );
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
                C.B[BK] = (1L<<62);
                C.B[BR] ^= (1L<<63);
                C.B[BR] |= (1L<<61);
            else:
                C.B[BK] = (1L<<58);
                C.B[BR] ^= (1L<<56);
                C.B[BR] |= (1L<<59);
        else:
            r = C.B[WR];
            k = C.B[WK];
            if(C.sqA > C.sq):
                C.B[WK] = 64L;
                C.B[WR] ^= 128L;
                C.B[WR] |= 32L;
            else:
                C.B[WK] = 4L;
                C.B[WR] ^= 1L;
                C.B[WR] |= 8L;

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
        C.NOCC = long( ~C.OCC );
        C.NWOCC = long( ~C.WOCC );
        C.NBOCC = long( ~C.BOCC );
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
    
        C.B[WK] = 16L; C.B[WQ] = 8L; C.B[WR] = 129L; C.B[WB] = 36L; C.B[WN] = 66L; C.B[WP] = 65280L;
        C.B[BK] = (1L<<60); C.B[BQ] = (1L<<59);
        C.B[BR] = (1L<<56) | (1L<<63);
        C.B[BB] = (1L<<58) | (1L<<61);
        C.B[BN] = (1L<<57) | (1L<<62);
        C.B[BP] = (255L<<48);
        C.ENPSQ = 0L;
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
        b = long(1L<<sq);
        for i in range(12):
            if(pc==' '):
                C.B[i] &= long(~b);
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
        C.CASTLES = 0L;
        C.ENPSQ = 0L;
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
                                b = long( 1L<<sq );
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
                        C.ENPSQ = (1L<<enSq);
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

    #Sample1();
    #Sample2();    
    
    # end of program



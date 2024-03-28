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
        0x6CFFD8BCD3813025, 0xD124186042012412, 0x47D1CB98DC98C626, 0x9960A3319A0370A7, 0xF57AA11C65FA8AEC, 0x666F4312B4C037E1, 0x2A68DDD475354CE9, 0xA2E0E09B5C0EE01D,
        0xE2791197D71749EF, 0x8041E0F89AAFD8F1, 0xC4E86860077C1E6B, 0xF21CA852246F6593, 0x2494C41F7D900347, 0x6674B60D9A900A65, 0xBF709C4103B32D43, 0x7E7C73602722894B,
        0x753A0BE05B7409DE, 0xFAD801465CEBC598, 0x75491B383EB986CE, 0x160836D6E157ADEF, 0x4293770388AFED51, 0xFC00457C53A7A8CC, 0x933A416F7FA1BEFB, 0x3A6DD28A944A89A4,
        0x2B32C9EDE5D36625, 0x598807C071807290, 0x51F67A2B4FCD94BE, 0x30468DEB19182555, 0x52502DB0AE2A8854, 0xC766DFDBFA0EE2B9, 0x138F57656ADC76B5, 0x096D4FAF27875385,
        0xF6C08BB990BB080D, 0xEA57DFA529A2C4FE, 0x5159A8BE8414092B, 0x2F7650DCB9C84A47, 0xCB9D650D37ED81BD, 0xC98D4D7C35F95288, 0x9AFC4746431B8281, 0xAC7E6366E9AEC902,
        0xE50204A876F2910C, 0xDCDA62861C5E9DF2, 0xB3E7DCF35BC01861, 0xDF5BC8E4CB5AC47D, 0x985E5D3573EE5DA0, 0x3F622C3D95F8D13F, 0x9CE96D4D9B47C5E4, 0x47C859E4A93F3B86,
        0x8B9EE7CFD60C44A9, 0x48CD5724C7FD3EF1, 0xEBE321BE5396A4C7, 0x781EF3D4A0CBADCF, 0x74B6985859DD0E89, 0xAB099F864255121A, 0x4B32732AFF896361, 0x3C4755EB59E83C65,
        0x0D08957E08521372, 0xFDF19B39AD6BC6B2, 0xF4D721133D240DA9, 0x8C3481A7C4E3D2BF, 0x06CFF88D337EFF50, 0x1D7AC438742547AC, 0xCDDBF6FB9AA9832D, 0x6B9E69C6883FA50B
        ];

    # Pawn Magics for black
    PawnMagicsBlack = [
        0x3BE7FC46927CF82F, 0x4AAC763FA470CE98, 0x0FF62BEE8FBD5F76, 0xB2589E054CC0E43C, 0x0D88BB0FD4C3F231, 0x20F213C013DD9FEA, 0xD0B2B77848F0A66D, 0xEB14C34F54F2D57A,
        0x19D7C8BAC44A9A6F, 0x9E090BB094DEE86D, 0xBA473B4EB44158E8, 0xA844702091EB8067, 0x23EC2A26EF0BE169, 0x4EF88CEE76CE3FC9, 0x0F17C5CCB32A834D, 0xC4D1814E4C75D21B,
        0x03976178DFD226F3, 0xB117C3E4260AEE44, 0xD9A5F62FFCC2D7EE, 0x4391D38271B166B8, 0xE843C4FF9888ABA1, 0x121B595647031BBD, 0x2D28D420366E2A36, 0xC932750F8F70B654,
        0x021A35782B70B577, 0x22484DC1D25713C4, 0x0E921CE58FA7D771, 0xA4454E470A24AC31, 0xA1A0D233233A1672, 0xECBB9B320FD66DD3, 0xFF52D3BAFC80874B, 0x016A9AD5C6274070,
        0x6761EA34FECAFF77, 0xCB99473867611CA4, 0x93E2A89D1DAF3327, 0xB0C4D93293A295C1, 0xC80CF6EC257F7312, 0x5AFA753D0ACD0130, 0x96AF80A64DEF717D, 0xF8ACCB6A2FE5196F,
        0xDD0A4D5B5C1D215E, 0xC34300BB46EB9347, 0x5411B3BE16DA5F92, 0x684585F768A7CE1B, 0x941465C6672E1F57, 0x2D7C51046B0EAA08, 0x648D13FAED26DA3E, 0xA4EC588D84466058,
        0x49130F7B82174554, 0xAAA5518D3961B481, 0xB27780EAA746F79F, 0xD1D092A030E42126, 0x7C0C9FF0C8720D80, 0x38B93FAD85A2150D, 0x1E7F6AF95FC31136, 0x1CFB3E0C75045016,
        0x05A7788C6DC71739, 0x0C32324921486AA6, 0xFDB67D5B6271DEF2, 0x76711792B83C3F48, 0xA57A37C961F4B050, 0x24AB64AD89927642, 0x8140B8DA4374A11F, 0x01D5067165EACDA4
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



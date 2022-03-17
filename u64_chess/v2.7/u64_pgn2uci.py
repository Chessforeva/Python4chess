#----------------------------------------------------------
#
#   PYTHON 2.7 version
#
#   pgn2uci written in python
#
#   This is a very slow but working chess games pgn-file parser
#    that creates uci moves strings for all chess games
#     to process on chess engines like
#            stockfish position startpos moves e2e4 e7e5 ....
#

execfile("u64_chess.py");

if True:

    # Make it faster, no need to analyse checkmate or not
    CHECK_FLAG = 0;
    CKMATE_FLAG = 0;

    
    pgn_file = "tatamast22.pgn";
    uci_file = "tatamast22uci.txt";
    
    St = 0;
    header = 0;
    moves = 1;
    ucis = 2;
    S = [ "", "", "" ];
    
    moveNr = 0;
    gamesCnt = 1;
    N = [ 0, 0 ];
    
    def printout():
            
        N[moveNr] = 1;
        q = 0;
        s = "";
        piec = "QRBNPK";
        prom1 = "QRBNqrbn";
        prom2 = "qrbnqrbn";

        S1 = S[moves].replace("ep","");
        for c in S1:
            w = c;
            if(w=="{"):
                q += 1;
            if(q>0 or ord(w)<=13):          # remove comments and tabs
                w = " ";
            if(w=="}"):
                q -= 1;
            s += w;

        SetStartPos();
        
        mv = [0 for x in range(4<<8)];

        MoveGen(mv);
        
        M = s.split(" ");       # Read each move
        for m in M:
        
            cs = 0;     # castling cases
            if( m == "0-0-0" or m == "O-O-O" ):
                cs = 2;
            else:
                if( m == "0-0" or m == "O-O" ):
                    cs = 1;
         
            if( not(cs) ):
                Pc = "P"; w = 0; Pp = " ";
                h1 = 0; v1 = 0; h2 = 0; v2 = 0;
                for c in m:
                    if(w<6):
                        if(c=="."):     # if it is move number only, ignore
                            w = 0;
                            continue;
                            
                        p = piec.find(c);
                        if(p>=0):
                            Pc = piec[p];
                    
                        if(w<3 and (c in ['x','-',':'])):
                            w = 3;
                            continue
                    
                        if(c>="a" and c<="h"):
                            if(w<3 and h1==0):
                                h1 = c;
                                w = 2;
                            else:
                                if(w<6):
                                    h2 = c;
                                    w = 4;
                            continue;

                        if(w>0 and c>='1' and c<='8'):
                            if(w<3 and v1==0):
                                v1 = c;
                                w = 3;
                            else:
                                if(w<6):
                                    v2 = c;
                                    w = 5;
                            continue;

                        if(c=='='):
                            w = 6;
                            continue;

                    if(w>4):
                        p = prom1.find(c);
                        if(p>=0):
                            Pp = prom2[p]; 

                if(h2==0):
                    h2 = h1; v2 = v1;
                    h1 = 0; v1 = 0;

                if(h2==0 and v2==0):
                    continue;
    
            f = 0;      # found
            p = 1;
            for i in range( mv[0] ):
            
                ty = mv[ p ] & 15;
                fr = mv[ p+1 ];
                to = mv[ p+2 ];
                fl = mv[ p+3 ];

                if(fl&32):
                    if (fr>to and cs==2):
                        f = 1;
                    if (fr<to and cs==1):
                        f = 1;
                
                if(not(f)):
                    if(ty>5):
                        ty -= 6;
                        
                    if(piec[ty]==Pc):
                        f = 1;
                        if( h1 and (not(h1==chr( 97+(fr&7) ))) ):
                            f = 0;
                        if( v1 and (not(v1==chr( 49+(fr>>3) ))) ):
                            f = 0;
                        if( h2 and (not(h2==chr( 97+(to&7) ))) ):
                            f = 0;
                        if( v2 and (not(v2==chr( 49+(to>>3) ))) ):
                            f = 0;

                    pr = " ";
                    if(fl&2):       # promotion
                        pr = prom2[ ((fl>>2)&3) ];
                        if( not(Pp==" ") and not(Pp==pr) ):
                            f = 0;
     
                if(f):      # if found
            
                    DoMove( mv, i );
                
                    u = "";
                    u += chr( 97+(fr&7) );
                    u += chr( 49+(fr>>3) );
                    u += chr( 97+(to&7) );
                    u += chr( 49+(to>>3) );
                    if( not(Pp==" ") ):
                        u += Pp;
                    
                    S[ucis] += u + " ";
                
                    MoveGen(mv);
                    if(C.ToMove==0):
                        N[moveNr] += 1;
                    break;

                p += 4;
    
        fuci.write( S[header] + "\n" + S[ucis] + "\n\n"  );
        N[gamesCnt] += 1;
        if( (N[gamesCnt] % 10)==0 ):
            print( N[gamesCnt] );
        
        return;
    
    fuci = open( uci_file, "w");
    fpgn = open( pgn_file, "r" );
    print( "Reading " + pgn_file );
    print( "Writing " + uci_file );
    
    for line in fpgn:
    
        if(line[0]=="["):
            if(St==2):
                printout();
            if(St!=1):
                S[header] = "";
                S[moves] = "";
                S[ucis] = "";
            St = 1;
            for c in line:
                if( ord(c)>13 ):
                    S[header] += c;
        else:
            if(St==1):
                if( line.find(".")>=0 ):
                    St = 2;

            if(St==2):
                S[moves] += " ";
                for c in line:
                    if( ord(c)>13 ):
                        S[moves] += c;
                S[moves] += " ";
    if(St==2):
        printout();

    
    fpgn.close();
    fuci.close();
    print( "done");

    # end of program

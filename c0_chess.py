# Chess library for python
# just chess logic scripts, no visual representation
# Board in variables, moves, FEN & PGN functions
# no clock, no chess engine
#-----------------------------------------------------
# Use it freely in Your scripts


#class c0_chess:
if True:

	global c0_position, c0_side, c0_sidemoves, c0_moving
	global c0_wKingmoved, c0_bKingmoved, c0_wLRockmoved, c0_wRRockmoved, c0_bLRockmoved, c0_bRRockmoved, c0_w00, c0_b00
	global c0_lastmovepawn, c0_become, c0_become_from_engine, c0_moveslist
	global c0_start_FEN, c0_fischer, c0_fischer_cst
	global c0_PG_viewer, c0_PG_1, c0_PGN_header, c0_errflag, PGN_text
	global c0_foundmove, c0_bestmove, c0_NAGs, c0_moves2do

	c0_position=""
	c0_side=1
	c0_sidemoves=1
	c0_moving=False

	c0_wKingmoved = False
	c0_bKingmoved = False
	c0_wLRockmoved = False
	c0_wRRockmoved = False
	c0_bLRockmoved = False
	c0_bRRockmoved = False
	c0_w00 = False
	c0_b00 = False

	c0_lastmovepawn = 0

	c0_become=""
	c0_become_from_engine=""
				# just engine

	c0_moveslist = ""

				# queue of movements delivered to 3d part above
	c0_moves2do=""

	c0_foundmove=""
	c0_bestmove=""

	c0_start_FEN=""
	c0_fischer=False
	c0_fischer_cst=""

	c0_PG_viewer=True
			# Set True for on-error-prints/ False for silent processing...

	c0_PG_1=""

	c0_PGN_header= []

	c0_errflag=False

	PGN_text=""
						# PGN support, the game data will be here....
	c0_NAGs=""

	c0_moves2do=""
	
	
	def substr(str, start, lens ):
		return str[start: start+lens]
	def substrall(str, start ):
		return str[start:]

	def charCodeAt(str, at):
		return ord(str[at])
	
	def fromCharCode(cd):
		return chr(cd)

	def parseInt(s):
		if(len(s)==0 or ("0123456789-.").find(s[0],0)<0): return 0
		else: return int(s)
	
	def ToString(val):
		return str(val)

	def IndexOf(buff,str):
		return buff.find(str,0)

	def window_confirm(messtxt):
		return True			# No dialogs at the moment...
	
	def c0_ReplaceAll(Source,stringToFind,stringToReplace):
		return Source.replace(stringToFind,stringToReplace)

	global pawnPos, knightPos, bishopPos, rookPos, queenPos, kingPos
	
	pawnPos = [ 0, 0, 0, 0, 0, 0, 0, 0, -25, 105, 135, 270, 270, 135, 105, -25, -80, 0, 90, 176, 176, 90, 0, -80, -85, -5, 40, 275, 275, 40, -5, -85, -90, -10, 30, 225, 225, 30, -10, -90, -95, -15, 15, 75, 75, 15, -15, -95, -100, -20, 10, 70, 70, 10, -20, -100, 0, 0, 0, 0, 0, 0, 0, 0 ]

	knightPos = [ -200, -100, -50, -50, -50, -50, -100, -200, -100, 0, 0, 0, 0, 0, 0, -100, -50, 0, 60, 60, 60, 60, 0, -50, -50, 0, 30, 60, 60, 30, 0, -50, -50, 0, 30, 60, 60, 30, 0, -50, -50, 0, 30, 30, 30, 30, 0, -50, -100, 0, 0, 0, 0, 0, 0, -100, -200, -50, -25, -25, -25, -25, -50, -200 ]
     
	bishopPos = [ -50,-50,-25,-10,-10,-25,-50,-50, -50,-25,-10,  0,  0,-10,-25,-50, -25,-10,  0, 25, 25, 0,-10,-25, -10,  0, 25, 40, 40, 25,  0,-10, -10,  0, 25, 40, 40, 25,  0,-10, -25,-10,  0, 25, 25,  0,-10,-25, -50,-25,-10,  0,  0,-10,-25,-50, -50,-50,-25,-10,-10,-25,-50,-50 ]

	rookPos = [ -60, -30, -10, 20, 20, -10, -30, -60,  40,  70,  90, 120,120,  90,  70, 40, -60, -30, -10, 20, 20, -10, -30, -60, -60, -30, -10, 20, 20, -10, -30, -60, -60, -30, -10, 20, 20, -10, -30, -60, -60, -30, -10, 20, 20, -10, -30, -60, -60, -30, -10, 20, 20, -10, -30, -60, -60, -50, -10, 20, 20, -10, -50, -60 ]

	queenPos = [ 20, 20, 20, 20, 20, 20, 20, 20, 20, 30, 30, 30, 30, 30, 30, 20, 20, 30, 40, 40, 40, 40, 30, 20, 20, 30, 40, 50, 50, 40, 30, 20, 20, 30, 40, 50, 50, 40, 30, 20, 20, 30, 40, 40, 40, 40, 30, 20, 20, 30, 30, 30, 30, 30, 30, 20, 20, 20, 20, 20, 20, 20, 20, 20 ]

	kingPos = [ 50, 150, -25, -125, -125, -25, 150, 50, 50, 150, -25, -125, -125, -25, 150, 50, 50, 150, -25, -125, -125, -25, 150, 50, 50, 150, -25, -125, -125, -25, 150, 50, 50, 150, -25, -125, -125, -25, 150, 50, 50, 150, -25, -125, -125, -25, 150, 50, 50, 150, -25, -125, -125, -25, 150, 50, 150, 250, 75, -25, -25, 75, 250, 150 ]


	#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# set up starting position...
	#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def c0_set_start_position( c0_mlist ):

		global c0_position, c0_side, c0_sidemoves, c0_moving
		global c0_wKingmoved, c0_bKingmoved, c0_wLRockmoved, c0_wRRockmoved, c0_bLRockmoved, c0_bRRockmoved, c0_w00, c0_b00
		global c0_lastmovepawn, c0_become, c0_become_from_engine, c0_moveslist
		global c0_start_FEN, c0_fischer, c0_fischer_cst
	
		
		if( len(c0_start_FEN)>0 ):

			c0_set_FEN( c0_start_FEN )
			if(c0_fischer): c0_fischer_adjustmoved()

		else:

			c0_position=""

			if(len(c0_mlist)==0):

				c0_add_piece("wpa2")
				c0_add_piece("wpb2")
				c0_add_piece("wpc2")
				c0_add_piece("wpd2")
				c0_add_piece("wpe2")
				c0_add_piece("wpf2")
				c0_add_piece("wpg2")
				c0_add_piece("wph2")
				c0_add_piece("wRa1")
				c0_add_piece("wNb1")
				c0_add_piece("wBc1")
				c0_add_piece("wQd1")
				c0_add_piece("wKe1")
				c0_add_piece("wBf1")
				c0_add_piece("wNg1")
				c0_add_piece("wRh1")
				c0_add_piece("bpa7")
				c0_add_piece("bpb7")
				c0_add_piece("bpc7")
				c0_add_piece("bpd7")
				c0_add_piece("bpe7")
				c0_add_piece("bpf7")
				c0_add_piece("bpg7")
				c0_add_piece("bph7")
				c0_add_piece("bRa8")
				c0_add_piece("bNb8")
				c0_add_piece("bBc8")
				c0_add_piece("bQd8")
				c0_add_piece("bKe8")
				c0_add_piece("bBf8")
				c0_add_piece("bNg8")
				c0_add_piece("bRh8")

			else:

				c0_position = "wpa2,wpb2,wpc2,wpd2,wpe2,wpf2,wpg2,wph2,wRa1,wNb1,wBc1,wQd1,wKe1,wBf1,wNg1,wRh1,bpa7,bpb7,bpc7,bpd7,bpe7,bpf7,bpg7,bph7,bRa8,bNb8,bBc8,bQd8,bKe8,bBf8,bNg8,bRh8,"


			c0_wKingmoved = False
			c0_bKingmoved = False
			c0_wLRockmoved = False
			c0_wRRockmoved = False
			c0_bLRockmoved = False
			c0_bRRockmoved = False
			c0_w00 = False
			c0_b00 = False

			c0_lastmovepawn = 0
			c0_sidemoves=1


		c0_become=""
		c0_become_from_engine=""
					# just engine

		c0_moveslist = ""

		c0_moving=False

		if(len(c0_mlist)>0):

			c0_z=0
			while(c0_z<len(c0_mlist)):

				c0_from_at=substr(c0_mlist,c0_z,2)
				c0_to_at=substr(c0_mlist,c0_z+2,2)
				if(c0_z+4<len(c0_mlist) and substr(c0_mlist,c0_z+4,1)=="["):

					c0_become_from_engine=substr(c0_mlist,c0_z+5,1)
					c0_z+=3

				else: c0_become_from_engine=""

				if(c0_fischer): c0_fischer_cstl_move(c0_from_at+c0_to_at,False)
				else: c0_moveto(c0_convH888(c0_from_at), c0_convH888(c0_to_at), False)
	
				c0_sidemoves=-c0_sidemoves

				c0_z+=4

			if( len(c0_start_FEN)>0 ):

				c0_set_board_situation( c0_position, c0_wKingmoved, c0_wLRockmoved, c0_wRRockmoved, c0_w00, c0_bKingmoved, c0_bLRockmoved, c0_bRRockmoved, c0_b00, c0_lastmovepawn, c0_moveslist, c0_sidemoves )

			else:

				c0_pos2=c0_position
				c0_position=""

				c0_q=0
				while(c0_q<len(c0_pos2)):
					c0_add_piece(substr(c0_pos2,c0_q,4))
					
					c0_q+=5



		c0_moveslist = c0_mlist


	#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Set board situation...
	#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def c0_set_board_situation( c0_figlist, c0_wK, c0_wLR, c0_wRR, c0_w_00, c0_bK, c0_bLR, c0_bRR, c0_b_00, c0_elpas, c0_ml, c0_s ):

		global c0_position, c0_side, c0_sidemoves, c0_moving
		global c0_side, c0_sidemoves, c0_moving
		global c0_wKingmoved, c0_bKingmoved, c0_wLRockmoved, c0_wRRockmoved, c0_bLRockmoved, c0_bRRockmoved, c0_w00, c0_b00
		global c0_lastmovepawn, c0_become, c0_become_from_engine, c0_moveslist
		
		c0_moving=False

		c0_position=""
		i=0
		while(i<len(c0_figlist)):

			c0_add_piece( substr(c0_figlist,i,4) )
			i+=4
			if( i<len(c0_figlist) and substr(c0_figlist,i,1)==";" ): i+=1


		c0_wKingmoved = c0_wK
		c0_bKingmoved = c0_bK
		c0_wLRockmoved = c0_wLR
		c0_wRRockmoved = c0_wRR
		c0_bLRockmoved = c0_bLR
		c0_bRRockmoved = c0_bRR
		c0_w00 = c0_w_00
		c0_b00 = c0_b_00

		c0_lastmovepawn = c0_elpas

		c0_become=""
		c0_become_from_engine=""
					# just engine

		c0_moveslist = c0_ml
		c0_sidemoves=c0_s



	#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# add a piece at position...
	#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def c0_add_piece( c0_pstring ):

		global c0_position

		c0_1_at=substr(c0_pstring,2,2)
		c0_1_figure=substr(c0_pstring,1,1)
		c0_1_color=substr(c0_pstring,0,1)

		# There were other visual activities before...
		if(IndexOf(c0_position,c0_1_at)<0): c0_position+=c0_pstring+";"

	#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# remove a piece from position...
	#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def c0_clear_at( c0_1_at ):
	
		global c0_position
		
		c0_a=IndexOf(c0_position,c0_1_at)
		if(c0_a>=0): c0_position=substr(c0_position,0,c0_a-2) + substrall(c0_position,c0_a+3)


	#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# move visualy a piece...
	#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def c0_just_move_piece( c0_2_from, c0_2_to ):

		global c0_position, c0_moving, c0_moves2do

		c0_clear_at( c0_2_to )
		c0_a=IndexOf(c0_position,c0_2_from)
		if(c0_a>=0):

			c0_2_figure = substr(c0_position,c0_a-1,1)
			c0_2_color = substr(c0_position,c0_a-2,1)
			c0_position=c0_position.replace( c0_2_from, c0_2_to )
			c0_moves2do+=c0_2_from+c0_2_to
			c0_moving=True


	# and add a promotion (or castling) indicator...
	def c0_and_promote_or_castle():

		global c0_become, c0_moves2do

		if(len(c0_become)>0): c0_moves2do+="["+c0_become+"]"



	#############################################################
	# CHESS related part for chess play
	#############################################################
	#-------------------------------------------------
	def c0_convE2(c0_vertikali,c0_horizontali):

		return fromCharCode(96+c0_horizontali)+ToString(c0_vertikali)


	#-------------------------------------------------
	def c0_convE777(c0_verthoriz):

		return fromCharCode(96+parseInt(substr(c0_verthoriz,1,1)))+substr(c0_verthoriz,0,1)


	#-------------------------------------------------
	def c0_conv52(c0_vertikali,c0_horizontali):

		return ToString(c0_vertikali)+ToString(c0_horizontali)


	#-------------------------------------------------
	def c0_convH888(c0_at8):

		c0_8horiz=charCodeAt(c0_at8,0) - 96
		c0_8vert=parseInt(substr(c0_at8,1,1))
		return ToString(c0_8vert) + ToString(c0_8horiz)

 
	#-------------------------------------------------
	def c0_move_to(c0_Zstr1,c0_Zstr2):

		c0_moveto( c0_convH888(c0_Zstr1), c0_convH888(c0_Zstr2), True )



	#-------------------------------------------------
	def c0_moveto(c0_from_at, c0_to_at, c0_draw):

		global c0_position, c0_side, c0_sidemoves, c0_moving
		global c0_side, c0_sidemoves, c0_moving
		global c0_wKingmoved, c0_bKingmoved, c0_wLRockmoved, c0_wRRockmoved, c0_bLRockmoved, c0_bRRockmoved, c0_w00, c0_b00
		global c0_lastmovepawn, c0_become, c0_become_from_engine, c0_moveslist
		

		c0_vert = parseInt(substr(c0_from_at,0,1))
		c0_horiz= parseInt(substr(c0_from_at,1,1))
		c0_vert2 = parseInt(substr(c0_to_at,0,1))
		c0_horiz2= parseInt(substr(c0_to_at,1,1))

		c0_p=IndexOf(c0_position, c0_convE2(c0_vert,c0_horiz) )
		c0_color=substr(c0_position,c0_p-2,1)
		c0_figure=substr(c0_position,c0_p-1,1)

		save_c0_position=c0_position

		c0_lastmovepawn = 0
		if(c0_draw): c0_become=""

		if(c0_draw):

			save_c0_position=c0_position
			c0_just_move_piece( c0_convE2(c0_vert, c0_horiz), c0_convE2(c0_vert2, c0_horiz2) )
			c0_position=save_c0_position


		c0_p2=IndexOf(c0_position, c0_convE2(c0_vert2,c0_horiz2) )
		if(c0_p2>=0):

			c0_position = substr(c0_position,0,c0_p2-2) + substrall(c0_position,c0_p2+3)

			if(not c0_wLRockmoved and c0_convE2(c0_vert2,c0_horiz2)=="a1"): c0_wLRockmoved=True
			if(not c0_wRRockmoved and c0_convE2(c0_vert2,c0_horiz2)=="h1"): c0_wRRockmoved=True
			if(not c0_bLRockmoved and c0_convE2(c0_vert2,c0_horiz2)=="a8"): c0_bLRockmoved=True
			if(not c0_bRRockmoved and c0_convE2(c0_vert2,c0_horiz2)=="h8"): c0_bRRockmoved=True


		else:

			if(c0_figure=="R"):

				if(c0_color=="w"):

					if(c0_convE2(c0_vert,c0_horiz)=="a1"): c0_wLRockmoved=True
					if(c0_convE2(c0_vert,c0_horiz)=="h1"): c0_wRRockmoved=True

				else:

					if(c0_convE2(c0_vert,c0_horiz)=="a8"): c0_bLRockmoved=True
					if(c0_convE2(c0_vert,c0_horiz)=="h8"): c0_bRRockmoved=True




			if(c0_figure=="K"):

				if(not c0_wKingmoved and c0_color=="w"):

					if(c0_convE2(c0_vert,c0_horiz)=="e1" and c0_convE2(c0_vert2,c0_horiz2)=="g1"):	# 0-0

						if(c0_draw):

							save_c0_position=c0_position
							c0_just_move_piece("h1","f1")
							c0_position=save_c0_position

						c0_position = c0_position.replace( "h1", "f1" )
								# Rf1
						c0_w00 = True
						c0_become="0"

					if(c0_convE2(c0_vert,c0_horiz)=="e1" and c0_convE2(c0_vert2,c0_horiz2)=="c1"):	# 0-0-0

						if(c0_draw):

							save_c0_position=c0_position
							c0_just_move_piece("a1","d1")
							c0_position=save_c0_position

						c0_position = c0_position.replace( "a1", "d1" )
								# Rd1
						c0_w00 = True
						c0_become="0"

					c0_wKingmoved=True

				if(not c0_bKingmoved and c0_color=="b"):

					if(c0_convE2(c0_vert,c0_horiz)=="e8" and c0_convE2(c0_vert2,c0_horiz2)=="g8"):	# 0-0

						if(c0_draw):

							save_c0_position=c0_position
							c0_just_move_piece("h8","f8")
							c0_position=save_c0_position

						c0_position = c0_position.replace( "h8", "f8" )
								# Rf8
						c0_b00 = True
						c0_become="0"

					if(c0_convE2(c0_vert,c0_horiz)=="e8" and c0_convE2(c0_vert2,c0_horiz2)=="c8"):	# 0-0-0

						if(c0_draw):

							save_c0_position=c0_position
							c0_just_move_piece("a8","d8")
							c0_position=save_c0_position

						c0_position = c0_position.replace( "a8", "d8" )
								# Rd8
						c0_b00 = True
						c0_become="0"

					c0_bKingmoved=True




		if(c0_figure=="p"):		# pawn

			if(c0_vert2==8 or c0_vert2==1):

				if(len(c0_become_from_engine)>0):

					c0_figure= c0_become_from_engine

				else:

					if(c0_draw):

						if(window_confirm("Promote a QUEEN?")):

							c0_figure = "Q"

						else:
							if(window_confirm("Then a ROOK?")):

								c0_figure = "R"

							else:
								if(window_confirm("Maybe a BISHOP?")):

									c0_figure = "B"

								else:
	
									if(window_confirm("Really a KNIGHT????")):

										c0_figure = "N"

									else:

										#print("I know, You need a new QUEEN.")
										c0_figure = "Q"


					else: c0_figure="Q"

				if(c0_draw):

					c0_become=c0_figure
					# just put in queue... (no,will be detected above in 3D)...
					#save_c0_position=c0_position
					#c0_moves2do+=c0_convE2(c0_vert2,c0_horiz2) + "=" + c0_become
					#c0_position=save_c0_position

				c0_position = c0_position.replace( "p"+c0_convE2(c0_vert,c0_horiz), c0_figure+c0_convE2(c0_vert,c0_horiz) )

			if(c0_p2<0 and c0_horiz!=c0_horiz2):

				if(c0_draw):

					save_c0_position=c0_position
					c0_clear_at( c0_convE2(c0_vert,c0_horiz2) )
					c0_position=save_c0_position

				c0_p3=IndexOf(c0_position, c0_convE2(c0_vert,c0_horiz2) )
				c0_position = substr(c0_position,0,c0_p3-2) + substrall(c0_position,c0_p3+3)

			if((c0_vert==2 and c0_vert2==4) or (c0_vert==7 and c0_vert2==5)): c0_lastmovepawn = c0_horiz


		c0_position = c0_position.replace( c0_convE2(c0_vert,c0_horiz), c0_convE2(c0_vert2,c0_horiz2) )

		if(c0_draw):

			c0_moveslist += c0_convE2(c0_vert,c0_horiz) + c0_convE2(c0_vert2,c0_horiz2)
			if(len(c0_become)>0): c0_moveslist += "["+c0_become+"]"
			c0_and_promote_or_castle()




	#-------------------------------------------------
	def c0_D_last_move_was():

		global c0_moveslist

		c0_ret=""
		if( len(c0_moveslist)>0 ):

			if (substr(c0_moveslist, len(c0_moveslist)-1, 1 )=="]" ): c0_ret= substr(c0_moveslist, len(c0_moveslist)-7, 7 )
			else: c0_ret= substr(c0_moveslist, len(c0_moveslist)-4, 4 )

		return c0_ret


	#-------------------------------------------------
	def c0_take_back():

		global c0_moveslist

		c0_movespre=""
		if( len(c0_moveslist)>0 ):

			if (substr(c0_moveslist, len(c0_moveslist)-1, 1 )=="]" ): c0_movespre= substr(c0_moveslist, 0, len(c0_moveslist)-7 )
			else: c0_movespre= substr(c0_moveslist, 0, len(c0_moveslist)-4 )


		c0_set_start_position( c0_movespre )



	#-------------------------------------------------
	def c0_D_is_empty(c0_Zstr):

		c0_Zs2=c0_convH888(c0_Zstr)
		return c0_is_empty( parseInt(substr(c0_Zs2,0,1)), parseInt(substr(c0_Zs2,1,1)))


	#-------------------------------------------------
	def c0_is_empty(c0_Zvert, c0_Zhoriz):

		global c0_position

		c0_good = True
		if(c0_Zvert<1 or c0_Zvert>8 or c0_Zhoriz<1 or c0_Zhoriz>8): c0_good=False
		else:

			c0_pz2=IndexOf(c0_position, c0_convE2(c0_Zvert,c0_Zhoriz) )
			if(c0_pz2>=0): c0_good=False

		return c0_good



	#-------------------------------------------------
	def c0_D_what_at(c0_Zstr1):

		global c0_position
		
		c0_ret=""
		c0_pz2=IndexOf(c0_position, c0_Zstr1 )
		if(c0_pz2>=0): c0_ret=substr(c0_position,c0_pz2-2,2)
		return c0_ret



	#-------------------------------------------------
	def c0_D_is_enemy(c0_Zstr,c0_mycolor):

		c0_Zs2=c0_convH888(c0_Zstr)
		return c0_is_enemy( parseInt(substr(c0_Zs2,0,1)), parseInt(substr(c0_Zs2,1,1)), c0_mycolor)



	#-------------------------------------------------
	def c0_is_enemy(c0_Zvert,c0_Zhoriz,c0_mycolor):

		global c0_position
		
		c0_is_there =False
		if(c0_Zvert>=1 and c0_Zvert<=8 and c0_Zhoriz>=1 and c0_Zhoriz<=8):

			c0_pz2=IndexOf(c0_position, c0_convE2(c0_Zvert,c0_Zhoriz) )

			if(c0_pz2>=0 and substr(c0_position,c0_pz2-2,1)!=c0_mycolor): c0_is_there=True

		return c0_is_there



	#-------------------------------------------------
	def c0_D_is_emptyline(c0_Zstr1,c0_Zstr2 ):

		c0_Zs1=c0_convH888(c0_Zstr1)
		c0_Zs2=c0_convH888(c0_Zstr2)
		return c0_is_emptyline( parseInt(substr(c0_Zs1,0,1)), parseInt(substr(c0_Zs1,1,1)) , parseInt(substr(c0_Zs2,0,1)), parseInt(substr(c0_Zs2,1,1)))


	#-------------------------------------------------
	def c0_is_emptyline(c0_Zvert,c0_Zhoriz,c0_Zvert2,c0_Zhoriz2):

		c0_good = True
		c0_DZvert=c0_Zvert2-c0_Zvert

		if(c0_DZvert<0): c0_DZvert=-1
		else:
			if(c0_DZvert>0): c0_DZvert=1
	
		c0_DZhoriz=c0_Zhoriz2-c0_Zhoriz

		if(c0_DZhoriz<0): c0_DZhoriz=-1
		else:
			if(c0_DZhoriz>0): c0_DZhoriz=1
	
		c0_PZvert=c0_Zvert+c0_DZvert
		c0_PZhoriz=c0_Zhoriz+c0_DZhoriz

		while(c0_PZvert!=c0_Zvert2 or c0_PZhoriz!=c0_Zhoriz2):

			if( not c0_is_empty( c0_PZvert, c0_PZhoriz ) ):

				c0_good=False
				break

			c0_PZvert+=c0_DZvert
			c0_PZhoriz+=c0_DZhoriz

		return c0_good



	#-------------------------------------------------
	def c0_D_is_check_to_king(c0_ZKcolor):

		return c0_is_check_to_king(c0_ZKcolor)


	#-------------------------------------------------
	def c0_is_check_to_king(c0_ZKcolor):

		global c0_position

		c0_is_check=False
		c0_Zp=IndexOf(c0_position,c0_ZKcolor+"K")
		c0_ZKhoriz=charCodeAt(substr(c0_position,c0_Zp+2,1),0) - 96
		c0_ZKvert=parseInt(substr(c0_position,c0_Zp+3,1))
		c0_ZK_at = ToString(c0_ZKvert) + ToString(c0_ZKhoriz)

		c0_i=0
		while( len(c0_position)>c0_i ):

			c0_Zcolor=substr(c0_position,c0_i,1)
			c0_Zfigure=substr(c0_position,c0_i+1,1)

			if(c0_Zcolor!=c0_ZKcolor):

				c0_Zhoriz=charCodeAt(substr(c0_position,c0_i+2,1),0) - 96
				c0_Zvert=parseInt(substr(c0_position,c0_i+3,1))
				c0_Z_at = ToString(c0_Zvert) + ToString(c0_Zhoriz)

				if(c0_can_be_moved( c0_Z_at, c0_ZK_at, True)):

					c0_is_check=True
					break

			c0_i+=5


		return c0_is_check



	#-------------------------------------------------
	def c0_is_attacked_king_before_move(c0_Qfrom_at, c0_Qto_at, c0_Qcolor):

		global c0_position, c0_side, c0_sidemoves, c0_moving
		global c0_side, c0_sidemoves, c0_moving
		global c0_wKingmoved, c0_bKingmoved, c0_wLRockmoved, c0_wRRockmoved, c0_bLRockmoved, c0_bRRockmoved, c0_w00, c0_b00
		global c0_lastmovepawn, c0_become, c0_become_from_engine, c0_moveslist
		
		c0_is_attack=False

		c0_save_position=c0_position
		c0_save_sidemoves=c0_sidemoves
		c0_save_wKingmoved=c0_wKingmoved
		c0_save_bKingmoved=c0_bKingmoved
		c0_save_wLRockmoved=c0_wLRockmoved
		c0_save_wRRockmoved=c0_wRRockmoved
		c0_save_bLRockmoved=c0_bLRockmoved
		c0_save_bRRockmoved=c0_bRRockmoved
		c0_save_w00=c0_w00
		c0_save_b00=c0_b00
		c0_save_become=c0_become

		c0_save_lastmovepawn=c0_lastmovepawn

		c0_moveto(c0_Qfrom_at, c0_Qto_at, False)
		c0_sidemoves=-c0_sidemoves

		if( c0_is_check_to_king(c0_Qcolor) ):

			c0_is_attack=True


		c0_position=c0_save_position
		c0_sidemoves=c0_save_sidemoves
		c0_wKingmoved=c0_save_wKingmoved
		c0_bKingmoved=c0_save_bKingmoved
		c0_wLRockmoved=c0_save_wLRockmoved
		c0_wRRockmoved=c0_save_wRRockmoved
		c0_bLRockmoved=c0_save_bLRockmoved
		c0_bRRockmoved=c0_save_bRRockmoved
		c0_lastmovepawn=c0_save_lastmovepawn
		c0_w00=c0_save_w00
		c0_b00=c0_save_b00
		c0_become=c0_save_become

		return c0_is_attack



	#-------------------------------------------------
	def c0_D_is_mate_to_king(c0_ZKcolor):

		return c0_is_mate_to_king(c0_ZKcolor, False)


	#-------------------------------------------------
	def c0_is_mate_to_king(c0_ZKcolor, c0_just_mate):
	
		global c0_position

		c0_is_mate=False

		if( c0_just_mate or c0_is_check_to_king(c0_ZKcolor) ):

			c0_i=0
			c0_is_mate=True
			while( c0_is_mate and (len(c0_position)>c0_i) ):

				c0_Zcolor=substr(c0_position,c0_i,1)
				if(c0_Zcolor==c0_ZKcolor):

					c0_Zhoriz=charCodeAt(substr(c0_position,c0_i+2,1),0) - 96
					c0_Zvert=parseInt(substr(c0_position,c0_i+3,1))
					c0_Z_at = ToString(c0_Zvert) + ToString(c0_Zhoriz)
					c0_vi=1
					while(c0_is_mate and c0_vi<=8):
						c0_vj=1
						while(c0_is_mate and c0_vj<=8):

							c0_Z_to_at=ToString(c0_vi)+ToString(c0_vj)
							if(c0_can_be_moved( c0_Z_at, c0_Z_to_at, False)):

								c0_is_mate=False
								break
							c0_vj+=1
						c0_vi+=1
				c0_i+=5

		return c0_is_mate


	#-------------------------------------------------
	def c0_D_is_pate_to_king(c0_ZWcolor):

		return c0_is_pate_to_king(c0_ZWcolor) and not c0_is_mate_to_king(c0_ZWcolor, False)


	#-------------------------------------------------
	def c0_is_pate_to_king(c0_ZWcolor):

		global c0_position

		c0_is_pate=True
		
		c0_j=0
		while( c0_is_pate and len(c0_position)>c0_j ):

			c0_Wcolor=substr(c0_position,c0_j,1)
			if(c0_Wcolor==c0_ZWcolor):

				c0_Whoriz=charCodeAt(substr(c0_position,c0_j+2,1),0) - 96
				c0_Wvert=parseInt(substr(c0_position,c0_j+3,1))
				c0_W_at = ToString(c0_Wvert) + ToString(c0_Whoriz)
				c0_wi=1
				while( c0_is_pate and c0_wi<=8 ):
					c0_wj=1
					while( c0_is_pate and c0_wj<=8 ):

						c0_W_to_at=ToString(c0_wi)+ToString(c0_wj)
						if(c0_can_be_moved( c0_W_at, c0_W_to_at, False)):

							c0_is_pate=False
							break
						c0_wj+=1
					c0_wi+=1

			c0_j+=5



		return c0_is_pate



	#-------------------------------------------------
	def c0_D_can_be_moved(c0_Zstr1, c0_Zstr2):

		return c0_can_be_moved( c0_convH888(c0_Zstr1), c0_convH888(c0_Zstr2), False)



	#-------------------------------------------------
	def c0_can_be_moved(c0_from_at, c0_to_at, c0_just_move_or_eat):


		global c0_position, c0_side, c0_sidemoves, c0_moving
		global c0_side, c0_sidemoves, c0_moving
		global c0_wKingmoved, c0_bKingmoved, c0_wLRockmoved, c0_wRRockmoved, c0_bLRockmoved, c0_bRRockmoved, c0_w00, c0_b00
		global c0_lastmovepawn, c0_become, c0_become_from_engine, c0_moveslist
		

		c0_can = False
		c0_vert = parseInt(substr(c0_from_at,0,1))
		c0_horiz= parseInt(substr(c0_from_at,1,1))
		c0_vert2 = parseInt(substr(c0_to_at,0,1))
		c0_horiz2= parseInt(substr(c0_to_at,1,1))

		c0_p=IndexOf(c0_position, c0_convE2(c0_vert,c0_horiz) )
		if(c0_p>=0):

			c0_color=substr(c0_position,c0_p-2,1)
			c0_figure=substr(c0_position,c0_p-1,1)

			if(c0_is_empty(c0_vert2,c0_horiz2) or c0_is_enemy(c0_vert2,c0_horiz2,c0_color)):

				c0_Dvert=c0_vert2-c0_vert
				if(c0_Dvert<0): c0_Dvert=-c0_Dvert
				c0_Dhoriz=c0_horiz2-c0_horiz
				if(c0_Dhoriz<0): c0_Dhoriz=-c0_Dhoriz

				if(c0_figure=="p"):

					if( c0_color=="w" ): c0_virziens=1
					else: c0_virziens=-1
	
					if(c0_horiz2==c0_horiz):

						if( (c0_vert2==c0_vert+c0_virziens and c0_is_empty(c0_vert2,c0_horiz2)) or (c0_color=="w" and c0_vert2==4 and c0_vert==2 and c0_is_empty(3,c0_horiz2) and c0_is_empty(4,c0_horiz2)) or (c0_color=="b" and c0_vert2==5 and c0_vert==7 and c0_is_empty(5,c0_horiz2) and c0_is_empty(6,c0_horiz2)) ):
							
							c0_can = True

					else:

						if( (c0_horiz2==c0_horiz+1 or c0_horiz2==c0_horiz-1) and c0_vert2==c0_vert+c0_virziens):
							if(c0_is_enemy(c0_vert2,c0_horiz2,c0_color) or (c0_lastmovepawn==c0_horiz2 and  ((c0_color=="w" and c0_vert2==6) or (c0_color=="b" and c0_vert2==3)) ) ):
	
								c0_can = True


				if(c0_figure=="N"):

					if( c0_Dvert+c0_Dhoriz==3 and c0_Dvert!=0 and c0_Dhoriz!=0 ): c0_can=True

				if(c0_figure=="B"):

					if( (c0_Dvert>0 and c0_Dvert==c0_Dhoriz) and c0_is_emptyline(c0_vert,c0_horiz,c0_vert2,c0_horiz2)): c0_can=True

				if(c0_figure=="R"):

					if( ((c0_Dvert==0 or c0_Dhoriz==0) and c0_Dvert!=c0_Dhoriz) and c0_is_emptyline(c0_vert,c0_horiz,c0_vert2,c0_horiz2)): c0_can=True

				if(c0_figure=="Q"):

					if( (c0_Dvert==0 or c0_Dhoriz==0 or c0_Dvert==c0_Dhoriz) and c0_is_emptyline(c0_vert,c0_horiz,c0_vert2,c0_horiz2)): c0_can=True

				if(c0_figure=="K"):

					if((c0_Dvert==0 and c0_Dhoriz==1) or (c0_Dhoriz==0 and c0_Dvert==1) or (c0_Dhoriz==1 and c0_Dvert==1)): c0_can=True
					else:
						if (not c0_just_move_or_eat and not c0_is_check_to_king(c0_color) and (not c0_fischer)):

							if(c0_color=="w"):

								if(not c0_wKingmoved and c0_vert==1 and c0_horiz==5 and c0_vert2==1):

									if( (c0_horiz2==7 and not c0_wRRockmoved and c0_is_empty(1,6) and c0_is_empty(1,7) and not c0_is_attacked_king_before_move("15", "16", c0_color) and not c0_is_attacked_king_before_move("15", "17", c0_color)) or (c0_horiz2==3 and not c0_wLRockmoved and c0_is_empty(1,2) and c0_is_empty(1,3) and c0_is_empty(1,4) and not c0_is_attacked_king_before_move("15", "14", c0_color) and not c0_is_attacked_king_before_move("15", "13", c0_color)) ):
	
										c0_can=True


							else:

								if(not c0_bKingmoved and c0_vert==8 and c0_horiz==5 and c0_vert2==8):

									if( (c0_horiz2==7 and not c0_bRRockmoved and c0_is_empty(8,6) and c0_is_empty(8,7) and not c0_is_attacked_king_before_move("85", "86", c0_color) and not c0_is_attacked_king_before_move("85", "87", c0_color)) or (c0_horiz2==3 and not c0_bLRockmoved and c0_is_empty(8,2) and c0_is_empty(8,3) and c0_is_empty(8,4) and not c0_is_attacked_king_before_move("85", "84", c0_color) and not c0_is_attacked_king_before_move("85", "83", c0_color)) ):
	
										c0_can=True




				if(not c0_just_move_or_eat and c0_can):

					c0_can = not c0_is_attacked_king_before_move(c0_from_at, c0_to_at, c0_color)



		return c0_can

	#---------------------------------------
	#  Function to get next possible moves
	#---------------------------------------
	def c0_get_next_moves():

		global c0_position, c0_sidemoves

		c0_Dposs=""
		c0_Da=0
		while( len(c0_position)>c0_Da ):

			c0_Dcolor=substr(c0_position,c0_Da,1)
			if((c0_sidemoves>0 and c0_Dcolor=="w")or(c0_sidemoves<0 and c0_Dcolor=="b")):

				c0_Dfigure=substr(c0_position,c0_Da+1,1)
				c0_Dhoriz=charCodeAt(substr(c0_position,c0_Da+2,1),0) - 96
				c0_Dvert=parseInt(substr(c0_position,c0_Da+3,1))
				c0_Dfrom_move=ToString(c0_Dvert)+ToString(c0_Dhoriz)

				if(c0_Dfigure=="p"):

					c0_Dposs+=c0_DCN(c0_Dfrom_move,c0_sidemoves,0,1)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,(2*c0_sidemoves),0,1)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,c0_sidemoves,1,1)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,c0_sidemoves,-1,1)

				if(c0_Dfigure=="N"):

					c0_Dposs+=c0_DCN(c0_Dfrom_move,2,1,1)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,2,-1,1)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,1,2,1)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,1,-2,1)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,-1,2,1)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,-1,-2,1)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,-2,1,1)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,-2,-1,1)

				if(c0_Dfigure=="B" or c0_Dfigure=="Q"):

					c0_Dposs+=c0_DCN(c0_Dfrom_move,1,1,8)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,1,-1,8)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,-1,1,8)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,-1,-1,8)

				if(c0_Dfigure=="R" or c0_Dfigure=="Q"):

					c0_Dposs+=c0_DCN(c0_Dfrom_move,1,0,8)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,-1,0,8)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,0,1,8)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,0,-1,8)

				if(c0_Dfigure=="K"):

					c0_Dposs+=c0_DCN(c0_Dfrom_move,1,1,1)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,1,0,1)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,1,-1,1)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,0,1,1)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,0,-1,1)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,-1,1,1)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,-1,0,1)
					c0_Dposs+=c0_DCN(c0_Dfrom_move,-1,-1,1)
					if((c0_Dcolor=="w" and c0_Dfrom_move=="15") or (c0_Dcolor=="b" and c0_Dfrom_move=="85")):

						c0_Dposs+=c0_DCN(c0_Dfrom_move,0,-2,1)
						c0_Dposs+=c0_DCN(c0_Dfrom_move,0,2,1)


			c0_Da+=5


		return c0_Dposs



	#---------------------------------------
	#
	def c0_DCN(c0_D7from_at, c0_Dvert_TX, c0_Dhoriz_TX, c0_Dcntx):

		global c0_position, c0_side, c0_sidemoves, c0_moving
		global c0_side, c0_sidemoves, c0_moving
		global c0_wKingmoved, c0_bKingmoved, c0_wLRockmoved, c0_wRRockmoved, c0_bLRockmoved, c0_bRRockmoved, c0_w00, c0_b00
		global c0_lastmovepawn, c0_become, c0_become_from_engine, c0_moveslist

		c0_D7poss=""
		c0_c7K=""

		saveD1sidemoves=c0_sidemoves
		saveD1wKingmoved=c0_wKingmoved
		saveD1bKingmoved=c0_bKingmoved
		saveD1wLRockmoved=c0_wLRockmoved
		saveD1wRRockmoved=c0_wRRockmoved
		saveD1bLRockmoved=c0_bLRockmoved
		saveD1bRRockmoved=c0_bRRockmoved
		saveD1w00=c0_w00
		saveD1b00=c0_b00
		saveD1lastmovepawn=c0_lastmovepawn
		saveD1position=c0_position
		saveD1become=c0_become

		c0_D7vert=parseInt(substr(c0_D7from_at,0,1))
		c0_D7horiz=parseInt(substr(c0_D7from_at,1,1))

		c0_Dj=0
		while( c0_Dj<c0_Dcntx ):

			c0_D7vert+=c0_Dvert_TX
			c0_D7horiz+=c0_Dhoriz_TX
			if(c0_D7vert>=1 and c0_D7vert<=8 and c0_D7horiz>=1 and c0_D7horiz<=8):

				c0_D7to_at=ToString(c0_D7vert)+ToString(c0_D7horiz)

				if( c0_can_be_moved( c0_D7from_at, c0_D7to_at, False ) ):

					c0_foundmove = c0_convE777( c0_D7from_at ) + c0_convE777( c0_D7to_at )
					c0_D7poss+=c0_foundmove + ","


				c0_wKingmoved=saveD1wKingmoved
				c0_bKingmoved=saveD1bKingmoved
				c0_wLRockmoved=saveD1wLRockmoved
				c0_wRRockmoved=saveD1wRRockmoved
				c0_bLRockmoved=saveD1bLRockmoved
				c0_bRRockmoved=saveD1bRRockmoved
				c0_w00=saveD1w00
				c0_b00=saveD1b00

				c0_lastmovepawn=saveD1lastmovepawn
				c0_position=saveD1position
				c0_sidemoves=saveD1sidemoves
				c0_become=saveD1become

			c0_Dj+=1

		return c0_D7poss


	#----------------------------------------------------------------------------
	#	PGN support part...
	#----------------------------------------------------------------------------

	#------------- Analyse PGN ...

	def c0_PG_gettable():

		global c0_start_FEN, c0_fischer, c0_fischer_cst
		global c0_PG_viewer, c0_PG_1, c0_PGN_header, c0_errflag, PGN_text

		rc=""

		Event_Name=""
		Event_Site=""
		Event_Date=""
		Roundv=""
		White=""
		Black=""
		Result=""
		ECO=""
		WhiteElo=""
		BlackElo=""
		Game_Date=""
		Source_Date=""

		AddInfo=""

		htms=""

		c0_PGN_header=[]

		PGN_text= c0_ReplaceAll( PGN_text,fromCharCode(10)," " )
		PGN_text= c0_ReplaceAll( PGN_text,fromCharCode(13)," " )
		PGN_text= c0_ReplaceAll( PGN_text,"   ", " " )
		PGN_text= c0_ReplaceAll( PGN_text,"  ", " " )

		str2=PGN_text
		while(True):

			at2=IndexOf(str2,"[")
			if(at2<0): break

			at2_1=IndexOf(str2,"(")
			at2_2=IndexOf(str2,"{")
			if((at2_1>=0 and at2_1<at2) or (at2_2>=0 and at2_2<at2)): break

			buf2= substrall(str2,at2+1)
			buf2= substr(buf2,0, IndexOf(buf2,"]") )
			str2= substrall(str2,at2+len(buf2)+2)

			c0_PGN_header.append(buf2)
			buf2= c0_ReplUrl(buf2)


			buf2= c0_ReplaceAll( buf2,"'","" )
			buf2= c0_ReplaceAll( buf2,fromCharCode(34),"" )

			# unicode symbol used html texts
			buf2= c0_ReplaceAll( buf2,"–","-" )

			buf3=buf2.upper()

			at9 = IndexOf(buf3,"SETUP ")
			if(at9>=0 and at9<3): 
				 c0_fischer=(substr(buf2,at9+6,1)=="1")

			at3 = IndexOf(buf3,"FEN ")
			if(at3>=0 and at3<3):
				c0_start_FEN=substrall(buf2,at3+4)
				c0_set_start_position("")
			else:
				at3 = IndexOf(buf3,"EVENT ")
				if(at3>=0): Event_Name=substrall(buf2,at3+6)
				else:
					at3 = IndexOf(buf3,"SITE ")
					if(at3>=0): Event_Site=substrall(buf2,at3+5)
					else:
						at3 = IndexOf(buf3,"DATE ")
						if(at3>=0 and at3<3): Game_Date=substrall(buf2,at3+5)
						else:
							at3 = IndexOf(buf3,"ROUND ")
							if(at3>=0): Roundv=substrall(buf2,at3+6)
							else:
								at3 = IndexOf(buf3,"WHITE ")
								if(at3>=0): White=substrall(buf2,at3+6)
								else:
									at3 = IndexOf(buf3,"BLACK ")
									if(at3>=0): Black=substrall(buf2,at3+6)
									else:
										at3 = IndexOf(buf3,"ECO ")
										if(at3>=0): ECO=substrall(buf2,at3+4)
										else:
											at3 = IndexOf(buf3,"WHITEELO ")
											if(at3>=0): WhiteElo=substrall(buf2,at3+9)
											else:
												at3 = IndexOf(buf3,"BLACKELO ")
												if(at3>=0): BlackElo=substrall(buf2,at3+9)
												else:
													at3 = IndexOf(buf3,"EVENTDATE ")
													if(at3>=0): Event_Date=substrall(buf2,at3+10)
													else:
														at3 = IndexOf(buf3,"SOURCEDATE ")
														if(at3>=0): Source_Date=substrall(buf2,at3+11)
														else:
															at3 = IndexOf(buf3,"RESULT ")
															if(at3>=0): Result=substrall(buf2,at3+7)
															else:
																if(len(AddInfo)>0): AddInfo+= "<BR>"
																AddInfo += buf2



		str2= c0_ReplUrl(str2)

		c0_errflag=c0_PG_parseString(str2)
		if(c0_fischer and len(c0_fischer_cst)>0): c0_fischer_adjustmoved()

		at3 = IndexOf(str2,"*")
		if(at3>=0): Result="not finished"
		at3 = IndexOf(str2,"1/2")
		if(at3>=0):  Result="1/2-1/2"
		at3 = IndexOf(str2,"1-0")
		if(at3>=0):  Result="1:0"
		at3 = IndexOf(str2,"1:0")
		if(at3>=0): Result="1:0"
		at3 = IndexOf(str2,"0-1")
		if(at3>=0): Result="0:1"
		at3 = IndexOf(str2,"0:1")
		if(at3>=0): Result="0:1"



	#------------------------------ PGN parser on chess moves
	def c0_ReplUrl(str):		# Replaces urls to links...

		str2=str
		while(True):

			urls=""
			at=IndexOf(str2,"http://")
			if(at>=0):  urls="HTTP://" + substrall(str2,at+7)
			else:

				at=IndexOf(str2,"https://")
				if(at>=0): urls="HTTPS://" + substrall(str2,at+8)

			if(len(urls)>0):

				at2=IndexOf(urls," ")
				if(at2>=0): urls=substr(urls,0,at2)

				str2=substr(str2,0,at) + "<a href='" +urls + "' target='blank' >link»</a>" + substrall(str2,at +len(urls))

			else: break


		str2= c0_ReplaceAll( str2, "HTTP://", "http://" )
		str2= c0_ReplaceAll( str2, "HTTPS://", "https://" )

		return(str2)



	#------------------------------ PGN parser on chess moves

	def c0_get_moves_from_PGN(c0_PGN_str):		# Parses PGN moves from string variable string for chess moves...

		global PGN_text, c0_errflag, c0_PG_1

		PGN_text= c0_PGN_str

		c0_PG_gettable()

		if(c0_errflag): print("There was an error in PGN parsing!")

		return c0_PG_1



	#------------------------------ PGN parser on chess moves

	def c0_PG_parseString(str):		# Parses own string for chess moves...

		global c0_position, c0_side, c0_sidemoves, c0_moving
		global c0_wKingmoved, c0_bKingmoved, c0_wLRockmoved, c0_wRRockmoved, c0_bLRockmoved, c0_bRRockmoved, c0_w00, c0_b00
		global c0_lastmovepawn, c0_become, c0_become_from_engine, c0_moveslist
		global c0_start_FEN, c0_fischer, c0_fischer_cst
		global c0_PG_viewer, c0_PG_1, c0_PGN_header, c0_errflag, PGN_text
		global c0_NAGs
	
		f_error=False
		gaj=1
		move=""
		color7="w"
		resultl="[1:0][1-0][1 : 0][1 - 0][0:1][0-1][0 : 1][0 - 1][1/2][1 / 2] [0.5:0.5][1/2:1/2][1/2-1/2][1/2 - 1/2][1/2 : 1/2][*]"

		commentv=""

		c0_PG_1=""

		if(len(c0_NAGs)==0): c0_NAGs_define()

		c0_1save_position=c0_position
		c0_1save_sidemoves=c0_sidemoves
		c0_1save_wKingmoved=c0_wKingmoved
		c0_1save_bKingmoved=c0_bKingmoved
		c0_1save_wLRockmoved=c0_wLRockmoved
		c0_1save_wRRockmoved=c0_wRRockmoved
		c0_1save_bLRockmoved=c0_bLRockmoved
		c0_1save_bRRockmoved=c0_bRRockmoved
		c0_1save_w00=c0_w00
		c0_1save_b00=c0_b00
		c0_1save_become=c0_become
		c0_1save_become_from_engine=c0_become_from_engine
		c0_1save_lastmovepawn= c0_lastmovepawn
		c0_1save_moveslist= c0_moveslist

		if( len(c0_start_FEN)>0 ): 
			str= ( "{[FEN " + c0_start_FEN + "]}" + " " ) + str
			if( IndexOf(c0_start_FEN," b ") > 0 ): color7="b"
		else:

			c0_position = "wpa2,wpb2,wpc2,wpd2,wpe2,wpf2,wpg2,wph2,wRa1,wNb1,wBc1,wQd1,wKe1,wBf1,wNg1,wRh1,bpa7,bpb7,bpc7,bpd7,bpe7,bpf7,bpg7,bph7,bRa8,bNb8,bBc8,bQd8,bKe8,bBf8,bNg8,bRh8,"

			c0_moveslist = ""

			c0_wKingmoved = False
			c0_bKingmoved = False
			c0_wLRockmoved = False
			c0_wRRockmoved = False
			c0_bLRockmoved = False
			c0_bRRockmoved = False
			c0_w00 = False
			c0_b00 = False

			c0_lastmovepawn = 0
			c0_sidemoves=1


		c0_become=""
		c0_become_from_engine=""
		c_v="0123456789"
		k=0
		reminder=""

		st_gaj=1
		st_atq=IndexOf(str,".")-1
		if(st_atq>=0):
			
			st_s=""
			while( st_atq>=0 ):

				st_c=substr(str,st_atq,1)
				if( IndexOf(c_v,st_c) < 0 ): break
				st_s=st_c+st_s
				st_atq-=1

			if(len(st_s)>0): st_gaj=parseInt(st_s)

		i=len(str)
		while(i>0):
			if( substr(str,i-1,1)!=" " ): break
			i-=1
			
		str=substr(str,0,i)

		atwas=-1
		atcnt=0
		Nag=""
		Nag_txt=""
		Nag_at2=0

		i=0
		while(i<len(str)):

			if( atwas<i ): 
				atwas=i
				atcnt=0
			else:
				if( atwas<=i ): atcnt+=1
				if( atcnt>50 ): 
					if(c0_PG_viewer): print("Sorry, can't parse this PGN!  Errors inside.")
					f_error=True
					break

			c=substr(str,i,1)
			while( c==" " and (i+1)<len(str) and substr(str,i+1,1)==" " ): 
				i+=1
				c=substr(str,i,1)

			if( c==" " and (i+1)<len(str) and IndexOf( ("{([$"), substr(str,i+1,1) )>=0): 
				i+=1
				c=substr(str,i,1)

			commentv=""

			if(c=="$"):

				Nag= substr(str,i,3)
				k=0
				while( k<len(Nag) ):

					c=substr(Nag,k,1)
					if( IndexOf(c_v,c) < 0 ): 
						Nag=substr(Nag,0,k)
						break
					k+=1

				if(len(Nag)>0):

					Nag_txt=""
					Nag_at2 = IndexOf(c0_NAGs,"["+Nag+"]")
					if(Nag_at2>=0):

						Nag_txt = substrall(c0_NAGs,Nag_at2+len(Nag)+3)
						Nag_txt = substr(Nag_txt,0, IndexOf(Nag_txt,"[")-1)

					else: Nag_txt = "Nag:" + Nag
					str=substr(str,0,i) +  "{"+ "[" + Nag_txt + "]" +"}" + substrall(str,i+len(Nag)+1)

				c=substr(str,i,1)


			if(c=="{" or c=="("):

				cc=1

				c1=")"
				if(c=="{"): c1="}"
					
				commentv=c
				i+=1
				while(i<len(str) and cc>0):

					c2=substr(str,i,1)
					commentv+=c2
					if(c2==c): cc+=1
					if(c2==c1): cc-=1
					if(i+1==len(str) and cc>0): commentv+=c1
					i+=1

				if(len(commentv)>0):

					while(True):

						Nag_at=IndexOf(commentv,"$")
						if( Nag_at<0): break
						Nag= substr(commentv,Nag_at+1,3)
						k=0
						while( k<len(Nag) ):

							c=substr(Nag,k,1)
							if( IndexOf(c_v,c) < 0 ): 
								Nag=substr(Nag,0,k)
								break
							k+=1

						if(len(Nag)>0):

							Nag_txt=""
							Nag_at2 = IndexOf(c0_NAGs,"["+Nag+"]")
							if(Nag_at2>=0):

								Nag_txt = substrall(c0_NAGs,Nag_at2+len(Nag)+3)
								Nag_txt = substr(Nag_txt,0, IndexOf(Nag_txt,"[")-1)

							else: Nag_txt = "Nag:" + Nag

							commentv=substr(commentv,0,Nag_at) + "[" + Nag_txt + "]" + substrall(commentv,Nag_at +len(Nag)+1)

						else: break



				if( color7=="b" ):

					j=i
					while( j<i+15 ):

						pj1=substr(str,j,1)
						if( IndexOf(("{([$"),pj1)>=0 ): break
						if( substr(str,j,3)=="..." ): 
							i=j+3
							if( substr(str,i,1)!=" " ):
							  str=substr(str,0,i)+" "+substrall(str,i);


							break

						j+=1


				i-=1


			else:
	
				if( c=="."  or (c==" " and color7=="b"  ) ):

					move=""
					while( i<len(str) and (substr(str,i,1)==" " or substr(str,i,1)==".") ): i+=1
					c=substr(str,i,1)
					while( i<len(str) ):

						c=substr(str,i,1)
						if( c==" "  ): break
						move+=c
						i+=1

					if(len(move)>0 and IndexOf(move,"Z0")<0):

						if(IndexOf(resultl,move)>=0 ):

							break

						else:

							move2=c0_from_Crafty_standard(move,color7)

							if(len(move2)==0): 
								if(c0_PG_viewer): print("Can't parse this PGN!  move:"+ToString(gaj)+"."+color7+" "+ move)
								f_error=True
								break

							from_horiz4=charCodeAt(substr(move2,0,1),0) - 96
							from_vert4=parseInt(substr(move2,1,1))
							to_horiz4=charCodeAt(substr(move2,2,1),0) - 96
							to_vert4=parseInt(substr(move2,3,1))

							from_move = ToString(from_vert4)+ToString(from_horiz4)
							to_move = ToString(to_vert4)+ToString(to_horiz4)

							if(len(move2)>4 and substr(move2,4,1)=="["): c0_become_from_engine=substr(move2,5,1)
							else: c0_become_from_engine="Q"

							if(c0_fischer): c0_fischer_cstl_move(move2,False)
							else: c0_moveto(from_move, to_move, False)
							


							c0_sidemoves=-c0_sidemoves
	
							c0_PG_1+=move2

							c0_become_from_engine=""
							c0_become=""

							if( color7=="w" ):

								color7="b"
								i-=1

							else:

								color7="w"
								gaj+=1


							if( color7=="w" and len(str)-i<10):

								reminder = substrall(str,i+1)
								while( len(reminder)>0 and substr(reminder,0,1)==" " ): reminder=substrall(reminder,1)
								if(len(reminder)>0 and IndexOf(resultl,reminder)>=0 ):

									break


				else:

					if(len(str)-i<10):

						reminder = substrall(str,i)
						while( len(reminder)>0 and substr(reminder,0,1)==" " ): reminder=substrall(reminder,1)
						if(len(reminder)>0 and IndexOf(resultl,reminder)>=0 ):

							break
	
			i+=1



		c0_position=c0_1save_position
		c0_sidemoves=c0_1save_sidemoves
		c0_wKingmoved=c0_1save_wKingmoved
		c0_bKingmoved=c0_1save_bKingmoved
		c0_wLRockmoved=c0_1save_wLRockmoved
		c0_wRRockmoved=c0_1save_wRRockmoved
		c0_bLRockmoved=c0_1save_bLRockmoved
		c0_bRRockmoved=c0_1save_bRRockmoved
		c0_w00=c0_1save_w00
		c0_b00=c0_1save_b00
		c0_become=c0_1save_become
		c0_become_from_engine=c0_1save_become_from_engine
		c0_lastmovepawn=c0_1save_lastmovepawn
		c0_moveslist=c0_1save_moveslist

		return f_error


	#------------------------------ just get tag string

	def c0_get_tag( str, tag):

		ret=""
		ctg1="["+tag+"]"
		ctg2="[/"+tag+"]"
		at1=IndexOf(str,ctg1)
		if(at1>=0):

			str=substr(str,at1+len(ctg1))
			at1=IndexOf(str,ctg2)
			if(at1>=0): ret=substr(str,0, at1)

		return ret




	#-------------------------------------------------
	# Crafty notation (quite a standard)
	#-------------------------------------------------
	def c0_from_Crafty_standard(c0_move,c0_color47):

		global c0_position

		c0_move=c0_ReplaceAll( c0_move, "ep", "" )
		c0_move=c0_ReplaceAll( c0_move, "8Q", "8=Q" )
		c0_move=c0_ReplaceAll( c0_move, "8R", "8=R" )
		c0_move=c0_ReplaceAll( c0_move, "8B", "8=B" )
		c0_move=c0_ReplaceAll( c0_move, "8N", "8=N" )
		c0_move=c0_ReplaceAll( c0_move, "1Q", "1=Q" )
		c0_move=c0_ReplaceAll( c0_move, "1R", "1=R" )
		c0_move=c0_ReplaceAll( c0_move, "1B", "1=B" )
		c0_move=c0_ReplaceAll( c0_move, "1N", "1=N" )
		c0_becomes7=""
		c0_sh7=IndexOf(c0_move,"=")

		c0_ret7=c0_fischer_cst_fCr(c0_move)
		
		if(len(c0_ret7)>0): return c0_ret7
		else:

			if(len(c0_move)>4 and (substr(c0_move,0,5)=="O-O-O" or substr(c0_move,0,5)=="0-0-0")):

				if(c0_color47=="w"):

					if(IndexOf(c0_position,"wKc1")<0 and c0_can_be_moved( "15","13",False) ): c0_ret7="e1c1[0]"

				else:

					if(IndexOf(c0_position,"bKc8")<0 and c0_can_be_moved( "85","83",False) ): c0_ret7="e8c8[0]"

			else:

				if(len(c0_move)>2 and (substr(c0_move,0,3)=="O-O" or substr(c0_move,0,3)=="0-0")):

					if(c0_color47=="w"):

						if(IndexOf(c0_position,"wKg1")<0 and c0_can_be_moved( "15","17",False) ): c0_ret7="e1g1[0]"

					else:

						if(IndexOf(c0_position,"bKg8")<0 and c0_can_be_moved( "85","87",False) ): c0_ret7="e8g8[0]"

	
		if( len(c0_ret7)==0 ):

			if( IndexOf(("{ab}{ba}{bc}{cb}{cd}{dc}{de}{ed}{ef}{fe}{fg}{gf}{gh}{hg}"),substr(c0_move,0,2))>=0 ):

				c0_Z81horiz=charCodeAt(c0_move,0) - 96
				c0_Z82horiz=charCodeAt(c0_move,1) - 96

				c0_i8=0
				while( len(c0_position)>c0_i8 ):

					c0_Z8color=substr(c0_position,c0_i8,1)
					c0_Z8figure=substr(c0_position,c0_i8+1,1)
					c0_Z8horiz=charCodeAt(substr(c0_position,c0_i8+2,1),0) - 96
					c0_Z8vert=parseInt(substr(c0_position,c0_i8+3,1))

					c0_Z82vert=c0_Z8vert
					if(c0_color47=="w"): c0_Z82vert+=1
					else: c0_Z82vert-=1
	
					c0_Z8from_at72 = ToString(c0_Z8vert) + ToString(c0_Z8horiz)
					c0_Z8to_at72 = ToString(c0_Z82vert) + ToString(c0_Z82horiz)

					if(c0_Z8color==c0_color47 and c0_Z8figure=="p" and c0_Z81horiz==c0_Z8horiz ):

						if( c0_can_be_moved( c0_Z8from_at72, c0_Z8to_at72,False) ):

							c0_ret7=c0_convE777(c0_Z8from_at72)+c0_convE777(c0_Z8to_at72)
							break

					c0_i8+=5




				if(c0_sh7>=0):

					c0_becomes7="["+substr(c0_move,c0_sh7+1,1)+"]"

				c0_ret7+=c0_becomes7

			else:

				c0_cp7=len(c0_move)

				c0_figure7=substr(c0_move,0,1)
				if(c0_figure7=="N" or c0_figure7=="B" or c0_figure7=="R" or c0_figure7=="Q" or c0_figure7=="K"): c0_move = substrall(c0_move,1)
				else: c0_figure7="p"

				if(c0_sh7>=0):

					c0_becomes7="["+substr(c0_move,c0_sh7+1,1)+"]"
					c0_move = substr(c0_move,0, c0_sh7)

				c0_move=c0_ReplaceAll( c0_move, "+", "" )
				c0_move=c0_ReplaceAll( c0_move, "-", "" )
				c0_move=c0_ReplaceAll( c0_move, "x", "" )
				c0_move=c0_ReplaceAll( c0_move, "X", "" )
				c0_move=c0_ReplaceAll( c0_move, "#", "" )
				c0_move=c0_ReplaceAll( c0_move, "!", "" )
				c0_move=c0_ReplaceAll( c0_move, "?", "" )

				c0_cp7=len(c0_move)
				c0_cp7-=1
				c0_to_at7 = substr(c0_move,c0_cp7-1,2)
				c0_vert72=parseInt(substr(c0_move,c0_cp7,1))
				c0_cp7-=1
				c0_horiz72=charCodeAt(substr(c0_move,c0_cp7,1),0) - 96
				c0_cp7-=1
				c0_to_at72 = ToString(c0_vert72) + ToString(c0_horiz72)
						
				if(c0_cp7>=0):

					c0_vert71=parseInt(substr(c0_move,c0_cp7,1))
					if(c0_vert71<1 or c0_vert71>8): c0_vert71=0
					else: c0_cp7-=1

				else: c0_vert71=0

				if(c0_cp7>=0):

					c0_horiz71=charCodeAt(substr(c0_move,c0_cp7,1),0) - 96
					c0_cp7-=1
					if(c0_horiz71<1 or c0_horiz71>8): c0_horiz71=0

				else: c0_horiz71=0

				c0_i4=0
				while( len(c0_position)>c0_i4 ):

					c0_Z4color=substr(c0_position,c0_i4,1)
					c0_Z4figure=substr(c0_position,c0_i4+1,1)
					c0_Z4horiz=charCodeAt(substr(c0_position,c0_i4+2,1),0) - 96
					c0_Z4vert=parseInt(substr(c0_position,c0_i4+3,1))
					c0_Z4from_at72 = ToString(c0_Z4vert) + ToString(c0_Z4horiz)
					c0_Z4from_at7 = substr(c0_position,c0_i4+2,2)

					if(c0_Z4color==c0_color47 and c0_figure7==c0_Z4figure):

						if((c0_vert71==0 or c0_vert71==c0_Z4vert) and (c0_horiz71==0 or c0_horiz71==c0_Z4horiz) ):

							if( c0_can_be_moved( c0_Z4from_at72,c0_to_at72,False)):

								c0_ret7=c0_Z4from_at7+c0_to_at7+c0_becomes7
								break

					c0_i4+=5



		return c0_ret7



	#============================ ADDITIONAL UPPER LEVEL FUNCTIONS...

	#----------------------------------
	# Gets  FEN for position
	#----------------------------------
	def c0_get_FEN():


		global c0_position, c0_side, c0_sidemoves, c0_moving
		global c0_wKingmoved, c0_bKingmoved, c0_wLRockmoved, c0_wRRockmoved, c0_bLRockmoved, c0_bRRockmoved, c0_w00, c0_b00
		global c0_lastmovepawn, c0_become, c0_become_from_engine, c0_moveslist
		global c0_start_FEN, c0_fischer, c0_fischer_cst
		
		c0_fs1=""
		c0_em7=0
		c0_at7=0

		c0_vert7=8
		while( c0_vert7>=1  ):
	
			c0_horz7=1;
			while(  c0_horz7<=8 ):

				c0_pos7 = fromCharCode(96+c0_horz7)+ToString(c0_vert7)
				c0_at7=IndexOf(c0_position, c0_pos7 )
				if( c0_at7>=0 ):

					if( c0_em7>0 ): 
						c0_fs1+=ToString(c0_em7)
						c0_em7=0
					c0_ch7=substr(c0_position, c0_at7-1, 1 )
					c0_color7=substr(c0_position, c0_at7-2, 1 )
					if( c0_color7=="w" ): c0_fs1+=c0_ch7.upper()
					else: c0_fs1+=c0_ch7.lower()

				else: c0_em7+=1
	
				c0_horz7+=1

			if( c0_em7>0 ): 
				c0_fs1+=ToString(c0_em7)
				c0_em7=0
			c0_vert7-=1
			if(c0_vert7<1): break
			c0_fs1+="/"


		c0_fs1+=" "
		if( c0_sidemoves>0): c0_fs1+="w"
		else: c0_fs1+="b"
		c0_fs1+=" "

		if(  (c0_w00 or c0_wKingmoved or (c0_wLRockmoved and c0_wRRockmoved)) and (c0_b00 or c0_bKingmoved or (c0_bLRockmoved and c0_bRRockmoved)) ): c0_fs1+="- "
		else:

			if( not (c0_w00 or c0_wKingmoved) and not c0_wLRockmoved ): c0_fs1+="Q"
			if( not (c0_w00 or c0_wKingmoved) and not c0_wRRockmoved ): c0_fs1+="K"
			if( not (c0_b00 or c0_bKingmoved) and not c0_bLRockmoved ): c0_fs1+="q"
			if( not (c0_b00 or c0_bKingmoved) and not c0_bRRockmoved ): c0_fs1+="k"
			c0_fs1+=" "


		c0_enpass7="-"

		if(c0_lastmovepawn>0):

			c0_lmove7=substr(c0_moveslist, len(c0_moveslist)-4, 4 )
			c0_vert7 = charCodeAt(c0_lmove7,1)

			if( substr(c0_lmove7,0,1)==substr(c0_lmove7,2,1) and (charCodeAt(c0_lmove7,0)-96==c0_lastmovepawn) and (( substr(c0_lmove7,1,1)=="7" and substr(c0_lmove7,3,1)=="5" ) or ( substr(c0_lmove7,1,1)=="2" and substr(c0_lmove7,3,1)=="4" )) ):

				c0_at7=IndexOf(c0_position, substr(c0_lmove7,2,2) )
				if( c0_at7>=0 and substr(c0_position, c0_at7-1,1 )=="p" ):

					c0_enpass7=substr(c0_lmove7,0,1)
					if( substr(c0_lmove7,1,1)=="7" ): c0_enpass7+="6"
					else: c0_enpass7+="3"



		c0_fs1+=c0_enpass7 + " "

		c0_fs1+="0 "
				# position repeating moves....

		c0_mcount7=1
		c0_i7=0
		while( c0_i7<len(c0_moveslist) ):

			c0_i7+=4
			if((len(c0_moveslist)>c0_i7) and (substr(c0_moveslist,c0_i7,1)=="[")): c0_i7+=3
			c0_mcount7+=0.5

		if(c0_mcount7 % 1 >0):
		         c0_mcount7-=0.5

		c0_fs1+=ToString(c0_mcount7) + " "


		return c0_fs1


	#----------------------------------
	# Sets position using FEN
	#----------------------------------
	def c0_set_FEN( c0_fen_str ):

		global c0_moveslist

		c0_vert7=8
		c0_horz7=1

		c0_fs1=""
		c0_fs2=""

		c0_i7=0
		while( c0_i7<len(c0_fen_str) ):

			c0_ch7=substr(c0_fen_str,c0_i7,1)
			if( c0_ch7==" " ): break
			c0_pusto=parseInt(c0_ch7)
			if(c0_pusto>=1 and c0_pusto<=8):
				c0_j7=1 
				while( c0_j7<=c0_pusto ):
					c0_fs1+="."
					c0_j7+=1
			else: c0_fs1+=c0_ch7
			c0_i7+=1

		c0_fs1+= (" " + substrall(c0_fen_str,c0_i7))

		c0_i7=0
		while( c0_i7<len(c0_fs1) ):

			c0_ch7=substr(c0_fs1,c0_i7,1)
			if( c0_ch7==" " ): break

			c0_pos7 = fromCharCode(96+c0_horz7)+ToString(c0_vert7)
			c0_color7=" "
			if(c0_ch7=="p" or c0_ch7=="n" or c0_ch7=="b" or c0_ch7=="r" or c0_ch7=="q" or c0_ch7=="k" ): c0_color7="b"
			if(c0_ch7=="P" or c0_ch7=="N" or c0_ch7=="B" or c0_ch7=="R" or c0_ch7=="Q" or c0_ch7=="K" ): c0_color7="w"
			if(c0_color7!=" "):

				if( c0_ch7=="P" or  c0_ch7=="p" ): c0_ch7="p"
				else: c0_ch7=c0_ch7.upper()

				c0_fs2+=(c0_color7 + c0_ch7 + c0_pos7 + ";")

			if(c0_ch7=="/"): 
				if(c0_horz7>1): 
					c0_vert7-=1
					c0_horz7=1
			else: 
				c0_horz7+=1
				if(c0_horz7>8): 
					c0_horz7=1
					c0_vert7-=1

			if(c0_vert7<1): break

			c0_i7+=1


		while( c0_i7<len(c0_fs1) ):
			if( substr(c0_fs1,c0_i7,1)==" " ): break
			c0_i7+=1
			
		while( c0_i7<len(c0_fs1) ):
			if( substr(c0_fs1,c0_i7,1)!=" " ): break
			c0_i7+=1

		# which moves
		c0_side7move=1
		if(c0_i7<len(c0_fs1) and substr(c0_fs1,c0_i7,1)=="b"): c0_side7move=-1

		while( c0_i7<len(c0_fs1) ):
			if( substr(c0_fs1,c0_i7,1)==" " ): break
			c0_i7+=1
			
		while( c0_i7<len(c0_fs1) ):
			if( substr(c0_fs1,c0_i7,1)!=" " ): break
			c0_i7+=1
			
		# castlings

		c0_wK7=False
		c0_wRL7=False
		c0_wRR7=False
		c0_wcastl7=False
		c0_bK7=False
		c0_bRL7=False
		c0_bRR7=False
		c0_bcastl7=False

		c0_q7="-"
		if(c0_i7<len(c0_fs1)):

			c0_q7=substrall(c0_fs1,c0_i7)
			c0_at7=IndexOf(c0_q7," ")
			if( c0_at7>=0 ): c0_q7=substr(c0_q7,0,c0_at7)

		if( IndexOf(c0_q7,"K")<0 ): c0_wRR7=True
		if( IndexOf(c0_q7,"Q")<0 ): c0_wRL7=True

		if( IndexOf(c0_q7,"k")<0 ): c0_bRR7=True
		if( IndexOf(c0_q7,"q")<0 ): c0_bRL7=True

		if( IndexOf(c0_q7,"-")>=0 ): 
			c0_wK7=True
			c0_bK7=True

		c0_fisch_castl_save(c0_q7,c0_fs2)

		while( c0_i7<len(c0_fs1) ):
			if( substr(c0_fs1,c0_i7,1)==" " ): break
			c0_i7+=1
			
		while( c0_i7<len(c0_fs1) ):
			if( substr(c0_fs1,c0_i7,1)!=" " ): break
			c0_i7+=1
			
		# en passant

		c0_q7="-"
		if(c0_i7<len(c0_fs1)): c0_q7=substr(c0_fs1,c0_i7,1)

		c0_enpass7=0
		if( IndexOf(c0_q7,"-")<0 ): c0_enpass7=charCodeAt(c0_q7,0)-96

		while( c0_i7<len(c0_fs1) ):
			if( substr(c0_fs1,c0_i7,1)==" " ): break
			c0_i7+=1
						
		while( c0_i7<len(c0_fs1) ):
			if( substr(c0_fs1,c0_i7,1)!=" " ): break
			c0_i7+=1
			
		# remaining information is omitted

		c0_set_board_situation( c0_fs2, c0_wK7, c0_wRL7, c0_wRR7, c0_wcastl7, c0_bK7, c0_bRL7, c0_bRR7, c0_bcastl7, c0_enpass7, c0_moveslist, c0_side7move )



	#----------------------------------
	# PGN parser on chess moves
	#----------------------------------
	def c0_put_to_PGN(c0_moves_str):		# To write moveslist to PGN string...

		global c0_position, c0_side, c0_sidemoves, c0_moving
		global c0_side, c0_sidemoves, c0_moving
		global c0_wKingmoved, c0_bKingmoved, c0_wLRockmoved, c0_wRRockmoved, c0_bLRockmoved, c0_bRRockmoved, c0_w00, c0_b00
		global c0_lastmovepawn, c0_become, c0_become_from_engine, c0_moveslist
		global c0_start_FEN, c0_fischer, c0_fischer_cst

		if( len(c0_moves_str)==0 ): c0_moves_str=c0_moveslist

		c0_errflag=False
		c0_1save_position=c0_position
		c0_1save_sidemoves=c0_sidemoves
		c0_1save_wKingmoved=c0_wKingmoved
		c0_1save_bKingmoved=c0_bKingmoved
		c0_1save_wLRockmoved=c0_wLRockmoved
		c0_1save_wRRockmoved=c0_wRRockmoved
		c0_1save_bLRockmoved=c0_bLRockmoved
		c0_1save_bRRockmoved=c0_bRRockmoved
		c0_1save_w00=c0_w00
		c0_1save_b00=c0_b00
		c0_1save_become=c0_become
		c0_1save_become_from_engine=c0_become_from_engine
		c0_1save_lastmovepawn= c0_lastmovepawn
		c0_1save_moveslist= c0_moveslist

		if( len(c0_start_FEN)>0 ): 
			c0_set_FEN( c0_start_FEN )
			c0_fischer_adjustmoved()
		else:

			c0_position = "wpa2,wpb2,wpc2,wpd2,wpe2,wpf2,wpg2,wph2,wRa1,wNb1,wBc1,wQd1,wKe1,wBf1,wNg1,wRh1,bpa7,bpb7,bpc7,bpd7,bpe7,bpf7,bpg7,bph7,bRa8,bNb8,bBc8,bQd8,bKe8,bBf8,bNg8,bRh8,"

			c0_moveslist = ""

			c0_wKingmoved = False
			c0_bKingmoved = False
			c0_wLRockmoved = False
			c0_wRRockmoved = False
			c0_bLRockmoved = False
			c0_bRRockmoved = False
			c0_w00 = False
			c0_b00 = False

			c0_lastmovepawn = 0
			c0_sidemoves=1


		c0_become=""
		c0_become_from_engine=""

		c0_PGN_ret=""

		Result=""

		CR=( fromCharCode(13) + fromCharCode(10) )
		c0_i7=0
		
	
		while( c0_i7<len(c0_PGN_header) ):

			c0_q9=c0_PGN_header[c0_i7].upper()
			c0_at_q8=IndexOf(c0_q9, "FEN " )
			if(c0_at_q8<0 and c0_fischer): c0_at_q8=IndexOf(c0_q9, "SETUP " )
			if( c0_at_q8<0 or c0_at_q8>3 ):

				c0_PGN_ret += ( "[" + c0_PGN_header[c0_i7] + "]" + CR )
				c0_at_q9=IndexOf(c0_q9, "RESULT " )
				if( c0_at_q9>=0 ):

					Result=substrall(c0_PGN_header[c0_i7], c0_at_q9 + 7 )
					Result=c0_ReplaceAll( Result, "'", "" )

			c0_i7+=1


		if( len(c0_start_FEN)>0 ):

			if(c0_fischer): c0_PGN_ret += "[SetUp " + fromCharCode(34) + "1" + fromCharCode(34) + "]" + CR
			c0_PGN_ret += "[FEN "  + fromCharCode(34) + c0_start_FEN + fromCharCode(34) + "]" + CR

		if( len(c0_PGN_ret)>0 ): c0_PGN_ret += CR

		c07_gaj=0
		c07_col="b"
		c0_i7=0

		while( c0_i7< len(c0_moves_str) ):

			if(c07_col=="w"): c07_col="b"
			else: 
				c07_col="w"
				c07_gaj+=1


			c0_move8=substr(c0_moves_str, c0_i7, 4 )
			c0_i7+=4
			if( c0_i7< len(c0_moves_str) and substr(c0_moves_str, c0_i7, 1 )=="[" ):

				c0_move8+=substr(c0_moves_str, c0_i7, 3 )
				c0_i7+=3


			c0_move9=c0_to_Crafty_standard( c0_move8, c07_col )
			if( len(c0_move9)>0 ):

				if( c07_col=="w" ): c0_PGN_ret+=ToString(c07_gaj) + ". "
				c0_PGN_ret+=c0_move9 + " "

			else: 
				c0_errflag=True
				break


		if(not c0_errflag): c0_PGN_ret+=" " +Result

		c0_position=c0_1save_position
		c0_sidemoves=c0_1save_sidemoves
		c0_wKingmoved=c0_1save_wKingmoved
		c0_bKingmoved=c0_1save_bKingmoved
		c0_wLRockmoved=c0_1save_wLRockmoved
		c0_wRRockmoved=c0_1save_wRRockmoved
		c0_bLRockmoved=c0_1save_bLRockmoved
		c0_bRRockmoved=c0_1save_bRRockmoved
		c0_w00=c0_1save_w00
		c0_b00=c0_1save_b00
		c0_become=c0_1save_become
		c0_become_from_engine=c0_1save_become_from_engine
		c0_lastmovepawn=c0_1save_lastmovepawn
		c0_moveslist=c0_1save_moveslist

		if(c0_errflag): print("Can't parse " + ToString(c07_gaj) + c07_col + ":" + c0_move8)

		if( len(c0_start_FEN)>0 ):

			c0_set_board_situation( c0_position, c0_wKingmoved, c0_wLRockmoved, c0_wRRockmoved, c0_w00, c0_bKingmoved, c0_bLRockmoved, c0_bRRockmoved, c0_b00, c0_lastmovepawn, c0_moveslist, c0_sidemoves )


		return c0_PGN_ret


	#-------------------------------------------------
	# Crafty notation (quite a standard)
	#-------------------------------------------------
	def c0_to_Crafty_standard(c0_move,c0_color47):

		global c0_position, c0_sidemoves, c0_become_from_engine 

		c0_ret9=c0_fischer_cst_tCr(c0_move)
		if(len(c0_ret9)>0):

			c0_fischer_cstl_move(c0_move,False)
			c0_sidemoves=-c0_sidemoves
			return c0_ret9


		c0_pos9=c0_position
		c0_at9=IndexOf(c0_position, substr(c0_move,0,2) )
		c0_at7=IndexOf(c0_position, substr(c0_move,2,2) )
		c0_become_from_engine=""
		if( len(c0_move)>4 ): c0_become_from_engine=substr(c0_move,5,1)

		if(c0_at9>=0 ):

			c0_9figure=substr(c0_position, c0_at9-1,1 )
			c0_9color=substr(c0_position, c0_at9-2,1 )
			if( c0_9color==c0_color47 ):

				c0_Z4horiz=charCodeAt(substr(c0_move,0,1),0) - 96
				c0_Z4vert=parseInt(substr(c0_move,1,1))
				c0_Z4from_at72 = ToString(c0_Z4vert) + ToString(c0_Z4horiz)
				c0_Z5horiz=charCodeAt(substr(c0_move,2,1),0) - 96
				c0_Z5vert=parseInt(substr(c0_move,3,1))
				c0_Z5to_at72 = ToString(c0_Z5vert) + ToString(c0_Z5horiz)

				if( len(c0_become_from_engine)==0 and c0_9figure=="p" and (c0_Z5vert==8 or c0_Z5vert==1) ): c0_become_from_engine="Q"

				if( c0_can_be_moved( c0_Z4from_at72,c0_Z5to_at72,False ) ):

					if( c0_9figure!="p" ):

						c0_figc9=0
						c0_i4=0
						while( len(c0_position)>c0_i4 ):

							c0_Q4color=substr(c0_position,c0_i4,1)
							c0_Q4figure=substr(c0_position,c0_i4+1,1)
							if(c0_Q4color==c0_color47 and c0_9figure==c0_Q4figure): c0_figc9+=1
							c0_i4+=5
							
						c0_i4=0
						while( len(c0_position)>c0_i4 ):

							c0_Q4color=substr(c0_position,c0_i4,1)
							c0_Q4figure=substr(c0_position,c0_i4+1,1)
							c0_Q4horiz=charCodeAt(substr(c0_position,c0_i4+2,1),0) - 96
							c0_Q4vert=parseInt(substr(c0_position,c0_i4+3,1))
							c0_Q4from_at72 = ToString(c0_Q4vert) + ToString(c0_Q4horiz)
							c0_Q4from_at7 = substr(c0_position,c0_i4+2,2)

							if(c0_Q4color==c0_color47 and c0_9figure==c0_Q4figure and c0_Q4from_at7 !=substr(c0_move,0,2) ):

								if( c0_can_be_moved( c0_Q4from_at72, c0_Z5to_at72,False)):

									if( c0_figc9 < 3 and c0_Z4horiz!=c0_Q4horiz ):

										c0_ret9 += substr(c0_move,0,1)

									else:

										c0_ret9 += substr(c0_move,0,2) + "-"

									break

							c0_i4+=5



					c0_moveto( c0_Z4from_at72,c0_Z5to_at72,False )
					c0_sidemoves=-c0_sidemoves

					if( c0_9figure=="K" and c0_9color=="w" and substr(c0_move,0,4) == "e1g1" ): c0_ret9="O-O"
					else:
						if( c0_9figure=="K" and c0_9color=="b" and substr(c0_move,0,4) == "e8g8" ): c0_ret9="O-O"
						else:
							if( c0_9figure=="K" and c0_9color=="w" and substr(c0_move,0,4) == "e1c1" ): c0_ret9="O-O-O"
							else:
								if( c0_9figure=="K" and c0_9color=="b" and substr(c0_move,0,4) == "e8c8" ): c0_ret9="O-O-O"
								else:

									if(c0_9figure!="p"): c0_ret9=c0_9figure+c0_ret9


									if( len(c0_pos9) > len(c0_position) ):

										if( (len(c0_ret9)>0) and substr(c0_ret9, len(c0_ret9)-1,1)=="-" ): c0_ret9=substr(c0_ret9,0,len(c0_ret9)-1)
										c0_ret9 += "x"


									if( len(c0_ret9)>0 and substr(c0_ret9,0,1)=="x" ): c0_ret9= substr(c0_move,0,1) + c0_ret9

									c0_ret9 +=substr(c0_move,2,2)
									if( len(c0_become_from_engine)>0 ): c0_ret9+= "=" + c0_become_from_engine
				
									c0_color479="w"
									if(c0_color47=="w"): c0_color479="b"
										
									if( c0_is_check_to_king( c0_color479 ) ):
										if( c0_is_mate_to_king( c0_color479, True ) ): c0_ret9+= "#"
										else:
											c0_ret9+= "+"




		return c0_ret9


	#-------------------------------------------------
	# Fischerrandom support functions...
	#-------------------------------------------------

	#------- Get castling settings into variable...
	def c0_fisch_castl_save(c0_fen_c,c0_fen_pos):

		global c0_fischer_cst

		c0_fischer_cst=""
		atW=IndexOf(c0_fen_pos,"wK")
		atB=IndexOf(c0_fen_pos,"bK")
		if(atW>=0 and atB>=0):

			c0_fischer_cst+=("{wK}"+substr(c0_fen_pos,atW,5)+"{bK}"+substr(c0_fen_pos,atB,5))

			c0_q8=1
			while( c0_q8<=16 ):

				if(c0_q8<9):
					c0_ch=fromCharCode( 96+c0_q8 )
					c0_cl="b"
					c0_vt="8"
					c0_hz=fromCharCode( 96+c0_q8 )
				else:
					c0_ch=fromCharCode( 64+c0_q8-8 )
					c0_cl="w"
					c0_vt="1"
					c0_hz=fromCharCode( 96+c0_q8-8 )	
			
				c0_rook=c0_cl+"R"+c0_hz+c0_vt+";"
				if(IndexOf(c0_fen_c,c0_ch)>=0 and IndexOf(c0_fen_pos,c0_rook)>=0):

					if(c0_q8<9):

						if(charCodeAt(substr(c0_fen_pos,atB+2,1),0)>charCodeAt(c0_hz,0)): c0_fischer_cst+="{bLR}"
						else: c0_fischer_cst+="{bRR}"

					else:

						if(charCodeAt(substr(c0_fen_pos,atW+2,1),0)>charCodeAt(c0_hz,0)): c0_fischer_cst+="{wLR}"
						else: c0_fischer_cst+="{wRR}"

					c0_fischer_cst+=c0_rook
				c0_q8+=1

			c0_q8=0
			while( c0_q8<len(c0_fen_pos) ):

				c0_pc=substr(c0_fen_pos,c0_q8+1,1)
				if(c0_pc=="R"):

					c0_cl=substr(c0_fen_pos,c0_q8,1)
					c0_hz=substr(c0_fen_pos,c0_q8+2,1)
					c0_rook=substr(c0_fen_pos,c0_q8,5)

					if(c0_cl=="w"):

						if(IndexOf(c0_fischer_cst,"{wLR}")<0 and IndexOf(c0_fen_c,"Q")>=0 and charCodeAt(substr(c0_fen_pos,atW+2,1),0)>charCodeAt(c0_hz,0)):
							c0_fischer_cst+="{wLR}"+c0_rook
						else:
							if(IndexOf(c0_fischer_cst,"{wRR}")<0 and IndexOf(c0_fen_c,"K")>=0 and charCodeAt(substr(c0_fen_pos,atW+2,1),0)<charCodeAt(c0_hz,0)):
								 c0_fischer_cst+="{wRR}"+c0_rook

					else:

						if(IndexOf(c0_fischer_cst,"{bLR}")<0 and IndexOf(c0_fen_c,"q")>=0 and charCodeAt(substr(c0_fen_pos,atB+2,1),0)>charCodeAt(c0_hz,0)):
							c0_fischer_cst+="{bLR}"+c0_rook
						else:
							if(IndexOf(c0_fischer_cst,"{bRR}")<0 and IndexOf(c0_fen_c,"k")>=0 and charCodeAt(substr(c0_fen_pos,atB+2,1),0)<charCodeAt(c0_hz,0)):
								c0_fischer_cst+="{bRR}"+c0_rook

				c0_q8+=5




	#------- Adjust main variables after position is set...
	def c0_fischer_adjustmoved():

		global c0_fischer_cst
		global c0_wKingmoved, c0_bKingmoved, c0_wLRockmoved, c0_wRRockmoved, c0_bLRockmoved, c0_bRRockmoved, c0_w00, c0_b00

		if(IndexOf(c0_fischer_cst,"{bLR}")>=0 and IndexOf(c0_fischer_cst,"{bK}")>=0):
		
			c0_bKingmoved = False
			c0_bLRockmoved = False
			c0_b00 = False

		if(IndexOf(c0_fischer_cst,"{bRR}")>=0 and IndexOf(c0_fischer_cst,"{bK}")>=0):
		
			c0_bKingmoved = False
			c0_bRRockmoved = False
			c0_b00 = False

		if(IndexOf(c0_fischer_cst,"{wLR}")>=0 and IndexOf(c0_fischer_cst,"{wK}")>=0):
		
			c0_wKingmoved = False
			c0_wLRockmoved = False
			c0_w00 = False

		if(IndexOf(c0_fischer_cst,"{wRR}")>=0 and IndexOf(c0_fischer_cst,"{wK}")>=0):
		
			c0_wKingmoved = False
			c0_wRRockmoved = False
			c0_w00 = False


	#------- Does fischer movings for castling...
	def c0_fischer_cstl_move(c0_movz,c0_draw):

		global c0_position, c0_sidemoves
		global c0_side, c0_sidemoves, c0_moving
		global c0_wKingmoved, c0_bKingmoved, c0_wLRockmoved, c0_wRRockmoved, c0_bLRockmoved, c0_bRRockmoved, c0_w00, c0_b00
		global c0_fischer_cst
		
		c0_king=""
		c0_rook=""
		c0_king2=""
		c0_rook2=""

		if(substr(c0_movz,0,4)=="00**"):

			if(c0_sidemoves>0):

				c0_king=substr(c0_fischer_cst, IndexOf(c0_fischer_cst,"{wK}")+4,4 )
				c0_rook=substr(c0_fischer_cst, IndexOf(c0_fischer_cst,"{wRR}")+5,4 )
				c0_king2="wKg1"
				c0_rook2="wRf1"
				c0_wKingmoved=True
				c0_wLRockmoved=True
				c0_wRRockmoved=True
				c0_w00=True

			else:

				c0_king=substr(c0_fischer_cst, IndexOf(c0_fischer_cst,"{bK}")+4,4 )
				c0_rook=substr(c0_fischer_cst, IndexOf(c0_fischer_cst,"{bRR}")+5,4 )
				c0_king2="bKg8"
				c0_rook2="bRf8"
				c0_bKingmoved=True
				c0_bLRockmoved=True
				c0_bRRockmoved=True
				c0_b00=True


		else:
			if(substr(c0_movz,0,4)=="000*"):

				if(c0_sidemoves>0):

					c0_king=substr(c0_fischer_cst, IndexOf(c0_fischer_cst,"{wK}")+4,4 )
					c0_rook=substr(c0_fischer_cst, IndexOf(c0_fischer_cst,"{wLR}")+5,4 )
					c0_king2="wKc1"
					c0_rook2="wRd1"
					c0_wKingmoved=True
					c0_wLRockmoved=True
					c0_wRRockmoved=True
					c0_w00=True

				else:

					c0_king=substr(c0_fischer_cst, IndexOf(c0_fischer_cst,"{bK}")+4,4 )
					c0_rook=substr(c0_fischer_cst, IndexOf(c0_fischer_cst,"{bLR}")+5,4 )
					c0_king2="bKc8"
					c0_rook2="bRd8"
					c0_bKingmoved=True
					c0_bLRockmoved=True
					c0_bRRockmoved=True
					c0_b00=True


			else:

				c0_from_at=substr(c0_movz,0,2)
				c0_to_at=substr(c0_movz,2,2)
				c0_moveto(c0_convH888(c0_from_at), c0_convH888(c0_to_at), c0_draw)


		if(len(c0_king)>0 and len(c0_rook)>0):

			if(c0_draw):

				c0_clear_at(substr(c0_king,2,2))
				c0_clear_at(substr(c0_rook,2,2))
				c0_add_piece(substr(c0_king2,0,2)+substr(c0_rook2,2,2))
				c0_moveto(c0_convH888(substr(c0_rook2,2,2)), c0_convH888(substr(c0_king2,2,2)), c0_draw)
				c0_add_piece(c0_rook2)

			else:

				if(not (c0_king==c0_king2)): c0_position=c0_ReplaceAll(c0_position,c0_king,c0_king2)
				if(not (c0_rook==c0_rook2)): c0_position=c0_ReplaceAll(c0_position,c0_rook,c0_rook2)

			c0_lastmovepawn = 0;


	#------- Saves fischer movings for castling from Crafty standard...
	def c0_fischer_cst_fCr(c0_move):

		c0_ret8=""
		if(c0_fischer):

			if((len(c0_move)>4) and (substr(c0_move,0,5)=="O-O-O" or substr(c0_move,0,5)=="0-0-0")): c0_ret8="000*"
			else:
				if((len(c0_move)>2) and (substr(c0_move,0,3)=="O-O" or substr(c0_move,0,3)=="0-0")): c0_ret8="00**"

		return c0_ret8


	#------- Saves to Crafty standard...
	def c0_fischer_cst_tCr(c0_move):

		c0_ret8=""
		if(c0_fischer):

			if(substr(c0_move,0,4)=="000*"): c0_ret8="0-0-0"
			else:
				if(substr(c0_move,0,4)=="00**"): c0_ret8="0-0"

		return c0_ret8


	def c0_NAGs_define():		# Just data of NAG codes...

		global c0_NAGs

		c0_NAGs+="[0] null annotation [1] good move ('!') [2] poor move ('?') [3] very good move ('!!') [4] very poor move ('??') [5] speculative move ('!?') [6] questionable move ('?!') [7] forced move (all others lose quickly) [8] singular move (no reasonable alternatives) [9] worst move [10]  drawish position [11] equal chances, quiet position (=) [12] equal chances, active position (ECO ->/<-) [13] unclear position (emerging &) [14] White has a slight advantage (+=) [15] Black has a slight advantage (=+) [16] White has a moderate advantage (+/-) [17] Black has a moderate advantage (-/+) [18]  White has a decisive advantage (+-) [19] Black has a decisive advantage (-+) [20] White has a crushing advantage (Black should resign) (+--) [21] Black has a crushing advantage (White should resign) (--+) [22] White is in zugzwang (zz) [23] Black is in zugzwang (zz) [24] White has a slight space advantage [25]  Black has a slight space advantage [26]  White has a moderate space advantage (O) [27] Black has a moderate space advantage (O) [28] White has a decisive space advantage [29] Black has a decisive space advantage [30] White has a slight time (development) advantage [31] Black has a slight time (development) advantage [32] White has a moderate time (development) advantage (@) [33] Black has a moderate time (development) advantage (@) [34] White has a decisive time (development) advantage [35] Black has a decisive time (development) advantage [36] White has the initiative (^) [37]  Black has the initiative (^) [38] White has a lasting initiative [39] Black has a lasting initiative [40] White has the attack (->) "

		c0_NAGs+="[41] Black has the attack (->) [42] White has insufficient compensation for material deficit [43] Black has insufficient compensation for material deficit [44] White has sufficient compensation for material deficit (=/&) [45] Black has sufficient compensation for material deficit (=/&) [46] White has more than adequate compensation for material deficit [47] Black has more than adequate compensation for material deficit [48] White has a slight center control advantage [49] Black has a slight center control advantage [50] White has a moderate center control advantage (#) [51] Black has a moderate center control advantage (#) [52] White has a decisive center control advantage [53] Black has a decisive center control advantage [54] White has a slight kingside control advantage [55] Black has a slight kingside control advantage [56] White has a moderate kingside control advantage (>>) [57] Black has a moderate kingside control advantage (>>) [58] White has a decisive kingside control advantage [59] Black has a decisive kingside control advantage [60] White has a slight queenside control advantage [61] Black has a slight queenside control advantage [62] White has a moderate queenside control advantage (<<) [63] Black has a moderate queenside control advantage (<<)  [64] White has a decisive queenside control advantage [65] Black has a decisive queenside control advantage [66] White has a vulnerable first rank [67] Black has a vulnerable first rank [68] White has a well protected first rank [69] Black has a well protected first rank [70] White has a poorly protected king [71] Black has a poorly protected king [72] White has a well protected king [73] Black has a well protected king [74] White has a poorly placed king [75] Black has a poorly placed king [76] White has a well placed king [77] Black has a well placed king [78] White has a very weak pawn structure [79] Black has a very weak pawn structure [80] White has a moderately weak pawn structure (DR:x a5) [81] Black has a moderately weak pawn structure (DR:x a5) [82] White has a moderately strong pawn structure [83] Black has a moderately strong pawn structure [84] White has a very strong pawn structure [85] Black has a very strong pawn structure "

		c0_NAGs+="[86] White has poor knight placement [87] Black has poor knight placement [88] White has good knight placement [89] Black has good knight placement [90] White has poor bishop placement [91] Black has poor bishop placement [92] White has good bishop placement (diagonal) [93] Black has good bishop placement [94] White has poor rook placement [95] Black has poor rook placement [96] White has good rook placement (rank <=> file or) [97] Black has good rook placement [98] White has poor queen placement [99] Black has poor queen placement [100] White has good queen placement [101] Black has good queen placement [102] White has poor piece coordination [103] Black has poor piece coordination [104] White has good piece coordination [105] Black has good piece coordination [106] White has played the opening very poorly  [107] Black has played the opening very poorly [108] White has played the opening poorly [109] Black has played the opening poorly [110] White has played the opening well [111] Black has played the opening well [112] White has played the opening very well [113] Black has played the opening very well [114] White has played the middlegame very poorly [115] Black has played the middlegame very poorly [116] White has played the middlegame poorly [117] Black has played the middlegame poorly [118] White has played the middlegame well [119] Black has played the middlegame well [120] White has played the middlegame very well [121] Black has played the middlegame very well [122] White has played the ending very poorly [123] Black has played the ending very poorly [124] White has played the ending poorly [125] Black has played the ending poorly [126] White has played the ending well [127] Black has played the ending well [128] White has played the ending very well [129] Black has played the ending very well [130] White has slight counterplay [131] Black has slight counterplay [132] White has moderate counterplay (->/<-) [133] Black has moderate counterplay [134] White has decisive counterplay [135] Black has decisive counterplay [136] White has moderate time control pressure [137] Black has moderate time control pressure [138] White has severe time control pressure [139] Black has severe time control pressure "

		c0_NAGs+="[140] With the idea [141] Aimed against [142] Better move [143] Worse move [144] Equivalent move [145] Editors Remark ('RR') [146] Novelty ('N') [147] Weak point [148] Endgame [149] Line [150] Diagonal [151] White has a pair of Bishops [152] Black has a pair of Bishops [153] Bishops of opposite color [154] Bishops of same color [190] Etc. [191] Doubled pawns [192] Isolated pawn [193] Connected pawns [194] Hanging pawns [195] Backwards pawn [201] Diagram ('D', '#') [xyz]"


	#-------------------------------------------------
	# Simple chess bestmove search algorithm...
	#-------------------------------------------------

	def c0_Simple_search ( Deep2search ):		# Simple search...

		global c0_bestmove, c0_become_from_engine

		c0_bestmove=""

		saveD0becomefromengine=c0_become_from_engine
		c0_become_from_engine="Q"

		Eval=c0_AlphaBeta ( Deep2search, Deep2search, -9999999, 9999999  )

		c0_become_from_engine=saveD0becomefromengine;

		return Eval 
	

	def c0_AlphaBeta ( start_ply, ply_depth, alpha, beta ):		# Alpha-Beta simple search...

		global c0_position, c0_side, c0_sidemoves, c0_moving
		global c0_wKingmoved, c0_bKingmoved, c0_wLRockmoved, c0_wRRockmoved, c0_bLRockmoved, c0_bRRockmoved, c0_w00, c0_b00
		global c0_lastmovepawn, c0_become, c0_become_from_engine, c0_moveslist
		global c0_bestmove

		ret_eval=alpha

		saveD1sidemoves=c0_sidemoves
		saveD1wKingmoved=c0_wKingmoved
		saveD1bKingmoved=c0_bKingmoved
		saveD1wLRockmoved=c0_wLRockmoved
		saveD1wRRockmoved=c0_wRRockmoved
		saveD1bLRockmoved=c0_bLRockmoved
		saveD1bRRockmoved=c0_bRRockmoved
		saveD1w00=c0_w00
		saveD1b00=c0_b00
		saveD1lastmovepawn=c0_lastmovepawn
		saveD1position=c0_position		
		saveD1become=c0_become
		saveD1moveslist=c0_moveslist


		if(c0_sidemoves >0 ):
			c0_col0="w"
			c0_col1="b"
		else:
			c0_col1="w"
			c0_col0="b"


		if(ply_depth > 0):
    
			NextMoves=c0_get_next_moves()

			if( len( NextMoves )>0 ):
 
				c0_z=0
				while(c0_z<len(NextMoves)):

					c0_moveto(c0_convH888(substr(NextMoves,c0_z,2)),c0_convH888(substr(NextMoves,c0_z+2,2)),False);
					c0_sidemoves = -c0_sidemoves
 
					eval = -c0_AlphaBeta(start_ply, ply_depth-1, -beta, -alpha)

					if(ply_depth == start_ply and c0_D_is_check_to_king (c0_col1)):
						eval = eval + 150
						if c0_D_is_mate_to_king (c0_col1):
							eval = 66666

 
					if(eval >= beta):
						ret_eval=beta
						c0_z=1000	# return
					else:
        
						if(eval > alpha):
							alpha = eval
							ret_eval=alpha
              
							# Best move is at starting ply
							if(ply_depth == start_ply):
								c0_bestmove = substr(NextMoves,c0_z,4)
         
					c0_wKingmoved = saveD1wKingmoved
					c0_bKingmoved = saveD1bKingmoved
					c0_wLRockmoved = saveD1wLRockmoved
					c0_wRRockmoved = saveD1wRRockmoved
					c0_bLRockmoved = saveD1bLRockmoved
					c0_bRRockmoved = saveD1bRRockmoved
					c0_w00 = saveD1w00
					c0_b00 = saveD1b00

					c0_lastmovepawn = saveD1lastmovepawn
					c0_position = saveD1position		
					c0_sidemoves = saveD1sidemoves;		
					c0_become = saveD1become
					c0_moveslist = saveD1moveslist
        
					c0_z=c0_z+5

   
			else:
				# stalemate or checkmate
    
				if c0_D_is_mate_to_king (c0_col0):
					ret_eval = -66666
				else:
					if c0_D_is_pate_to_king (c0_col0):
						ret_eval = 0
    
		else:
			ret_eval = c0_EvalPosition()


		return ret_eval


	# Evaluation of current postition...


	def c0_EvalPosition():

		global c0_position, c0_side, c0_sidemoves
		global pawnPos, knightPos, bishopPos, rookPos, queenPos, kingPos
		
		Value=0
		Material=0
		PosVal=0
		i=0


		while( i<len( c0_position ) ):

			piece=substr( c0_position, i, 4 )
			color=substr( piece, 0, 1 )
			figure=substr( piece, 1, 1 )

			c0_Z3horiz=charCodeAt(piece,2) - 96
			c0_Z3vert=parseInt(substr( piece, 3, 1 ))
    
			at_i = (c0_Z3horiz-1) + ( (c0_Z3vert-1)*8 )
 
			if(color=="w"):
				at_i=63-at_i

    
			# Material and position

			if(figure=="p"):
				Material = 800
				PosVal = pawnPos[at_i]
			else:
				if(figure=="N"):
					Material = 3350
					PosVal = knightPos[at_i]
				else:   
					if(figure=="B"):
						Material = 3450
						PosVal = bishopPos[at_i]
					else:        
						if(figure=="R"):
							Material = 5000
							PosVal = rookPos[at_i]
						else:
							if(figure=="Q"):
								Material = 9750
								PosVal = queenPos[at_i]
        
							else:
								Material = 60000
								PosVal = kingPos[at_i]  

    
			if( (color=="w" and c0_sidemoves>0) or (color=="b" and c0_sidemoves<0) ):
				Value = Value + Material + PosVal
			else:
				Value = Value - Material - PosVal

			i=i+5
			
		return Value


# HERE IS REMOVABLE SOURCE OF 30KB IF NO NEEDED
# Chess library for Blender python
# universal 30Kb code of most played chess openings
# parameter moves:e2e4
# returns next variants, strength, ECO code
# chessforeva.blogspot.com


	global c0_opn
	
	c0_opn=[0,0,0,0,0,0,0,0,0,0,0,0,0]
	
	c0_opn[1]="A00.b1c31c7c54-1d7d55e2e49.A01.b2b31d7d52c1b29-2e7e55c1b29b8c67e2e39g8f69-3d7d62-3g8f61c1b29.A00.b2b41e7e59c1b29.A10.c2c41A40.b7b61b1c39c8b79-3A30.c7c51A34.b1c34A35.b8c65g1f32-1A36.g2g37g7g69f1g29f8g79A37.g1f39-6A34.g7g61g2g39f8g79f1g29b8c69-5g8f62g2g39-3A30.g1f33b8c63b1c35-1d2d44c5d49f3d49-4g7g61-1g8f64b1c39-3g2g31b8c64f1g29g7g69-3g7g65f1g29f8g79b1c39b8c69-7A11.c7c61b1c31d7d59-2d2d42d7d59-2e2e43d7d59e4d59c6d59d2d49g8f69b1c39-7A12.g1f33d7d59b2b34-1e2e35g8f69-5A10.d7d61-1A20.e7e52A21.b1c37A25.b8c63A27.g1f33-1A25.g2g36g7g69f1g29f8g79-5A21.d7d61g2g39-2f8b41-1A22.g8f64g1f35b8c69e2e33-1g2g36d7d59c4d59f6d59-6g2g34A23.d7d56c4d59f6d59f1g29d5b69g1f39b8c69-7A22.f8b44f1g29-5A20.g2g32b8c64f1g29g7g69b1c39f8g79-5g8f65f1g29c7c63-1d7d56c4d59f6d59-7A13.e7e61b1c33d7d59d2d49c7c64-1g8f65-4d2d41d7d59b1c39-3g1f33d7d57b2b32-1d2d43g8f69-2g2g33g8f69-3g8f62g2g39-3g2g32d7d59f1g29g8f69g1f39f8e79-7A10.f7f51b1c34g8f69g2g39-3g1f32g8f69-2g2g33g8f69f1g29-4g7g61b1c34f8g79d2d42-1g2g37e7e59f1g29-5d2d41f8g79-2e2e41-1g1f31f8g79-2g2g32f8g79f1g29d7d64-1e7e55b1c39-6A15.g8f63A16.b1c36c7c51g1f35-1g2g34-2d7d51c4d59f6d59A17.g2g39g7g69f1g29-6A16.e7e51g1f36b8c69g2g39-3g2g33-2A17.e7e62d2d42-1A18.e2e43d7d59e4e59-3A17.g1f33d7d59d2d49-4A16.g7g63d2d41f8g79-2e2e43d7d69d2d49f8g79-4g2g35f8g79f1g29e8g89e2e44-1g1f35d7d69-8A15.d2d41e7e69-2g1f31c7c51-1e7e63g2g39-2g7g64b1c34-1g2g35f8g79f1g29e8g89-6g2g31c7c62-1e7e62f1g29d7d59-3g7g65f1g29f8g79b1c39e8g89.A40.d2d43b7b61-1b8c61g1f39-2A43.c7c51d4d58d7d61-1A44.e7e54e2e49d7d69b1c39-4A43.e7e61-1g8f63A56.c2c49-3A43.e2e31-2A41.c7c61c2c49-2A84.d7d52D00.b1c31g8f69D01.c1g59-3D00.c1f41g8f69-2c1g51c7c64-1h7h65g5h49c7c69-4D01.c2c47D06.b8c61b1c33-1D07.c4d53d8d59e2e39e7e59b1c39f8b49c1d29b4c39-8D06.g1f33c8g49-3D10.c7c64b1c32d5c41-1e7e61-1g8f68c4d51c6d59c1f49-3e2e34a7a63d1c29-2e7e65g1f39b8d79d1c24f8d69-2f1d35d5c49d3c49b7b59c4d39-8g7g61g1f39f8g79-4g1f34a7a61-1d5c43a2a49c8f59-3e7e64c1g55-1e2e34b8d79-6c4d51c6d59b1c37b8c63g1f39g8f69c1f49-4g8f66c1f43b8c69e2e39-3g1f36b8c69c1f49c8f59e2e39e7e69f1d39-9g1f32"

	c0_opn[2]="g8f69b1c39b8c69c1f49-7e2e31g8f69b1c39-3D11.g1f35e7e61-1g8f69D15.b1c36a7a61c4c59-2d5c43D16.a2a49D17.c8f59D18.e2e35D19.e7e69f1c49f8b49e1g19b8d74-1e8g85d1e29-7D17.f3e54b8d75e5c49-2e7e64-5D15.e7e64c1g55d5c43-1h7h66g5f69d8f69-4e2e34b8d79d1c25f8d69-2f1d34d5c49d3c49b7b59-8D13.c4d51D14.c6d59b1c39b8c69c1f49c8f59e2e39e7e69-8D11.d1c21-1e2e32a7a62-1D12.c8f54b1c39e7e69f3h49-4D11.e7e63-5D06.c8f51-1D20.d5c41b1c31-1e2e32g8f69f1c49e7e69g1f39c7c59e1g19a7a69-8e2e41e7e54g1f39e5d49-3g8f65e4e59f6d59f1c49d5b69-6D21.g1f35a7a61D22.e2e39-2D21.e7e61-1D23.g8f67D24.b1c31-1D25.e2e38D26.e7e69f1c49c7c59e1g19D27.a7a69-9D08.e7e51d4e59d5d49g1f39b8c69-5D30.e7e63D31.b1c36D32.c7c51c4d59e6d59g1f39b8c69D33.g2g39g8f69f1g29D34.f8e79e1g19e8g89c1g59-12D31.c7c62c4d51e6d59-2e2e34g8f69g1f39b8d79d1c25f8d69-2f1d34-5e2e41-1g1f33d5c44-1g8f65-3f8e71c4d52e6d59c1f49-3g1f37g8f69c1f42-1c1g57e8g84e2e39-2h7h65g5h49e8g89-7D35.g8f64D50.c1g54D51.b8d73e2e39-2D50.f8e76D53.e2e37D54.e8g89D55.g1f39-3D50.g1f32-3D35.c4d53e6d59D36.c1g59c7c63e2e39-2f8e76e2e39c7c64-1e8g85f1d39-7D37.g1f32f8e79-4D30.c4d51e6d59b1c39-3g1f32c7c51c4d59e6d59g2g39-4c7c62d1c25-1e2e34-2g8f66b1c35c7c63-1f8e76c1g59-3c1g51-1g2g33f8e79f1g29e8g89e1g19-8D06.g8f61-2D00.e2e31g8f69-2D02.g1f32b8c61c1f49-2c7c51-1c7c61c2c49e7e64-1g8f65-3c8f51-1e7e61c2c49-2g8f66c1f41c7c54-1e7e65e2e39-3D03.c1g51e7e65-1f6e44-2D02.c2c45c7c64b1c35d5c45a2a49c8f59-3e7e64-2c4d51c6d59b1c39b8c69-4e2e32-2D25.d5c41e2e39e7e69f1c49c7c59-5D02.e7e63b1c37c7c63-1f8e76c1g59-3g2g32-3D04.e2e31D05.e7e69f1d39-3D02.g2g31-4A41.d7d61A42.c2c42e7e57g1f39e5e49-3g7g62b1c39f8g79-4A41.e2e43g7g62-1g8f67b1c39g7g69-4g1f33c8g43c2c49-2g7g64c2c49f8g79b1c39-4g8f62c2c49-3g2g31-2A40.e7e61c2c46b7b61a2a33-1b1c33-1e2e43c8b79-3A43.c7c51d4d59-2A40.d7d51b1c36-1g1f33-2A84.f7f52b1c32g8f69-2g1f32g8f69-2g2g35g8f69f1g29f8e79-5A40.f8b41c1d29-2g8f62b1c35f8b49d1c24-1e2e35-3g1f34b7b69-4e2e41d7d59b1c39-3g1f32c7c51-1d7d51-1f7f52g2g39g8f69f1g29-4g8f63c2c49-3g2g31-2A80.f7f51b1c31d7d54-1g8f65c1g59d7d59-4c1g51g7g69-2A84.c2c41g8f69b1c36A85.g7g69-2A86.g2g33"


	c0_opn[3]="-3A80.e2e41A82.f5e49b1c39A83.g8f69c1g59-5A80.g1f31g8f69g2g39g7g69f1g29f8g79e1g19e8g89-8A81.g2g33g7g61-1g8f68f1g29e7e62-1g7g67c2c42f8g79-2g1f35f8g79e1g19e8g89c2c49d7d69b1c39-7g1h31-6A40.g7g61c2c45f8g79b1c35c7c52d4d59-2d7d67e2e49b8c69-4e2e42d7d69b1c39-3g1f31d7d69-4e2e43f8g79b1c35d7d69-2c2c42-1g1f32d7d69-4g1f31f8g79c2c49-4A45.g8f65b1c31d7d59c1g59b8d79-4c1f41-1c1g51c7c51g5f69g7f69-3d7d51g5f69e7f69e2e39-4e7e62e2e49h7h69g5f69d8f69b1c39-6f6e43g5f48c7c56f2f39d8a59c2c39e4f69b1d29c5d49d2b39-8d7d53-2g5h41-2g7g61g5f69e7f69-4c2c31-1A50.c2c46b8c61g1f39e7e69-3A56.c7c51d4d58A57.b7b55c4b58a7a69b1c31-1b5a64A58.c8a64A59.b1c39d7d65-1g7g64-3A57.g7g65b1c39c8a69e2e49a6f19e1f19d7d69-8b5b62d7d63b1c39-2d8b62b1c39-2e7e63b1c39-3e2e31-1f2f31-3g1f31g7g69-3A56.d7d61b1c39g7g69e2e49f8g79-5e7e51b1c39d7d69e2e49f8e79-5A60.e7e62b1c39A61.e6d59c4d59d7d69A65.e2e47A66.g7g69f2f46A67.f8g79f1b59f6d79-4A70.g1f33-3A61.g1f32A62.g7g69-7A56.g7g61b1c39f8g79e2e49d7d69-6e2e31g7g69-2g1f31c5d49f3d49e7e59-5A50.c7c61b1c39d7d59g1f39-4A53.d7d61b1c37b8d74e2e46e7e59g1f39-3g1f33-2e7e52A54.g1f39-2A53.g7g62e2e49f8g79-4g1f32b8d75-1g7g64-3A51.e7e51d4e59f6e41-1A52.f6g48c1f44b8c69g1f39f8b49-4g1f35f8c59e2e39b8c69-7E00.e7e64E20.b1c34c7c51d4d59e6d59c4d59d7d69e2e49g7g69-7d7d51c1g54f8e79e2e39-3c4d53e6d59c1g59f8e79e2e39-5g1f32-2f8b48E24.a2a31b4c39b2c39-3E30.c1g51h7h69E31.g5h49-3E32.d1c23E38.c7c53d4c59b4c52-1b8a62a2a39-2E39.e8g85a2a39b4c59g1f39b7b69-7E34.d7d51E35.c4d59d8d59-3E33.e8g85a2a39b4c39c2c39b7b68c1g59c8a62-1c8b77f2f39-4f6e41c3c29-7E40.e2e34E43.b7b62f1d33c8b79-2E44.g1e26-2E41.c7c53f1d36b8c69g1f39-3E42.g1e23c5d49e3d49-4E46.e8g84E47.f1d37c7c52g1f39-2E48.d7d57g1f39c7c59e1g19-5E46.g1e22d7d59a2a39b4e79c4d59-7E20.f2f31d7d59a2a39b4c39b2c39-5g1f31b7b64-1c7c55g2g39-3g2g31-3E10.g1f34E12.b7b65a2a32c8a63d1c29a6b79b1c39c7c59e2e49c5d49f3d49-8c8b76b1c39d7d59c4d59f6d59-6b1c31c8b75a2a39d7d59-3f8b44c1g59-3E14.e2e31c8b79f1d39-3E15.g2g35c8a66b1d21-1b2b36f8b49c1d29b4e79f1g29c7c69d2c39d7d59-8d1a41-2c8b73E16.f1g29E17.f8e79b1c32-1e1g17e8g89E18.b1c39E19.f6e49"


	c0_opn[4]="c3e49b7e49f3e19-12E10.c7c51d4d59e6d59c4d59d7d69b1c39g7g69-7d7d52b1c38b8d71-1c7c61-1d5c41-1f8b41-1f8e74c1f43e8g89e2e39-3c1g56e8g85e2e39-2h7h64-4g2g31-2E11.f8b41b1d23b7b69a2a39-3c1d26a7a52-1d8e77g2g39b8c69-6E00.g2g31c7c52d4d55e6d59c4d59-3g1f34-2E01.d7d55E02.f1g26E03.d5c44-1E06.f8e75E07.g1f39e8g89E08.e1g19-5E01.g1f33-2E00.f8b42c1d29-4D70.g7g63b1c38d7d52D82.c1f41D83.f8g79e2e39c7c59-4D80.c1g51f6e49-2D85.c4d55f6d59c1d21f8g79e2e49-3e2e49d5c39D86.b2c39f8g79c1e31c7c59d1d29-3f1b51-1f1c44c7c56g1e29b8c65c1e39e8g89e1g19-4e8g84e1g19-4e8g83g1e29-3g1f33c7c59a1b19e8g89f1e29c5d49c3d49-13D90.g1f33f8g79D92.c1f41D93.e8g89-2D91.c1g52f6e49c4d59e4g59f3g59e7e69-6D90.c4d51f6d59e2e49d5c39b2c39-5D96.d1b33D97.d5c49b3c49e8g89e2e49a7a69-6D94.e2e31e8g89-5E61.f8g77c1g51-1E70.e2e48d7d69f1d31e8g89g1e29-3E73.f1e22e8g89c1g54b8a63-1E74.c7c53E75.d4d59-2E73.h7h62g5e39-3g1f35e7e59e1g19b8c69d4d59c6e79-8E80.f2f32E81.e8g89c1e37E83.b8c62g1e29-2E81.b8d71-1c7c51-1E85.e7e54E87.d4d56-1E86.g1e23-3E81.c1g51-1g1e21-3E76.f2f41e8g89g1f39b8a62-1c7c57d4d59e7e69f1e29e6d59c4d59-9E70.g1e21e8g89e2g39-3E90.g1f33e8g89E91.f1e29b8a61-1b8d71-1E92.e7e58c1e31-1d4d51a7a59-2d4e51d6e59d1d89f8d89c1g59-5E94.e1g16b8a61-1E97.b8c68d4d59c6e79b2b46a7a54-1f6h55f1e19-3E98.f3e13f6d79-8E90.h2h31-3E71.h2h31e8g89c1g59-4E70.e8g81g1f39d7d69f1e29e7e59-6E61.g1f31E62.d7d62-1E61.e8g87c1g55-1g2g34-3g2g31e8g89f1g29d7d69-6D70.f2f31-1g1f31E60.f8g79b1c31-1g2g38e8g89f1g29d7d69e1g19b8d79-8D70.g2g31E60.f8g79f1g29d7d52c4d59f6d59e2e49-4e8g87b1c37d7d69g1f39b8c64-1b8d75e1g19-5g1f32d7d69-8A45.e2e31g7g69-2A46.g1f32A47.b7b61-1A46.c7c51c2c31-1d4d55b7b53c1g59-2d7d61-1e7e62-1g7g62b1c39-3e2e32g7g69-3d7d51c1f41-1c2c47c7c63b1c39-2e7e66b1c39f8e79-4e2e31-2d7d61c2c49-2e7e63c1f41c7c59-2c1g51c7c54e2e39-2d7d51-1f8e71-1h7h62g5h49-3c2c44b7b64a2a32-1b1c32-1g2g35c8a66b2b39-2c8b73f1g29-4c7c51d4d59-2d7d51b1c39-2f8b42c1d29d8e79g2g39-5e2e31b7b66f1d39c8b79e1g19-4c7c53f1d39-3g2g31b7b51-1b7b63f1g29c8b79e1g19-4c7c52f1g29-2d7d52f1g29-4A48.g7g64D02.b1c31d7d59c1f49f8g79e2e39e8g89f1e29-7A48.c1f41"


	c0_opn[5]="f8g79e2e39d7d63-1e8g86-4c1g51f8g79b1d29d7d54e2e39e8g89-3e8g85-4c2c31f8g79-2c2c44c7c51-1f8g79b1c37d7d52c4d59f6d59e2e49d5c39b2c39c7c59-7d7d61e2e49e8g89f1e29e7e59-5e8g85c1g51-1e2e48d7d69f1e29e7e59e1g19b8c69d4d59c6e79-10g2g32e8g89f1g29d7d69e1g19-7e2e31f8g79-2A49.g2g32f8g79f1g29e8g89c2c41-1e1g18d7d52-1d7d67c2c49b8d79-10A45.g2g31g7g69f1g29f8g79.A40.e2e45B00.b7b61d2d49c8b79f1d39-4b8c61d2d44d7d56-1e7e53-2g1f35d7d66d2d49g8f69b1c39c8g49-5e7e53-3B20.c7c54B23.b1c31a7a61-1b8c66f1b51c6d47b5c49e7e69-3g7g62-2f2f42d7d61g1f39-2e7e62g1f39d7d59-3g7g66g1f39f8g79f1b55c6d49e1g19-3f1c44e7e69-6g1e21-1g1f31d7d64-1g7g65-2B24.g2g34B25.g7g69f1g29f8g79B26.d2d39d7d67c1e35a8b84-1e7e65d1d29-3f2f44e7e69g1f39g8e79e1g19e8g89c1e39c6d49-9e7e62c1e39d7d69-4B25.g1e21-6B23.d7d61f2f45b8c65g1f39g7g69-3g7g64g1f39f8g79-4g2g34b8c69f1g29g7g69d2d39-6e7e61f2f42d7d59-2g1e21-1g1f33a7a65-1b8c64-2g2g33b8c63f1g29-2d7d56-3g7g61-2B20.b2b31b8c69c1b29-3B22.c2c31d7d53e4d59d8d59d2d49b8c61g1f39c8g49f1e29-4c5d41c3d49-2e7e61g1f39g8f69-3g7g61-1g8f65g1f39c8g46f1e29e7e69e1g14b8c69-2h2h35g4h59e1g19-6e7e63-7d7d61d2d49g8f69f1d39-4e7e61d2d49d7d59e4d56e6d59g1f39b8c69-4e4e53-4g7g61d2d49c5d49c3d49d7d59-5g8f63e4e59f6d59d2d47c5d49c3d42d7d69-2d1d41e7e69-2g1f36b8c65c3d43d7d69f1c49-3f1c46d5b69c4b39d7d59e5d69d8d69-7e7e64c3d49b7b64-1d7d65-6g1f32b8c65f1c49-2e7e64-6B20.c2c41b8c69b1c39g7g69-4d2d31b8c69g2g39g7g69f1g29f8g79f2f49-7d2d41c5d49c2c39d4c37b1c39b8c69g1f39-4g8f62e4e59f6d59-6B21.f2f41b8c64g1f39-2d7d55-2B20.g1e21b8c69-2B27.g1f37B28.a7a61c2c33-1c2c43-1d2d43c5d49f3d49g8f69-5B30.b8c63b1c31d7d61d2d49c5d49f3d49g8f69-5e7e51f1c49f8e79d2d39-4e7e62d2d49c5d49f3d49-4g7g62d2d49c5d49f3d49f8g79c1e39g8f69f1c49-8g8f61-2c2c31d7d55e4d59d8d59d2d49-4g8f64e4e59f6d59d2d49c5d49-6d2d31g7g69g2g39f8g79f1g29-5B32.d2d46c5d49f3d49d7d61-1d8b61d4b39g8f69b1c39e7e69-5d8c71b1c39e7e69c1e34a7a69-2f1e25a7a69e1g19g8f69-7e7e51d4b59a7a61b5d69f8d69d1d69d8f69-5d7d68b1c34a7a69b5a39b7b59c3d59-5c2c45f8e79b1c39a7a69b5a39-8e7e61b1c39d8c79-3B34.g7g61B35.b1c34f8g79c1e39g8f69f1c47d8a52-1e8g87c4b39"


	c0_opn[6]="d7d69-4f1e22-5B34.c1e31-1B36.c2c44B37.f8g76B38.c1e39B39.g8f69b1c39e8g86f1e29d7d69e1g19c8d79-5f6g43d1g49c6d49g4d19-8B36.g8f63b1c39d7d69f1e29c6d49d1d49f8g79-9B32.g8f65B33.b1c39d7d63c1g54c8d71-1e7e68d1d29a7a66e1c19c8d74f2f49-2h7h65g5e39-4f8e73e1c19e8g89-6f1c42d8b64-1e7e65c1e39-3f1e22e7e59d4b39f8e79-4f2f31-2e7e55d4b59d7d69a2a41-1c1g58a7a69b5a39b7b59c3d55d8a52g5d29a5d89d2g59d8a59g5d29a5d89-7f8e77g5f69e7f69c2c39e8g86a3c29f6g59a2a49-4f6g53a3c29-7g5f64g7f69c3d59f6f56c2c33f8g79e4f59c8f59a3c29-5f1d36c8e69e1g19e6d59e4d59-6f8g73c2c34f6f59e4f59c8f59-4f1d35c6e79d5e79d8e79-10g5f61g7f69b5a39b7b59c3d59-7c3d51f6d59e4d59c6b89c2c49-8e7e61d4b59-2g7g61-6B30.f1b51d7d61e1g19c8d79f1e19g8f69-5e7e62b5c63b7c69d2d39-3e1g16g8e79c2c34a7a69-2f1e15a7a69-5B31.g7g65b5c63b7c63e1g19f8g79-3d7c66d2d39f8g79h2h39g8f69b1c39-7e1g16f8g79c2c34g8f69f1e19e8g89d2d49-5f1e15e7e53-1g8f66-5B30.g8f61-3B50.d7d64b1c31g8f69-2c2c31g8f69f1d32b8c69-2f1e25b8c62-1b8d72-1g7g64e1g19f8g79-4h2h31-3d2d31-1B53.d2d48c5d49d1d41a7a63-1b8c66f1b59c8d79b5c69d7c69b1c39g8f69c1g59e7e69e1c19f8e79-12B54.f3d49B55.g8f69B56.b1c39B90.a7a65a2a41-1c1e32e7e54d4b39c8e67d1d22-1f2f37b8d75g2g49-2f8e74d1d29-4f8e72f2f39-4e7e63f2f36b7b59-2g2g43-2f6g41e3g59h7h69g5h49g7g59h4g39f8g79-8B94.c1g52B95.e7e69B96.f2f49b8d71d1f39d8c79e1c19-4B97.d8b63d1d27b6b29a1b19b2a39f4f59b8c69f5e69f7e69d4c69b7c69-10d4b32-2B98.f8e74d1f39B99.d8c79e1c19b8d79g2g49b7b59g5f69d7f69g4g59f6d79f4f59-15B90.f1c41e7e69c4b38b7b55e1g19f8e79-3b8d72-1f8e72-2e1g11-3B92.f1e22e7e56d4b39f8e79c1e32c8e69-2e1g17e8g89c1e33c8e69-2g1h16-6e7e63e1g19f8e79f2f49-5B90.f2f31e7e55d4b39c8e69c1e39-4e7e64c1e39b7b59-4B93.f2f41d8c72-1e7e54d4f39b8d79a2a49-4e7e62-2B91.g2g31e7e59d4e29-4B56.b8c61B60.c1g55c8d71-1B62.e7e68B63.d1d29B66.a7a66B67.e1c19B68.c8d75B69.f2f49-2B67.h7h64g5e39-4B64.f8e73B65.e1c19e8g89-6B57.f1c42d8b64d4b39e7e69-3e7e65c1e39-3B58.f1e21e7e59-2B56.f2f31-2B80.e7e61c1e32-1B83.f1e24-1B81.g2g43-2B70.g7g62B72.c1e37f8g79f1e21-1B75.f2f39b8c63d1d29e8g89e1c14-1f1c45c8d79e1c19-6B76.e8g86d1d28B77.b8c69e1c14c6d43e3d49c8e69"


	c0_opn[7]="-3d6d56e4d59f6d59d4c69b7c69-6f1c45B78.c8d79B79.e1c19a8c89c4b39c6e59-8B76.f1c41b8c69-6B70.f1c41f8g79-2f1e21f8g79c1e33-1e1g16e8g89-4B71.f2f41-3B55.f2f31e7e59-5B53.g8f61b1c39c5d49f3d49a7a65-1b8c61-1g7g62-6B51.f1b51b8c61e1g19c8d79f1e19-4b8d72d2d46g8f69b1c39-3e1g13-2B52.c8d76b5d79b8d71e1g19g8f69-3d8d78c2c44b8c69b1c39-3e1g15b8c67c2c39g8f69-3g8f62-6B50.f1c41g8f69d2d39-4B40.e7e62b1c31a7a65d2d47c5d49f3d49d8c79-4g2g32-2b8c64d2d49c5d49f3d49-5b2b31-1c2c31d7d55e4d57d8d55d2d49g8f69-3e6d54d2d49-3e4e52-2g8f64e4e59f6d59d2d49c5d49c3d49d7d69-8c2c41b8c69b1c39-3d2d31b8c67g2g39d7d54b1d29-2g7g65f1g29f8g79e1g19g8e79-7d7d52b1d29-3d2d47c5d49B41.f3d49a7a64B43.b1c33b7b53f1d39d8b69-3d8c76f1d33b8c65-1g8f64-2f1e23g8f69e1g19-3g2g32-3B41.c2c41g8f69b1c39-3B42.f1d34b8c61d4c69-2d8b61-1d8c71e1g19g8f69-3f8c52d4b39c5a73-1c5e76e1g19-4g7g61-1g8f63e1g19d7d64c2c49-2d8c75d1e29d7d69-6B41.f1e21-2B44.b8c62B45.b1c38B46.a7a62f1e29-2B45.d7d61-1B47.d8c76B48.c1e33B49.a7a69f1d39g8f69e1g19-5B47.f1e24a7a69e1g19g8f69c1e35f8b49-2g1h14-5g2g31a7a69f1g29g8f69e1g19-7B44.d4b51d7d69c1f43e6e59f4e39-3c2c46g8f69b1c39a7a69b5a39f8e79f1e29-10B41.d8b61d4b39-2g8f62b1c39B45.b8c63d4b57d7d66c1f49e6e59f4g59a7a69b5a39b7b59c3d55-1g5f64g7f69c3d59-10f8b43a2a39b4c39b5c39d7d59-6d4c62b7c69-3B41.d7d65c1e32a7a69-2f1e24a7a63-1f8e76e1g19e8g89-4g2g42h7h69-3f8b41-2f1d31b8c69-7B27.g7g61c2c31f8g79-2d2d48c5d44f3d49f8g79-3f8g75b1c39c5d49f3d49b8c69-7B29.g8f61b1c35-1e4e54f6d59-4B20.g2g31b8c69f1g29-4B10.c7c61b1c31d7d59B11.g1f39c8g47h2h39g4f39d1f39e7e69-5B12.d5e42c3e49-5B10.c2c41d7d59c4d53c6d59e4d59g8f69-4e4d56c6d59c4d59g8f69b1c39f6d59-8d2d31d7d59b1d29e7e59g1f39f8d69-6d2d48B12.d7d59B15.b1c32d5e49c3e49B17.b8d72e4g53g8f69f1d39e7e69g1f39f8d69d1e29h7h69g5e49f6e49e2e49-11f1c42g8f69e4g59e7e69d1e29-5g1f33g8f69e4f69d7f69-5B18.c8f55e4g39B19.f5g69f1c41-1g1f32b8d79h2h49h7h69h4h59g6h79-6h2h46h7h69g1f39b8d79h4h59g6h79f1d39h7d39d1d39e7e69c1f49-14B15.g8f61e4f69B16.g7f69-5B15.g7g61-2B12.b1d21d5e49d2e49b8d73e4g53g8f69f1d39e7e69-4f1c42g8f69-2g1f33g8f69-3c8f55e4g39f5g69g1f32-1h2h47"


	c0_opn[8]="h7h69g1f39b8d79h4h59g6h79f1d39h7d39d1d39e7e69-13g8f61e4f69g7f69-6B13.e4d52c6d59B14.c2c47g8f69b1c39b8c62c1g53-1g1f36c8g49c4d59f6d59d1b39g4f39g2f39-8e7e66g1f39f8b46c4d56f6d59c1d29-3f1d33-2f8e73c4d59f6d59f1d39-6g7g61-4B13.f1d32b8c69c2c39g8f69c1f49c8g49d1b39-9B12.e4e52c6c51d4c59-2c8f58b1c34e7e69g2g49f5g69g1e29c6c59-6c2c31e7e69c1e39-3g1f33e7e69f1e29b8d74e1g19-2c6c55-4h2h41-3f2f31-2B10.g7g61b1c39-3g1f31d7d59b1c39-4B01.d7d51b1c31-1e4d59d8d55b1c39d5a57d2d47c7c63f1c43-1g1f36g8f69-3g8f66f1c42-1g1f37c7c66f1c49c8f59-3c8g43-4f1c41-1g1f31g8f69-3d5d61d2d49g8f69g1f39a7a69-5d5d81d2d49-4g8f64b1c31f6d59-2c2c41c7c65-1e7e64-2d2d45c8g43-1f6d56c2c45d5b69g1f39-3g1f34g7g69-4f1b51c8d79b5e29-3g1f31f6d59d2d49-6B07.d7d61b1c31-1d2d49g7g61b1c38f8g79c1e35-1f2f44-3g1f31-2g8f68b1c39b8d71g1f39e7e59f1c49f8e79-5c7c61f2f46d8a59f1d39e7e59-4g1f33-2e7e51d4e53d6e59d1d89e8d89-4g1f36b8d79f1c49f8e79e1g19e8g89f1e19c7c69a2a49-10g7g66c1e31c7c66d1d29b7b59-3f8g73d1d29-3c1g51f8g79d1d29-3f1e21f8g79-2f2f31-1B09.f2f42f8g79g1f39c7c53f1b59c8d79e4e59f6g49-5e8g86f1d39-5B08.g1f32f8g79f1e29e8g89e1g19c7c65-1c8g44-6B07.g2g31f8g79f1g29e8g89g1e29e7e59-8f1d31e7e59-2f2f31-4C20.e7e52C23.b1c31b8c62-1C25.g8f67C27.f1c43-1C26.f2f43C29.d7d59f4e59f6e49-4C25.g2g33-3C21.d2d41e5d49C22.d1d49b8c69d4e39g8f69-6C23.f1c41b8c61-1g8f68C24.d2d39b8c64g1f39-2c7c63g1f39-2f8c52-4C30.f2f41C31.d7d51e4d59-2C33.e5f46f1c42-1C34.g1f37C37.g7g59-3C30.f8c51g1f39d7d69-4C25.g1f38C44.b8c68C46.b1c31g8f69C47.d2d44e5d49f3d49f8b49d4c69b7c69f1d39d7d59e4d59c6d59e1g19e8g89c1g59c7c69-14C48.f1b53c6d44-1C49.f8b45e1g19e8g89d2d39d7d69-6C46.g2g32f8c59f1g29d7d69-6C44.c2c31g8f69d2d49-3d2d41e5d49c2c31-1f1c41f8c52-1g8f67e1g14-1e4e55d7d59c4b59-5C45.f3d47f8c55c1e34d8f69c2c39g8e79f1c49-5d4b31-1d4c64d8f69d1d29d7c69b1c39-6g8f64b1c32f8b49d4c69b7c69f1d39d7d59e4d59-7d4c67b7c69e4e59d8e79d1e29f6d59c2c49c8a65b2b39-2d5b64-12C60.f1b56C68.a7a67C70.b5a48b7b51a4b39-2C71.d7d61C74.c2c35C75.c8d79-2C72.e1g14-2C77.g8f69d1e21b7b59a4b39-3d2d31b7b54a4b39-2d7d65c2c39-3d2d41e5d49e1g19f8e79f1e19-5C78.e1g18b7b51"


	c0_opn[9]="a4b39c8b73f1e19f8c59-3f8c53a2a49-2f8e73f1e19d7d64-1e8g85-5C80.f6e41d2d49b7b59a4b39d7d59d4e59C81.c8e69b1d24e4c59c2c39-3C82.c2c35f8c59-9C78.f8c51-1C84.f8e77C85.a4c61d7c69d2d39-3C86.d1e21b7b59a4b39-3C87.f1e19C88.b7b59a4b39d7d66C90.c2c39e8g89C91.d2d41c8g49-2C92.h2h39c6a54C96.b3c29c7c59d2d49d8c79b1d29c5d49c3d49-8C94.c6b81C95.d2d49b8d79b1d29c8b79b3c29f8e89d2f19-8C92.c8b72d2d49f8e89b1d23e7f89-2f3g56e8f89g5f39f8e89f3g59-8f6d71d2d49-2f8e81-5C88.e8g83a2a41c8b79d2d39d7d69-4C89.c2c35d7d54e4d59f6d59f3e59c6e59e1e59c7c69d2d49e7d69e5e19-10C90.d7d65h2h39c6a59b3c29c7c59d2d49-7C88.d2d41-1h2h31c8b79d2d39-11C68.b5c61d7c69b1c31-1d2d41e5d49d1d49d8d49f3d49-5e1g17c8g42h2h39h7h59d2d39-4C69.d8d62-1f7f65d2d49c8g43d4e59d8d19f1d19-4e5d46f3d49c6c59d4b39d8d19f1d19-12C61.c6d41f3d49e5d49-3C62.d7d61d2d49-2C63.f7f51b1c36f5e49c3e49-3d2d33f5e49d3e49-4C64.f8c51c2c33-1e1g16-2C60.g7g61-1g8e71-1C65.g8f61d2d31d7d69-2e1g18C67.f6e48d2d49e4d69b5c69d7c69d4e59d6f59d1d89e8d89b1c39d8e89h2h39-12C65.f8c51c2c39-5C50.f1c41f8c54C51.b2b41c5b49c2c39-3C53.c2c35g8f69d2d35a7a63-1d7d66-2d2d44e5d49C54.c3d49c5b49b1c34-1c1d25-7C50.d2d31g8f69-2e1g11g8f69-3f8e71-1C55.g8f64d2d35f8c53c2c39-2f8e75e1g19e8g89f1e19d7d69-5h7h61-2C56.d2d41e5d49e1g14-1e4e55-3C57.f3g52d7d59e4d59C58.c6a59c4b59c7c69C59.d5c69b7c69-11C41.d7d61d2d48b8d72f1c49-2e5d45f3d49g8f69b1c39f8e79-5g8f62b1c39b8d79-4f1c41-2C40.f7f51-1C42.g8f61b1c31b8c66d2d44e5d49f3d49-3f1b55-2f8b43-2C43.d2d41f6e49f1d39d7d59f3e59b8d79e5d79c8d79e1g19-9C42.f3e56d7d69e5f39f6e49b1c31e4c39d2c39f8e79-4d1e22d8e79d2d39e4f69c1g59e7e29f1e29f8e79b1c39c7c69-10d2d46d6d59f1d39b8c64e1g19f8e79c2c49c6b49d3e29e8g89b1c39-8f8d63e1g19e8g89c2c49c7c69-5f8e72e1g19b8c69c2c49-14C00.e7e61b1c31d7d59-2d1e21c7c59-2d2d31c7c52g1f39b8c69g2g39-4d7d57b1d27c7c53g1f39b8c69g2g39-4g8f66g1f39b7b63-1b8c62-1c7c53g2g39b8c69f1g29-7d1e22-3d2d48c7c51-1d7d59C01.b1c34b8c61-1C10.d5e41c3e49b8d76g1f39g8f69e4f69d7f69-5c8d73g1f39d7c69f1d39b8d79-7C15.f8b45e4d51e6d59f1d39b8c69a2a39-5C16.e4e58b7b61-1C17.c7c57C18.a2a38b4a51b2b49c5d49c3b59a5c79-5C19.b4c38"


	c0_opn[10]="b2c39d8a51c1d29-2d8c72d1g44f7f59-2g1f35-2g8e76d1g46d8c74g4g79h8g89g7h79c5d49g1e29-6e8g85f1d39-3g1f33-5C17.c1d21g8e79-3C16.d8d71-1g8e71a2a39b4c39b2c39c7c59d1g49-7C15.g1e21d5e49a2a39b4e79-5C10.g8f63C11.c1g56C13.d5e43c3e49b8d73g1f39-2f8e76g5f69e7f65g1f39-2g7f64g1f39-6C12.f8b42e4e59h7h69g5d29b4c39b2c39f6e49d1g49g7g69f1d39e4d29e1d29c7c59-13C13.f8e73e4e59C14.f6d79g5e76d8e79f2f49a7a65g1f39c7c59-3e8g84g1f39-5h2h43-5C11.e4e53f6d79c3e21c7c59c2c39-3f2f48c7c59g1f39b8c69c1e39a7a64d1d29b7b59-3c5d45f3d49f8c59d1d29e8g89e1c19-15C03.b1d23a7a61g1f39c7c59-3C04.b8c61g1f39g8f69e4e59f6d79-5C07.c7c52e4d56d8d55g1f39c5d49f1c49d5d69e1g19g8f69d2b39b8c69b3d49c6d49f3d49a7a69-13C08.e6d54f1b53-1C09.g1f36b8c69f1b59f8d69-6C07.g1f33b8c63e4d59e6d59-3c5d44e4d59d8d59f1c49d5d69-5g8f62-3C03.d5e41d2e49b8d76g1f39g8f69e4f69d7f69-5c8d73g1f39d7c69f1d39b8d79-7f8e71f1d35c7c59d4c59g8f69d1e29-5g1f34g8f69-3C05.g8f64C06.e4e59f6d79c2c32c7c59f1d39b8c69g1e29c5d49c3d49f7f69e5f69d7f69-10f1d35c7c59c2c39b8c69g1e29c5d47c3d49f7f69e5f69d7f69d2f36f8d69e1g19-3e1g13f8d69d2f39-8d8b62d2f39c5d49c3d49f7f69-10f2f41c7c59c2c39b8c69d2f39d8b69-8C05.f1d31c7c59-4C01.e4d51e6d59c2c41g8f69-2f1d34b8c63c2c39f8d69-3f8d66g1f39-3g1f34f8d64c2c49-2g8f65f1d39-5C02.e4e51c7c59c2c39b8c67g1f39c8d74a2a33-1f1e26g8e79-3d8b64a2a35c5c49-2f1d31-1f1e22-2g8e71-3d8b62g1f39b8c64a2a39-2c8d75-4g1f31-5C00.g1f31d7d59b1c35g8f69e4e59f6d79d2d49c7c59d4c59-7e4e54c7c59b2b49-6A40.g7g61b1c31f8g79-2B06.d2d49c7c61-1d7d61b1c39f8g79-3f8g78b1c36c7c63c1e31-1f1c42d7d69-2f2f42d7d59e4e59-3g1f33d7d55-1d7d64-3d7d66c1e34a7a66d1d29-2c7c63d1d29-3f2f43g8f69g1f39e8g89-4g1f31-3c2c31d7d69-2c2c41d7d69b1c39-3f2f41-1g1f31d7d69b1c35-1f1c44-6B02.g8f61b1c31d7d58e4d54f6d59f1c49-3e4e55-2e7e51-2e4e58f6d59b1c31-1c2c41d5b69c4c53b6d59-2d2d46d7d69e5d69-5B03.d2d48d7d69c2c43d5b69e5d67c7d64b1c39g7g69-3e7d65b1c39f8e79-4f2f42d6e59f4e59-5B04.g1f36c8g45B05.f1e29c7c63-1e7e66e1g19f8e79c2c49d5b69-7B04.d6e52f3e59-2g7g62f1c49d5b69c4b39f8g79.A02.f2f41A03.d7d56g1f39g7g64-1g8f65-3A02.e7e51-1g8f61g1f39.A04.g1f31b7b61-1b8c61"


	c0_opn[11]="d2d49d7d59-3c7c51b2b31-1c2c46b8c64b1c35e7e53-1g7g66-2d2d43c5d49f3d49-3g2g31-2g7g62d2d49-2g8f63b1c37e7e69g2g39-3g2g32-3e2e41-1g2g32b8c67f1g29g7g69e1g19f8g79-5g7g62f1g29f8g79-5A06.d7d52b2b31c8g44-1g8f65c1b29-3A09.c2c42c7c64b2b32-1d2d42g8f69-2e2e34g8f69b1c39-4d5c41-1d5d41-1e7e63d2d43-1g2g36g8f69f1g29-5A06.d2d43c7c61c2c49e7e64-1g8f65-3e7e61c2c49-2g8f66c2c49c7c64b1c39-2d5c41e2e39-2e7e64b1c37f8e79-2g2g32-5e2e31-1A07.g2g33b8c61-1A08.c7c51f1g29b8c69-3A07.c7c62f1g29c8g47e1g19b8d79-3g8f62-3c8g41f1g29b8d79-3g7g61f1g29f8g79-3g8f63f1g29c7c65e1g19-2e7e64e1g19f8e79-7A04.d7d61d2d49c8g45-1g8f64-3e7e61c2c45-1g2g34-2f7f51c2c41g8f69-2d2d43g8f69-2g2g35g8f69f1g29g7g69-5g7g61c2c42f8g79b1c34-1d2d45-3d2d43f8g79c2c49-3e2e41f8g79d2d49d7d69-4g2g32f8g79f1g29-4A05.g8f64b2b31g7g69c1b29f8g79g2g39-5c2c45b7b61g2g39c8b79f1g29e7e69e1g19-6c7c51b1c37b8c64g2g39-2d7d52c4d59f6d59-3e7e62g2g39-3g2g32b7b69f1g29c8b79-5c7c61b1c34-1d2d45d7d59-3d7d61d2d49-2e7e62b1c34d7d55d2d49f8e79-3f8b44d1c29e8g89-4d2d41-1g2g34b7b63f1g29c8b79e1g19f8e79-5d7d56d2d42-1f1g27f8e79e1g19e8g89-7g7g63b1c36d7d52c4d59f6d59-3f8g77d2d41e8g89-2e2e47d7d69d2d49e8g89f1e29e7e59e1g19b8c69d4d59c6e79-10g2g31e8g89f1g29-5b2b31f8g79c1b29-3d2d41f8g79g2g39-3g2g32f8g79f1g29e8g89d2d42-1e1g17d7d69b1c34-1d2d45-9d2d41d7d52c2c49-2e7e63c2c49-2g7g64c2c49f8g79b1c39-5g2g32b7b51f1g29c8b79-3b7b61f1g29c8b79e1g19e7e69-5c7c51f1g29-2d7d52f1g29c7c67e1g19c8g49-3e7e62-3g7g65b2b32f8g79c1b29e8g89f1g29d7d69d2d49-7f1g27f8g79c2c41-1e1g18e8g89c2c43d7d69-2d2d33d7d54-1d7d65-2d2d43d7d69.A00.g2g31c7c51f1g29b8c69-3d7d53f1g26c7c64-1g8f65-2g1f33-2e7e51f1g29-2g7g61f1g29f8g79c2c49-4g8f62f1g29d7d55-1g7g64"


	def c0_Opening(c0_fmoves):

		global c0_opn
		
		c0_retdata=""

		c0_mvs=""
		c0_s=""
		c0_c=""

		c0_ECO=""
		c0_kf=""

		c0_i=0
		c0_j=0

		c0_pt=0
		c0_nm=0


		c0_NMoves=""
		c0_OName=""
		c0_op=""

		c0_i=1
		while( c0_i<12 ):

			c0_s=c0_opn[ c0_i ]
			c0_j=0
			while( c0_j<len(c0_s) ):

				c0_c=c0_s[c0_j: c0_j+1]			# Looking for special symbols or type of information...
				if(c0_c=="-"):					# Other variant...

					c0_j+=1
					c0_nm=0
					while( (c0_j+c0_nm<len(c0_s)) and (("0123456789").find(c0_s[c0_j+c0_nm:c0_j+c0_nm+1])>=0 ) ):

						c0_nm+=1


									# Next value is length for moves to shorten...
					c0_mvs=c0_mvs[0: len(c0_mvs)- (4*int( c0_s[c0_j:c0_j+c0_nm] )) ]
					c0_j+=c0_nm

				else:
					if(c0_c=="."):			# Will be other opening or variant...

						c0_j+=1
						c0_mvs=""

					else:
						if(("abcdefgh").find(c0_c)>=0):		# If it is a chess move...

							c0_mvs+=c0_s[c0_j:c0_j+4]
							c0_j+=4

						else:
							if(("0123456789").find(c0_c)>=0):	# If it is a coefficient (for best move searches)...

								c0_kf=c0_c
								if((len(c0_mvs)>len(c0_fmoves)) and (c0_mvs[0:len(c0_fmoves)]==c0_fmoves)):

									c0_next= c0_mvs[len(c0_fmoves):len(c0_fmoves)+4]

									if(c0_NMoves.find(c0_next)<0):
										c0_NMoves+=c0_next+" ("+c0_kf+") "

								c0_j+=1

							else:
										# Opening information... ECO code and name (Main name for x00)

								c0_ECO=c0_s[c0_j:c0_j+3]
								c0_j+=3
								c0_pt=0
								while( c0_s[c0_j+c0_pt:c0_j+c0_pt+1]!="." ):
									c0_pt+=1


								if((len(c0_mvs)<=len(c0_fmoves)) and (c0_fmoves[0:len(c0_mvs)]==c0_mvs)):

									if((len(c0_mvs)>len(c0_op)) and (len(c0_op)<len(c0_fmoves))):

										c0_op=c0_mvs
										c0_OName="ECO "+c0_ECO

								c0_j+=(c0_pt+1)


			c0_i+=1


						# Sorting by coeff. descending
		c0_i=1
		while(c0_i<10):

			c0_j=6
			while(c0_j<(len(c0_NMoves)-9)):

				c0_j+=9
				if( (int(c0_NMoves[c0_j:c0_j+1])==c0_i) and (int(c0_NMoves[c0_j:c0_j+1])>=int(c0_NMoves[6:6+1])) ):

					c0_NMoves=c0_NMoves[c0_j-6:c0_j-6+9]+c0_NMoves[0:c0_j-6]+c0_NMoves[c0_j-6+9:]

			c0_i+=1


		if( len(c0_NMoves)>0 ):
			c0_retdata=c0_NMoves + c0_OName

		return c0_retdata
	
	# END OF REMOVABLE OPENINGS DATABASE
	

	def c0_SAMPLES():		# Just samples...


		global c0_position, c0_side, c0_sidemoves, c0_moving
		global c0_wKingmoved, c0_bKingmoved, c0_wLRockmoved, c0_wRRockmoved, c0_bLRockmoved, c0_bRRockmoved, c0_w00, c0_b00
		global c0_lastmovepawn, c0_become, c0_become_from_engine, c0_moveslist
		global c0_start_FEN
		global c0_bestmove
	
		print("============================================")
		print("===== Routine of SAMPLES for chess logic ===")
		print("============================================")
 

		c0_side=1							# This side is white.   For black set -1
		c0_set_start_position("")			# Set the initial position... 
	
		# 1. Test for basic chess functions (ok)
		print( "Setting up the starting position" )
		c0_set_start_position("")
		print( c0_position )
		print( "FEN function : " + c0_get_FEN() )

		# Make a first move e4...
		c0_move_to("e2","e4")
		print( "Position after e4:")
		print( c0_position )
    
		# Show the last move made...
		print ( "Last move:" + c0_D_last_move_was() )

		# switch sides
		c0_sidemoves = -c0_sidemoves
		print ( "All movements till now:" + c0_moveslist )
    
		# To see possible movements...
		print( "Now possible moves:")
		print( c0_get_next_moves() )
    
		# And take it back...
		c0_take_back()
		print ( "Position after takeback" )
		print( c0_position )
		c0_sidemoves = -c0_sidemoves
  
		# Other functions:
		# Is e2-e4 a legal move in current position...
		print( "Can move a2-a4? ")
		print( c0_D_can_be_moved("a2","a4") )
    
		# Is there stalemate to the white king right now? ("b"/"w"- the parameter)
		print( "White king in stalemate? ")
		print( c0_D_is_pate_to_king("w") )
    
		# Is there check to the white king right now? 
		print( "Check to white king?")
		print( c0_D_is_check_to_king("w") )
    
		# Is there checkmate to the white king right now? 
		print( "Is checkmate to white king?")
		print( c0_D_is_mate_to_king("w") )
	
		# What a piece on the square g7?
		print( "Piece on g7:" + c0_D_what_at("g7") )
    
		# Is the square g6 empty? (no piece on it)
		print( "Is empty square g6? ")
		print( c0_D_is_empty("g6") )
    
		# FEN position setup test
		c0_start_FEN="7k/Q7/2P2K2/8/8/8/8/8 w - - 0 70"
		c0_set_start_position("");
		c0_set_FEN ("7k/Q7/2P2K2/8/8/8/8/8 w - - 0 70")
    
		print( "Position after setup FEN=7k/Q7/2P2K2/8/8/8/8/8 w - - 0 70")
		print( c0_position )

		c0_start_FEN=""
		c0_set_start_position("")

		# 2.PGN functions test (ok):
		print("PGN -> moves")
		PGN0="1.d4 d5 2.c4 e6 {comment goes here} 3.Nf3 Nf6 4.g3 Be7 (4.h4 or variant) 5.Bg2 0-0 6.0-0 dxc4 7.Qc2 a6 8.Qxc4 b5 9.Qc2 Bb7 10.Bd2 Be4 11.Qc1 Bb7 12.Qc2 Ra7 13.Rc1 Be4 14.Qb3 Bd5 15.Qe3 Nbd7 16.Ba5 Bd6 17.Nc3 Bb7 18.Ng5 Bxg2 19.Kxg2 Qa8+ 20.Qf3 Qxf3+ 21.Kxf3 e5 22.e3 Be7 23.Ne2 Re8 24.Kg2 Nd5 25.Nf3 Bd6 26.dxe5 Nxe5 27.Nxe5 Rxe5 28.Nd4 Ra8 29.Nc6 Re6 30.Rc2 Nb6 31.b3 Kf8 32.Rd1 Ke8 33.Nd4 Rf6 34.e4 Rg6 35.e5 Be7 36.Rxc7 Nd5 37.Rb7 Bd8 38.Nf5 Nf4+ 39.Kf3 Bxa5 40.gxf4 Bb4 41.Rdd7 Rc8 42.Rxf7 Rc3+ 43.Ke4 1-0"

		mlist0=c0_get_moves_from_PGN(PGN0)
		print (mlist0)

    
		print("moves -> PGN (reverse action)")
		print ( c0_put_to_PGN(mlist0) )
 
    
		# 3.Fischerrandom support test (ok):
		print("Fischer-random  PGN -> moves")
		PGN3='[Event "Champ Showdown 9LX 2020"][Site "lichess.org INT"][Date "2020.09.11"]';
		PGN3=PGN3+'[Round "1.5"][White "Vachier-Lagrave, Maxime"][Black "Carlsen, Magnus"]';
		PGN3=PGN3+'[Result "0-1"][Variant "Chess960"][SetUp "1"]';
		PGN3=PGN3+'[FEN "nnbrkqrb/pppppppp/8/8/8/8/PPPPPPPP/NNBRKQRB w GDgd - 0 1"]';
		PGN3=PGN3+'[WhiteTitle "GM"][BlackTitle "GM"][WhiteElo "2778"][BlackElo "2863"]';
		PGN3=PGN3+'[EventDate "2020.09.11"]';
		PGN3=PGN3+'1. e4 c5 2. Nb3 b6 3. Qe2 g6 4. O-O Ba6 5. d3 Nc6 6. g3 Nc7 7. Nc3 Bxc3 8. bxc3 g5 ';
		PGN3=PGN3+'9. f4 gxf4 10. Bxf4 Ne6 11. e5 Qg7 12. Rde1 Rh8 13. Qh5 c4 14. Nc1 cxd3 15.cxd3 Qg6 ';
		PGN3=PGN3+'16. Qd1 h5 17. Re3 h4 18. Ne2 O-O-O 19. d4 Na5 20. Be4 Qg7 21. Rf2 Rdg8 22. Bg2 Bb7 ';
		PGN3=PGN3+'23. d5 Nxf4 24. Rxf4 hxg3 25. hxg3 Kb8 26. Qd3 Qh7 27. Qxh7 Rxh7 28.Nc1 Rc8 29. Nb3 Nc4 ';
		PGN3=PGN3+'30. Re2 e6 31. d6 Rg7 32. Bxb7 Kxb7 33. Kg2 Rg5 34. Rfe4 Ka6 35. g4 b5 36. a4 bxa4 ';
		PGN3=PGN3+'37. Ra2 a3 38. Nd2 Nxd2 39. Rxa3+ Kb6 40. Rb4+ Kc6 41.Ra6+ Kd5 42. Ra5+ Rc5 43. Rd4+ Kc6 ';
		PGN3=PGN3+'44. Rxa7 Nc4 45. Rc7+ Kb5 46. Rxd7 Nxe5 47.Rb7+ Kc6 48. Rc7+ Kb6 49. Rb4+ Rb5 50. Rxb5+ Kxb5 ';
		PGN3=PGN3+'51. d7 Nxd7 52. Rxd7 Rxg4+ 53.Kf3 f5 54. Re7 Re4 55. Rc7 Rc4 56. Re7 Rxc3+ 57. Kf4 Rc4+ ';
		PGN3=PGN3+'58. Kf3 Re4 59. Rc7 e5 60. Rc8 Rc4 61. Re8 Rf4+ 62. Kg3 Re4 63. Kf3 Kc5 ';
		PGN3=PGN3+'64. Ra8 Kd5 65. Ra5+ Ke6 66.Ra6+ Ke7 0-1';
		mlist3= c0_get_moves_from_PGN(PGN3)
		print (mlist3)

		print("moves -> PGN (reverse action)")    
		print( c0_put_to_PGN(mlist3) )

		# clear it all
		c0_start_FEN=""
		c0_set_start_position("")
		print ("Starting position...")
   
		# There is also a simple chess search/position evaluation
		# algorithm written in python here, but it's weak.
		# Have to connect to UCI chess engines for serious chess
		# It's just a demo.
		
		c0_Simple_search(1)
		
		print ( "Search depth 1: " + c0_bestmove )

		# There is a short data openings database function
		print("Openings, variants on request: e2e4...")
		print( c0_Opening("e2e4") )
		
		print("On request: 1.d4 d5 2.c4...")
		print( c0_Opening("d2d4d7d5c2c4" ))
		
		print ("xexe");
		
		
#Call for samples demonstration function...
c0_SAMPLES();



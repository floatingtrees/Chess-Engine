# position_swapped finds the piece on a square, search square is the square that's being looked at
# white = True means that it's white to move; otherwise it's black
# in_check is a list that holds the square of the piece that's checking the king 
# row = True means that the program is searching on a row or column; otherwise it's searching a diagonal
# possibly pinned contains a piece that might be pinned; if pinned is True, possibly pinned gets appended to pinned
def in_check_from_square(position_swapped, search_square, white, in_check, possibly_pinned_pieces, row, pinned):
	if row and white: # no issues with this bloc
		piece_check = "r"
		piece_safe = 'b'
	elif row and not white:
		piece_check = "R"
		piece_safe = 'B'
	elif not row and not white:
		piece_check = "B"
		piece_safe = 'R'
	elif not row and white:
		piece_check = "b"
		piece_safe = 'r'
	# Color is no longer used past this point

	stop_searching_row = False 
	try:
		piece = position_swapped[search_square]
	except KeyError: # Exceptions are around the same speed as if key in dict
		pass
	else:
		if white:
			if piece[0] == "p" or piece[0]  == "n" or piece[0] == piece_safe:
				stop_searching_row = True
			elif piece[0]  == piece_check or piece[0] == "q":
				if len(possibly_pinned_pieces) == 0:
					in_check.append(search_square)
					stop_searching_row = True
				else:
					pinned = True
			else:
				possibly_pinned_pieces.append(piece)
		else:
			if piece[0] == "P" or piece[0] == "N" or piece[0]  == piece_safe:
				stop_searching_row = True
			elif piece[0] == piece_check or piece[0] == "Q":
				if len(possibly_pinned_pieces) == 0:
					in_check.append(search_square)
					stop_searching_row = True
				else:
					pinned = True
			else:
				possibly_pinned_pieces.append(piece)
		if len(possibly_pinned_pieces) > 1:
			stop_searching_row = True
	return in_check, stop_searching_row, possibly_pinned_pieces, pinned # 


def knight_checks_search(in_check, position_swapped, king_location_y, king_location_x, white):
	knightChecks = [[1, 2], [2, 1], [-1, 2], [-2, 1], [-1, -2], [-2, -1], [1, -2], [2, -1]]
	for i in knightChecks:
		try:
			piece = position_swapped[king_location_y + i[0], king_location_x + i[1]][0]
		except KeyError:
			pass 
		else:
			if white:
				if piece == "n":
					in_check.append((king_location_y + i[0], king_location_x + i[1]))
			else:
				if piece == "N":
					in_check.append((king_location_y + i[0], king_location_x + i[1]))
	return in_check

def pins_and_checks_search(position, position_swapped, white):
	pinned =  False
	in_check = []
	pinned_pieces = []
	possibly_pinned_pieces = []

	if white:
		king_location_y, king_location_x = position["K0"]
	else:
		king_location_y, king_location_x = position["k0"]

	in_check = knight_checks_search(in_check,  position_swapped, king_location_y, king_location_x, white)


	for i in range(1, 7): # + 0
		if king_location_y + i > 7:
			break
		search_square = (king_location_y + i, king_location_x) # row_search
		in_check, stop_searching_row, possibly_pinned_pieces, pinned = in_check_from_square(position_swapped, search_square, white, 
																		in_check, possibly_pinned_pieces, True, pinned)
		if pinned:
			pinned_pieces.append((possibly_pinned_pieces, search_square))
			pinned = False
			break
		if stop_searching_row:
			break
	possibly_pinned_pieces = []


	for i in range(1, 7): # 0 +
		if king_location_x + i > 7:
			break
		search_square = (king_location_y, king_location_x + i) # row_search
		in_check, stop_searching_row, possibly_pinned_pieces, pinned = in_check_from_square(position_swapped, search_square, white, 
																		in_check, possibly_pinned_pieces, True, pinned)
		if pinned:
			pinned_pieces.append((possibly_pinned_pieces, search_square))
			pinned = False
			break
		if stop_searching_row:
			break


	possibly_pinned_pieces = []
	for i in range(1, 7): # + + 
		if king_location_y + i > 7 or king_location_x + i > 7:
			break
		search_square = (king_location_y + 1, king_location_x + 1) # diagonal
		in_check, stop_searching_row, possibly_pinned_pieces, pinned = in_check_from_square(position_swapped, search_square, white, 
																		in_check, possibly_pinned_pieces, False, pinned)
		if pinned:
			pinned_pieces.append((possibly_pinned_pieces, search_square))
			pinned = False
			break
		if stop_searching_row:
			break
	possibly_pinned_pieces = []


	for i in range(1, 7): # - 0
		if king_location_y - i < 0:
			break
		search_square = (king_location_y - i, king_location_x) # row_search
		in_check, stop_searching_row, possibly_pinned_pieces, pinned = in_check_from_square(position_swapped, search_square, white, 
																		in_check, possibly_pinned_pieces, True, pinned)
		if pinned:
			pinned_pieces.append((possibly_pinned_pieces, search_square))
			pinned = False
			break
		if stop_searching_row:
			break
	possibly_pinned_pieces = []

	for i in range(1, 7): # 0 -, Problem here
		if king_location_x - i < 0:
			break
		search_square = (king_location_y, king_location_x - i) # row_search
		in_check, stop_searching_row, possibly_pinned_pieces, pinned = in_check_from_square(position_swapped, search_square, white, 
																		in_check, possibly_pinned_pieces, True, pinned)
		if pinned:
			pinned_pieces.append((possibly_pinned_pieces, search_square))
			pinned = False
			break
		if stop_searching_row:
			break
	possibly_pinned_pieces = []

	for i in range(1, 7): # - -
		if king_location_y - i < 0 or king_location_x - i < 0:
			break
		search_square = (king_location_y - i, king_location_x - i) # row_search
		in_check, stop_searching_row, possibly_pinned_pieces, pinned = in_check_from_square(position_swapped, search_square, white, 
																		in_check, possibly_pinned_pieces, False, pinned)
		if pinned:
			pinned_pieces.append((possibly_pinned_pieces, search_square))
			pinned = False
			break
		if stop_searching_row:
			break
	possibly_pinned_pieces = []

	for i in range(1, 7): # + -
		if king_location_y + i > 7 or king_location_x - i < 0:
			break
		search_square = (king_location_y + i, king_location_x - i) # row_search
		in_check, stop_searching_row, possibly_pinned_pieces, pinned = in_check_from_square(position_swapped, search_square, white, 
																		in_check, possibly_pinned_pieces, False, pinned)
		if pinned:
			pinned_pieces.append((possibly_pinned_pieces, search_square))
			pinned = False
			break
		if stop_searching_row:
			break
	possibly_pinned_pieces = []


	for i in range(1, 7): # - +
		if king_location_y - i < 0 or king_location_x + i > 7:
			break
		search_square = (king_location_y - i, king_location_x + i) # row_search
		in_check, stop_searching_row, possibly_pinned_pieces, pinned = in_check_from_square(position_swapped, search_square, white, 
																		in_check, possibly_pinned_pieces, False, pinned)
		if pinned:
			pinned_pieces.append((possibly_pinned_pieces, search_square))
			pinned = False
			break
		if stop_searching_row:
			break
	possibly_pinned_pieces = []


	print("pins: ", pinned_pieces, "checks: ", in_check)
	return pinned_pieces, in_check
	

def fancy_french_move(legal_moves, original_square, previous_move, white): # Moves are (piece, (prev_y, prev_x), (current_y, current_x))
	# works for all colors
	# previous move is a pawn move that went 2 squares forward the original square is on rank 3 or 4
	if previous_move[1][1] == original_square[1] + 1:
		if white:
			legal_moves.append(("P", original_square, (original_square[0]-1, original_square[1] + 1)))
		else:
			legal_moves.append(("p", original_square, (original_square[0]+1, original_square[1] - 1)))

	elif previous_move[1][1] == original_square[1] - 1:
		if white:
			legal_moves.append(("P", original_square, (original_square[0]-1, original_square[1] - 1))) #Squares are (y, x)
		else:
			legal_moves.append(("p", original_square, (original_square[0]+1, original_square[1] - 1)))
	return legal_moves



def w_pawn_capture_search(legal_moves, original_square, capture_square): # list, tuple, tuple
	try:
		movement_square_occupier = position_swapped[capture_square][0]
	except KeyError:
		pass
	else:
		legal_moves.append(('p', original_square, capture_square))
	return legal_moves



def w_pawn_legal_moves_search(legal_moves, position, position_swapped, piece, en_passant_maybe, previous_move): # list, dict, dict, str, bool
	piece_location = position[piece]
	piece_current_y = piece_location[0]
	piece_current_x = piece_location[1]
	if piece_current_y == 6:
		forward_squares = 3
	else:
		forward_squares = 2
	if en_passant_maybe and piece_current_y == 3:
		legal_moves = fancy_french_move(legal_moves, piece_location, previous_move, white = True)
	for i in range(1, forward_squares):
		try:
			movement_square_occupier = position_swapped[(piece_current_y - i, piece_current_x)][0]
		except KeyError:
			legal_moves.append((piece[0], (piece_current_y, piece_current_x), (piece_current_y - i, piece_current_x)))
		else:
			break
	for i in range(-1, 2, 2):
		legal_moves = w_pawn_capture_search(legal_moves, piece_location, (piece_current_y - 1, piece_current_x + i))
	return legal_moves



def w_knight_legal_moves_search(legal_moves, position, position_swapped, piece, en_passant_maybe, previous_move): 
	knight_moves = [[1, 2], [2, 1], [-1, 2], [-2, 1], [-1, -2], [-2, -1], [1, -2], [2, -1]]
	location = position[piece]
	for i in knight_moves:
		move_y = location[0] + i[0]
		move_x = location[1] + i[1]
		if move_x >= 0 and move_x <= 7 and move_y >= 0 and move_y <= 7:
			try:
				position_swapped[()] 




def legal_move_search(position, position_swapped, white, previous_move):
	pinned_pieces, in_check = pins_and_checks_search(position, position_swapped, white)
	legal_moves = []
	if white: 
		if previous_move[0] == "p" and previous_move[1][0] == 1 and previous_move[2][0] == 3: # Is fancy french possible
			en_passant_maybe = True
		else:
			en_passant_maybe = False
		for piece in position:
			if piece[0] == "P":
				legal_moves = w_pawn_legal_moves_search(legal_moves, position, position_swapped, piece, en_passant_maybe, previous_move)
			if piece[0] == "N":
				legal_moves = w_knight_legal_moves_search(legal_moves, position, position_swapped, piece, en_passant_maybe, previous_move)



	return legal_moves

	


if __name__ == "__main__":
	white = True
	# goes row (8-1), column (a-h) # q0 is pinning pawn to king, "q0":(4, 7)
	start_position = {"r0" : (0, 0), "n0" : (0, 1), "b0" : (0, 2), "q0":(0, 3), "k0" : (0, 4), "b1" : (0, 5), "n2": (0, 6), "r2":(0, 7), 
			"p0": (1, 0), "p1": (1, 1), "p2":(1, 2), "p3":(1, 3), "p4":(1, 4), "p5":(1, 5), "p6": (1, 6), "p7":(1, 7),
			"P0":(6, 0), "P1":(6, 1), "P2":(6, 2), "P3":(6, 3), "P4":(6, 4), "P5":(6, 5), "P6":(6, 6), "P7":(6, 7),
			"R0":(7, 0), "N0":(7, 1), "B0":(7, 2), "Q0":(7, 3), "K0":(7, 4), "B1":(7, 5), "N1":(7, 6), "R1":(7, 7)}
	previous_move = ("p", (1, 0), (3, 1))
	position_swapped = dict([(value, key) for key, value in start_position.items()])
	legal_moves = legal_move_search(start_position, position_swapped, white, previous_move)
	print(legal_moves)

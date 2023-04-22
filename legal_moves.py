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


	stop_searching_row = False 
	try:
		piece = position_swapped[search_square]
	except KeyError:
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



def pins_and_checks_search(position, position_swapped, white):
	pinned =  False
	in_check = []
	pinned_pieces = []
	possibly_pinned_pieces = []

	if white:
		king_location_y, king_location_x = position["K0"]
	else:
		king_location_y, king_location_x = position["k0"]


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
	return pinned_pieces, in_checkx
	

def pawn_capture_search(legal_moves, original_square, capture_square): # tuple, tuple
	try:
		movement_square_occupier = position_swapped[capture_square][0]
	except KeyError:
		legal_moves.append((original_square, capture_square))

def legal_move_search(position, position_swapped, white, white_pieces, black_pieces):
	pinned_pieces, in_check = pins_and_checks_search(position, position_swapped, white)
'''	legal_moves = []
	if white: 
		for piece in position:
			if piece[0] == "P":
				piece_location = position[piece]
				piece_current_y = piece_location[0]
				piece_current_x = piece_location[1]
				if piece_current_y == 6:
					forward_squares = 2
				for i in range(1, forward_squares):
					try:
						movement_square_occupier = position_swapped[(piece_current_y + i, piece_current_x)][0]
					except KeyError:
						legal_moves.append((current_position_y, current_position_x), (piece_current_y + i, piece_current_x))
					else:
						break
				for i in range(-1, 2, 2):
					pawn_capture_search(legal_moves, piece_location, '''


	


if __name__ == "__main__":
	white = True
	# goes row (8-1), column (a-h) # q0 is pinning pawn to king, "q0":(4, 7)
	start_position = {"r0" : (0, 0), "n0" : (0, 1), "b0" : (0, 2), "q0":(0, 3), "k0" : (0, 4), "b1" : (0, 5), "n2": (0, 6), "r2":(0, 7), 
			"p0": (1, 0), "p1": (1, 1), "p2":(1, 2), "p3":(1, 3), "p4":(1, 4), "p5":(1, 5), "p6": (1, 6), "p7":(1, 7),
			"P0":(6, 0), "P1":(6, 1), "P2":(6, 2), "P3":(6, 3), "P4":(6, 4), "P5":(6, 5), "P6":(6, 6), "P7":(6, 7),
			"R0":(7, 0), "N0":(7, 1), "B0":(7, 2), "Q0":(7, 3), "K0":(7, 4), "B1":(7, 5), "N1":(7, 6), "R1":(7, 7)}

	position_swapped = dict([(value, key) for key, value in start_position.items()])
	legal_move_search(start_position, position_swapped, white)

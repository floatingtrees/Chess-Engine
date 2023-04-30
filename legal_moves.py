# position_swapped finds the piece on a square, search square is the square that's being looked at
# white = True means that it's white to move; otherwise it's black
# in_check is a list that holds the square of the piece that's checking the king 
# row = True means that the program is searching on a row or column; otherwise it's searching a diagonal
# possibly pinned contains a piece that might be pinned; if pinned is True, possibly pinned gets appended to pinned

#Quiescence search captures can use (roughly) the same algorithm

import math
import time

global white_pieces
white_pieces = ("K", "Q", "R", "B", "N", "P", "O-O-O", "O-O")
global black_pieces
black_pieces = ("k", "q", "r", "b", "n", "p", "o-o-o", "o-o")

global bishop_moves
bishop_moves = ((1, 1), (1, -1), (-1, 1), (-1, -1))

global rook_moves
rook_moves = ((1, 0), (-1, 0), (0, 1), (0, -1))	

global knight_moves
knight_moves = ((1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (-2, -1), (1, -2), (2, -1))

global queen_moves
queen_moves = bishop_moves + rook_moves


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
	else:
		raise RuntimeError("piece_check and piece_safe were not able to be defined with row: %s and white: %s"%(row, white))
	# Color is no longer used past this point (in this function ofc)

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
					in_check.append(((search_square, piece_check)))
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
					in_check.append(((search_square), piece_check))
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
					in_check.append(((king_location_y + i[0], king_location_x + i[1]), "n"))
			else:
				if piece == "N":
					in_check.append(((king_location_y + i[0], king_location_x + i[1]), "N"))
	return in_check

def pins_and_checks_search(position, position_swapped, white, king_location_y, king_location_x):
	pinned =  False
	in_check = []
	pinned_pieces = []
	possibly_pinned_pieces = []

	in_check = knight_checks_search(in_check,  position_swapped, king_location_y, king_location_x, white)


	for directions in queen_moves:
		if directions[0] == 0 or directions[1] == 0:
			row = True
		else:
			row = False
		for move_length in range(1, 7): # + 0
			move_y = king_location_y + directions[0] * move_length
			move_x = king_location_x + directions[1] * move_length
			if 0 <= move_x <= 7 and 0 <= move_y <= 7:
				search_square = (move_y, move_x) # row_search
				in_check, stop_searching_row, possibly_pinned_pieces, pinned = in_check_from_square(position_swapped, search_square, white,
																				in_check, possibly_pinned_pieces, row, pinned)
				if pinned:
					pinned_pieces.append((possibly_pinned_pieces[0], search_square))
					pinned = False
					break
				if stop_searching_row:
					break
			else:
				break
		possibly_pinned_pieces = []

	if white:
		for i in range(-1, 2, 2):
			search_square_pawn = (king_location_y - 1, king_location_x + i)
			if search_square_pawn in position_swapped and position_swapped[search_square_pawn][0] == 'p':
				in_check.append((search_square_pawn, "p"))
	else:
		for i in range(-1, 2, 2):
			search_square_pawn = (king_location_y + 1, king_location_x + i)
			if search_square_pawn in position_swapped and position_swapped[search_square_pawn][0] == 'P':
				in_check.append((search_square_pawn, "P"))

	return pinned_pieces, in_check


def fancy_french_move(legal_moves, original_square, previous_move, white): # Moves are (piece, (prev_y, prev_x), (current_y, current_x))
	# works for all colors
	# previous move is a pawn move that went 2 squares forward the original square is on rank 3 or 4
	if previous_move[1][1] == original_square[1] + 1:
		if white:
			legal_moves.append(("P", original_square, (original_square[0]-1, original_square[1] + 1)))
			return legal_moves
		else:
			legal_moves.append(("p", original_square, (original_square[0]+1, original_square[1] + 1)))
			return legal_moves

	elif previous_move[1][1] == original_square[1] - 1:
		if white:
			legal_moves.append(("P", original_square, (original_square[0]-1, original_square[1] - 1))) #Squares are (y, x)
			return legal_moves
		else:
			legal_moves.append(("p", original_square, (original_square[0]+1, original_square[1] - 1)))
			return legal_moves
	return legal_moves


def w_pawn_capture_search(legal_moves, position_swapped, original_square, capture_square): # list, tuple, tuple
	if capture_square in position_swapped:
		movement_square_occupier = position_swapped[capture_square][0]
		if movement_square_occupier in black_pieces:
			legal_moves.append(('P', original_square, capture_square))
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
		legal_moves = w_pawn_capture_search(legal_moves, position_swapped, piece_location, (piece_current_y - 1, piece_current_x + i))
	return legal_moves

def b_pawn_capture_search(legal_moves, position_swapped, original_square, capture_square): # list, tuple, tuple
	if capture_square in position_swapped:
		movement_square_occupier = position_swapped[capture_square][0]
		if movement_square_occupier in white_pieces:
			legal_moves.append(('p', original_square, capture_square))

	return legal_moves


def b_pawn_legal_moves_search(legal_moves, position, position_swapped, piece, en_passant_maybe, previous_move): # list, dict, dict, str, bool
	piece_location = position[piece]
	piece_current_y = piece_location[0]
	piece_current_x = piece_location[1]
	if piece_current_y == 1:
		forward_squares = 3
	else:
		forward_squares = 2
	if en_passant_maybe and piece_current_y == 4:
		legal_moves = fancy_french_move(legal_moves, piece_location, previous_move, white = False)
	for i in range(1, forward_squares):
		if (piece_current_y + i, piece_current_x) not in position_swapped:
			legal_moves.append(("p", piece_location, (piece_current_y + i, piece_current_x)))
		else:
			break
	for i in range(-1, 2, 2):
		legal_moves = b_pawn_capture_search(legal_moves, position_swapped, piece_location, (piece_current_y + 1, piece_current_x + i))
	return legal_moves


def knight_legal_moves_search(legal_moves, position, position_swapped, piece, white): 
	if white:
		piece_type = "N"
	else:
		piece_type = "n"

	knight_moves = ((1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (-2, -1), (1, -2), (2, -1))
	location = position[piece]
	for i in knight_moves: # Don't break
		move_y = location[0] + i[0]
		move_x = location[1] + i[1]
		if 0 <= move_x <= 7 and 0 <= move_y <= 7:
			if (move_y, move_x) not in position_swapped:
				legal_moves.append((piece_type, location, (move_y, move_x)))
			else:
				if white:
					if piece[0] in white_pieces:
						pass
					else:
						legal_moves.append((piece_type, location, (move_y, move_x)))
				else:
					if piece[0] in black_pieces:
						pass
					else:
						legal_moves.append((piece_type, location, (move_y, move_x)))
	return legal_moves

def bishop_moves_search(legal_moves, position, position_swapped, piece, white):
	if white:
		piece_type = "B"
	else:
		piece_type = "b"


	location = position[piece]
	location_y = location[0]
	location_x = location[1]
	for direction in bishop_moves:
		for move_length in range(1, 8):
			move_y = location_y + direction[0] * move_length
			move_x = location_x + direction[1] * move_length
			if 0 <= move_x <= 7 and 0 <= move_y <= 7: # Use or because it's cheaper to eval
				if (move_y, move_x) not in position_swapped:
					legal_moves.append((piece_type, location, (move_y, move_x)))
				else:
					if white:
						if position_swapped[(move_y, move_x)][0] in white_pieces:
							break
						else:
							legal_moves.append((piece_type, location, (move_y, move_x)))
							break
					else:
						if position_swapped[(move_y, move_x)][0] in black_pieces:
							break
						else:
							legal_moves.append((piece_type, location, (move_y, move_x)))
							break
			else:
				break
	return legal_moves

def rook_moves_search(legal_moves, position, position_swapped, piece, white):
	if white:
		piece_type = "R"
	else:
		piece_type = "r"

	location = position[piece]
	location_y = location[0]
	location_x = location[1]
	for direction in rook_moves:
		for move_length in range(1, 8):
			move_y = location_y + direction[0] * move_length
			move_x = location_x + direction[1] * move_length
			if 0 <= move_x <= 7 and 0 <= move_y <= 7: # Use or because it's cheaper to eval
				if (move_y, move_x) not in position_swapped:
					legal_moves.append((piece_type, location, (move_y, move_x)))
				else:
					if white:
						if position_swapped[(move_y, move_x)][0] in white_pieces:
							break
						else:
							legal_moves.append((piece_type, location, (move_y, move_x)))
							break
					else:
						if position_swapped[(move_y, move_x)][0] in black_pieces:
							break
						else:
							legal_moves.append((piece_type, location, (move_y, move_x)))
							break
			else:
				break
	return legal_moves

def queen_moves_search(legal_moves, position, position_swapped, piece, white):
	if white:
		piece_type = "Q"
	else:
		piece_type = "q"

	location = position[piece]
	location_y = location[0]
	location_x = location[1]
	for direction in queen_moves:
		for move_length in range(1, 8):
			move_y = location_y + direction[0] * move_length
			move_x = location_x + direction[1] * move_length
			if 0 <= move_x <= 7 and 0 <= move_y <= 7: # Use or because it's cheaper to eval
				if (move_y, move_x) not in position_swapped:
					legal_moves.append((piece_type, location, (move_y, move_x)))
				else:
					if white:
						if position_swapped[(move_y, move_x)][0] in white_pieces:
							break
						else:
							legal_moves.append((piece_type, location, (move_y, move_x)))
							break
					else:
						if position_swapped[(move_y, move_x)][0] in black_pieces:
							break
						else:
							legal_moves.append((piece_type, location, (move_y, move_x)))
							break
			else:
				break
	return legal_moves

def king_moves_search(legal_moves, position, position_swapped, piece, white):
	if white:
		piece_type = "K"
	else:
		piece_type = "k"
	try:
		if white:
			king_location_y, king_location_x = position["K0"]
		else:
			king_location_y, king_location_x = position["k0"]
	except KeyError:
		print("KING NOT FOUND")


	location = position[piece]
	location_y = location[0]
	location_x = location[1]
	for direction in queen_moves:
		move_y = location_y + direction[0]
		move_x = location_x + direction[1]
		if 0 <= move_x <= 7 and 0 <= move_y <= 7:
			if position_swapped.get((move_y, move_x)) == None:
				moving_into_check = pins_and_checks_search(position, position_swapped, white, move_y, move_x)[1]
				if len(moving_into_check) == 0:
					legal_moves.append((piece_type, location, (move_y, move_x)))
			else:
				if white:
					if position_swapped[(move_y, move_x)][0] not in white_pieces:
						moving_into_check = pins_and_checks_search(position, position_swapped, white, move_y, move_x)[1]
						if len(moving_into_check) == 0:
							legal_moves.append((piece_type, location, (move_y, move_x)))
				else:
					if position_swapped[(move_y, move_x)][0] not in black_pieces:
						moving_into_check = pins_and_checks_search(position, position_swapped, white, move_y, move_x)[1]
						if len(moving_into_check) == 0:
							legal_moves.append((piece_type, location, (move_y, move_x)))
	# print("king: " + str(len(legal_moves)))
	return legal_moves

last_position_str = ""
def legal_move_search(position, position_swapped, white, previous_move, castling_kingside, castling_queenside): # If in check, only consider moves that end on top of the check square
	global last_position_str
	last_position_str = str(position) + "\n-----and-----\n" + str(position_swapped)
	try:
		if white:
			king_location_y, king_location_x = position["K0"]
		else:
			king_location_y, king_location_x = position["k0"]
	except KeyError:
		raise KeyError("KING NOT FOUND")
	pinned_pieces, in_check = pins_and_checks_search(position, position_swapped, white, king_location_y, king_location_x)
	legal_moves = []

	if len(in_check) == 2:
		legal_moves = king_moves_search(legal_moves, position, position_swapped, ["k0", "K0"][white], white)
		return legal_moves # king moves only if in double check

	else:
		if white:
			if previous_move[0] == "p" and previous_move[1][0] == 1 and previous_move[2][0] == 3: # Is fancy french possible
				en_passant_maybe = True
			else:
				en_passant_maybe = False

			if castling_kingside:
				if (7,5) not in position_swapped and (7, 4) not in position_swapped:
					legal_moves.append(("O-O", (7, 4), (7, 6)))
			if castling_queenside:
				if (7, 3) not in position_swapped and (7, 2) not in position_swapped and (7, 1) not in position_swapped:
					legal_moves.append(("O-O-O", (7, 4), (7, 2)))



			for piece in position:
				if piece[0] == "P":
					legal_moves = w_pawn_legal_moves_search(legal_moves, position, position_swapped, piece, en_passant_maybe, previous_move)
				elif piece[0] == "N":
					legal_moves = knight_legal_moves_search(legal_moves, position, position_swapped, piece, white)
				elif piece[0] == "B":
					legal_moves = bishop_moves_search(legal_moves, position, position_swapped, piece, white) # Captures not working
				elif piece[0] == "R":
					legal_moves = rook_moves_search(legal_moves, position, position_swapped, piece, white)
				elif piece[0] == "Q":
					legal_moves = queen_moves_search(legal_moves, position, position_swapped, piece, white)
				elif piece[0] == "K":
					legal_moves = king_moves_search(legal_moves, position, position_swapped, piece, white)

		else: # elif black
			if previous_move[0] == "P" and previous_move[1][0] == 6 and previous_move[2][0] == 4:
				en_passant_maybe = True
			else:
				en_passant_maybe = False


			if castling_kingside:
				if (0, 5) not in position_swapped and (0, 4) not in position_swapped:
					legal_moves.append(("o-o", (0, 4), (0, 6)))
			if castling_queenside:
				if (0, 3) not in position_swapped and (0, 2) not in position_swapped and (0, 1) not in position_swapped:
					legal_moves.append(("o-o-o", (0, 4), (0, 2)))


			for piece in position:
				if piece[0] == "p":
					legal_moves = b_pawn_legal_moves_search(legal_moves, position, position_swapped, piece, en_passant_maybe, previous_move)
				elif piece[0] == "n":
					legal_moves = knight_legal_moves_search(legal_moves, position, position_swapped, piece, white)
				elif piece[0] == "b":
					legal_moves = bishop_moves_search(legal_moves, position, position_swapped, piece, white) # Captures not working
				elif piece[0] == "r":
					legal_moves = rook_moves_search(legal_moves, position, position_swapped, piece, white)
				elif piece[0] == "q":
					legal_moves = queen_moves_search(legal_moves, position, position_swapped, piece, white)
				elif piece[0] == "k":
					legal_moves = king_moves_search(legal_moves, position, position_swapped, piece, white)
		# print("all legal moves: " + str(len(legal_moves)))

	# for loop to check for pawn promotions
	if len(in_check) == 1: # returns forced_moves instead of legal_moves
		if white:
			in_check = in_check[0]
			forced_moves = []

			checking_piece = in_check[1] # Don't need the [0] after because in_check[1] is 1 character

			checking_square_y = in_check[0][0]
			checking_square_x = in_check[0][1]

			square_distance = (checking_square_y - king_location_y, checking_square_x - king_location_x)
			square_distance_max = max(abs(checking_square_y - king_location_y), abs(checking_square_x - king_location_x))
			direction_y = square_distance[0] // square_distance_max
			direction_x = square_distance[1] // square_distance_max

			if checking_piece == "n":
				for move in legal_moves:
					if move[0] == "K":
						forced_moves.append(move)
					elif move[2] == in_check[0]:
						forced_moves.append(move)

			elif checking_piece == "b":
				for i in range(1, square_distance_max + 1):
					move_y = king_location_y + i * direction_y
					move_x = king_location_x + i * direction_x
					for move in legal_moves:
						if move[2] == (move_y, move_x) or move[0] == "K":
							forced_moves.append(move)

			elif checking_piece == "r":
				for i in range(1, square_distance_max + 1):
					move_y = king_location_y + i * direction_y
					move_x = king_location_x + i * direction_x
					for move in legal_moves:
						if move[2] == (move_y, move_x) or move[0] == "K":
							forced_moves.append(move)

			elif checking_piece == "p":
				for move in legal_moves:
					if move[0] == "K" or move[2] == (in_check[0]):
						forced_moves.append(move)

			else:
				print("Error")
		else:
			in_check = in_check[0]
			forced_moves = []

			checking_piece = in_check[1] # Don't need the [0] after because in_check[1] is 1 character

			checking_square_y = in_check[0][0]
			checking_square_x = in_check[0][1]

			square_distance = (checking_square_y - king_location_y, checking_square_x - king_location_x)
			square_distance_max = max(abs(checking_square_y - king_location_y), abs(checking_square_x - king_location_x))
			direction_y = square_distance[0] // square_distance_max
			direction_x = square_distance[1] // square_distance_max

			if checking_piece == "N":
				for move in legal_moves:
					if move[0] == "k":
						forced_moves.append(move)
					elif move[2] == in_check[0]:
						forced_moves.append(move)

			elif checking_piece == "B":
				for i in range(1, square_distance_max + 1):
					move_y = king_location_y + i * direction_y
					move_x = king_location_x + i * direction_x
					for move in legal_moves:
						if move[2] == (move_y, move_x) or move[0] == "k":
							forced_moves.append(move)

			elif checking_piece == "R":
				for i in range(1, square_distance_max + 1):
					move_y = king_location_y + i * direction_y
					move_x = king_location_x + i * direction_x
					for move in legal_moves:
						if move[2] == (move_y, move_x) or move[0] == "k":
							forced_moves.append(move)

			elif checking_piece == "P":
				for move in legal_moves:
					if move[0] == "k" or move[2] == (in_check[0]):
						forced_moves.append(move)

			else:
				print("Error")
		# if len(forced_moves) == 0:
		# 	print(legal_moves)
		legal_moves = forced_moves

	if len(pinned_pieces) >= 1:
		pinned_legal_moves = []
		for pin in pinned_pieces:
			piece = pin[0]
			location = position[piece]
			for move in legal_moves:
				if move[1] == location:

					dist_y = pin[1][0] - king_location_y
					dist_x = pin[1][1] - king_location_x
					pin_distance_max = max(abs(dist_y), abs(dist_x))
					dist_y_unit = dist_y//pin_distance_max
					dist_x_unit = dist_x//pin_distance_max

					for i in range(1, pin_distance_max + 1):
						move_y = king_location_y + i * dist_y_unit
						move_x = king_location_x + i * dist_x_unit
						if move[2] == (move_y, move_x):
							pinned_legal_moves.append(move)
				else:
					pinned_legal_moves.append(move)
		return pinned_legal_moves

	#print("all legal moves afterwards: " + str(len(legal_moves)))

	return legal_moves

#testing only
if __name__ == "__main__":
	white = False
	# goes row (8-1), column (a-h) # q0 is pinning pawn to king, "q0":(4, 7)
	# start_position = {"r0" : (0, 0), "n0" : (0, 1), "b0" : (0, 2), "q0":(0, 3), "k0" : (0, 4), "b1" : (0, 5), "n2": (0, 6), "r2":(0, 7), 
	# 		"p0": (1, 0), "p1": (1, 1), "p2":(1, 2), "p3":(1, 3), "p4":(1, 4), "p5":(1, 5), "p6": (1, 6), "p7":(1, 7),
	# 		"P0":(6, 0), "P1":(6, 1), "P2":(6, 2), "P3":(6, 3), "P4":(6, 4), "P5":(6, 5), "P6":(6, 6), "P7":(6, 7),
	# 		"R0":(7, 0), "N0":(7, 1), "B0":(7, 2), "Q0":(7, 3), "K0":(7, 4), "B1":(7, 5), "N1":(7, 6), "R1":(7, 7)}
	start_position = {'k0': (4, 5), 'K0': (7, 4), 'N0': (7, 1), 'r0': (0, 0), 'R1': (5, 5), 'N1': (7, 6), 'n0': (0, 1), 'B1': (5, 7), 'b0': (0, 2), 'R0': (7, 0), 'b1': (5, 0), 'Q0': (1, 6)}

	previous_move = ("Q", (-1, -1), (-1, -1))
	position_swapped = dict([(value, key) for key, value in start_position.items()])

	start = time.time()
	legal_moves = legal_move_search(start_position, position_swapped, white, previous_move, True, True)
	
	# testing code below
	# search_pieces = ["R"]
	# printed_list = []
	# for i in legal_moves:
	# 	for j in search_pieces:
	# 		if i[0] == j:
	# 			printed_list.append(i)
	# print(start_position)
	# print(position_swapped)
	print(legal_moves)
	print(time.time() - start)

	# make sure no global variables are accidentally modified
	assert white_pieces == ("K", "Q", "R", "B", "N", "P", "O-O-O", "O-O"), "White pieces changed"
	assert black_pieces == ("k", "q", "r", "b", "n", "p", "o-o-o", "o-o"), "Black pieces changed"
	assert rook_moves == ((1, 0), (-1, 0), (0, 1), (0, -1)), "Rook moves changed"
	assert bishop_moves == ((1, 1), (1, -1), (-1, 1), (-1, -1)), "Bishop moves changed"
	assert knight_moves == ((1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (-2, -1), (1, -2), (2, -1)), "Knight moves changed"
	assert queen_moves == bishop_moves + rook_moves, "Queen moves changed"





"""start_position = {"r0" : (0, 0), "n0" : (0, 1), "b0" : (0, 2), "q0":(0, 3), "k0" : (0, 4), "b1" : (0, 5), "n2": (0, 6), "r2":(0, 7), 
			"p0": (1, 0), "p1": (1, 1), "p2":(1, 2), "p3":(1, 3), "p4":(1, 4), "p5":(1, 5), "p6": (1, 6), "p7":(1, 7),
			"P0":(6, 0), "P1":(6, 1), "P2":(6, 2), "P3":(6, 3), "P4":(6, 4), "P5":(6, 5), "P6":(6, 6), "P7":(6, 7),
			"R0":(7, 0), "N0":(7, 1), "B0":(7, 2), "Q0":(7, 3), "K0":(7, 4), "B1":(7, 5), "N1":(7, 6), "R1":(7, 7)}"""

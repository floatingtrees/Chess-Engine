'''
This is the file for the main recursive algorithm that looks through all possible moves using Alpha-Beta Pruning.
'''

import legal_moves
import evaluate
import random
import primitive_evaluate


#if transform piece the moved piece changes into the new transform_piece
def move_position(position, position_swapped, initial, final, transform_piece=None, captured_piece=None, french_captured=None, depth=-1):
	french_capture = None
	french_captured_position = None

	# print(f"initial:{position}")
	# print(f"{initial} and {final}, depth={depth}")

	#fancy-baguette-move
	if position_swapped.get(final) == None and initial[1] != final[1] and ((position_swapped[initial][0] == "P" and initial[0] == 3 and final[0] == 2) or (position_swapped[initial][0] == "p" and initial[0] == 4 and final[0] == 5)):
		french_capture = position_swapped[(initial[0], final[1])]
		french_captured_position = (initial[0], final[1])

		# raise Exception(f"fancy french time! {(french_capture, french_captured_position)}")
		
		del position[position_swapped[(initial[0], final[1])]]
		del position_swapped[(initial[0], final[1])]

		assert position_swapped == dict([(value, key) for key, value in position.items()]), f"assertion: position={position}, reversed={position_swapped}, initial={initial}, final={final}, captured_piece={captured_piece}, french={french_captured}"
	
	# elif french_captured != (None, None) and french_captured != None:
	elif captured_piece == None and initial[1] != final[1] and ((position_swapped[initial][0] == "P" and initial[0] == 2 and final[0] == 3) or (position_swapped[initial][0] == "p" and initial[0] == 5 and final[0] == 4)):
		#NOTE: in order for the pawns to work without having to be named specifically 0-7 in the correct order, french_capture was made
		# position[french_captured[0]] = french_captured[1]
		# position_swapped[french_captured[1]] = french_captured[0]

		if position_swapped[initial][0] == "P":
			#we're using the fact that pawn p1 is on x=1 and can't have moved files
			position["p" + str(initial[1])] = (initial[0] + 1, initial[1])
			position_swapped[(initial[0] + 1, initial[1])] = "p" + str(initial[1])

			
		else: #black pawn
			position["P" + str(initial[1])] = (initial[0] - 1, initial[1])
			position_swapped[(initial[0] - 1, initial[1])] = "P" + str(initial[1])
		# print("its rewind time")

		assert position_swapped == dict([(value, key) for key, value in position.items()]), f"assertion: position={position}, reversed={position_swapped}, initial={initial}, final={final}, captured_piece={captured_piece}, french={french_captured}"

	#captured piece, remove from position dictionary
	# try:
	if position_swapped.get(final) != None:
		# print(position_swapped)
		del position[position_swapped.get(final)]
		del position_swapped[final]

	# except Exception as e:
	# 	raise Exception(f"error: {position} and \n{position_swapped}, initial={initial}, final={final}")

	#autoqueen
	try:
		if (position_swapped[initial][0] == "p" or position_swapped[initial][0] == "P") and (final[0] == 0 or final[0] == 7):
			if position_swapped[initial][0] == "p":
				transform_piece = "q" + position_swapped[initial]
			else:
				transform_piece = "Q" + position_swapped[initial]
	except Exception as e:
		raise Exception(f"error 2: {position} and \n{position_swapped}, initial={initial}, final={final}")


	#castling
	if abs(final[1] - initial[1]) == 2 and position_swapped[initial][0] == "k" or position_swapped[initial][0] == "K":
		if position_swapped[initial][0] == "k":
			#black queenside castling
			if initial[1] == 4 and final[1] == 2:
				#move rook (bottom code deals with king)
				move_position(position, position_swapped, (0, 0), (0, 3), depth=depth)
			elif initial[1] == 2 and final[1] == 4:
				#rewind rook
				move_position(position, position_swapped, (0, 3), (0, 0), depth=depth)
			#black kingside castling
			elif initial[1] == 4 and final[1] == 6:
				#move rook
				move_position(position, position_swapped, (0, 7), (0, 5), depth=depth)
			elif initial[1] == 6 and final[1] == 4:
				#rewind rook
				move_position(position, position_swapped, (0, 5), (0, 7), depth=depth)
		elif position_swapped[initial][0] == "K":
			#white queenside castling
			if initial[1] == 4 and final[1] == 2:
				#move rook (bottom code deals with king)
				move_position(position, position_swapped, (7, 0), (7, 3), depth=depth)
			elif initial[1] == 2 and final[1] == 4:
				#rewind rook
				move_position(position, position_swapped, (7, 3), (7, 0), depth=depth)
			#white kingside castling
			elif initial[1] == 4 and final[1] == 6:
				#move rook
				move_position(position, position_swapped, (7, 7), (7, 5), depth=depth)
			elif initial[1] == 6 and final[1] == 4:
				#rewind rook
				move_position(position, position_swapped, (7, 5), (7, 7), depth=depth)

		position[position_swapped[initial]] = final
		position_swapped[final] = position_swapped[initial]
		del position_swapped[initial]
	elif transform_piece != None:
		del position[position_swapped[initial]]
		del position_swapped[initial]
		position_swapped[final] = transform_piece
		position[transform_piece] = final
	else:
		piece = position_swapped[initial]
		position[piece] = final
		position_swapped[final] = piece
		del position_swapped[initial]
	
	return (french_capture, french_captured_position)
	# print(f"final: {position}")

#if old_piece is not None, the initial position's old_piece is put back
def rewind_position(position, position_swapped, initial, final, old_piece, old_other_piece=None, french_captured=None):
	move_position(position, position_swapped, initial, final, captured_piece=old_piece, transform_piece=old_other_piece, french_captured=french_captured)
	if old_piece != None:
		position[old_piece] = initial
		position_swapped[initial] = old_piece

last_position = None
def alphabeta(position, position_swapped, alpha, beta, white=True, depth=0, max_depth=4, previous_moves=[("K", (-1, -1), (-1, -1))], can_castle=[True, True, True, True], sort=False):  # castling: white king, white queen, black king, black queen
	if depth == max_depth:
		return primitive_evaluate.evaluate(position)

	if not sort and depth == 0:
		move_dict = alphabeta(position, position_swapped, alpha, beta, white, max_depth=2, previous_moves=previous_moves, can_castle=can_castle, sort=True)
		if move_dict == 0:
			raise Exception("stalemate")
		# print(move_dict)
		sorted_position = [x[0] for x in sorted(move_dict.items(), key=lambda x: x[1], reverse=white)]
		# print(sorted_position)
	if sort:
		value_list = {}

	# stalemate
	if len(previous_moves) >= 6 and previous_moves[-1] == previous_moves[-5] and previous_moves[-2] == previous_moves[-6]:
		# print("stalemate!")
		return 0

	#white is maximize
	elif white:
		val = -99999
		best_move = None
		if not sort and depth == 0:
			legal_move_list = sorted_position
		else:
			legal_move_list = legal_moves.legal_move_search(position, position_swapped, True, previous_moves[-1], can_castle[0], can_castle[1])
		# print(f"current white parent search: {position}, can_castle: {can_castle}")
		for move in legal_move_list:
			# print(f"white move found: {move}")
			#tries to get the piece that might be captured
			old_piece = position_swapped.get(move[2])
			#pre-promotion pawn
			old_other_piece = position_swapped.get(move[1])

			#king taken, value is maximum
			if old_piece != None and "k" in old_piece:
				#print(f"black king taken, {old_piece}")
				val = 95000 - depth
				best_move = move
				if sort:
					value_list[move] = val
			
			if val < 90000:
				#if just castled when rewinding castling needs to be set to true again
				delta_king_castle = can_castle[0]
				delta_queen_castle = can_castle[1]

				# print(move)
				if move[0][0] == "R" and move[1] == (7, 7):
					can_castle[0] = False
				elif move[0][0] == "R" and move[1] == (7, 0):
					can_castle[1] = False
				elif move[0][0] == "O" or move[0][0] == "K":
					can_castle[0] = False
					can_castle[1] = False

				#make the move
				french_captured = move_position(position, position_swapped, move[1], move[2], depth=depth)
				previous_moves.append(move)

				new_val = alphabeta(position, position_swapped, alpha, beta, False, depth + 1, max_depth, previous_moves, can_castle)
				if sort:
					value_list[move] = new_val
					best_move = move
				else:
					rand = random.randint(0, 2)
					if new_val >= val or rand == 0 and new_val == val:
						val = new_val
						best_move = move

				# print(f"rewinding {move[2]}, {move[1]}")
				#retract the move
				rewind_position(position, position_swapped, move[2], move[1], old_piece, old_other_piece, french_captured=french_captured)
				previous_moves.pop()

				#rewind castle
				can_castle[0] = delta_king_castle
				can_castle[1] = delta_queen_castle

			if val > beta:
				break
			alpha = max(alpha, val)

		#only return the best move if it's the first layer (return to function call)
		if depth == 0:
			if best_move == None:
				raise Exception(f"no legal moves available—-stalemate? Position: {position}")
			if sort:
				return value_list
			return best_move
		elif best_move == None:
			#stalemated
			return 0
		return val
	else:
		val = 99999
		best_move = None

		if not sort and depth == 0:
			legal_move_list = sorted_position
		else:
			legal_move_list = legal_moves.legal_move_search(position, position_swapped, False, previous_moves[-1], can_castle[2], can_castle[3])
		#print(f"current black parent search: {position}, can_castle: {can_castle}")
		for move in legal_move_list:
			#print(f"black move found: {move}")
			#tries to get the piece that might be captured
			old_piece = position_swapped.get(move[2])
			#pre-promotion pawn
			old_other_piece = position_swapped.get(move[1])

			if best_move == None:
				best_move = move

			#king taken, value is maximum
			if old_piece != None and "K" in old_piece:
				#print(f"white king taken, {old_piece}")
				val = -95000 + depth
				best_move = move
				if sort:
					value_list[move] = val

			if val > -90000:
				#if just castled when rewinding castling needs to be set to true again
				delta_king_castle = can_castle[2]
				delta_queen_castle = can_castle[3]

				if move[0][0] == "r" and move[1] == (0, 7):
					can_castle[2] = False
				elif move[0][0] == "r" and move[1] == (0, 0):
					can_castle[3] = False
				elif move[0][0] == "o" or move[0][0] == "k":
					can_castle[2] = False
					can_castle[3] = False

				#make the move
				french_captured = move_position(position, position_swapped, move[1], move[2], depth=depth)
				# print(previous_moves)
				previous_moves.append(move)
				new_val = alphabeta(position, position_swapped, alpha, beta, True, depth + 1, max_depth, previous_moves, can_castle)
				if sort:
					value_list[move] = new_val
					best_move = move
				else:
					rand = random.randint(0, 2)
					if new_val < val or rand == 0 and new_val == val:
						val = new_val
						best_move = move

				# print(f"rewinding {move[2]}, {move[1]}")
				#retract the move
				rewind_position(position, position_swapped, move[2], move[1], old_piece, old_other_piece, french_captured=french_captured)
				previous_moves.pop()

				#rewind castle
				can_castle[2] = delta_king_castle
				can_castle[3] = delta_queen_castle

			if val < alpha:
				break
			beta = min(beta, val)
		
		if depth == 0:
			if best_move == None:
				raise Exception(f"no legal moves available—-stalemate? Position: {position}")
			if sort:
				return value_list
			return best_move
		elif best_move == None:
			#stalemated
			return 0
		return val

#temporary move search
if __name__ == "__main__":
	position = {"r0" : (0, 0), "n0" : (0, 1), "b0" : (0, 2), "q0":(0, 3), "k0" : (0, 4), "b1" : (0, 5), "n2": (0, 6), "r2":(0, 7), 
			"p0": (1, 0), "p1": (1, 1), "p2":(1, 2), "p3":(1, 3), "p4":(1, 4), "p5":(1, 5), "p6": (1, 6), "p7":(1, 7),
			"P0":(6, 0), "P1":(6, 1), "P2":(6, 2), "P3":(6, 3), "P4":(6, 4), "P5":(6, 5), "P6":(6, 6), "P7":(6, 7),
			"R0":(7, 0), "N0":(7, 1), "B0":(7, 2), "Q0":(7, 3), "K0":(7, 4), "B1":(7, 5), "N1":(7, 6), "R1":(7, 7)}
	# position = {"P0" : (4, 0), "k0" : (0, 4), 
	# 		"p1":(4, 1), "K0":(7, 4)}

	position_swapped = dict([(value, key) for key, value in position.items()])

	# testing
	# old_piece = None#position_swapped.get((0, 4))
	# old_other_piece = None#position_swapped.get((1, 0))
	# print(f"before moving: {position} and {position_swapped}")
	# move_position(position, position_swapped, (4, 1), (5, 0))
	# print(f"after one move: {position} and {position_swapped}")
	# rewind_position(position, position_swapped, (5, 0), (4, 1), old_piece, old_other_piece)
	# print(f"after one rewind: {position} and {position_swapped}")

	previous_moves = [("K", (-1, -1), (-1, -1))]
	# can_castle = [True, True, True, True]
	can_castle = [False, False, False, False]

	# take turns
	for i in range(200):
		# try:
			# print("before move: " + str(position))
		# print(previous_moves)
		#pass

		depth = 3
		if len(position) < 5:
			depth = 5
		elif len(position) < 9:
			depth = 4

		move = alphabeta(position, position_swapped, -99999, 99999, white=(i % 2 == 0), max_depth=depth, can_castle=can_castle, previous_moves=previous_moves)
		if move[0][0] == "r" and move[1] == (0, 7):
			can_castle[2] = False
		elif move[0][0] == "r" and move[1] == (0, 0):
			can_castle[3] = False
		elif move[0][0] == "o" or move[0][0] == "k":
			can_castle[2] = False
			can_castle[3] = False
		if move[0][0] == "R" and move[1] == (7, 7):
			can_castle[0] = False
		elif move[0][0] == "R" and move[1] == (7, 0):
			can_castle[1] = False
		elif move[0][0] == "O" or move[0][0] == "K":
			can_castle[0] = False
			can_castle[1] = False

		print(f"{move[1][1]}{7 - move[1][0]}{move[2][1]}{7 - move[2][0]}")
		move_position(position, position_swapped, move[1], move[2])
		previous_moves.append(move)

		# except Exception as e:
		# 	print(e)
		# 	print("-------exception-------")
		# 	print(evaluate.last_position)
		# 	break
		



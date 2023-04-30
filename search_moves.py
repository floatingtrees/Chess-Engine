'''
This is the file for the main recursive algorithm that looks through all possible moves using Alpha-Beta Pruning.
'''

import legal_moves
import evaluate
import random

#if transform piece the moved piece changes into the new transform_piece
def move_position(position, position_swapped, initial, final, transform_piece=None):
	#captured piece, remove from position dictionary
	if position_swapped.get(final) != None:
		del position[position_swapped.get(final)]

	#autoqueen
	if (position_swapped[initial][0] == "p" or position_swapped[initial][0] == "P") and (final[0] == 0 or final[0] == 7):
		if position_swapped[initial][0] == "p":
			transform_piece = "q" + position_swapped[initial]
		else:
			transform_piece = "Q" + position_swapped[initial]

	if transform_piece != None:
		del position[position_swapped[initial]]
		del position_swapped[initial]
		position_swapped[final] = transform_piece
		position[transform_piece] = final
	else:
		piece = position_swapped[initial]
		position[piece] = final

		position_swapped[final] = piece
		del position_swapped[initial]

#if old_piece is not None, the initial position's old_piece is put back
def rewind_position(position, position_swapped, initial, final, old_piece, old_other_piece=None):
	move_position(position, position_swapped, initial, final, old_other_piece)
	if old_piece != None:
		position[old_piece] = initial
		position_swapped[initial] = old_piece



last_position = None
def alphabeta(position, position_swapped, alpha, beta, white=True, depth=0, max_depth=4, previous_move=("K", (-1, -1), (-1, -1))):
	if depth == max_depth:
		return evaluate.evaluate(position)

	#white is maximize
	if white:
		val = -99999
		best_move = None
		for move in legal_moves.legal_move_search(position, position_swapped, True, previous_move, False, False):
			#tries to get the piece that might be captured
			old_piece = position_swapped.get(move[2])
			#pre-promotion pawn
			old_other_piece = position_swapped.get(move[1])

			#king taken, value is maximum
			if old_piece != None and "k" in old_piece:
				#print(f"black king taken, {old_piece}")
				val = 90000
				best_move = move

			
			if val < 90000:
				#make the move
				move_position(position, position_swapped, move[1], move[2])
				
				rand = random.randint(0, 2)
				new_val = alphabeta(position, position_swapped, alpha, beta, False, depth + 1, max_depth)#, move)
				if new_val >= val or rand == 0 and new_val == val:
					val = new_val
					best_move = move

				#retract the move
				rewind_position(position, position_swapped, move[2], move[1], old_piece, old_other_piece)

			if val > beta:
				break
			alpha = max(alpha, val)

		#only return the best move if it's the first layer (return to function call)
		if depth == 0:
			if best_move == None:
				raise Exception(f"no legal moves available—-stalemate? Position: {position}")
			return best_move
		return val
	else:
		val = 99999
		best_move = None

		count = 0
		for move in legal_moves.legal_move_search(position, position_swapped, False, previous_move, False, False):
			count += 1
			#tries to get the piece that might be captured
			old_piece = position_swapped.get(move[2])
			#pre-promotion pawn
			old_other_piece = position_swapped.get(move[1])

			if best_move == None:
				best_move = move

			#king taken, value is maximum
			if old_piece != None and "K" in old_piece:
				#print(f"white king taken, {old_piece}")
				val = -90000
				best_move = move

			if val > -90000:
				#make the move
				move_position(position, position_swapped, move[1], move[2])
				new_val = alphabeta(position, position_swapped, alpha, beta, True, depth + 1, max_depth)#, move)
				rand = random.randint(0, 2)
				if new_val < val or rand == 0 and new_val == val:
					val = new_val
					best_move = move

				#retract the move
				rewind_position(position, position_swapped, move[2], move[1], old_piece, old_other_piece)

			if val < alpha:
				break
			beta = min(beta, val)
		
		if depth == 0:
			# if count == 1:
			# 	print("forced move by black")
			if best_move == None:
				raise Exception(f"no legal moves available—-stalemate? Position: {position}")
			return best_move
		return val

#temporary move search
if __name__ == "__main__":
	position = {"r0" : (0, 0), "n0" : (0, 1), "b0" : (0, 2), "q0":(0, 3), "k0" : (0, 4), "b1" : (0, 5), "n2": (0, 6), "r2":(0, 7), 
			"p0": (1, 0), "p1": (1, 1), "p2":(1, 2), "p3":(1, 3), "p4":(1, 4), "p5":(1, 5), "p6": (1, 6), "p7":(1, 7),
			"P0":(6, 0), "P1":(6, 1), "P2":(6, 2), "P3":(6, 3), "P4":(6, 4), "P5":(6, 5), "P6":(6, 6), "P7":(6, 7),
			"R0":(7, 0), "N0":(7, 1), "B0":(7, 2), "Q0":(7, 3), "K0":(7, 4), "B1":(7, 5), "N1":(7, 6), "R1":(7, 7)}

	position_swapped = dict([(value, key) for key, value in position.items()])

	# testing
	# old_piece = position_swapped.get((5, 0))
	# old_other_piece = position_swapped.get((1, 0))
	# print(f"before moving: {position}")
	# move_position(position, position_swapped, (1, 0), (5, 0))
	# print(f"after one move: {position}")
	# rewind_position(position, position_swapped, (5, 0), (1, 0), old_piece, old_other_piece)
	# print(f"after one rewind: {position}")

	# take turns
	for i in range(200):
		# try:
			# print("before move: " + str(position))
		move = alphabeta(position, position_swapped, -99999, 99999, white=(i % 2 == 0), max_depth=3 + i % 2)
		print(f"{move[1][1]}{7 - move[1][0]}{move[2][1]}{7 - move[2][0]}")
		move_position(position, position_swapped, move[1], move[2])
		# except Exception as e:
		# 	print(e)
		# 	print("-------exception-------")
		# 	print(evaluate.last_position)
		# 	break
		



'''
This is the file for the main recursive algorithm that looks through all possible moves using Alpha-Beta Pruning.
'''

import legal_moves
import evaluate

#legal_moves.legal_move_search(position, position_swapped, white, previous_move, castling_kingside, castling_queenside):
#NOTE: in the framework for alphabeta, position_swapped, previous_move, and castling_kingside and castling_queenside are ignored since they should be part of the position dictionary

def evaluate_position(position);
	return 10 #should return the difference in white pieces and black pieces; put this in a separate namespace

def move_position(position, position_swapped, piece, initial, final):
	piece = legal_moves.position_swapped[initial];
	legal_moves.position

def alphabeta(position, position_swapped, alpha, beta, maximizing, depth=0, max_depth=5):
	if depth == max_depth:
		return evaluate_position(position)

	#white is maximize
	if maximizing:
		val = -999
		for move in legal_moves.legal_move_search(position, True):
			#make the move, NOTE: position is not stored as array but as dictionary for white/black pieces, which is rather problematic for
			#position[move[1][0], move[1][1]] = something
			val = max(val, alphabeta(position, position_swapped, alpha, beta, False, depth + 1, max_depth))
			#retract the move
			#position[move[1][0], move[1][1]] = old thing

			if val > beta:
				break
			alpha = max(alpha, val)

		return val
	else:
		val = 999
		for move in legal_moves.legal_move_search(position, False):
			#make the move, NOTE: position is not stored as array but as dictionary for white/black pieces, which is rather problematic for
			#position[move[1][0], move[1][1]] = something
			val = min(val, alphabeta(position, position_swapped, alpha, beta, True, depth + 1, max_depth))
			#retract the move
			#position[move[1][0], move[1][1]] = old thing

			if val < alpha:
				break
			beta = min(beta, val)

		return val
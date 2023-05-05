import piece_squares

global center_squares

center_squares = {(3, 3), (3, 4), (4, 3), (4, 4)}
outer_center_squares = {(2, 2), (2, 3), (2, 4), (2, 5), (5, 5), (5, 4), (5, 3), (5, 2), (3, 2), (3, 5), (4, 2), (4, 2)}

piece_square_values = {"P": 0, "N": 1, "B": 2, "R": 3, "Q": 4, "K": 5, "p": -1, "n": -2, "b": -3, "r": -4, "q": -5, "k": -6}

material_dict = {"P": 0, "N": 781, "B": 825, "R": 1276, "Q": 2538, "K": 0, "p": 0, "n": 781, "b": 825, "r": 1276, "q": 2538, "k": 0}

midgame_values = [126, 781, 825, 1276, 2538, 0]
endgame_values = [208, 854, 915, 1380, 2682, 0]

def evaluate(position):
	items = position.items()
	score = 0
	material_sum = 0
	for (key, val) in items: # Ignore pawns for calculating game stage
		material_sum += material_dict[key[0]]

		
	if material_sum > 15258:
		piece_vals = midgame_values
		opening = True
		endgame_index = 0
		eg_square_vals = False

	elif material_sum < 3915:
		piece_vals = endgame_values
		opening = False
		endgame_index = 1
		eg_square_vals = True
	else:
		endgame_index = (material_sum - 3915) / 11343
		#pawn, knight, bishop, rook, queen, king
		piece_vals = [midgame_values[0] + (endgame_values[0]-midgame_values[0]) * endgame_index,
					  midgame_values[1] + (endgame_values[1]-midgame_values[1]) * endgame_index,
					  midgame_values[2] + (endgame_values[2]-midgame_values[2]) * endgame_index,
					  midgame_values[3] + (endgame_values[3]-midgame_values[3]) * endgame_index,
					  midgame_values[4] + (endgame_values[4]-midgame_values[4]) * endgame_index,
					  0]
		opening = False
		eg_square_vals = False

	for (key, val) in items:
		piece = key[0]
		piece_square_val = piece_square_values[piece]
		row = val[0]
		col = val[1]
		if piece_square_val < 0:
			if piece_square_val == -1:
				score -= piece_vals[0] + piece_squares.pawn_square_vals[row][col][eg_square_vals]
				#print(piece_squares.pawn_square_vals[row][col][eg_sqaure_vals])
			else:
				#print(piece_squares.piece_square_vals[-1 * (piece_square_val + 1)][row][col if col < 4 else (7 - col)][eg_sqaure_vals], key)
				score -= piece_vals[-1 * (piece_square_val + 1)] + piece_squares.piece_square_vals[-1 * (piece_square_val + 1)][row][col if col < 4 else (7 - col)][eg_square_vals]
		elif piece_square_val == 0:
			score += piece_vals[0] + piece_squares.pawn_square_vals[7 - row][col][eg_square_vals]
			#print(piece_squares.pawn_square_vals[7 - row][col][eg_sqaure_vals], key)
		else:
			score += piece_vals[piece_square_val] + piece_squares.piece_square_vals[piece_square_val][7 - row][col if col < 4 else (7 - col)][eg_square_vals]
			#print(piece_squares.piece_square_vals[piece_square_val][7 - row][col if col < 4 else (7 - col)][eg_sqaure_vals], key)

	return score


def time_test(starting_position):


	import timeit
	from legal_moves import legal_move_search

	times = []

	for i in range(10):
		starttime = timeit.default_timer()
		previous_move = ("P", (6, 4), (4, 4))
		position_swapped = dict([(value, key) for key, value in starting_position.items()])
		for j in range(10000):
			legal_move_search(starting_position, position_swapped, True, previous_move, True, True)
			#evaluate(starting_position)
		times.append(timeit.default_timer() - starttime)
	print(sum(times) / len(times))

#testing only
if __name__ == '__main__':
	starting_position = {"r0": (0, 0), "n0": (0, 1), "b0": (0, 2), "q0": (0, 3), "k0": (0, 4), "b1": (0, 5), "n2": (0, 6), "r2": (0, 7),
		 "p0": (1, 0), "p1": (1, 1), "p2": (1, 2), "p3": (1, 3), "p4": (1, 4), "p5": (1, 5), "p6": (1, 6), "p7": (1, 7),
		 "P0": (6, 0), "P1": (6, 1), "P2": (6, 2), "P3": (6, 3), "P4": (6, 4), "P5": (6, 5), "P6": (6, 6), "P7": (6, 7),
		 "R0": (7, 0), "N0": (7, 1), "B0": (7, 2), "Q0": (7, 3), "K0": (7, 4), "B1": (7, 5), "N1": (7, 6),
		 "R1": (7, 7)}
	#score = evaluate(starting_position)
	#print(score)
	time_test(starting_position)

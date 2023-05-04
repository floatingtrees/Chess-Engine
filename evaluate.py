global center_squares

center_squares = {(3, 3), (3, 4), (4, 3), (4, 4)}
outer_center_squares = {(2, 2), (2, 3), (2, 4), (2, 5), (5, 5), (5, 4), (5, 3), (5, 2), (3, 2), (3, 5), (4, 2), (4, 2)}

material_dict = {"P": 0, "N": 781, "B": 825, "R": 1276, "Q": 2538, "K": 0, "p": 0, "n": 781, "b": 825, "r": 1276, "q": 2538, "k": 0}

midgame_values = [126, 781, 825, 1276, 2538]
endgame_values = [208, 854, 915, 1380, 2682]

def evaluate(position):
	items = position.items()
	score = 0
	material_sum = 0
	for (key, val) in items: # Ignore pawns for calculating game stage
		material_sum += material_dict[key[0]]
		# piece = key[0]
		# if piece == "N":
		# 	material_sum += 781
		# elif piece == "B":
		# 	material_sum += 825
		# elif piece == "R":
		# 	material_sum += 1276
		# elif piece == "Q":
		# 	material_sum += 2538
		# elif piece == "n":
		# 	material_sum += 781
		# elif piece == "b":
		# 	material_sum += 825
		# elif piece == "r":
		# 	material_sum += 1276
		# elif piece == "q":
		# 	material_sum += 2538

	if material_sum > 15258:
		pawn_value, knight_value, bishop_value, rook_value, queen_value = midgame_values
		opening = True
		endgame_index = 0

	elif material_sum < 3915:
		pawn_value, knight_value, bishop_value, rook_value, queen_value = endgame_values
		opening = False
		endgame_index = 1
	else:
		endgame_index = (material_sum - 3915) / 11343
		values = []
		pawn_value = midgame_values[0] + (endgame_values[0]-midgame_values[0]) * endgame_index
		knight_value = midgame_values[1] + (endgame_values[1]-midgame_values[1]) * endgame_index
		bishop_value = midgame_values[2] + (endgame_values[2]-midgame_values[2]) * endgame_index
		rook_value = midgame_values[3] + (endgame_values[3]-midgame_values[3]) * endgame_index
		queen_value = midgame_values[4] + (endgame_values[4]-midgame_values[4]) * endgame_index
		opening = False

	promotion_value = bishop_value / 1.5

	for (key, val) in items:
		piece = key[0]
		if piece == "P":
			score += pawn_value
			if opening:
				if val in center_squares:
					score += 300
				elif val in outer_center_squares:
					score += 150
			else:
				score += promotion_value / (val[0] + 1) * (1-endgame_index)
		elif piece == "N":
			score += knight_value
			if opening:
				if val in center_squares:
					score += 300
				elif val in outer_center_squares:
					score += 150 
				elif val == (7, 1) or val == (7, 6):
					score -= 75
		elif piece == "B":
			score += bishop_value
			if opening:
				if val in center_squares:
					score += 250
				elif val in outer_center_squares:
					score += 225
				elif val == (7, 2) or val == (7, 5):
					score -= 75
		elif piece == "R":
			score += rook_value
			if opening:
				if val in center_squares:
					score += 40
				elif val in outer_center_squares:
					score += 40
		elif piece == "Q":
			score += queen_value
			if opening:
				if val in center_squares:
					score += 40
				elif val in outer_center_squares:
					score += 40
		elif piece == "p":
			score -= pawn_value
			if opening:
				if val in center_squares:
					score -= 300
				elif val in outer_center_squares:
					score -= 150
			else:
				score -= promotion_value / (8-val[0]) * (1-endgame_index)
		elif piece == "n":
			score -= knight_value
			if opening:
				if val in center_squares:
					score -= 300
				elif val in outer_center_squares:
					score -= 150
				elif val == (0, 1) or val == (0, 6):
					score += 75
		elif piece == "b":
			score -= bishop_value
			if opening:
				if val in center_squares:
					score -= 250
				elif val in outer_center_squares:
					score -= 225
				elif val == (0, 2) or val == (0, 5):
					score += 75
		elif piece == "r":
			score -= rook_value
			if opening:
				if val in center_squares:
					score -= 40
				elif val in outer_center_squares:
					score -= 40
		elif piece == "q":
			score -= queen_value
			if opening:
				if val in center_squares:
					score -= 40
				elif val in outer_center_squares:
					score -= 40
		elif piece == "k":
			if opening:
				if val == (0, 6) or val == (0, 2):
					score -= 100
		elif piece == "K":
			if opening:
				if val == (7, 6) or val == (7, 2):
					score += 100

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


global center_squares
center_squares = {(3, 3), (3, 4), (4, 3), (4, 4)}
outer_center_squares = {(2, 2), (2, 3), (2, 4), (2, 5), (5, 5), (5, 4), (5, 3), (5, 2), (3, 2), (3, 5), (4, 2), (4, 2)}

midgame_values = [126, 781, 825, 1276, 2538]
endgame_values = [208, 854, 915, 1380, 2682]

def evaluate(position):
	score = 0
	material_sum = 0
	for key, val in position: # Ignore pawns for calculating game stage
		if key[0] == "N":
			material_sum += 781
		elif key[0] == "B":
			material_sum += 825
		elif key[0] == "R":
			material_sum += 1276
		elif key[0] == "Q":
			material_sum += 2538
		elif key[0] == "n":
			material_sum += 781
		elif key[0] == "b":
			material_sum += 825
		elif key[0] == "r":
			material_sum += 1276
		elif key[0] == "q":
			material_sum += 2538

		if material_sum > 15258:
			pawn_value, knight_value, bishop_value, rook_value, queen_value = midgame_values
		elif material_sum < 3915:
			pawn_value, knight_value, bishop_value, rook_value, queen_value = endgame_values
		else:
			values = []
			pawn_value = midgame_values[0] + ((endgame_values[0]-midgame_values[0]) * (material_sum - 3915)) / 11343
			knight_value = midgame_values[1] + ((endgame_values[1]-midgame_values[1]) * (material_sum - 3915)) / 11343
			bishop_value = midgame_values[2] + ((endgame_values[2]-midgame_values[2]) * (material_sum - 3915)) / 11343

			rook_value = midgame_values[3] + ((endgame_values[3]-midgame_values[3]) * (material_sum - 3915)) / 11343
			queen_value = midgame_values[4] + ((endgame_values[4]-midgame_values[4]) * (material_sum - 3915)) / 11343



		for key, val in position:
			if key[0] == "P":
				score += pawn_value
				if val in center_squares:
					score += 175
				elif val in outer_center_squares:
					score += 150
			elif key[0] == "N":
				score += knight_value
				if val in center_squares:
					score += 300
				elif val in outer_center_squares:
					score += 200
			elif key[0] == "B":
				score += bishop_value
				if val in center_squares:
					score += 150
				elif val in outer_center_squares:
					score += 125
			elif key[0] == "R":
				score += rook_value
				if val in center_squares:
					score += 40
				elif val in outer_center_squares:
					score += 40
			elif key[0] == "Q":
				score += queen_value
				if val in center_squares:
					score += 40
				elif val in outer_center_squares:
					score += 40
			elif key[0] == "p":
				score -= pawn_value
				if val in center_squares:
					score -= 175
				elif val in outer_center_squares:
					score -= 150
			elif key[0] == "n":
				score -= knight_value
				if val in center_squares:
					score -= 300
				elif val in outer_center_squares:
					score -= 200
			elif key[0] == "b":
				score -= bishop_value
				if val in center_squares:
					score -= 150
				elif val in outer_center_squares:
					score -= 120
			elif key[0] == "r":
				score -= rook_value
				if val in center_squares:
					score -= 40
				elif val in outer_center_squares:
					score -= 40
			elif key[0] == "q":
				score -= queen_value
				if val in center_squares:
					score -= 40
				elif val in outer_center_squares:
					score -= 40

	return score

if __name__ == '__main__':
	score = evaluate({"r0" : (0, 0), "n0" : (0, 1), "b0" : (0, 2), "q0":(0, 3), "k0" : (0, 4), "b1" : (0, 5), "n2": (0, 6), "r2":(0, 7), 
			"p0": (1, 0), "p1": (1, 1), "p2":(1, 2), "p3":(1, 3), "p4":(1, 4), "p5":(1, 5), "p6": (1, 6), "p7":(1, 7),
			"P0":(6, 0), "P1":(6, 1), "P2":(6, 2), "P3":(6, 3), "P4":(6, 4), "P5":(6, 5), "P6":(6, 6), "P7":(6, 7),
			"R0":(7, 0), "N0":(7, 1), "B0":(7, 2), "Q0":(7, 3), "K0":(7, 4), "B1":(7, 5), "N1":(7, 6), "R1":(7, 7)})
	print(score)

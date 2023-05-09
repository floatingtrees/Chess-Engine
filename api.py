import timeit

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
import uvicorn
import search_moves
import json

app = FastAPI()
origins = ["*"]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


position = {"r0" : (0, 0), "n0" : (0, 1), "b0" : (0, 2), "q0":(0, 3), "k0" : (0, 4), "b1" : (0, 5), "n2": (0, 6), "r2":(0, 7), 
			"p0": (1, 0), "p1": (1, 1), "p2":(1, 2), "p3":(1, 3), "p4":(1, 4), "p5":(1, 5), "p6": (1, 6), "p7":(1, 7),
			"P0":(6, 0), "P1":(6, 1), "P2":(6, 2), "P3":(6, 3), "P4":(6, 4), "P5":(6, 5), "P6":(6, 6), "P7":(6, 7),
			"R0":(7, 0), "N0":(7, 1), "B0":(7, 2), "Q0":(7, 3), "K0":(7, 4), "B1":(7, 5), "N1":(7, 6), "R1":(7, 7)}
position_swapped = dict([(value, key) for key, value in position.items()])
can_castle = [True, True, True, True]

previous_moves = [("K", (-1, -1), (-1, -1))]

def update_castling(move):
	global can_castle
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
		print("castled!")
		can_castle[0] = False
		can_castle[1] = False

@app.get("/make_move_web")
async def make_move_web(player_move: str, castled: str, board_position: str):
	previous_moves = []
	javascript_position = json.loads(board_position)
	can_castle = json.loads(castled)
	print(can_castle)

	new_position_swapped = {}
	new_position = {}

	#literally just assign incrementally on a first-come-first-serve-basis (screws up fancy frog moves but idc)
	
	#pawn, knight, bishop, rook, queen
	white_pieces_count = [8, 0, 0, 0, 0]
	black_pieces_count = [8, 0, 0, 0, 0]

	for i in range(8):
		for j in range(8):
			piece = javascript_position[i][j]["piece"]
			if piece == "wpawn":
				if j == 1: #must be identical to number
					piece = f"P{i}"
				else:
					piece = f"P{white_pieces_count[0]}"
					white_pieces_count[0] += 1
			elif piece == "wknight":
				piece = f"N{white_pieces_count[1]}"
				white_pieces_count[1] += 1
			elif piece == "wbishop":
				piece = f"B{white_pieces_count[2]}"
				white_pieces_count[2] += 1
			elif piece == "wrook":
				piece = f"R{white_pieces_count[3]}"
				white_pieces_count[3] += 1
			elif piece == "wqueen":
				piece = f"Q{white_pieces_count[4]}"
				white_pieces_count[4] += 1
			elif piece == "wking":
				piece = "K0"

			if piece == "bpawn":
				if j == 6: #must be identical to number
					piece = f"p{i}"
				else:
					piece = f"p{black_pieces_count[0]}"
					black_pieces_count[0] += 1
			elif piece == "bknight":
				piece = f"n{black_pieces_count[1]}"
				black_pieces_count[1] += 1
			elif piece == "bbishop":
				piece = f"b{black_pieces_count[2]}"
				black_pieces_count[2] += 1
			elif piece == "brook":
				piece = f"r{black_pieces_count[3]}"
				black_pieces_count[3] += 1
			elif piece == "bqueen":
				piece = f"q{black_pieces_count[4]}"
				black_pieces_count[4] += 1
			elif piece == "bking":
				piece = "k0"

			if piece != None:
				new_position_swapped[(7 - j, i)] = piece
				new_position[piece] = (7 - j, i)

	move_pos = ((7 - int(player_move[1]), int(player_move[0])), (7 - int(player_move[3]), int(player_move[2])))
	move = (new_position_swapped[move_pos[0]][0], move_pos[0], move_pos[1])
	search_moves.move_position(new_position, new_position_swapped, move[1], move[2])
	previous_moves.append(move)

	start_time = timeit.default_timer()
	depth = 4

	move = search_moves.alphabeta(new_position, new_position_swapped, -99999, 99999, white=False, max_depth=depth, previous_moves=previous_moves, can_castle=can_castle)
	
	search_moves.move_position(position, position_swapped, move[1], move[2])
	update_castling(move)
	
	print(f"returned {move[1][1]}{7 - move[1][0]}{move[2][1]}{7 - move[2][0]}")
	print(f"time taken: {timeit.default_timer() - start_time} on depth {depth} with move")

	return f"{move[1][1]}{7 - move[1][0]}{move[2][1]}{7 - move[2][0]}"

@app.get("/make_move")
async def make_move(player_move: str):
	global position
	global position_swapped
	global previous_moves
	global can_castle

	# print(f"moved {player_move}")

	move_pos = ((7 - int(player_move[1]), int(player_move[0])), (7 - int(player_move[3]), int(player_move[2])))
	move = (position_swapped[move_pos[0]][0], move_pos[0], move_pos[1])
	search_moves.move_position(position, position_swapped, move[1], move[2])
	update_castling(move)
	previous_moves.append(move)

	start_time = timeit.default_timer()
	depth = 4
	original_move = "None"
	depth_5_moves = False
	# print(f"position: {position}, castling: {can_castle}")
	move = search_moves.alphabeta(position, position_swapped, -99999, 99999, white=False, max_depth=depth, previous_moves=previous_moves, can_castle=can_castle)
	if (timeit.default_timer() - start_time) < 1 and depth_5_moves:
		original_move = move
		depth += 1
		move = search_moves.alphabeta(position, position_swapped, -99999, 99999, white=False, max_depth=depth, previous_moves=previous_moves, can_castle=can_castle)
	search_moves.move_position(position, position_swapped, move[1], move[2])
	update_castling(move)
	previous_moves.append(move)
	
	print(f"returned {move[1][1]}{7 - move[1][0]}{move[2][1]}{7 - move[2][0]}")
	print(f"time taken: {timeit.default_timer() - start_time} on depth {depth} with move {move} and original move {original_move}")

	return f"{move[1][1]}{7 - move[1][0]}{move[2][1]}{7 - move[2][0]}"

uvicorn.run(app, port=8080, host="0.0.0.0")
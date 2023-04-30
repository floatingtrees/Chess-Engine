from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
import uvicorn
import search_moves

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

@app.get("/make_move")
async def make_move(player_move: str):
	global position
	global position_swapped

	print(f"moved {player_move}")

	search_moves.move_position(position, position_swapped, (7 - int(player_move[1]), int(player_move[0])), (7 - int(player_move[3]), int(player_move[2])))
	move = search_moves.alphabeta(position, position_swapped, -99999, 99999, white=False, max_depth=4)
	search_moves.move_position(position, position_swapped, move[1], move[2])
	
	print(f"returned {move[1][1]}{7 - move[1][0]}{move[2][1]}{7 - move[2][0]}")

	return f"{move[1][1]}{7 - move[1][0]}{move[2][1]}{7 - move[2][0]}"

uvicorn.run(app, port=8080, host="0.0.0.0")
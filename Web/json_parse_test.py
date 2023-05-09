import json

data = """[[{"position":[0,0],"piece":"wrook"},{"position":[0,1],"piece":"wpawn"},{"position":[0,2],"piece":null},{"position":[0,3],"piece":null},{"position":[0,4],"piece":null},{"position":[0,5],"piece":null},{"position":[0,6],"piece":"bpawn"},{"position":[0,7],"piece":"brook"}],[{"position":[1,0],"piece":"wknight"},{"position":[1,1],"piece":"wpawn"},{"position":[1,2],"piece":null},{"position":[1,3],"piece":null},{"position":[1,4],"piece":null},{"position":[1,5],"piece":null},{"position":[1,6],"piece":"bpawn"},{"position":[1,7],"piece":"bknight"}],[{"position":[2,0],"piece":"wbishop"},{"position":[2,1],"piece":"wpawn"},{"position":[2,2],"piece":null},{"position":[2,3],"piece":null},{"position":[2,4],"piece":null},{"position":[2,5],"piece":null},{"position":[2,6],"piece":"bpawn"},{"position":[2,7],"piece":"bbishop"}],[{"position":[3,0],"piece":"wqueen"},{"position":[3,1],"piece":"wpawn"},{"position":[3,2],"piece":null},{"position":[3,3],"piece":null},{"position":[3,4],"piece":null},{"position":[3,5],"piece":null},{"position":[3,6],"piece":"bpawn"},{"position":[3,7],"piece":"bqueen"}],[{"position":[4,0],"piece":"wking"},{"position":[4,1],"piece":"wpawn"},{"position":[4,2],"piece":null},{"position":[4,3],"piece":null},{"position":[4,4],"piece":null},{"position":[4,5],"piece":null},{"position":[4,6],"piece":"bpawn"},{"position":[4,7],"piece":"bking"}],[{"position":[5,0],"piece":"wbishop"},{"position":[5,1],"piece":"wpawn"},{"position":[5,2],"piece":null},{"position":[5,3],"piece":null},{"position":[5,4],"piece":null},{"position":[5,5],"piece":null},{"position":[5,6],"piece":"bpawn"},{"position":[5,7],"piece":"bbishop"}],[{"position":[6,0],"piece":"wknight"},{"position":[6,1],"piece":"wpawn"},{"position":[6,2],"piece":null},{"position":[6,3],"piece":null},{"position":[6,4],"piece":null},{"position":[6,5],"piece":null},{"position":[6,6],"piece":"bpawn"},{"position":[6,7],"piece":"bknight"}],[{"position":[7,0],"piece":"wrook"},{"position":[7,1],"piece":"wpawn"},{"position":[7,2],"piece":null},{"position":[7,3],"piece":null},{"position":[7,4],"piece":null},{"position":[7,5],"piece":null},{"position":[7,6],"piece":"bpawn"},{"position":[7,7],"piece":"brook"}]]"""

board = json.loads(data)
print(board[0][3]["piece"])
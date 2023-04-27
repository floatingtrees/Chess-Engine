const canvas = document.getElementById("gameCanvas");
const canvasCtx = canvas.getContext("2d");

canvas.addEventListener("mousedown", mouseDown, false);

//from https://stackoverflow.com/questions/3684285/how-to-prevent-text-select-outside-html5-canvas-on-double-click
canvas.onselectstart = function () { return false; }

const lightTile = "#EDE7DD";
const darkTile = "#70AF73";
const highlightedTile = "#F2B64E";

class Tile {
	constructor(position, piece) {
		this.position = position;
		this.piece = piece;
	}
}
class Board {
	constructor() {
		this.positions = [];
		for (let i = 0; i < 8; i++) {
			this.positions.push([]);
			for (let j = 0; j < 8; j++) {
				this.positions[i].push(new Tile([i, j], null));
			}
		}
	}
}

const initialPieces = [
	//row is 0=a, etc
	[0, 0, "wrook"], [1, 0, "wknight"], [2, 0, "wbishop"], [3, 0, "wqueen"], [4, 0, "wking"], [5, 0, "wbishop"], [6, 0, "wknight"], [7, 0, "wrook"],
	[0, 1, "wpawn"], [1, 1, "wpawn"], [2, 1, "wpawn"], [3, 1, "wpawn"], [4, 1, "wpawn"], [5, 1, "wpawn"], [6, 1, "wpawn"], [7, 1, "wpawn"],
	[0, 7, "brook"], [1, 7, "bknight"], [2, 7, "bbishop"], [3, 7, "bqueen"], [4, 7, "bking"], [5, 7, "bbishop"], [6, 7, "bknight"], [7, 7, "brook"],
	[0, 6, "bpawn"], [1, 6, "bpawn"], [2, 6, "bpawn"], [3, 6, "bpawn"], [4, 6, "bpawn"], [5, 6, "bpawn"], [6, 6, "bpawn"], [7, 6, "bpawn"],
];

//boolean value for loaded or not
const piecesSrc = [
	"wking", "wqueen", "wknight", "wbishop", "wrook", "wpawn",
	"bking", "bqueen", "bknight", "bbishop", "brook", "bpawn"
];

const piecesLoaded = {};

var board = new Board();
var selectedTile = [-1, -1];

//store the king positions for quick access
const wKing = [-1, -1];
const bKing = [-1, -1];
const lastEnPassant = [-1, "w"]; //if the previous move can be en passant, set this to position

//if king moves, both will be set to false; if one rook moves one will be set to false
const whiteCastles = [true, true];
const blackCastles = [true, true];

start();

function start() {
	for (i of piecesSrc) {
		let piece = new Image();
		piece.src = `res/${i}.png`;
		piece.name = i;
		piece.onload = function() {
			piecesLoaded[this.name] = this;
		};
	}

	for (i of initialPieces) {
		board.positions[i[0]][i[1]].piece = i[2];

		//king position
		if (i[2] == "wking") {
			wKing[0] = i[0];
			wKing[1] = i[1];
		} else if (i[2] == "bking") {
			bKing[0] = i[0];
			bKing[1] = i[1];
		}
	}

	update();
}
function update() {
	drawBoard();

	//30fps target
	setTimeout(update, 30);
}

//integer interpolation between a and b where index is added to the first value
function interpolate(a, b, index) {
	if (a > b) return a - index;
	return a + index;
}

//moves the piece into given new position and reverts changes after evaluation
function kingInCheck(piece, oldPos, newPos) {
	let kingPos = [-1, -1];
	let playerColor = piece.slice(0, 1);
	if (piece.slice(1) == "king") {
		kingPos = newPos;
	} else {
		if (playerColor == "w") {
			kingPos = wKing;
		} else {
			kingPos = bKing;
		}
	}
	console.log(`${playerColor}king: ${kingPos[0]}, ${kingPos[1]}`);

	let knightChecks = [[1, 2], [2, 1], [-1, 2], [-2, 1], [-1, -2], [-2, -1], [1, -2], [2, -1]];
	for (let i of knightChecks) {
		//new position skipped
		if (newPos[0] == kingPos[0] + i[0] && newPos[1] == kingPos[1] + i[1]) continue;

		//legal position
		if (kingPos[0] + i[0] >= 0 && kingPos[0] + i[0] <= 7 && kingPos[1] + i[1] >= 0 && kingPos[1] + i[1] <= 7) {
			let piece = board.positions[kingPos[0] + i[0]][kingPos[1] + i[1]].piece;
			if (piece != null && piece.slice(0, 1) != playerColor && piece.slice(1) == "knight") {
				console.log("knight checking!");
				return true;
			}
		}
	}

	let diagonalChecks = [[1, 1], [1, -1], [-1, 1], [-1, -1]];
	for (let i of diagonalChecks) {
		//j is the diagonal multiplier
		for (let j = 1; kingPos[0] + i[0] * j >= 0 && kingPos[0] + i[0] * j <= 7 && kingPos[1] + i[1] * j >= 0 && kingPos[1] + i[1] * j <= 7; j++) {
			//old position skipped
			if (oldPos[0] == kingPos[0] + i[0] * j && oldPos[1] == kingPos[1] + i[1] * j) continue;

			//new position blocks
			if (newPos[0] == kingPos[0] + i[0] * j && newPos[1] == kingPos[1] + i[1] * j) break;

			let piece = board.positions[kingPos[0] + i[0] * j][kingPos[1] + i[1] * j].piece;
			if (piece != null) {
				let pieceColor = piece.slice(0, 1);
				let pieceName = piece.slice(1);

				//friendly piece blocks diagonal
				if (pieceColor == playerColor) break;
				//rooks and knights can't attack diagonals
				if (pieceName == "rook" || pieceName == "knight") break;
				//queens and bishops always will check
				if (pieceName == "queen" || pieceName == "bishop") {
					console.log("diagonal checked!");
					return true;
				}
				//enemy king checks if one away
				if (pieceName == "king") {
					if (j == 1) {
						console.log(`enemy ${piece} check! at ${kingPos[0] + i[0] * j}, ${kingPos[1] + i[1] * j}`);
						return true;
					} else {
						break;
					}
				}
				if (pieceName == "pawn") {
					//pawn attacking
					if (j == 1 && (i[1] == 1 && pieceColor == "b" || i[1] == -1 && pieceColor == "w")) {
						console.log("pawn check!");
						return true;
					} else {
						break;
					}
				}
			}
		}
	}

	let straightChecks = [[1, 0], [0, 1], [-1, 0], [0, -1]];
	for (let i of straightChecks) {
		//j is the vertical/horizontal multiplier
		for (let j = 1; kingPos[0] + i[0] * j >= 0 && kingPos[0] + i[0] * j <= 7 && kingPos[1] + i[1] * j >= 0 && kingPos[1] + i[1] * j <= 7; j++) {
			//old position skipped
			if (oldPos[0] == kingPos[0] + i[0] * j && oldPos[1] == kingPos[1] + i[1] * j) continue;

			//new position blocks
			if (newPos[0] == kingPos[0] + i[0] * j && newPos[1] == kingPos[1] + i[1] * j) break;

			let piece = board.positions[kingPos[0] + i[0] * j][kingPos[1] + i[1] * j].piece;
			if (piece != null) {
				let pieceColor = piece.slice(0, 1);
				let pieceName = piece.slice(1);

				//friendly piece blocks line
				if (pieceColor == playerColor) break;
				//bishops, knights, and pawns can't attack lines
				if (pieceName == "bishop" || pieceName == "knight" || pieceName == "pawn") break;
				//queens and rooks always will check
				if (pieceName == "queen" || pieceName == "rook") {
					console.log("vertical/horizontal checked!");
					return true;
				}
				//enemy king checks if one away
				if (pieceName == "king") {
					if (j == 1) {
						console.log("enemy king check!");
						return true;
					} else {
						break;
					}
				}
			}
		}
	}

	return false;
}
function moveIsLegal(piece, oldPos, newPos) {
	console.log(`${JSON.stringify(piece)}, ${JSON.stringify(oldPos)}, ${JSON.stringify(newPos)}`);

	//check for checks (no pun intended)
	if (kingInCheck(piece, oldPos, newPos)) {
		return false;
	}

	//can't have a friendly piece on new square
	if (board.positions[newPos[0]][newPos[1]].piece != null && board.positions[newPos[0]][newPos[1]].piece.slice(0, 1) == piece.slice(0, 1)) {
		console.log("obstructed");
		return false;
	}

	let pieceName = piece.slice(1);

	switch (pieceName) {
	case "knight":
		//move two and one
		if (Math.abs(newPos[0] - oldPos[0]) == 2 && Math.abs(newPos[1] - oldPos[1]) == 1 || Math.abs(newPos[0] - oldPos[0]) == 1 && Math.abs(newPos[1] - oldPos[1]) == 2) {
			return true;
		} else {
			return false;
		}
		break;
	case "rook":
		//straight lines
		if (newPos[0] - oldPos[0] == 0 || newPos[1] - oldPos[1] == 0) {
			if (newPos[0] - oldPos[0] == 0) {
				for (let i = Math.min(newPos[1], oldPos[1]) + 1; i < Math.max(newPos[1], oldPos[1]); i++) {
					if (board.positions[newPos[0]][i].piece != null) {
						return false;
					}
				}
				return true;
			} else {
				for (let i = Math.min(newPos[0], oldPos[0]) + 1; i < Math.max(newPos[0], oldPos[0]); i++) {
					if (board.positions[i][newPos[1]].piece != null) {
						return false;
					}
				}
				return true;
			}
		}
		return false;
	case "queen":
		//straight lines
		if (newPos[0] - oldPos[0] == 0 || newPos[1] - oldPos[1] == 0) {
			if (newPos[0] - oldPos[0] == 0) {
				for (let i = Math.min(newPos[1], oldPos[1]) + 1; i < Math.max(newPos[1], oldPos[1]); i++) {
					if (board.positions[newPos[0]][i].piece != null) {
						return false;
					}
				}
				return true;
			} else {
				for (let i = Math.min(newPos[0], oldPos[0]) + 1; i < Math.max(newPos[0], oldPos[0]); i++) {
					if (board.positions[i][newPos[1]].piece != null) {
						return false;
					}
				}
				return true;
			}
		}

		//diagonals
		if (Math.abs(newPos[0] - oldPos[0]) == Math.abs(newPos[1] - oldPos[1])) {
			if (Math.abs(newPos[0] - oldPos[0]) == Math.abs(newPos[1] - oldPos[1])) {
				for (let i = 1; i < Math.abs(newPos[1] - oldPos[1]); i++) {
					if (board.positions[interpolate(oldPos[0], newPos[0], i)][interpolate(oldPos[1], newPos[1], i)].piece != null) {
						return false;
					}
				}
				return true;
			}
		}

		return false;
	case "king":
		//king side castling
		if (piece == "wking" && whiteCastles[1] && oldPos[1] == 0 && oldPos[0] == 4 && newPos[1] == 0 && newPos[0] == 6) {
			if (board.positions[wKing[0] + 1][wKing[1]].piece == null && board.positions[wKing[0] + 2][wKing[1]].piece == null && !kingInCheck(piece, wKing, wKing) && !kingInCheck(piece, wKing, [wKing[0] + 1, wKing[1]]) && !kingInCheck(piece, wKing, [wKing[0] + 2, wKing[1]])) {
				return true;
			}
		}
		//queen side castling
		if (piece == "wking" && whiteCastles[0] && oldPos[1] == 0 && oldPos[0] == 4 && newPos[1] == 0 && newPos[0] == 2) {
			if (board.positions[wKing[0] - 1][wKing[1]].piece == null && board.positions[wKing[0] - 2][wKing[1]].piece == null && board.positions[wKing[0] - 3][wKing[1]].piece == null && !kingInCheck(piece, wKing, wKing) && !kingInCheck(piece, wKing, [wKing[0] - 1, wKing[1]]) && !kingInCheck(piece, wKing, [wKing[0] - 2, wKing[1]])) {
				return true;
			}
		}
		//king side castling
		if (piece == "bking" && blackCastles[1] && oldPos[1] == 7 && oldPos[0] == 4 && newPos[1] == 7 && newPos[0] == 6) {
			if (board.positions[bKing[0] + 1][bKing[1]].piece == null && board.positions[bKing[0] + 2][bKing[1]].piece == null && !kingInCheck(piece, bKing, bKing) && !kingInCheck(piece, bKing, [bKing[0] + 1, bKing[1]]) && !kingInCheck(piece, bKing, [bKing[0] + 2, bKing[1]])) {
				return true;
			}
		}
		//queen side castling
		if (piece == "bking" && blackCastles[0] && oldPos[1] == 7 && oldPos[0] == 4 && newPos[1] == 7 && newPos[0] == 2) {
			if (board.positions[bKing[0] - 1][bKing[1]].piece == null && board.positions[bKing[0] - 2][bKing[1]].piece == null && board.positions[bKing[0] - 3][bKing[1]].piece == null && !kingInCheck(piece, bKing, bKing) && !kingInCheck(piece, bKing, [bKing[0] - 1, bKing[1]]) && !kingInCheck(piece, bKing, [bKing[0] - 2, bKing[1]])) {
				return true;
			}
		}
		return Math.abs(newPos[0] - oldPos[0]) <= 1 && Math.abs(newPos[1] - oldPos[1]) <= 1;
	case "bishop":
		if (Math.abs(newPos[0] - oldPos[0]) == Math.abs(newPos[1] - oldPos[1])) {
			for (let i = 1; i < Math.abs(newPos[1] - oldPos[1]); i++) {
				if (board.positions[interpolate(oldPos[0], newPos[0], i)][interpolate(oldPos[1], newPos[1], i)].piece != null) {
					return false;
				}
			}
			return true;
		}
		return false;
	case "pawn":
		//has enemy piece
		if (board.positions[newPos[0]][newPos[1]].piece != null) {
			//diagonal by one
			if (piece.slice(0, 1) == "w") {
				return newPos[1] - oldPos[1] == 1 && Math.abs(newPos[0] - oldPos[0]) == 1;
			} else {
				return newPos[1] - oldPos[1] == -1 && Math.abs(newPos[0] - oldPos[0]) == 1;
			}
		} else {
			//en passant
			if (lastEnPassant[0] != -1) {
				if (piece.slice(0, 1) == "w") {
					if (Math.abs(newPos[0] - oldPos[0]) == 1 && oldPos[1] == 4 && lastEnPassant[1] == "b") return true;
				} else {
					if (Math.abs(newPos[0] - oldPos[0]) == 1 && oldPos[1] == 3 && lastEnPassant[1] == "w") return true;
				}
			}
			//straight by one (or two if on rank 2/7)
			if (piece.slice(0, 1) == "w") {
				return newPos[0] == oldPos[0] && (newPos[1] - oldPos[1] == 1 || newPos[1] - oldPos[1] == 2 && oldPos[1] == 1);
			} else {
				return newPos[0] == oldPos[0] && (newPos[1] - oldPos[1] == -1 || newPos[1] - oldPos[1] == -2 && oldPos[1] == 6);
			}
		}
	}


	return true;
}
function drawBoard() {
	for (let i = 0; i < 8; i++) {
		for (let j = 0; j < 8; j++) {
			//NOTE: from white's perspective
			if ((i + j) % 2 == 0) {
				canvasCtx.fillStyle = lightTile;
			} else {
				canvasCtx.fillStyle = darkTile;
			}
			if (selectedTile[0] == i && selectedTile[1] == 7 - j) {
				canvasCtx.fillStyle = highlightedTile;
			}
			canvasCtx.fillRect(i * 50, 350 - j * 50, 50, 50);

			//draw pieces
			if (board.positions[i][j].piece != null && board.positions[i][j].piece in piecesLoaded) {
				canvasCtx.drawImage(piecesLoaded[board.positions[i][j].piece], i * 50, 350 - j * 50, 50, 50);
			}
		}
	}
}

//controls
function mouseDown(event) {
	let x = Math.floor(event.offsetX / 50);
	let y = Math.floor(event.offsetY / 50);

	if (selectedTile[0] != x || selectedTile[1] != y) {
		let newTile = board.positions[x][7 - y];

		let oldTile = null;
		if (selectedTile[0] != -1 && selectedTile[1] != -1) {
			oldTile = board.positions[selectedTile[0]][7 - selectedTile[1]];
		}

		//if selectedTile is not null and piece has been clicked
		if (selectedTile[0] != -1 && selectedTile[1] != -1 && oldTile.piece != null && moveIsLegal(oldTile.piece, [selectedTile[0], 7 - selectedTile[1]], [x, 7 - y])) {

			//remove en passanted pawn if pawn made capture move on empty square
			if (newTile.piece == null && selectedTile[0] != x) {
				if (oldTile.piece == "wpawn") {
					//removes black pawn
					board.positions[x][4].piece = null;
				} else if (oldTile.piece == "bpawn") {
					//removes white pawn
					board.positions[x][3].piece = null;
				}
			}

			newTile.piece = board.positions[selectedTile[0]][7 - selectedTile[1]].piece;

			//update king position if king
			if (newTile.piece == "wking") {
				wKing[0] = x;
				wKing[1] = 7 - y;

				whiteCastles[0] = false;
				whiteCastles[1] = false;

				//castling
				if (oldTile.position[0] == 4 && oldTile.position[1] == 0 && newTile.position[0] == 6 && newTile.position[1] == 0) {
					board.positions[5][0].piece = "wrook";
					board.positions[7][0].piece = null;
				} else if (oldTile.position[0] == 4 && oldTile.position[1] == 0 && newTile.position[0] == 2 && newTile.position[1] == 0) {
					board.positions[3][0].piece = "wrook";
					board.positions[0][0].piece = null;
				}
			} else if (newTile.piece == "bking") {
				bKing[0] = x;
				bKing[1] = 7 - y;

				blackCastles[0] = false;
				blackCastles[1] = false;

				//castling
				if (oldTile.position[0] == 4 && oldTile.position[1] == 7 && newTile.position[0] == 6 && newTile.position[1] == 7) {
					board.positions[5][7].piece = "brook";
					board.positions[7][7].piece = null;
				} else if (oldTile.position[0] == 4 && oldTile.position[1] == 7 && newTile.position[0] == 2 && newTile.position[1] == 7) {
					board.positions[3][7].piece = "brook";
					board.positions[0][7].piece = null;
				}
			}
			//remove castling
			if (newTile.piece == "wrook" && oldTile.position[0] == 0 && oldTile.position[1] == 0) {
				whiteCastles[0] = false;
			} else if (newTile.piece == "wrook" && oldTile.position[0] == 7 && oldTile.position[1] == 0) {
				whiteCastles[1] = false;
			} else if (newTile.piece == "brook" && oldTile.position[0] == 0 && oldTile.position[1] == 7) {
				whiteCastles[0] = false;
			} else if (newTile.piece == "brook" && oldTile.position[0] == 7 && oldTile.position[1] == 7) {
				whiteCastles[1] = false;
			}

			//update en passant if applicable otherwise set to false
			if (newTile.piece.slice(1) == "pawn" && Math.abs(selectedTile[1] - y) == 2) {
				lastEnPassant[0] = x;
				lastEnPassant[1] = newTile.piece.slice(0, 1);
			} else {
				lastEnPassant[0] = -1;
			}

			oldTile.piece = null;

			selectedTile = [-1, -1];
		} else {
			selectedTile = [x, y];
		}
	} else {
		//deselect
		selectedTile = [-1, -1];
	}
}
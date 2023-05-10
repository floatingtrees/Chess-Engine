# Chess-Engine (Cyan IDE)
Our open source recreation of mainstream chess algorithms, including a frontend client in JavaScript and a backend server w/ algorithm in python.

Some common variables: Position is a dictionary that maps pieces to their locations, and position_swapped is a dictionary that maps a location to a piece. The locations are stored as (y, x), where y is the piece's distance from the 8th rank and x is the piece's distance from the a file (eg. e4 would be recorded as (4, 4), and a8 would be (0, 7)). Legal_moves is a list of all legal moves in a given position, and moves as stored as tuples containing (piece_type, starting_square, destination_square).  

Things to figure out: [Alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning), 
making an [evaluation function](https://en.wikipedia.org/wiki/Evaluation_function), 
[Quiescence searches](https://en.wikipedia.org/wiki/Quiescence_search), 
[Negamax](https://en.wikipedia.org/wiki/Negamax#:~:text=Negamax%20search%20is%20a%20variant,the%20value%20to%20player%20B.), 
[Principal variation searches](https://en.wikipedia.org/wiki/Principal_variation_search) (use neural networks to generate the initial branch), 
and [NNUEs](https://github.com/glinscott/nnue-pytorch/blob/master/docs/nnue.md).

NNUE inputs: 32{total pieces} * (64{king position} + 64{self king position} + 12{piece type} + 64{piece position}) + 4{castling} + 16{en_passant}, concat order: side_to_move + (side to not move + extra positional information)

Team: Jonathan Zhou, Zack Sima, Eric Brewster


from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood


from directions import DIRECTIONS
from board import BOARD
from input_tiles import TILES, min_swaps


# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

class Hashable:
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, __value: object) -> bool:
        return hash(self) == hash(__value)

    def __repr__(self):
        return str(self)


# slide puzzle propositions 
@proposition(E)
class Assigned(Hashable): # checks if number is assigned to a position 
    def __init__(self, tile, pos) -> None:
        self.tile = tile
        self.pos = pos

    def __str__(self) -> str:
        return f"({self.tile} @ {self.pos})"

@proposition(E) 
class Correct(Hashable): # checks if a number is at the right position 
    def __init__(self, tile) -> None:
        self.tile = tile
        self.pos = pos

    def __str__(self) -> str:
        return f"({self.tile} is at the correct position)"
    
@constraint.exactly_one(E) 
@proposition(E) 
class Blank(Hashable): # checks if a position is blank 
    def __init__(self, pos) -> None:
        self.pos = pos

    def __str__(self) -> str:
        return f"({self.pos} is blank.)"
    
@proposition(E)
class Above(Hashable): # checks if a position [p][q] above the blank tile is valid
    def __init__(self, pos) -> None:
        self.pos = pos

    def __str__(self) -> str:
        return f"(The position above the blank is a valid position on the board.)"

@proposition(E)   
class Below(Hashable): # checks if a position [p][q] below the blank tile is valid
    def __init__(self, pos) -> None:
        self.pos = pos

    def __str__(self) -> str:
        return f"(The position below the blank is a valid position on the board.)"

@proposition(E)
class Left(Hashable): # checks if a position [p][q] to the left of blank tile is valid
    def __init__(self, pos) -> None:
        self.pos = pos

    def __str__(self) -> str:
        return f"(The position to the left of blank is a valid position on the board.)"

@proposition(E)
class Right(Hashable): # checks if a position [p][q] to the right of the blank tile is valid
    def __init__(self) -> None:
        self.pos = pos

    def __str__(self) -> str:
        return f"(The position to the right of blank is a valid position on the board.)"

@proposition(E)
class CanSwap(Hashable): # checks if tile can move into a position (position has to be blank)
    def __init__(self, pos, d) -> None:
        self.pos = pos
        self.d = d
    
    def __str__(self) -> str:
        return f"({self.pos} can move {self.d}.)"
    
@proposition(E)
class on_board(Hashable): # checks if position is on the board (valid position to move into)
    def __init__(self, pos) -> None:
        self.pos = pos

    def __str__(self) -> str:
        return f"({self.pos} is a valid position.)"
    
@proposition(E)
class goal_state(Hashable):
    def __init__(self, BOARD) -> None:
        self.BOARD = BOARD
    
    def __str__(self) -> str:
        return f"(The board is in its goal state.)"

@proposition(E)
class clock(Hashable):
    def __init__(self, min_swaps) -> None:
        self.min_swaps = min_swaps
    
    def __str__(self) -> str:
        return f"(The board is solved within {self.min_swaps} moves.)"

        

# assign propositions to variables 
board = [[1,2,3], [4,5,6], [7,8,"empty_box"]] # test input board 

assigned_props = []
for t in TILES:
    for pos in BOARD:
        assigned_props.append(Assigned(t, pos))

correct_props = []
for t in TILES:
    correct_props.append(Correct(t))

blank_props = []
for pos in BOARD:
    blank_props.append(Blank(pos))

can_swap_props = []
for pos in BOARD:
    for d in DIRECTIONS:
        can_swap_props.append(CanSwap(pos, d))

on_board_props = [] 
for pos in BOARD:
    on_board_props.append(on_board(pos))

above_props = []
for pos in BOARD:
    above_props.append(Above(pos))

w = goal_state(BOARD)
c = clock(min_swaps)

below_props = []
for pos in BOARD:
    below_props.append(Below(pos))

left_props = []
for pos in BOARD:
    left_props.append(Left(pos))

right_props = []
for pos in BOARD:
    right_props.append(Right(pos))




def build_theory():
    # The initial tile has to be a blank in order to swap with a target tile
    for pos in BOARD:
        E.add_constraint(CanSwap(pos, d) for d in DIRECTIONS >> Blank(pos))

    # A tile can only swap with a position above, below, or beside it that is on the board
    for pos in BOARD:
        E.add_constraint(CanSwap(pos, d) for d in DIRECTIONS >> (Above(pos) | Below(pos) | Left(pos) | Right(pos)))
    

    # Check if the tile above, below, left, or right is a valid position 
    board_len = len(BOARD)
    for i in range(board_len):
        if i > 3:
            E.add_constraint(on_board(BOARD[i-3]) >> Above(BOARD[i]))
        if i < 6:
            E.add_constraint(on_board(BOARD[i+3]) >> Below(BOARD[i]))
        if i == 1 or i == 2 or i == 4 or i == 5 or i == 7 or i == 8:
            E.add_constraint(on_board(BOARD[i-1]) >> Left(BOARD[i]))
        if i == 0 or i == 1 or i == 3 or i == 4 or i == 6 or i == 7:
            E.add_constraint(on_board(BOARD[i+1] >> Right(BOARD[i])))

    # All tiles need to be in their correct positions to solve the puzzle and the clock needs to be at the correct time as stated in the input_tiles file.
    E.add_constraint(Correct(1) & Correct(2) & Correct(3) & Correct(4) & Correct(5) & Correct(6) & Correct(7) & Correct(8) & Correct('blank') & clock(min_swaps) >> goal_state(BOARD))

    # constraints for correct positions of each tile 
    for pos in BOARD:
        E.add_constraint(Correct(1, '[0][0]'))
        E.add_constraint(Correct(2, '[0][1]'))
        E.add_constraint(Correct(3, '[0][2]'))
        E.add_constraint(Correct(4, '[1][0]'))
        E.add_constraint(Correct(5, '[1][1]'))
        E.add_constraint(Correct(6, '[1][2]'))
        E.add_constraint(Correct(7, '[2][0]'))
        E.add_constraint(Correct(8, '[2][1]'))
        E.add_constraint(Correct('blank', '[2][2]'))
    
    
        # Check if the tile above, below, left, or right is a valid position 
    for pos in BOARD:
        pass

        # constraints for correct positions of each tile 
        E.add_constraint(Correct(1) >> Assigned(1, '[0][0]'))
        E.add_constraint(Correct(2) >> Assigned(2, '[0][1]'))
        E.add_constraint(Correct(3) >> Assigned(3, '[0][2]'))
        E.add_constraint(Correct(4) >> Assigned(4, '[1][0]'))
        E.add_constraint(Correct(5) >> Assigned(5, '[1][1]'))
        E.add_constraint(Correct(6) >> Assigned(6, '[1][2]'))
        E.add_constraint(Correct(7) >> Assigned(7, '[2][0]'))
        E.add_constraint(Correct(8) >> Assigned(8, '[2][1]'))
        E.add_constraint(Correct('blank') >> Assigned('blank', '[2][2]'))

    return E



if __name__ == "__main__":

    T = build_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()

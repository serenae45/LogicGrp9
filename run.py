from bauhaus import Encoding, proposition, constraint, Or, And
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
class Puzzle_Board(Hashable):
    def __init__(self, tile1, tile2, tile3, tile4, tile5, tile6, tile7, tile8, tile9) -> None:
        self.pos1 = tile1
        self.pos2 = tile2
        self.pos3 = tile3
        self.pos4 = tile4
        self.pos5 = tile5
        self.pos6 = tile6
        self.pos7 = tile7
        self.pos8 = tile8
        self.pos9 = tile9

    def __repr__(self) -> str:
        return f"([[{self.pos1},{self.pos2},{self.pos3}],
         [{self.pos4},{self.pos5},{self.pos6}],
         [{self.pos7},{self.pos8},{self.pos9}]])"

@proposition(E)
class Assigned(Hashable): # checks if number is assigned to a position 
    def __init__(self, tile, pos) -> None:
        self.tile = tile
        self.pos = pos

    def __str__(self) -> str:
        return f"({self.tile} @ {self.pos})"

# @proposition(E) 
# class Correct(Hashable): # checks if a number is at the right position 
#     def __init__(self, tile):
#         self.tile = tile

#     def __str__(self) -> str:
#         return f"({self.tile} is at the correct position)"
    
# @proposition(E) 
# class Blank(Hashable): # checks if a position is blank 
#     def __init__(self, pos) -> None:
#         self.pos = pos

#     def __str__(self) -> str:
#         return f"({self.pos} is blank.)"
    
# @proposition(E)
# class Above(Hashable): # checks if a position [p][q] above the blank tile is valid
#     def __init__(self, pos) -> None:
#         self.pos = pos

#     def __str__(self) -> str:
#         return f"(The position above the blank is a valid position on the board.)"

# @proposition(E)   
# class Below(Hashable): # checks if a position [p][q] below the blank tile is valid
#     def __init__(self, pos) -> None:
#         self.pos = pos

#     def __str__(self) -> str:
#         return f"(The position below the blank is a valid position on the board.)"

# @proposition(E)
# class Left(Hashable): # checks if a position [p][q] to the left of blank tile is valid
#     def __init__(self, pos) -> None:
#         self.pos = pos

#     def __str__(self) -> str:
#         return f"(The position to the left of blank is a valid position on the board.)"

# @proposition(E)
# class Right(Hashable): # checks if a position [p][q] to the right of the blank tile is valid
#     def __init__(self) -> None:
#         self.pos = pos

#     def __str__(self) -> str:
#         return f"(The position to the right of blank is a valid position on the board.)"

# @proposition(E)
# class CanSwap(Hashable): # checks if tile can move into a position (position has to be blank)
#     def __init__(self, pos, d) -> None:
#         self.pos = pos
#         self.d = d
    
#     def __str__(self) -> str:
#         return f"({self.pos} can move {self.d}.)"
    
# @proposition(E)
# class on_board(Hashable): # checks if position is on the board (valid position to move into)
#     def __init__(self, pos) -> None:
#         self.pos = pos

#     def __str__(self) -> str:
#         return f"({self.pos} is a valid position.)"
    
#@proposition(E)
#class goal_state(Hashable):
#    def __init__(self) -> None:
#    
#    def __str__(self) -> str:
#        return f"(The board is in its goal state.)"

# @proposition(E)
# class clock(Hashable):
#     def __init__(self, min_swaps) -> None:
#         self.min_swaps = min_swaps
    
#     def __str__(self) -> str:
#         return f"(The board is solved within {self.min_swaps} moves.)"
    
@proposition(E)
class Swap_pos1pos2(Hashable):
    def __init__(self, pos1, pos2) -> None:
        self.pos1 = pos1
        self.pos2 = pos2

    def __repr__(self) -> str:
        return f"({self.pos1} swapped with {self.pos2})" #Using Srings [0][0] to represent postion
    #at the moem


@proposition(E)
class Swap_pos1pos4(Hashable):
    def __init__(self, pos1, pos4) -> None:
        self.pos1 = pos1
        self.pos4 = pos4

    def __repr__(self) -> str:
        return f"({self.pos1} swapped with {self.pos4})"

@proposition(E)
class Swap_pos2pos3(Hashable):
    def __init__(self, pos2, pos3) -> None:
        self.pos2 = pos2
        self.pos3 = pos3

    def __repr__(self) -> str:
        return f"({self.pos2} swapped with {self.pos3})"

@proposition(E)
class Swap_pos2pos5(Hashable):
    def __init__(self, pos2, pos5) -> None:
        self.pos2 = pos2
        self.pos5 = pos5

    def __repr__(self) -> str:
        return f"({self.pos2} swapped with {self.pos5})"

@proposition(E)
class Swap_pos3pos6(Hashable):
    def __init__(self, pos3, pos6) -> None:
        self.pos3 = pos3
        self.pos6 = pos6

    def __repr__(self) -> str:
        return f"({self.pos3} swapped with {self.pos6})"

@proposition(E)
class Swap_pos4pos5(Hashable):
    def __init__(self, pos4, pos5) -> None:
        self.pos4 = pos4
        self.pos5 = pos5

    def __repr__(self) -> str:
        return f"({self.pos4} swapped with {self.pos5})"
    
@proposition(E)
class Swap_pos4pos7(Hashable):
    def __init__(self, pos4, pos7) -> None:
        self.pos4 = pos4
        self.pos7 = pos7

    def __repr__(self) -> str:
        return f"({self.pos4} swapped with {self.pos7})"
    
@proposition(E)
class Swap_pos5pos6(Hashable):
    def __init__(self, pos5, pos6) -> None:
        self.pos5 = pos5
        self.pos6 = pos6

    def __repr__(self) -> str:
        return f"({self.pos5} swapped with {self.pos5})"

@proposition(E)
class Swap_pos5pos8(Hashable):
    def __init__(self, pos5, pos8) -> None:
        self.pos5 = pos5
        self.pos8 = pos8

    def __repr__(self) -> str:
        return f"({self.pos5} swapped with {self.pos8})"
    
@proposition(E)
class Swap_pos6pos9(Hashable):
    def __init__(self, pos6, pos9) -> None:
        self.pos6 = pos6
        self.pos9 = pos9

    def __repr__(self) -> str:
        return f"({self.pos6} swapped with {self.pos9})"
    
@proposition(E)
class Swap_pos7pos8(Hashable):
    def __init__(self, pos7, pos8) -> None:
        self.pos7 = pos7
        self.pos8 = pos8

    def __repr__(self) -> str:
        return f"({self.pos7} swapped with {self.pos8})"

# At most min_swaps of the A instances are true, this is the time constraints
@constraint.at_most_k(E, min_swaps)
@proposition(E)
class Swap_tiles(Hashable):
    def __init__(self, pos_a, pos_b) -> None:
        self.tile_a = pos_a
        self.tile_b = pos_b

    def __repr__(self) -> str:
        return f"(Tile at {self.posa} swapped with the tile at {self.posb})"

# assign propositions to variables 

#*** Instead of string representation (0, 0), use a tuple (0, 0)
assigned_props = []
for t in TILES:
    for pos in BOARD:
            assigned_props.append(Assigned(t, pos))
#***


# assigned_props = []
# for t in TILES:
#     for pos in BOARD:
#         assigned_props.append(Assigned(t, pos))

# instantiate objects for other swap propositions

#Swap_pos1pos2_obj = Swap_pos1pos2(pos1=(0, 0), pos2=(0, 1))
#Swap_pos1pos4_obj = Swap_pos1pos4(pos1=(0, 0), pos4=(1, 0))
#Swap_pos2pos3_obj = Swap_pos2pos3(pos2=(0, 1), pos3=(0, 2))
#Swap_pos2pos5_obj = Swap_pos2pos5(pos2=(0, 1), pos5=(1, 1))
#Swap_pos3pos6_obj = Swap_pos3pos6(pos3=(0, 2), pos6=(1, 2))
#Swap_pos4pos5_obj = Swap_pos4pos5(pos4=(1, 0), pos5=(1, 1))
#Swap_pos4pos7_obj = Swap_pos4pos7(pos4=(1, 0), pos7=(2, 0))
#Swap_pos5pos6_obj = Swap_pos5pos6(pos5=(1, 1), pos6=(1, 2))
#Swap_pos5pos8_obj = Swap_pos5pos8(pos5=(1, 1), pos8=(2, 1))
#Swap_pos6pos9_obj = Swap_pos6pos9(pos6=(1, 2), pos9=(2, 2))
#Swap_pos7pos8_obj = Swap_pos7pos8(pos7=(2, 0), pos8=(2, 1))
#Swap_pos8pos9_obj = Swap_pos8pos9(pos8=(2, 1), pos9=(2, 2))




#TODO:put into build theory
# Add these instantiated to constraints

# correct_props = []
# for t in TILES:
#     correct_props.append(Correct(t))

# blank_props = []
# for pos in BOARD:
#     blank_props.append(Blank(pos))

# can_swap_props = []
# for pos in BOARD:
#     for d in DIRECTIONS:
#         can_swap_props.append(CanSwap(pos, d))

# on_board_props = [] 
# for pos in BOARD:
#     on_board_props.append(on_board(pos))

# above_props = []
# for pos in BOARD:
#     above_props.append(Above(pos))

#w = goal_state()
pb = Puzzle_Board(TILES[0], TILES[1], TILES[2], TILES[3], TILES[4], TILES[5], TILES[6], TILES[7], TILES[8])
win = Puzzle_Board('1', '2', '3', '4', '5', '6', '7', '8', 'blank')
Assigned(pb.pos1,(0,0))
Assigned(pb.pos2,(0,1))
Assigned(pb.pos3, (0, 2))
Assigned(pb.pos4, (1, 0)) 
Assigned(pb.pos5, (1, 1))
Assigned(pb.pos6, (1, 2))
Assigned(pb.pos7, (2, 0))
Assigned(pb.pos8, (2, 1)) 
Assigned(pb.pos9, (2, 2))
# c = clock(min_swaps)

# below_props = []
# for pos in BOARD:
#     below_props.append(Below(pos))

# left_props = []
# for pos in BOARD:
#     left_props.append(Left(pos))

# right_props = []
# for pos in BOARD:
#     right_props.append(Right(pos))




def build_theory():
    # # The initial tile has to be a blank in order to swap with a target tile
    # for pos in BOARD:
    #     E.add_constraint(CanSwap(pos, d) for d in DIRECTIONS >> Blank(pos))

    # # A tile can only swap with a position above, below, or beside it that is on the board
    # for pos in BOARD:
    #     E.add_constraint(CanSwap(pos, d) for d in DIRECTIONS >> (Above(pos) | Below(pos) | Left(pos) | Right(pos)))
    

    # # Check if the tile above, below, left, or right is a valid position 
    # board_len = len(BOARD)
    # for i in range(board_len):
    #     if i > 3:
    #         E.add_constraint(on_board(BOARD[i-3]) >> Above(BOARD[i]))
    #     if i < 6:
    #         E.add_constraint(on_board(BOARD[i+3]) >> Below(BOARD[i]))
    #     if i == 1 or i == 2 or i == 4 or i == 5 or i == 7 or i == 8:
    #         E.add_constraint(on_board(BOARD[i-1]) >> Left(BOARD[i]))
    #     if i == 0 or i == 1 or i == 3 or i == 4 or i == 6 or i == 7:
    #         E.add_constraint(on_board(BOARD[i+1] >> Right(BOARD[i])))

    # if time == min_swaps:
    #     E.add_constraint(clock(min_swaps))

    # All tiles need to be in their correct positions to solve the puzzle and the clock needs to be at the correct time as stated in the input_tiles file.
    E.add_constraint(Assigned('1', (0, 0)) & Assigned('2', (0, 1)) & Assigned('3', (0, 2)) & Assigned('4', (1, 0)) 
                     & Assigned('5', (1, 1)) & Assigned('6', (1, 2)) & Assigned('7', (2, 0)) & Assigned('8', (2, 1)) 
                     & Assigned('blank', (2, 2)) >> win)
    

    
    # makes sure only one tile is always assigned to one position.
    for t1 in TILES:
        for t2 in TILES:
            if t1!= t2:
                for pos in BOARD:
                    E.add_constraint(Assigned(t1, pos) >> ~Assigned(t2, pos))

    #This swaps the tiles
    for x in TILES:
        E.add_constraint((Swap_tiles((0,0), (0,1)) & Assigned(x, (0, 0)) & Assigned('blank', (0, 1))) >> (Assigned('blank', (0, 0)) & Assigned(x, (0, 1) & ~Swap_tiles((0,0), (0,1))))) #negated swap so it does not keep swapping infinitely
        E.add_constraint((Swap_tiles((0,0), (1,0)) & Assigned(x, (0, 0)) & Assigned('blank', (1, 0))) >> (Assigned('blank', (0, 0)) & Assigned(x, (1, 0) & ~Swap_tiles((0,0), (1,0)))))
        E.add_constraint((Swap_tiles((0,1), (0,2)) & Assigned(x, (0, 1)) & Assigned('blank', (0, 2))) >> (Assigned('blank', (0, 1)) & Assigned(x, (0, 2) & ~Swap_tiles((0,1), (0,2)))))
        E.add_constraint((Swap_tiles((0,1), (1,1)) & Assigned(x, (0, 1)) & Assigned('blank', (1, 1))) >> (Assigned('blank', (0, 1)) & Assigned(x, (1, 1) & ~Swap_tiles((0,1), (1,1)))))
        E.add_constraint((Swap_tiles((0,2), (1,2)) & Assigned(x, (0, 2)) & Assigned('blank', (1, 2))) >> (Assigned('blank', (0, 2)) & Assigned(x, (1, 2) & ~Swap_tiles((0,2), (1,2)))))
        E.add_constraint((Swap_tiles((1,0), (1,1)) & Assigned(x, (1, 0)) & Assigned('blank', (1, 1))) >> (Assigned('blank', (1, 0)) & Assigned(x, (1, 1) & ~Swap_tiles((1,0), (1,1)))))
        E.add_constraint((Swap_tiles((1,0), (2,0)) & Assigned(x, (1, 0)) & Assigned('blank', (2, 0))) >> (Assigned('blank', (1, 0)) & Assigned(x, (2, 0) & ~Swap_tiles((1,0), (2,0)))))
        E.add_constraint((Swap_tiles((1,1), (1,2)) & Assigned(x, (1, 1)) & Assigned('blank', (1, 2))) >> (Assigned('blank', (1, 1)) & Assigned(x, (1, 2) & ~Swap_tiles((1,1), (1,2)))))
        E.add_constraint((Swap_tiles((1,1), (2,1)) & Assigned(x, (1, 1)) & Assigned('blank', (2, 1))) >> (Assigned('blank', (1, 1)) & Assigned(x, (2, 1) & ~Swap_tiles((1,1), (2,1)))))
        E.add_constraint((Swap_tiles((1,2), (2,2)) & Assigned(x, (1, 2)) & Assigned('blank', (2, 2))) >> (Assigned('blank', (1, 2)) & Assigned(x, (2, 2) & ~Swap_tiles((1,2), (2,2)))))
        E.add_constraint((Swap_tiles((2,0), (2,1)) & Assigned(x, (2, 1)) & Assigned('blank', (2, 1))) >> (Assigned('blank', (2, 0)) & Assigned(x, (2, 1) & ~Swap_tiles((2,0), (2,1)))))
        E.add_constraint((Swap_tiles((2,1), (2,2)) & Assigned(x, (2, 1)) & Assigned('blank', (2, 2))) >> (Assigned('blank', (2, 1)) & Assigned(x, (2, 2) & ~Swap_tiles((2,1), (2,2)))))
        
        E.add_constraint((Swap_tiles((0,0), (0,1)) & Assigned('blank', (0, 0)) & Assigned(x, (0, 1))) >> (Assigned(x, (0, 0)) & Assigned('blank', (0, 1)) & ~Swap_tiles((0,0), (0,1))))
        E.add_constraint((Swap_tiles((0,0), (1,0)) & Assigned('blank', (0, 0)) & Assigned(x, (1, 0))) >> (Assigned(x, (0, 0)) & Assigned('blank', (1, 0)) & ~Swap_tiles((0,0), (1,0))))
        E.add_constraint((Swap_tiles((0,1), (0,2)) & Assigned('blank', (0, 1)) & Assigned(x, (0, 2))) >> (Assigned(x, (0, 1)) & Assigned('blank', (0, 2)) & ~Swap_tiles((0,1), (0,2))))
        E.add_constraint((Swap_tiles((0,1), (1,1)) & Assigned('blank', (0, 1)) & Assigned(x, (1, 1))) >> (Assigned(x, (0, 1)) & Assigned('blank', (1, 1)) & ~Swap_tiles((0,1), (1,1))))
        E.add_constraint((Swap_tiles((0,2), (1,2)) & Assigned('blank', (0, 2)) & Assigned(x, (1, 2))) >> (Assigned(x, (0, 2)) & Assigned('blank', (1, 2)) & ~Swap_tiles((0,2), (1,2))))
        E.add_constraint((Swap_tiles((1,0), (1,1)) & Assigned('blank', (1, 0)) & Assigned(x, (1, 1))) >> (Assigned(x, (1, 0)) & Assigned('blank', (1, 1)) & ~Swap_tiles((1,0), (1,1))))
        E.add_constraint((Swap_tiles((1,0), (2,0)) & Assigned('blank', (1, 0)) & Assigned(x, (2, 0))) >> (Assigned(x, (1, 0)) & Assigned('blank', (2, 0)) & ~Swap_tiles((1,0), (2,0))))
        E.add_constraint((Swap_tiles((1,1), (1,2)) & Assigned('blank', (1, 1)) & Assigned(x, (1, 2))) >> (Assigned(x, (1, 1)) & Assigned('blank', (1, 2)) & ~Swap_tiles((1,1), (1,2))))
        E.add_constraint((Swap_tiles((1,1), (2,1)) & Assigned('blank', (1, 1)) & Assigned(x, (2, 1))) >> (Assigned(x, (1, 1)) & Assigned('blank', (2, 1)) & ~Swap_tiles((1,1), (2,1))))
        E.add_constraint((Swap_tiles((1,2), (2,2)) & Assigned('blank', (1, 2)) & Assigned(x, (2, 2))) >> (Assigned(x, (1, 2)) & Assigned('blank', (2, 2)) & ~Swap_tiles((1,2), (2,2))))
        E.add_constraint((Swap_tiles((2,0), (2,1)) & Assigned('blank', (2, 0)) & Assigned(x, (2, 1))) >> (Assigned(x, (2, 0)) & Assigned('blank', (2, 1)) & ~Swap_tiles((2,0), (2,1))))
        E.add_constraint((Swap_tiles((2,1), (2,2)) & Assigned('blank', (2, 1)) & Assigned(x, (2, 2))) >> (Assigned(x, (2, 1)) & Assigned('blank', (2, 2)) & ~Swap_tiles((2,1), (2,2))))

        #E.add_constraint(Swap_pos1pos2_obj & Assigned(x, (0, 0)) & Assigned('blank', (0, 1)) >> Assigned('blank', (0, 0)) & Assigned(x, (0, 1)) & ~(Assigned(x, (0, 0))) & ~(Assigned('blank', (0, 1))))
        #E.add_constraint(Swap_pos1pos4_obj & Assigned(x, (0, 0)) & Assigned('blank', (1, 0)) >> Assigned('blank', (0, 0)) & Assigned(x, (1, 0)) & ~(Assigned(x, (0, 0))) & ~(Assigned('blank', (1, 0))))
        #E.add_constraint(Swap_pos2pos3_obj & Assigned(x, (0, 1)) & Assigned('blank', (0, 2)) >> Assigned('blank', (0, 1)) & Assigned(x, (0, 2)) & ~(Assigned(x, (0, 1))) & ~(Assigned('blank', (0, 2))))
        #E.add_constraint(Swap_pos2pos5_obj & Assigned(x, (0, 1)) & Assigned('blank', (1, 1)) >> Assigned('blank', (0, 1)) & Assigned(x, (1, 1)) & ~(Assigned(x, (0, 1))) & ~(Assigned('blank', (1, 1))))
        #E.add_constraint(Swap_pos3pos6_obj & Assigned(x, (0, 2)) & Assigned('blank', (1, 2)) >> Assigned('blank', (0, 2)) & Assigned(x, (1, 2)) & ~(Assigned(x, (0, 2))) & ~(Assigned('blank', (1, 2))))
        #E.add_constraint(Swap_pos4pos5_obj & Assigned(x, (1, 0)) & Assigned('blank', (1, 1)) >> Assigned('blank', (1, 0)) & Assigned(x, (1, 1)) & ~(Assigned(x, (1, 0))) & ~(Assigned('blank', (1, 1))))
        #E.add_constraint(Swap_pos4pos7_obj & Assigned(x, (1, 0)) & Assigned('blank', (2, 0)) >> Assigned('blank', (1, 0)) & Assigned(x, (2, 0)) & ~(Assigned(x, (1, 0))) & ~(Assigned('blank', (2, 0))))
        #E.add_constraint(Swap_pos5pos6_obj & Assigned(x, (1, 1)) & Assigned('blank', (1, 2)) >> Assigned('blank', (1, 1)) & Assigned(x, (1, 2)) & ~(Assigned(x, (1, 1))) & ~(Assigned('blank', (1, 2))))
        #E.add_constraint(Swap_pos5pos8_obj & Assigned(x, (1, 1)) & Assigned('blank', (2, 1)) >> Assigned('blank', (1, 1)) & Assigned(x, (2, 1)) & ~(Assigned(x, (1, 1))) & ~(Assigned('blank', (2, 1))))
        #E.add_constraint(Swap_pos6pos9_obj & Assigned(x, (1, 2)) & Assigned('blank', (2, 2)) >> Assigned('blank', (1, 2)) & Assigned(x, (2, 2)) & ~(Assigned(x, (1, 2))) & ~(Assigned('blank', (2, 2))))
        #E.add_constraint(Swap_pos7pos8_obj & Assigned(x, (2, 0)) & Assigned('blank', (2, 1)) >> Assigned('blank', (2, 0)) & Assigned(x, (2, 1)) & ~(Assigned(x, (2, 0))) & ~(Assigned('blank', (2, 1))))
        #E.add_constraint(Swap_pos8pos9_obj & Assigned(x, (2, 1)) & Assigned('blank', (2, 2)) >> Assigned('blank', (2, 1)) & Assigned(x, (2, 2)) & ~(Assigned(x, (2, 1))) & ~(Assigned('blank', (2, 2))))

        #E.add_constraint(Swap_pos1pos2_obj & Assigned('blank', (0, 0)) & Assigned(x, (0, 1)) >> Assigned(x, (0, 0)) & Assigned('blank', (0, 1)) & ~(Assigned('blank', (0, 0))) & ~(Assigned(x, (0, 1))))
        #E.add_constraint(Swap_pos1pos4_obj & Assigned('blank', (0, 0)) & Assigned(x, (1, 0)) >> Assigned(x, (0, 0)) & Assigned('blank', (1, 0)) & ~(Assigned('blank', (0, 0))) & ~(Assigned(x, (1, 0))))
        #E.add_constraint(Swap_pos2pos3_obj & Assigned('blank', (0, 1)) & Assigned(x, (0, 2)) >> Assigned(x, (0, 1)) & Assigned('blank', (0, 2)) & ~(Assigned('blank', (0, 1))) & ~(Assigned(x, (0, 2))))
        #E.add_constraint(Swap_pos2pos5_obj & Assigned('blank', (0, 1)) & Assigned(x, (1, 1)) >> Assigned(x, (0, 1)) & Assigned('blank', (1, 1)) & ~(Assigned('blank', (0, 1))) & ~(Assigned(x, (1, 1))))
        #E.add_constraint(Swap_pos3pos6_obj & Assigned('blank', (0, 2)) & Assigned(x, (1, 2)) >> Assigned(x, (0, 2)) & Assigned('blank', (1, 2)) & ~(Assigned('blank', (0, 2))) & ~(Assigned(x, (1, 2))))
        #E.add_constraint(Swap_pos4pos5_obj & Assigned('blank', (1, 0)) & Assigned(x, (1, 1)) >> Assigned(x, (1, 0)) & Assigned('blank', (1, 1)) & ~(Assigned('blank', (1, 0))) & ~(Assigned(x, (1, 1))))
        #E.add_constraint(Swap_pos4pos7_obj & Assigned('blank', (1, 0)) & Assigned(x, (2, 0)) >> Assigned(x, (1, 0)) & Assigned('blank', (2, 0)) & ~(Assigned('blank', (1, 0))) & ~(Assigned(x, (2, 0))))
        #E.add_constraint(Swap_pos5pos6_obj & Assigned('blank', (1, 1)) & Assigned(x, (1, 2)) >> Assigned(x, (1, 1)) & Assigned('blank', (1, 2)) & ~(Assigned('blank', (1, 1))) & ~(Assigned(x, (1, 2))))
        #E.add_constraint(Swap_pos5pos8_obj & Assigned('blank', (1, 1)) & Assigned(x, (2, 1)) >> Assigned(x, (1, 1)) & Assigned('blank', (2, 1)) & ~(Assigned('blank', (1, 1))) & ~(Assigned(x, (2, 1))))
        #E.add_constraint(Swap_pos6pos9_obj & Assigned('blank', (1, 2)) & Assigned(x, (2, 2)) >> Assigned(x, (1, 2)) & Assigned('blank', (2, 2)) & ~(Assigned('blank', (1, 2))) & ~(Assigned(x, (2, 2))))
        #E.add_constraint(Swap_pos7pos8_obj & Assigned('blank', (2, 0)) & Assigned(x, (2, 1)) >> Assigned(x, (2, 0)) & Assigned('blank', (2, 1)) & ~(Assigned('blank', (2, 0))) & ~(Assigned(x, (2, 1))))
        #E.add_constraint(Swap_pos8pos9_obj & Assigned('blank', (2, 1 )) & Assigned(x, (2, 2)) >> Assigned(x, (2, 1)) & Assigned('blank', (2, 2)) & ~(Assigned('blank', (2, 1))) & ~(Assigned(x, (2, 2))))
    

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
    # for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
    #     # Ensure that you only send these functions NNF formulas
    #     # Literals are compiled to NNF here
    #     print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()

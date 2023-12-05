from bauhaus import Encoding, proposition, constraint, Or, And
from bauhaus.utils import count_solutions, likelihood


from board import BOARD
from input_tiles import TILES, min_swaps

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

board = [['1', '2', '3'], ['4', 'blank', '6'], ['7', '5', '8']]

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
        return f"([[{self.pos1},{self.pos2},{self.pos3}],[{self.pos4},{self.pos5},{self.pos6}],[{self.pos7},{self.pos8},{self.pos9}]])"

@proposition(E)
class Assigned(Hashable): # checks if number is assigned to a position 
    def __init__(self, tile, pos) -> None:
        self.tile = tile
        self.pos = pos

    def __str__(self) -> str:
        return f"({self.tile} @ {self.pos})"

@proposition(E)
class clock(Hashable):
    def __init__(self, swaptimer, min_swaps) -> None:
        self.min_swaps = min_swaps
        self.swaptimer = swaptimer
    
    def __str__(self) -> str:
        return f"(The board is at time {self.swaptimer} and is below the minimum swaps.)"
    
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
    
@proposition(E)
class Swap_pos8pos9(Hashable):
    def __init__(self, pos8, pos9) -> None:
        self.pos8 = pos8
        self.pos9 = pos9

    def __repr__(self):
        return f"({self.pos8} swapped with {self.pos9})"


# At most min_swaps of the A instances are true, this is the time constraints
# @constraint.at_most_k(E, min_swaps)
# @proposition(E)
# class Swap_tiles(Hashable):
#     def __init__(self, pos_a, pos_b) -> None:
#         self.tile_a = pos_a
#         self.tile_b = pos_b

#     def __repr__(self) -> str:
#         return f"(Tile at {self.tile_b} swapped with the tile at {self.tile_a})"
    
@proposition(E)
class swapped(Hashable):
    def __init__(self, pos1, pos2, swaptimer) -> None:
        self.pos1 = pos1
        self.pos2 = pos2
        self.swaptimer = swaptimer

    def __str__(self) -> str:
        return f"(The tiles at positions {self.pos1} and {self.pos2} swapped at time {self.swaptimer})"

# assign propositions to variables 

assigned_props = [
    Assigned(tile, pos)
    for tile, pos in zip(TILES, BOARD)
]


# instantiate objects for other swap propositions

Swap_pos1pos2_obj = Swap_pos1pos2(pos1=(0, 0), pos2=(0, 1))
Swap_pos1pos4_obj = Swap_pos1pos4(pos1=(0, 0), pos4=(1, 0))
Swap_pos2pos3_obj = Swap_pos2pos3(pos2=(0, 1), pos3=(0, 2))
Swap_pos2pos5_obj = Swap_pos2pos5(pos2=(0, 1), pos5=(1, 1))
Swap_pos3pos6_obj = Swap_pos3pos6(pos3=(0, 2), pos6=(1, 2))
Swap_pos4pos5_obj = Swap_pos4pos5(pos4=(1, 0), pos5=(1, 1))
Swap_pos4pos7_obj = Swap_pos4pos7(pos4=(1, 0), pos7=(2, 0))
Swap_pos5pos6_obj = Swap_pos5pos6(pos5=(1, 1), pos6=(1, 2))
Swap_pos5pos8_obj = Swap_pos5pos8(pos5=(1, 1), pos8=(2, 1))
Swap_pos6pos9_obj = Swap_pos6pos9(pos6=(1, 2), pos9=(2, 2))
Swap_pos7pos8_obj = Swap_pos7pos8(pos7=(2, 0), pos8=(2, 1))
Swap_pos8pos9_obj = Swap_pos8pos9(pos8=(2, 1), pos9=(2, 2))


    

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

Assigned(pb.pos1, (0, 0))
Assigned(pb.pos2, (0, 1))
Assigned(pb.pos3, (0, 2))
Assigned(pb.pos4, (1, 0)) 
Assigned(pb.pos5, (1, 1))
Assigned(pb.pos6, (1, 2))
Assigned(pb.pos7, (2, 0))
Assigned(pb.pos8, (2, 1)) 
Assigned(pb.pos9, (2, 2))

# below_props = []
# for pos in BOARD:
#     below_props.append(Below(pos))

# left_props = []
# for pos in BOARD:
#     left_props.append(Left(pos))

# right_props = []
# for pos in BOARD:
#     right_props.append(Right(pos))


Swap_pos1pos2_obj = Swap_pos1pos2(pos1=(0, 0), pos2=(0, 1))
Swap_pos1pos4_obj = Swap_pos1pos4(pos1=(0, 0), pos4=(1, 0))
Swap_pos2pos3_obj = Swap_pos2pos3(pos2=(0, 1), pos3=(0, 2))
Swap_pos2pos5_obj = Swap_pos2pos5(pos2=(0, 1), pos5=(1, 1))
Swap_pos3pos6_obj = Swap_pos3pos6(pos3=(0, 2), pos6=(1, 2))
Swap_pos4pos5_obj = Swap_pos4pos5(pos4=(1, 0), pos5=(1, 1))
Swap_pos4pos7_obj = Swap_pos4pos7(pos4=(1, 0), pos7=(2, 0))
Swap_pos5pos6_obj = Swap_pos5pos6(pos5=(1, 1), pos6=(1, 2))
Swap_pos5pos8_obj = Swap_pos5pos8(pos5=(1, 1), pos8=(2, 1))
Swap_pos6pos9_obj = Swap_pos6pos9(pos6=(1, 2), pos9=(2, 2))
Swap_pos7pos8_obj = Swap_pos7pos8(pos7=(2, 0), pos8=(2, 1))
Swap_pos8pos9_obj = Swap_pos8pos9(pos8=(2, 1), pos9=(2, 2))






                    
    
                    

def build_theory():
    # Encoding that will store all of your constraints
    #Construct initial board
    for i in range(3):
        for j in range(3):
            if(board[i][j] == '1'):
                (Assigned('1', (i, j)))
                for tile in TILES:
                    if tile != '1':
                        E.add_constraint(~Assigned(tile, (i, j)))
            elif(board[i][j] == '2'):
                E.add_constraint(Assigned('2',(i, j)))
                for tile in TILES:
                    if tile != '2':
                        E.add_constraint(~Assigned(tile, (i, j)))
            elif(board[i][j] == '3'):
                E.add_constraint(Assigned('3', (i, j)))
                for tile in TILES:
                    if tile != '3':
                        E.add_constraint(~Assigned(tile, (i, j)))
            elif(board[i][j] == '4'):
                E.add_constraint(Assigned('4', (i, j)))
                for tile in TILES:
                    if tile != '4':
                        E.add_constraint(~Assigned(tile, (i, j)))
            elif(board[i][j] == '5'):
                E.add_constraint(Assigned('5', (i, j)))
                for tile in TILES:
                    if tile != '5':
                        E.add_constraint(~Assigned(tile, (i, j)))
            elif(board[i][j] == '6'):
                E.add_constraint(Assigned('6', (i, j)))
                for tile in TILES:
                    if tile != '6':
                        E.add_constraint(~Assigned(tile, (i, j)))
            elif(board[i][j] == '7'):
                E.add_constraint(Assigned('7', (i, j)))
                for tile in TILES:
                    if tile != '7':
                        E.add_constraint(~Assigned(tile, (i, j)))
            elif(board[i][j] == '8'):
                E.add_constraint(Assigned('8', (i, j)))
                for tile in TILES:
                    if tile != '8':
                        E.add_constraint(~Assigned(tile, (i, j)))
            elif(board[i][j] == 'blank'):
                E.add_constraint(Assigned('blank', (i, j)))
                for tile in TILES:
                    if tile != 'blank':
                        E.add_constraint(~Assigned(tile, (i, j)))
            else:
                print("Error in setting up the board")

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

    # The swaptimer keeps track of the number of swaps that occur
    swaptimer = 0
    # All tiles need to be in their correct positions to solve the puzzle and the clock needs to be at the correct time as stated in the input_tiles file.
    E.add_constraint(And(Assigned('1', (0, 0)), Assigned('2', (0, 1)), Assigned('3', (0, 2)) , Assigned('4', (1, 0)), 
                         Assigned('5', (1, 1)), Assigned('6', (1, 2)), Assigned('7', (2, 0)), Assigned('8', (2, 1)), 
                         Assigned('blank', (2, 2)), ~clock(swaptimer, min_swaps) >> win))
    

    
    # makes sure only one tile is always assigned to one position.
    # for t1 in TILES:
    #     for t2 in TILES:
    #         if t1!= t2:
    #             for pos in BOARD:
    #                 E.add_constraint(Assigned(t1, pos) >> ~Assigned(t2, pos))


    #This swaps the tiles
    for x in TILES:
        # E.add_constraint((Swap_tiles((0,0), (0,1)) & Assigned(x, (0, 0)) & Assigned('blank', (0, 1))) >> (Assigned('blank', (0, 0)) & Assigned(x, (0, 1) & ~Swap_tiles((0,0), (0,1))))) #negated swap so it does not keep swapping infinitely
        # E.add_constraint((Swap_tiles((0,0), (1,0)) & Assigned(x, (0, 0)) & Assigned('blank', (1, 0))) >> (Assigned('blank', (0, 0)) & Assigned(x, (1, 0) & ~Swap_tiles((0,0), (1,0)))))
        # E.add_constraint((Swap_tiles((0,1), (0,2)) & Assigned(x, (0, 1)) & Assigned('blank', (0, 2))) >> (Assigned('blank', (0, 1)) & Assigned(x, (0, 2) & ~Swap_tiles((0,1), (0,2)))))
        # E.add_constraint((Swap_tiles((0,1), (1,1)) & Assigned(x, (0, 1)) & Assigned('blank', (1, 1))) >> (Assigned('blank', (0, 1)) & Assigned(x, (1, 1) & ~Swap_tiles((0,1), (1,1)))))
        # E.add_constraint((Swap_tiles((0,2), (1,2)) & Assigned(x, (0, 2)) & Assigned('blank', (1, 2))) >> (Assigned('blank', (0, 2)) & Assigned(x, (1, 2) & ~Swap_tiles((0,2), (1,2)))))
        # E.add_constraint((Swap_tiles((1,0), (1,1)) & Assigned(x, (1, 0)) & Assigned('blank', (1, 1))) >> (Assigned('blank', (1, 0)) & Assigned(x, (1, 1) & ~Swap_tiles((1,0), (1,1)))))
        # E.add_constraint((Swap_tiles((1,0), (2,0)) & Assigned(x, (1, 0)) & Assigned('blank', (2, 0))) >> (Assigned('blank', (1, 0)) & Assigned(x, (2, 0) & ~Swap_tiles((1,0), (2,0)))))
        # E.add_constraint((Swap_tiles((1,1), (1,2)) & Assigned(x, (1, 1)) & Assigned('blank', (1, 2))) >> (Assigned('blank', (1, 1)) & Assigned(x, (1, 2) & ~Swap_tiles((1,1), (1,2)))))
        # E.add_constraint((Swap_tiles((1,1), (2,1)) & Assigned(x, (1, 1)) & Assigned('blank', (2, 1))) >> (Assigned('blank', (1, 1)) & Assigned(x, (2, 1) & ~Swap_tiles((1,1), (2,1)))))
        # E.add_constraint((Swap_tiles((1,2), (2,2)) & Assigned(x, (1, 2)) & Assigned('blank', (2, 2))) >> (Assigned('blank', (1, 2)) & Assigned(x, (2, 2) & ~Swap_tiles((1,2), (2,2)))))
        # E.add_constraint((Swap_tiles((2,0), (2,1)) & Assigned(x, (2, 1)) & Assigned('blank', (2, 1))) >> (Assigned('blank', (2, 0)) & Assigned(x, (2, 1) & ~Swap_tiles((2,0), (2,1)))))
        # E.add_constraint((Swap_tiles((2,1), (2,2)) & Assigned(x, (2, 1)) & Assigned('blank', (2, 2))) >> (Assigned('blank', (2, 1)) & Assigned(x, (2, 2) & ~Swap_tiles((2,1), (2,2)))))
        
        # E.add_constraint((Swap_tiles((0,0), (0,1)) & Assigned('blank', (0, 0)) & Assigned(x, (0, 1))) >> (Assigned(x, (0, 0)) & Assigned('blank', (0, 1)) & ~Swap_tiles((0,0), (0,1))))
        # E.add_constraint((Swap_tiles((0,0), (1,0)) & Assigned('blank', (0, 0)) & Assigned(x, (1, 0))) >> (Assigned(x, (0, 0)) & Assigned('blank', (1, 0)) & ~Swap_tiles((0,0), (1,0))))
        # E.add_constraint((Swap_tiles((0,1), (0,2)) & Assigned('blank', (0, 1)) & Assigned(x, (0, 2))) >> (Assigned(x, (0, 1)) & Assigned('blank', (0, 2)) & ~Swap_tiles((0,1), (0,2))))
        # E.add_constraint((Swap_tiles((0,1), (1,1)) & Assigned('blank', (0, 1)) & Assigned(x, (1, 1))) >> (Assigned(x, (0, 1)) & Assigned('blank', (1, 1)) & ~Swap_tiles((0,1), (1,1))))
        # E.add_constraint((Swap_tiles((0,2), (1,2)) & Assigned('blank', (0, 2)) & Assigned(x, (1, 2))) >> (Assigned(x, (0, 2)) & Assigned('blank', (1, 2)) & ~Swap_tiles((0,2), (1,2))))
        # E.add_constraint((Swap_tiles((1,0), (1,1)) & Assigned('blank', (1, 0)) & Assigned(x, (1, 1))) >> (Assigned(x, (1, 0)) & Assigned('blank', (1, 1)) & ~Swap_tiles((1,0), (1,1))))
        # E.add_constraint((Swap_tiles((1,0), (2,0)) & Assigned('blank', (1, 0)) & Assigned(x, (2, 0))) >> (Assigned(x, (1, 0)) & Assigned('blank', (2, 0)) & ~Swap_tiles((1,0), (2,0))))
        # E.add_constraint((Swap_tiles((1,1), (1,2)) & Assigned('blank', (1, 1)) & Assigned(x, (1, 2))) >> (Assigned(x, (1, 1)) & Assigned('blank', (1, 2)) & ~Swap_tiles((1,1), (1,2))))
        # E.add_constraint((Swap_tiles((1,1), (2,1)) & Assigned('blank', (1, 1)) & Assigned(x, (2, 1))) >> (Assigned(x, (1, 1)) & Assigned('blank', (2, 1)) & ~Swap_tiles((1,1), (2,1))))
        # E.add_constraint((Swap_tiles((1,2), (2,2)) & Assigned('blank', (1, 2)) & Assigned(x, (2, 2))) >> (Assigned(x, (1, 2)) & Assigned('blank', (2, 2)) & ~Swap_tiles((1,2), (2,2))))
        # E.add_constraint((Swap_tiles((2,0), (2,1)) & Assigned('blank', (2, 0)) & Assigned(x, (2, 1))) >> (Assigned(x, (2, 0)) & Assigned('blank', (2, 1)) & ~Swap_tiles((2,0), (2,1))))
        # E.add_constraint((Swap_tiles((2,1), (2,2)) & Assigned('blank', (2, 1)) & Assigned(x, (2, 2))) >> (Assigned(x, (2, 1)) & Assigned('blank', (2, 2)) & ~Swap_tiles((2,1), (2,2))))
        
        swap1 = [Swap_pos1pos2_obj, Assigned(x, (0, 0)), Assigned('blank', (0, 1)), clock(swaptimer, min_swaps)]
        swap2 = [Assigned('blank', (0, 0)), Assigned(x, (0, 1)) , ~(Assigned(x, (0, 0))), ~(Assigned('blank', (0, 1))), swapped((0, 0), (0, 1), swaptimer)]

        swap3 = [Swap_pos1pos4_obj, Assigned(x, (0, 0)), Assigned('blank', (1, 0)), clock(swaptimer, min_swaps)]
        swap4 = [Assigned('blank', (0, 0)) , Assigned(x, (1, 0)), ~(Assigned(x, (0, 0))),  ~(Assigned('blank', (1, 0))), swapped((0, 0), (1, 0), swaptimer)]

        swap5 = [Swap_pos2pos3_obj, Assigned(x, (0, 1)) , Assigned('blank', (0, 2)), clock(swaptimer, min_swaps)]
        swap6 = [Assigned('blank', (0, 1)) , Assigned(x, (0, 2)) , ~(Assigned(x, (0, 1))) , ~(Assigned('blank', (0, 2))), swapped((0, 1), (0, 2), swaptimer)]

        swap7 = [Swap_pos2pos5_obj , Assigned(x, (0, 1)) , Assigned('blank', (1, 1)), clock(swaptimer, min_swaps)]
        swap8 = [Assigned('blank', (0, 1)) , Assigned(x, (1, 1)) , ~(Assigned(x, (0, 1))) , ~(Assigned('blank', (1, 1))), swapped((0, 1), (1, 1), swaptimer)]

        swap9 = [Swap_pos3pos6_obj , Assigned(x, (0, 2)) , Assigned('blank', (1, 2)), clock(swaptimer, min_swaps)]
        swap10= [Assigned('blank', (0, 2)) , Assigned(x, (1, 2)) , ~(Assigned(x, (0, 2))) , ~(Assigned('blank', (1, 2))), swapped((0, 2), (1, 2), swaptimer)]

        swap11 = [Swap_pos4pos5_obj , Assigned(x, (1, 0)) , Assigned('blank', (1, 1)), clock(swaptimer, min_swaps)]
        swap12 = [ Assigned('blank', (1, 0)) , Assigned(x, (1, 1)) , ~(Assigned(x, (1, 0))) , ~(Assigned('blank', (1, 1))), swapped((1, 0), (1, 1), swaptimer)]

        swap13 = [Swap_pos4pos7_obj , Assigned(x, (1, 0)) , Assigned('blank', (2, 0)), clock(swaptimer, min_swaps)]
        swap14 = [Assigned('blank', (1, 0)) , Assigned(x, (2, 0)) , ~(Assigned(x, (1, 0))) , ~(Assigned('blank', (2, 0))), swapped((1, 0), (2, 0), swaptimer)]

        swap15 = [Swap_pos5pos6_obj , Assigned(x, (1, 1)) , Assigned('blank', (1, 2)), clock(swaptimer, min_swaps)]
        swap16 =[Assigned('blank', (1, 1)) , Assigned(x, (1, 2)) , ~(Assigned(x, (1, 1))) , ~(Assigned('blank', (1, 2))), swapped((1, 1), (1, 2), swaptimer)]

        swap17= [Swap_pos5pos8_obj , Assigned(x, (1, 1)) , Assigned('blank', (2, 1)), clock(swaptimer, min_swaps)]
        swap18 = [Assigned('blank', (1, 1)) , Assigned(x, (2, 1)) , ~(Assigned(x, (1, 1))) , ~(Assigned('blank', (2, 1))), swapped((2, 1), (1, 1), swaptimer)]

        swap19= [Swap_pos6pos9_obj , Assigned(x, (1, 2)) , Assigned('blank', (2, 2)), clock(swaptimer, min_swaps)]
        swap20 = [Assigned('blank', (1, 2)) , Assigned(x, (2, 2)) , ~(Assigned(x, (1, 2))) , ~(Assigned('blank', (2, 2))), swapped((1, 2), (2, 2), swaptimer)]

        swap21 = [Swap_pos7pos8_obj , Assigned(x, (2, 0)) , Assigned('blank', (2, 1)), clock(swaptimer, min_swaps)]
        swap22 = [Assigned('blank', (2, 0)), Assigned(x, (2, 1)), ~(Assigned(x, (2, 0))), ~(Assigned('blank', (2, 1))), swapped((2, 0), (2, 1), swaptimer)]

        swap23= [Swap_pos8pos9_obj , Assigned(x, (2, 1)) , Assigned('blank', (2, 2)), clock(swaptimer, min_swaps)]
        swap24 = [Assigned('blank', (2, 1)) , Assigned(x, (2, 2)) , ~(Assigned(x, (2, 1))) , ~(Assigned('blank', (2, 2))), swapped((2, 1), (2, 2), swaptimer)]
        

        # if the swaptimer reaches the number of minimum swaps for the board, clock is no longer true.
        if swaptimer == min_swaps:
            E.add_constraint(~clock(swaptimer, min_swaps))
        else: 
            E.add_constraint(clock(swaptimer, min_swaps))

        # incrementing swaptimer when a swap between two tiles occur
        for pos1 in BOARD:
            for pos2 in BOARD:
                if pos1 != pos2:
                    if swapped(pos1, pos2, swaptimer):
                        swaptimer += 1


        E.add_constraint(And(swap1) >> And(swap2))
        E.add_constraint(And(swap3) >> And(swap4))
        E.add_constraint(And(swap5) >> And(swap6))
        E.add_constraint(And(swap7) >> And(swap8))
        E.add_constraint(And(swap9) >> And(swap10))
        E.add_constraint(And(swap11) >> And(swap12))
        E.add_constraint(And(swap13) >> And(swap14))
        E.add_constraint(And(swap15) >> And(swap16))
        E.add_constraint(And(swap17) >> And(swap18))
        E.add_constraint(And(swap19) >> And(swap20))
        E.add_constraint(And(swap21) >> And(swap22))
        E.add_constraint(And(swap23) >> And(swap24))

        E.add_constraint(And(swap2) >> And(swap1))
        E.add_constraint(And(swap4) >> And(swap3))
        E.add_constraint(And(swap6) >> And(swap5))
        E.add_constraint(And(swap8) >> And(swap7))
        E.add_constraint(And(swap10) >> And(swap9))
        E.add_constraint(And(swap12) >> And(swap11))
        E.add_constraint(And(swap14) >> And(swap13))
        E.add_constraint(And(swap16) >> And(swap15))
        E.add_constraint(And(swap18) >> And(swap17))
        E.add_constraint(And(swap20) >> And(swap19))
        E.add_constraint(And(swap22) >> And(swap21))
        E.add_constraint(And(swap24) >> And(swap23))
    

        return E


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
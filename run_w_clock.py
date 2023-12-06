from bauhaus import Encoding, proposition, constraint, Or, And
from bauhaus.utils import count_solutions, likelihood

from board import BOARD
from input_tiles import TILES, max_swaps

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

swaptimer = 0
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

    def __str__(self) -> str:
        return f"([[{self.pos1},{self.pos2},{self.pos3}],[{self.pos4},{self.pos5},{self.pos6}],[{self.pos7},{self.pos8},{self.pos9}]])"

@proposition(E)
class Assigned(Hashable): # checks if number is assigned to a position 
    def __init__(self, tile, pos, swaptimer) -> None:
        self.tile = tile
        self.pos = pos
        self.timer = swaptimer

    def __str__(self) -> str:
        return f"({self.tile} @ {self.pos} at time {self.timer})"
    

@proposition(E)
class clock(Hashable):
    def __init__(self, swaptimer, max_swaps) -> None:
        self.max_swaps = max_swaps
        self.swaptimer = swaptimer
    
    def __str__(self) -> str:
        return f"(The board is at time {self.swaptimer}.)"
    
@proposition(E)
class Swap_pos1pos2(Hashable):
    def __init__(self, pos1, pos2) -> None:
        self.pos1 = pos1
        self.pos2 = pos2

    def __repr__(self) -> str:
        return f"()" 
  


@proposition(E)
class Swap_pos1pos4(Hashable):
    def __init__(self, pos1, pos4) -> None:
        self.pos1 = pos1
        self.pos4 = pos4

    def __repr__(self) -> str:
        return f"()"

@proposition(E)
class Swap_pos2pos3(Hashable):
    def __init__(self, pos2, pos3) -> None:
        self.pos2 = pos2
        self.pos3 = pos3

    def __repr__(self) -> str:
        return f"()"

@proposition(E)
class Swap_pos2pos5(Hashable):
    def __init__(self, pos2, pos5) -> None:
        self.pos2 = pos2
        self.pos5 = pos5

    def __repr__(self) -> str:
        return f"()"

@proposition(E)
class Swap_pos3pos6(Hashable):
    def __init__(self, pos3, pos6) -> None:
        self.pos3 = pos3
        self.pos6 = pos6

    def __repr__(self) -> str:
        return f"()"

@proposition(E)
class Swap_pos4pos5(Hashable):
    def __init__(self, pos4, pos5) -> None:
        self.pos4 = pos4
        self.pos5 = pos5

    def __repr__(self) -> str:
        return f"()"
    
@proposition(E)
class Swap_pos4pos7(Hashable):
    def __init__(self, pos4, pos7) -> None:
        self.pos4 = pos4
        self.pos7 = pos7

    def __repr__(self) -> str:
        return f"()"
    
@proposition(E)
class Swap_pos5pos6(Hashable):
    def __init__(self, pos5, pos6) -> None:
        self.pos5 = pos5
        self.pos6 = pos6

    def __repr__(self) -> str:
        return f"()"

@proposition(E)
class Swap_pos5pos8(Hashable):
    def __init__(self, pos5, pos8) -> None:
        self.pos5 = pos5
        self.pos8 = pos8

    def __repr__(self) -> str:
        return f"()"
    
@proposition(E)
class Swap_pos6pos9(Hashable):
    def __init__(self, pos6, pos9) -> None:
        self.pos6 = pos6
        self.pos9 = pos9

    def __repr__(self) -> str:
        return f"()"

    
@proposition(E)
class Swap_pos7pos8(Hashable):
    def __init__(self, pos7, pos8) -> None:
        self.pos7 = pos7
        self.pos8 = pos8

    def __repr__(self) -> str:
        return f"()"
    
@proposition(E)
class Swap_pos8pos9(Hashable):
    def __init__(self, pos8, pos9) -> None:
        self.pos8 = pos8
        self.pos9 = pos9

    def __repr__(self):
        return f"()"


    
@proposition(E)
class swapped(Hashable):
    def __init__(self, pos1, pos2, swaptimer, time_updater, clock_updater) -> None:
        self.pos1 = pos1
        self.pos2 = pos2
        self.swaptimer = swaptimer
        self.time_updater = time_updater
        self.clock_updater = clock_updater

    def __str__(self) -> str:
        return f"(The tiles at positions {self.pos1} and {self.pos2} swapped at time {self.swaptimer})"

def time_updater(pos1, pos2, swaptimer, E):
    for pos in BOARD:
        if pos1 != pos and pos2 != pos:
            for tile in TILES:
                if(Assigned(tile, pos, swaptimer)):
                    E.add_constraint(Assigned(tile, pos, swaptimer+1))
                else:
                    E.add_constraint(~Assigned(tile, pos, swaptimer+1))
    return E

def clock_updater(E, swaptimer):
# if the swaptimer reaches the number of minimum swaps for the board, clock is no longer true.
    if swaptimer >= max_swaps:
        E.add_constraint(~clock(swaptimer, max_swaps))
    else: 
        E.add_constraint(clock(swaptimer, max_swaps))
    return E

# assign propositions to variables 
assigned_props = []
for t in TILES:
    for pos in BOARD:
        for i in range(max_swaps + 1):
            assigned_props.append(Assigned(t, pos, i))

#assigned_props = [Assigned(tile, pos, swaptimer) for tile, pos in zip(TILES, BOARD)]
swapped_props = []
for pos1 in BOARD:
    for pos2 in BOARD:
        if pos1 != pos2:
            for i in range(max_swaps + 1):
                swapped_props.append(swapped(pos1, pos2, i, time_updater(pos1, pos2, i, E), clock_updater(E, i)))



# instantiate objects for other swap propositions

# Swap_pos1pos2_obj = Swap_pos1pos2(pos1=(0, 0), pos2=(0, 1))
# Swap_pos1pos4_obj = Swap_pos1pos4(pos1=(0, 0), pos4=(1, 0))
# Swap_pos2pos3_obj = Swap_pos2pos3(pos2=(0, 1), pos3=(0, 2))
# Swap_pos2pos5_obj = Swap_pos2pos5(pos2=(0, 1), pos5=(1, 1))
# Swap_pos3pos6_obj = Swap_pos3pos6(pos3=(0, 2), pos6=(1, 2))
# Swap_pos4pos5_obj = Swap_pos4pos5(pos4=(1, 0), pos5=(1, 1))
# Swap_pos4pos7_obj = Swap_pos4pos7(pos4=(1, 0), pos7=(2, 0))
# Swap_pos5pos6_obj = Swap_pos5pos6(pos5=(1, 1), pos6=(1, 2))
# Swap_pos5pos8_obj = Swap_pos5pos8(pos5=(1, 1), pos8=(2, 1))
# Swap_pos6pos9_obj = Swap_pos6pos9(pos6=(1, 2), pos9=(2, 2))
# Swap_pos7pos8_obj = Swap_pos7pos8(pos7=(2, 0), pos8=(2, 1))
# Swap_pos8pos9_obj = Swap_pos8pos9(pos8=(2, 1), pos9=(2, 2))


    

#w = goal_state()
pb = Puzzle_Board(TILES[0], TILES[1], TILES[2], TILES[3], TILES[4], TILES[5], TILES[6], TILES[7], TILES[8])
win = Puzzle_Board('1', '2', '3', '4', '5', '6', '7', '8', 'blank')

# Assigned(pb.pos1, (0, 0))
# Assigned(pb.pos2, (0, 1))
# Assigned(pb.pos3, (0, 2))
# Assigned(pb.pos4, (1, 0))
# Assigned(pb.pos5, (1, 1))
# Assigned(pb.pos6, (1, 2))
# Assigned(pb.pos7, (2, 0))
# Assigned(pb.pos8, (2, 1))
# Assigned(pb.pos9, (2, 2))





def timer_add(time):
    ''' incrementing swaptimer when a swap between two tiles occur
    '''
    new_time = time + 1
    return new_time




def build_theory(swaptimer):
    # Encoding that will store all of your constraints
    #Construct initial board
    for i in range(3):
        for j in range(3):
            if(board[i][j] == '1'):
                E.add_constraint(Assigned('1', (i, j), 0))
                for tile in TILES:
                    if tile != '1':
                        E.add_constraint(~Assigned(tile, (i, j), 0))
            elif(board[i][j] == '2'):
                E.add_constraint(Assigned('2',(i, j), 0))
                for tile in TILES:
                    if tile != '2':
                        E.add_constraint(~Assigned(tile, (i, j), 0))
            elif(board[i][j] == '3'):
                E.add_constraint(Assigned('3', (i, j), 0))
                for tile in TILES:
                    if tile != '3':
                        E.add_constraint(~Assigned(tile, (i, j), 0))
            elif(board[i][j] == '4'):
                E.add_constraint(Assigned('4', (i, j), 0))
                for tile in TILES:
                    if tile != '4':
                        E.add_constraint(~Assigned(tile, (i, j), 0))
            elif(board[i][j] == '5'):
                E.add_constraint(Assigned('5', (i, j), 0))
                for tile in TILES:
                    if tile != '5':
                        E.add_constraint(~Assigned(tile, (i, j), 0))
            elif(board[i][j] == '6'):
                E.add_constraint(Assigned('6', (i, j), 0))
                for tile in TILES:
                    if tile != '6':
                        E.add_constraint(~Assigned(tile, (i, j), 0))
            elif(board[i][j] == '7'):
                E.add_constraint(Assigned('7', (i, j), 0))
                for tile in TILES:
                    if tile != '7':
                        E.add_constraint(~Assigned(tile, (i, j), 0))
            elif(board[i][j] == '8'):
                E.add_constraint(Assigned('8', (i, j), 0))
                for tile in TILES:
                    if tile != '8':
                        E.add_constraint(~Assigned(tile, (i, j), 0))
            elif(board[i][j] == 'blank'):
                E.add_constraint(Assigned('blank', (i, j), 0))
                for tile in TILES:
                    if tile != 'blank':
                        E.add_constraint(~Assigned(tile, (i, j), 0))
            else:
                print("Error in setting up the board")




    # The swaptimer keeps track of the number of swaps that occur
    
    for i in range(max_swaps + 1):
        # All tiles need to be in their correct positions to solve the puzzle and the clock needs to be at the correct time as stated in the input_tiles file.
        E.add_constraint(And(Assigned('1', (0, 0), i), Assigned('2', (0, 1), i), Assigned('3', (0, 2), i) , Assigned('4', (1, 0), i), 
                         Assigned('5', (1, 1), i), Assigned('6', (1, 2), i), Assigned('7', (2, 0), i), Assigned('8', (2, 1), i), 
                         Assigned('blank', (2, 2), i), ~clock(swaptimer, max_swaps)) >> win)
    
        #Has to go both ways,  a win implies tiles are in correct position
        E.add_constraint(win >> And(Assigned('1', (0, 0), i), Assigned('2', (0, 1), i), Assigned('3', (0, 2), i) , Assigned('4', (1, 0), i), 
                        Assigned('5', (1, 1), i), Assigned('6', (1, 2), i), Assigned('7', (2, 0), i), Assigned('8', (2, 1), i), 
                        Assigned('blank', (2, 2), i), ~clock(swaptimer, max_swaps)))
    
    # makes sure only one tile is always assigned to one position.
    # for t1 in TILES:
    #     for t2 in TILES:
    #         if t1!= t2:
    #             for pos in BOARD:
    #                 E.add_constraint(Assigned(t1, pos) >> ~Assigned(t2, pos))


    #This swaps the tiles
    for x in TILES:
        
        swap1 = [Assigned(x, (0, 0), swaptimer), Assigned('blank', (0, 1), swaptimer), clock(swaptimer, max_swaps)]
        swap2 = [Assigned('blank', (0, 0), swaptimer+1), Assigned(x, (0, 1), swaptimer+1), swapped((0, 0), (0, 1), timer_add(swaptimer), time_updater((0, 0), (0, 1), swaptimer, E), clock_updater(E, swaptimer + 1))]

        swap3 = [Assigned(x, (0, 0), swaptimer), Assigned('blank', (1, 0), swaptimer), clock(swaptimer, max_swaps)]
        swap4 = [Assigned('blank', (0, 0), swaptimer+1) , Assigned(x, (1, 0), swaptimer+1), swapped((0, 0), (1, 0), timer_add(swaptimer), time_updater((0, 0), (1, 0), swaptimer, E), clock_updater(E, swaptimer + 1))]

        swap5 = [ Assigned(x, (0, 1), swaptimer) , Assigned('blank', (0, 2), swaptimer), clock(swaptimer, max_swaps)]
        swap6 = [Assigned('blank', (0, 1), swaptimer+1) , Assigned(x, (0, 2), swaptimer+1), swapped((0, 1), (0, 2), timer_add(swaptimer), time_updater((0, 1), (0, 2), swaptimer, E), clock_updater(E, swaptimer + 1))]

        swap7 = [Assigned(x, (0, 1), swaptimer) , Assigned('blank', (1, 1), swaptimer), clock(swaptimer, max_swaps)]
        swap8 = [Assigned('blank', (0, 1), swaptimer+1) , Assigned(x, (1, 1), swaptimer+1), swapped((0, 1), (1, 1), timer_add(swaptimer), time_updater((0, 1), (1, 1), swaptimer, E), clock_updater(E, swaptimer + 1))]

        swap9 = [Assigned(x, (0, 2), swaptimer) , Assigned('blank', (1, 2), swaptimer), clock(swaptimer, max_swaps)]
        swap10 = [Assigned('blank', (0, 2), swaptimer+1) , Assigned(x, (1, 2), swaptimer+1), swapped((0, 2), (1, 2), timer_add(swaptimer), time_updater((0, 2), (1, 2), swaptimer, E), clock_updater(E, swaptimer + 1))]

        swap11 = [Assigned(x, (1, 0), swaptimer) , Assigned('blank', (1, 1), swaptimer), clock(swaptimer, max_swaps)]
        swap12 = [Assigned('blank', (1, 0), swaptimer+1) , Assigned(x, (1, 1), swaptimer+1), swapped((1, 0), (1, 1), timer_add(swaptimer), time_updater((1, 0), (1, 1), swaptimer, E), clock_updater(E, swaptimer + 1))]

        swap13 = [Assigned(x, (1, 0), swaptimer) , Assigned('blank', (2, 0), swaptimer), clock(swaptimer, max_swaps)]
        swap14 = [Assigned('blank', (1, 0), swaptimer+1) , Assigned(x, (2, 0), swaptimer+1), swapped((1, 0), (2, 0), timer_add(swaptimer), time_updater((1, 0), (2, 0),swaptimer, E), clock_updater(E, swaptimer + 1))]

        swap15 = [Assigned(x, (1, 1), swaptimer) , Assigned('blank', (1, 2), swaptimer), clock(swaptimer, max_swaps)]
        swap16 = [Assigned('blank', (1, 1), swaptimer+1) , Assigned(x, (1, 2), swaptimer+1), swapped((1, 1), (1, 2), timer_add(swaptimer), time_updater((2, 1), (2, 2), swaptimer, E), clock_updater(E, swaptimer + 1))]

        swap17 = [Assigned(x, (1, 1), swaptimer) , Assigned('blank', (2, 1), swaptimer), clock(swaptimer, max_swaps)]
        swap18 = [Assigned('blank', (1, 1), swaptimer+1) , Assigned(x, (2, 1), swaptimer+1), swapped((2, 1), (1, 1), timer_add(swaptimer), time_updater((2, 1), (1, 1), swaptimer, E), clock_updater(E, swaptimer + 1))]

        swap19 = [Assigned(x, (1, 2), swaptimer) , Assigned('blank', (2, 2), swaptimer), clock(swaptimer, max_swaps)]
        swap20 = [Assigned('blank', (1, 2), swaptimer+1) , Assigned(x, (2, 2), swaptimer+1), swapped((1, 2), (2, 2), timer_add(swaptimer), time_updater((1, 2), (2, 2), swaptimer, E), clock_updater(E, swaptimer + 1))]

        swap21 = [Assigned(x, (2, 0), swaptimer) , Assigned('blank', (2, 1), swaptimer), clock(swaptimer, max_swaps)]
        swap22 = [Assigned('blank', (2, 0), swaptimer+1), Assigned(x, (2, 1), swaptimer+1), swapped((2, 0), (2, 1), timer_add(swaptimer), time_updater((2, 0), (2, 1), swaptimer, E), clock_updater(E, swaptimer + 1))]

        swap23 = [Assigned(x, (2, 1), swaptimer) , Assigned('blank', (2, 2), swaptimer), clock(swaptimer, max_swaps)]
        swap24 = [Assigned('blank', (2, 1), swaptimer+1) , Assigned(x, (2, 2), swaptimer+1), swapped((2, 1), (2, 2), timer_add(swaptimer), time_updater((2, 1), (2, 2), swaptimer, E), clock_updater(E, swaptimer + 1))]
        

        


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

    T = build_theory(swaptimer)
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
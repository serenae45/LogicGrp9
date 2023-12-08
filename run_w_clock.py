from bauhaus import Encoding, proposition, constraint, Or, And
from bauhaus.utils import count_solutions, likelihood

from board import BOARD
from input_tiles import TILES, max_swaps

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

E = Encoding()

# This variable keeps track of the time, which is the amount of swaps which have occured.
swaptimer = 0
# This board variable takes all the input positions and assigns them to this list
#  which can then be used for indexing to initialize the board at time 0.
board = [[TILES[0], TILES[1], TILES[2]], [TILES[3], TILES[4], TILES[5]], [TILES[6], TILES[7], TILES[8]]]


class Hashable:
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, __value: object) -> bool:
        return hash(self) == hash(__value)

    def __repr__(self):
        return str(self)

# slide puzzle propositions
@proposition(E)
class Assigned(Hashable):
    """Checks if a number is assigned to a position at a given time."""
    def __init__(self, tile, pos, swaptimer) -> None:
        self.tile = tile
        self.pos = pos
        self.timer = swaptimer

    def __str__(self) -> str:
        return f"\n({self.tile} @ {self.pos} at time {self.timer})"

@proposition(E)
class Clock(Hashable):
    """Represents the time of the board."""
    def __init__(self, swaptimer, max_swaps) -> None:
        self.max_swaps = max_swaps
        self.swaptimer = swaptimer
    
    def __str__(self) -> str:
        return f"(The board has reached its maximum number of swaps at time {self.swaptimer}.)"

@proposition(E)
class GoalState(Hashable):
    """Represents the goal state of the board."""
    def __init__(self, swaptimer) -> None:
        self.x = self
        self.time = swaptimer

    def __str__(self) -> str:
       return f"(The board is in its goal state at time {self.time}.)"

@proposition(E)
class Swapped(Hashable):
    """Represents a swap between two positions."""
    def __init__(self, pos1, pos2, swaptimer, board_updater, clock_updater) -> None:
        self.pos1 = pos1
        self.pos2 = pos2
        self.swaptimer = swaptimer
        self.board_updater = board_updater
        self.clock_updater = clock_updater

    def __str__(self) -> str:
        return f"\n(The tiles at positions {self.pos1} and {self.pos2} swapped at time {self.swaptimer})"

def board_updater(t1, t2, pos1, pos2, swaptimer, E):
    """Updates the time based on tile positions after a swap."""
    for tile0 in TILES:
            if t1!= tile0:
                E.add_constraint(~Assigned(tile0, pos1, swaptimer+1))
            if t2 != tile0:
                E.add_constraint(~Assigned(tile0, pos2, swaptimer+1))
    for pos in BOARD:
        if pos1 != pos and pos2 != pos:
            for tile1 in TILES:
                if(Assigned(tile1, pos, swaptimer)):
                    E.add_constraint(Assigned(tile1, pos, swaptimer+1))
                    for tile2 in TILES:
                        if tile2 != tile1:
                            E.add_constraint(~Assigned(tile2, pos, swaptimer+1))
                else:
                    E.add_constraint(~Assigned(tile1, pos, swaptimer+1))
    return E

def clock_updater(E, swaptimer):
    """Updates the clock based on the current swaptimer."""
    if swaptimer >= max_swaps:
        E.add_constraint(Clock(swaptimer, max_swaps))
    else: 
        E.add_constraint(~Clock(swaptimer, max_swaps))
    return E

# assign propositions to variables 
assigned_props = []
for t in TILES:
    for pos in BOARD:
        for i in range(max_swaps + 1):
            assigned_props.append(Assigned(t, pos, i))

swapped_props = []
for pos1 in BOARD:
    for pos2 in BOARD:
        if pos1 != pos2:
            for t1 in TILES:
                    if t1!= 'blank':
                        for i in range(max_swaps + 1):
                            swapped_props.append(Swapped(pos1, pos2, i, board_updater(t1, 'blank', pos1, pos2, i, E), clock_updater(E, i)))

w = GoalState(swaptimer)

def timer_add(time):
    """Increments swaptimer when a swap between two tiles occurs."""
    new_time = time + 1
    return new_time



def build_theory(swaptimer):
    '''Below the for loops initialize the board with the input tiles at time 0.'''
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
    
    
    # All tiles need to be in their correct positions to solve the puzzle and the clock needs to be at the correct time as stated in the input_tiles file.
    E.add_constraint(And(
                    Assigned('1', (0, 0), max_swaps), Assigned('2', (0, 1), max_swaps), Assigned('3', (0, 2), max_swaps) , Assigned('4', (1, 0), max_swaps), 
                    Assigned('5', (1, 1), max_swaps), Assigned('6', (1, 2), max_swaps), Assigned('7', (2, 0), max_swaps), Assigned('8', (2, 1), max_swaps), 
                    Assigned('blank', (2, 2), max_swaps), Clock(swaptimer, max_swaps)) >> w
                    )
    
    #Has to go both ways,  a win implies tiles are in correct position
    E.add_constraint(w(swaptimer) >> And(
                    Assigned('1', (0, 0), max_swaps), Assigned('2', (0, 1), max_swaps), Assigned('3', (0, 2), max_swaps) , Assigned('4', (1, 0), max_swaps), 
                    Assigned('5', (1, 1), max_swaps), Assigned('6', (1, 2), max_swaps), Assigned('7', (2, 0), max_swaps), Assigned('8', (2, 1), max_swaps), 
                    Assigned('blank', (2, 2), max_swaps))
                    )
    



    #This swaps the tiles
    for tile in TILES:
        for row in range(3):
            for col in range(3):
                if board[row][col] == tile:
                    if col + 1 < 3:  # Check if the swap is within the board bounds
                        swap1 = [Assigned(tile, (row, col), swaptimer), Assigned('blank', (row, col + 1), swaptimer), ~Clock(swaptimer, max_swaps)]
                        swap2 = [Assigned('blank', (row, col), swaptimer + 1), Assigned(tile, (row, col + 1), swaptimer + 1),
                                Swapped((row, col), (row, col + 1), timer_add(swaptimer), board_updater((row, col), (row, col + 1), swaptimer, E),
                                        clock_updater(E, swaptimer + 1))]
                        
                        E.add_constraint(And(swap1) >> And(swap2))
                        E.add_constraint(And(swap2) >> And(swap1))

                    if row + 1 < 3:  # Check if the swap is within the board bounds
                        swap3 = [Assigned(tile, (row, col), swaptimer), Assigned('blank', (row + 1, col), swaptimer), ~Clock(swaptimer, max_swaps)]
                        swap4 = [Assigned('blank', (row, col), swaptimer + 1), Assigned(tile, (row + 1, col), swaptimer + 1),
<<<<<<< HEAD
                                Swapped((row, col), (row + 1, col), timer_add(swaptimer), board_updater((row, col), (row + 1, col), swaptimer, E),
=======
                                Swapped((row, col), (row + 1, col), timer_add(swaptimer), board_updater('blank', tile, (row, col), (row + 1, col), swaptimer, E),
>>>>>>> e04c9aeb632075085b12b46d18807dcc76894e10
                                        clock_updater(E, swaptimer + 1))]
                        
                        E.add_constraint(And(swap3) >> And(swap4))
                        E.add_constraint(And(swap4) >> And(swap3))

                    if col - 1 >= 0:  # Check if the swap is within the board bounds
                        swap5 = [Assigned(tile, (row, col), swaptimer), Assigned('blank', (row, col - 1), swaptimer), ~Clock(swaptimer, max_swaps)]
                        swap6 = [Assigned('blank', (row, col), swaptimer + 1), Assigned(tile, (row, col - 1), swaptimer + 1),
                                Swapped((row, col), (row, col - 1), timer_add(swaptimer), board_updater((row, col), (row, col - 1), swaptimer, E),
                                        clock_updater(E, swaptimer + 1))]
                        
                        E.add_constraint(And(swap5) >> And(swap6))
                        E.add_constraint(And(swap6) >> And(swap5))

                    if row - 1 >= 0:  # Check if the swap is within the board bounds
                        swap7 = [Assigned(tile, (row, col), swaptimer), Assigned('blank', (row - 1, col), swaptimer), ~Clock(swaptimer, max_swaps)]
                        swap8 = [Assigned('blank', (row, col), swaptimer + 1), Assigned(tile, (row - 1, col), swaptimer + 1),
                                Swapped((row, col), (row - 1, col), timer_add(swaptimer), board_updater((row, col), (row - 1, col), swaptimer, E),
                                        clock_updater(E, swaptimer + 1))]
                        
                        E.add_constraint(And(swap7) >> And(swap8))
                        E.add_constraint(And(swap8) >> And(swap7))


    return E


if __name__ == "__main__":
    T = build_theory(swaptimer)
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v, vn in zip([w, ~w], ['win', 'no win']):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()
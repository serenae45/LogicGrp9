
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood


from directions import DIRECTIONS
from board import BOARD
from tiles import TILES


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

'''
# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class BasicPropositions:

    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __repr__(self):
        return f"A.{self.data}"

# Different classes for propositions are useful because this allows for more dynamic constraint creation
# for propositions within that class. For example, you can enforce that "at least one" of the propositions
# that are instances of this class must be true by using a @constraint decorator.
# other options include: at most one, exactly one, at most k, and implies all.
# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html
@constraint.at_least_one(E)
@proposition(E)
class FancyPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"

'''



'''
# Call your variables whatever you want
a = BasicPropositions("a")
b = BasicPropositions("b")   
c = BasicPropositions("c")
d = BasicPropositions("d")
e = BasicPropositions("e")
# At least one of these will be true
x = FancyPropositions("x")
y = FancyPropositions("y")
z = FancyPropositions("z")
'''


# slide puzzle propositions 
@proposition(E)
class assigned(Hashable): # checks if number is assigned to a position 
    def __init__(self, tile, pos):
        self.tile = tile
        self.pos = pos

    def __str__(self) -> str:
        return f"({self.tile} @ {self.pos})"

@proposition(E) 
class correct(Hashable): # checks if a number is at the right position 
    def __init__(self, tile, pos):
        self.tile = tile
        self.pos = pos

    def __str__(self) -> str:
        return f"({self.tile} is at the correct position)"
    
@constraint.exactly_one(E) 
@proposition(E) 
class blank(Hashable): # checks if a position is blank 
    def __init__(self, pos):
        self.pos = pos

    def __str__(self) -> str:
        return f"({self.pos} is blank.)"
    
@proposition(E)
class above(Hashable): # checks if a position [p][q] above the blank tile is valid
    def __init__(self, pos):
        self.pos = pos

    def __str__(self) -> str:
        return f"(The position above the blank is a valid position on the board.)"

@proposition(E)
class can_swap(Hashable): # checks if tile can move into a position (position has to be blank)
    def __init__(self, pos, d):
        self.pos = pos
        self.d = d
    
    def __str__(self) -> str:
        return f"({self.pos} can move {self.d}.)"
    



# assign propositions to variables 
board = [[1,2,3], [4,5,6], [7,8,"empty_box"]] # test input board 

assigned_props = []
for t in TILES:
    for pos in BOARD:
        assigned_props.append(assigned(t, pos))

correct_props = []
for t in TILES:
    for pos in BOARD:
        correct_props.append(correct(t, pos))

blank_props = []
for pos in BOARD:
    blank_props.append(blank(pos))

above_props = []
length = len(BOARD)
for i in range(length):
        if i >= 3:
            above_props.append(above(BOARD[i-3]))

'''
# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    # Add custom constraints by creating formulas with the variables you created. 
    E.add_constraint((a | b) & ~x)
    # Implication
    E.add_constraint(y >> z)
    # Negate a formula
    E.add_constraint(~(x & y))
    # You can also add more customized "fancy" constraints. Use case: you don't want to enforce "exactly one"
    # for every instance of BasicPropositions, but you want to enforce it for a, b, and c.:
    constraint.add_exactly_one(E, a, b, c)

    return E

'''

def build_theory():
    # The initial tile has to be a blank in order to swap with a target tile
    for pos in BOARD:
        E.add_constraint(can_swap(pos, d) for d in DIRECTIONS >> blank(pos))

    # A tile can only swap with a position above, below, or beside it that is on the board
    for pos in BOARD:
        E.add_constraint(can_swap(pos, d) for d in DIRECTIONS >> (above(pos) | below(pos) | left(pos) | right(pos)))
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

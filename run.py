
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

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

# slide puzzle propositions 
@proposition(E)
class assigned(num, pos): # checks if number is assigned to a position 
    def __init__(self, num, pos):
        self.num = num
        self.pos = pos

    def __str__(self) -> str:
        return f"({self.num} @ {self.pos})"

@proposition(E) 
class correct(num, pos): # checks if a number is at the right position 
    def __init__(self, num, pos):
        self.num = num
        self.pos = pos

    def __str__(self) -> str:
        return f"({self.num} is at the correct position)"
    
@constraint.exactly_one(E) 
@proposition(E) 
class blank(i, j): # checks if a position is blank 
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __str__(self) -> str:
        return f"({self.i}, {self.j} is blank."


# assign propositions to variables 
board = [[1,2,3], [4,5,6], [7,8,"empty_box"]] # test input board 
assigned_props = []

for i in board:
    for j in i: 
        assigned_props.append(Assigned(j, [i,j])) # not sure if the indexing is right here 
        
    
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


if __name__ == "__main__":

    T = example_theory()
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

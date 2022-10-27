
from bauhaus import Encoding, proposition, constraint, print_theory
from bauhaus.utils import count_solutions, likelihood

# Encoding that will store all of your constraints
E = Encoding()

DICE = [1]#, 2, 3, 4]
SIDE = [1, 2, 3, 4, 5, 6]
COLOURS = ['red', 'green', 'blue', 'yellow']
DIRECTION = ['top', 'bottom', 'left', 'right', 'front', 'back']


PROPOSITIONS = []

class Unique(object):
    def __hash__(self):
        return hash(str(self))
    def __eq__(self, other):
        return hash(self) == hash(other)
    def __repr__(self):
        return str(self)
    def __str__(self):
        assert False, "You need to define the __str__ function on a proposition class"


# Proposition for a dice side to have a colour
@proposition(E)
class DiceSideCol(Unique):
    def __init__(self, dice, side, colour):
        self.dice = dice
        self.side = side
        self.colour = colour

    def __str__(self):
        return f"d{self.dice}:s{self.side}={self.colour}"

# Proposition for a dice side to be pointing in a particular orientation
@proposition(E)
class DiceSideDir(Unique):
    def __init__(self, dice, side, direction):
        self.dice = dice
        self.side = side
        self.direction = direction

    def __str__(self):
        return f"d{self.dice}:s{self.side}={self.direction}"

# Dice in a slot
@proposition(E)
class DiceInSlot(Unique):
    def __init__(self, dice, slot):
        self.dice = dice
        self.slot = slot

    def __str__(self):
        return f"d{self.dice} in slot-{self.slot}"


###############
# CONSTRAINTS #
###############

# Each dice must have the side appear in exactly one direction
for dice in DICE:
    for side in SIDE:
        constraint.add_exactly_one(E, [DiceSideDir(dice, side, direction) for direction in DIRECTION])

# Each direction must have exactly one side
for dice in DICE:
    for direction in DIRECTION:
        constraint.add_exactly_one(E, [DiceSideDir(dice, side, direction) for side in SIDE])

# Opposite sides must add up to 7
for dice in DICE:
    for side1 in SIDE:
        for side2 in SIDE:
            if side1 + side2 == 7:
                E.add_constraint(DiceSideDir(dice, side1, 'top') >> DiceSideDir(dice, side2, 'bottom'))
                E.add_constraint(DiceSideDir(dice, side1, 'bottom') >> DiceSideDir(dice, side2, 'top'))
                E.add_constraint(DiceSideDir(dice, side1, 'left') >> DiceSideDir(dice, side2, 'right'))
                E.add_constraint(DiceSideDir(dice, side1, 'right') >> DiceSideDir(dice, side2, 'left'))
                E.add_constraint(DiceSideDir(dice, side1, 'front') >> DiceSideDir(dice, side2, 'back'))
                E.add_constraint(DiceSideDir(dice, side1, 'back') >> DiceSideDir(dice, side2, 'front'))

# 1, 2, 3 must be clockwise around a corner
cw_horizontal = ['front', 'left', 'back', 'right']
cw_vertical = ['top', 'right', 'bottom', 'left']
cw_straight = ['top', 'front', 'bottom', 'back']
for dice in DICE:
    for i in range(4):
        E.add_constraint((DiceSideDir(dice, 1, 'top') & DiceSideDir(dice, 2, cw_horizontal[i])) >> DiceSideDir(dice, 3, cw_horizontal[(i+1)%4]))
        E.add_constraint((DiceSideDir(dice, 1, 'bottom') & DiceSideDir(dice, 2, cw_horizontal[i])) >> DiceSideDir(dice, 3, cw_horizontal[(i+3)%4]))
        E.add_constraint((DiceSideDir(dice, 1, 'left') & DiceSideDir(dice, 2, cw_straight[i])) >> DiceSideDir(dice, 3, cw_straight[(i+1)%4]))
        E.add_constraint((DiceSideDir(dice, 1, 'right') & DiceSideDir(dice, 2, cw_straight[i])) >> DiceSideDir(dice, 3, cw_straight[(i+3)%4]))
        E.add_constraint((DiceSideDir(dice, 1, 'front') & DiceSideDir(dice, 2, cw_vertical[i])) >> DiceSideDir(dice, 3, cw_vertical[(i+1)%4]))
        E.add_constraint((DiceSideDir(dice, 1, 'back') & DiceSideDir(dice, 2, cw_vertical[i])) >> DiceSideDir(dice, 3, cw_vertical[(i+3)%4]))



T = E.compile()
# E.introspect()

sol = T.solve()
# E.pprint(T, sol)
# E.introspect(sol)
# print_theory(sol)

# After compilation (and only after), you can check some of the properties
# of your model:
print("\nSatisfiable: %s" % T.satisfiable())
print("# Solutions: %d" % count_solutions(T))
# print("   Solution: %s" % T.solve())
print_theory(sol)
print()




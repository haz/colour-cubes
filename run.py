
from bauhaus import Encoding, proposition, constraint, print_theory
from bauhaus.utils import count_solutions, likelihood

from nnf import config
config.sat_backend = "kissat"

from viz import viz_all_dice

from diceconfigs import CONFIG as DICE_CONFIG

# Encoding that will store all of your constraints
E = Encoding()

DICE = [1, 2, 3, 4]
SLOTS = [1, 2, 3, 4]
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
        return f"col(d{self.dice}:s{self.side})={self.colour}"

# Proposition for a dice side to be pointing in a particular orientation
@proposition(E)
class DiceSideDir(Unique):
    def __init__(self, dice, side, direction):
        self.dice = dice
        self.side = side
        self.direction = direction

    def __str__(self):
        return f"dir(d{self.dice}:s{self.side})={self.direction}"

# Dice in a slot
@proposition(E)
class DiceInSlot(Unique):
    def __init__(self, dice, slot):
        self.dice = dice
        self.slot = slot

    def __str__(self):
        return f"slot(d{self.dice})={self.slot}"

@proposition(E)
class BoxColour(Unique):
    def __init__(self, slot, direction, colour):
        self.slot = slot
        self.direction = direction
        self.colour = colour

    def __str__(self):
        return f"box(slot-{self.slot} @ dir-{self.direction})={self.colour}"


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

# Each dice side must have exactly one colour
for dice in DICE:
    for side in SIDE:
        constraint.add_exactly_one(E, [DiceSideCol(dice, side, colour) for colour in COLOURS])

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


# Specific dice configuration
for dice in DICE_CONFIG:
    for (d,s,c) in DICE_CONFIG[dice]:
        E.add_constraint(DiceSideCol(d,s,c))


####################
# Slot constraints
#####################

# A dice can only be in one slot
for dice in DICE:
    constraint.add_exactly_one(E, [DiceInSlot(dice, slot) for slot in SLOTS])
for slot in SLOTS:
    constraint.add_exactly_one(E, [DiceInSlot(dice, slot) for dice in DICE])

# If a dice of a particular configuration is in a slot, then the colour facing each direction is defined
for dice in DICE:
    for slot in SLOTS:
        for col in COLOURS:
            for direction in set(DIRECTION) - set(['left', 'right']):
                E.add_constraint((DiceSideCol(dice, direction, col) & DiceSideDir(dice, side, direction) & DiceInSlot(dice, slot)) >> BoxColour(slot, direction, col))

# A box side colour must have exactly one colour
for slot in SLOTS:
    for direction in DIRECTION:
        constraint.add_exactly_one(E, [BoxColour(slot, direction, colour) for colour in COLOURS])


#########################
# Rules of the game
#########################

# For all of the sides (other than left and right), the box colours are unique
for direction in set(DIRECTION) - set(['left', 'right']):
    for s1 in SLOTS:
        for s2 in SLOTS:
            if s1 != s2:
                for col in COLOURS:
                    E.add_constraint(~BoxColour(s1, direction, col) | ~BoxColour(s2, direction, col))





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
print(viz_all_dice(sol, DICE))
print()

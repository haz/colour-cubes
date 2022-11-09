
from sty import fg, bg

COLS = {
    'red': bg.red + fg.white,
    'green': bg.green + fg.black,
    'blue': bg.li_blue + fg.white,
    'yellow': bg.li_yellow + fg.black
}

def viz_dice(sol, dice):
    side_mapping = {}
    col_mapping = {}
    for k in sol:
        if f'dir(d{dice}' == str(k)[:6] and sol[k]:
            side_mapping[str(k).split('=')[1]] = str(k)[8]
        if f'col(d{dice}' == str(k)[:6] and sol[k]:
            col_mapping[str(k)[8]] = COLS[str(k).split('=')[1]]

    def f(dir):
        return col_mapping[side_mapping[dir]]+side_mapping[dir]+fg.rs+bg.rs

    return [
        f"\tdice {dice}",
        '',
        f"\t {f('top')}  ",
        f"\t{f('left')}{f('front')}{f('right')} ",
        f"\t {f('bottom')}  ",
        f"\t {f('back')}  "
    ]

def extract_dice_order(sol, dices):
    """Gets the order of the dice in the slots from the solution"""
    dice_order = {}
    for k in sol:
        # If it is a slot proposition and the proposition is set to true
        if 'slot(d' in str(k) and sol[k]:
            # Assign the dice that is in the slot
            dice_order[str(k).split('=')[1]] = str(k)[6]
    # Return the dice in the order of the slots
    return [dice_order[str(s)] for s in range(1, len(dices)+1)]


def viz_all_dice(sol, dices):
    dice_order = extract_dice_order(sol, dices)
    dice_strings = [viz_dice(sol, d) for d in dice_order]
    dice_strings = [d for d in zip(*dice_strings)]
    return "\n".join(["\t".join(d) for d in dice_strings])



def dump_dice_details(sol, dice):
    """Prints out the details of a particular dice in the solution"""
    for var in sol:
        if (f'd{dice}' in str(var)) and sol[var]:
            print(var)


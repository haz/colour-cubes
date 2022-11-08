
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

def viz_all_dice(sol, dices):
    dice_strings = [viz_dice(sol, d) for d in dices]
    dice_strings = [d for d in zip(*dice_strings)]
    return "\n".join(["\t".join(d) for d in dice_strings])

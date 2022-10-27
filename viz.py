

def print_dice(sol, dice):
    side_mapping = {}
    for k in sol:
        if 'dir(' == str(k)[:4] and sol[k]:
            side_mapping[str(k).split('=')[1]] = str(k)[8]
    print(f"dice {dice}:")
    print(f"  {side_mapping['top']}")
    print(f"{side_mapping['left']} {side_mapping['front']} {side_mapping['right']}")
    print(f"  {side_mapping['bottom']}")
    print(f"  {side_mapping['back']}")

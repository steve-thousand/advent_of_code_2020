def solve(puzzle_input):
    energy_levels = [[int(x) for x in row]
                     for row in puzzle_input.strip().split("\n")]

    goal_steps = 100
    step = 1
    total_flashes = 0
    while True:
        total_flashes_in_step = 0
        to_flash = set()
        for y, row in enumerate(energy_levels):
            for x, energy_level in enumerate(row):
                if energy_level == 9:
                    # flash
                    to_flash.add((x, y))
                else:
                    energy_levels[y][x] += 1
        already_flashed = set()
        while len(to_flash) > 0:
            total_flashes_in_step += len(to_flash)
            new_to_flash = set()
            for flash in to_flash:
                x_flash = flash[0]
                y_flash = flash[1]
                energy_levels[y_flash][x_flash] = 0
                already_flashed.add((x_flash, y_flash))
                for dy in range(-1, 2):
                    y_adjacent = y_flash + dy
                    for dx in range(-1, 2):
                        x_adjacent = x_flash + dx
                        if dy == 0 and dx == 0 or (x_adjacent, y_adjacent) in already_flashed or (x_adjacent, y_adjacent) in to_flash:
                            continue
                        if y_adjacent < 0 or y_adjacent > len(energy_levels) - 1 or x_adjacent < 0 or x_adjacent > len(energy_levels[0]) - 1:
                            continue
                        if energy_levels[y_adjacent][x_adjacent] == 9:
                            new_to_flash.add((x_adjacent, y_adjacent))
                        else:
                            energy_levels[y_adjacent][x_adjacent] += 1
            to_flash = new_to_flash

        total_flashes += total_flashes_in_step
        if step == goal_steps:
            # part 1
            print(total_flashes)

        if total_flashes_in_step == 100:
            # part 2
            print(step)
            break

        step += 1

    return


solve("""
1553421288
5255384882
1224315732
4258242274
1658564216
6872651182
5775552238
5622545172
8766672318
2178374835
""")

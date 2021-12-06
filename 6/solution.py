def simulate_days(starting_fishes, days):
    cycle_length = 7
    cycle_day = 0
    cycle_buckets = [0] * cycle_length
    for fish in starting_fishes:
        cycle_buckets[fish] += 1

    ready_queue = [0, 0]

    for day in range(0, days):
        birthing_fish = cycle_buckets[cycle_day]
        cycle_buckets[cycle_day] += ready_queue.pop(0)
        ready_queue.append(birthing_fish)
        cycle_day += 1
        cycle_day %= cycle_length

    return sum(cycle_buckets) + sum(ready_queue)


def solve(puzzle_input):
    starting_fishes = [int(x) for x in puzzle_input.strip().split(',')]

    # part 1
    print(simulate_days(starting_fishes, 80))

    # part 2
    print(simulate_days(starting_fishes, 256))

    return


solve("""
1,1,3,5,3,1,1,4,1,1,5,2,4,3,1,1,3,1,1,5,5,1,3,2,5,4,1,1,5,1,4,2,1,4,2,1,4,4,1,5,1,4,4,1,1,5,1,5,1,5,1,1,1,5,1,2,5,1,1,3,2,2,2,1,4,1,1,2,4,1,3,1,2,1,3,5,2,3,5,1,1,4,3,3,5,1,5,3,1,2,3,4,1,1,5,4,1,3,4,4,1,2,4,4,1,1,3,5,3,1,2,2,5,1,4,1,3,3,3,3,1,1,2,1,5,3,4,5,1,5,2,5,3,2,1,4,2,1,1,1,4,1,2,1,2,2,4,5,5,5,4,1,4,1,4,2,3,2,3,1,1,2,3,1,1,1,5,2,2,5,3,1,4,1,2,1,1,5,3,1,4,5,1,4,2,1,1,5,1,5,4,1,5,5,2,3,1,3,5,1,1,1,1,3,1,1,4,1,5,2,1,1,3,5,1,1,4,2,1,2,5,2,5,1,1,1,2,3,5,5,1,4,3,2,2,3,2,1,1,4,1,3,5,2,3,1,1,5,1,3,5,1,1,5,5,3,1,3,3,1,2,3,1,5,1,3,2,1,3,1,1,2,3,5,3,5,5,4,3,1,5,1,1,2,3,2,2,1,1,2,1,4,1,2,3,3,3,1,3,5
""")

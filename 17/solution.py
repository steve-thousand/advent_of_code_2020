# forgive me

def solve(puzzle_input):
    target_dimensions = [[int(y) for y in x[2:].split("..")] for x in puzzle_input.strip().replace(
        "target area: ", "").split(", ")]

    highest_point = max(target_dimensions[1])
    lowest_point = min(target_dimensions[1])
    max_y_velocity = -(lowest_point + 1)
    max_y = 0
    while max_y_velocity > 0:
        max_y += max_y_velocity
        max_y_velocity -= 1
    max_y_velocity = -(lowest_point + 1)

    # part 1
    print(max_y)

    nearest_point = min(target_dimensions[0])
    farthest_point = max(target_dimensions[0])
    min_x_velocity = 0
    while True:
        test_x = min_x_velocity
        farthest_x = 0
        while test_x > 0:
            farthest_x += test_x
            test_x -= 1
        if farthest_x >= nearest_point and farthest_x <= farthest_point:
            break
        min_x_velocity += 1

    max_x_velocity = farthest_point

    def test(x_velocity, y_velocity):
        x = 0
        y = 0
        while True:
            y += y_velocity
            x += x_velocity
            y_velocity -= 1
            if x_velocity > 0:
                x_velocity -= 1
            if x >= nearest_point and x <= farthest_point and y <= highest_point and y >= lowest_point:
                return True
            elif x > farthest_point or y < lowest_point:
                return False

    possible_velocities = []
    for y in range(-max_y_velocity - 1, max_y_velocity + 1):
        for x in range(min_x_velocity, max_x_velocity + 1):
            if test(x, y):
                possible_velocities.append((x, y))

    # part 2
    print(len(possible_velocities))

    return


solve("""
target area: x=81..129, y=-150..-108
""")

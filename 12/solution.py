def visit(location, locations_by_source, visited=set(), one_small_already_visited=False, allow_one_small_twice=False):
    paths = []
    visited.add(location)
    if location in locations_by_source:
        for possible_location in locations_by_source[location]:
            if possible_location == "start":
                continue
            if possible_location == "end":
                paths.append([possible_location])
                continue
            visited_copy = visited.copy()
            if possible_location.islower() and possible_location in visited and allow_one_small_twice and not one_small_already_visited:
                inner_paths = visit(possible_location, locations_by_source,
                                    visited_copy, True, allow_one_small_twice)
                paths.extend(inner_paths)
            elif possible_location.isupper() or possible_location not in visited:
                inner_paths = visit(possible_location, locations_by_source,
                                    visited_copy, one_small_already_visited, allow_one_small_twice)
                paths.extend(inner_paths)
    for path in paths:
        path.insert(0, location)
    return paths


def solve(puzzle_input):
    connections = [x.split("-") for x in puzzle_input.strip().split('\n')]

    locations_by_source = {}
    for connection in connections:
        source = connection[0]
        destination = connection[1]
        if source not in locations_by_source:
            locations_by_source[source] = []
        if destination not in locations_by_source:
            locations_by_source[destination] = []
        locations_by_source[source].append(destination)
        locations_by_source[destination].append(source)

    # part 1
    paths = visit("start", locations_by_source)
    print(len(paths))

    # part 2
    paths = visit("start", locations_by_source, allow_one_small_twice=True)
    print(len(paths))

    return


solve("""
CI-hb
IK-lr
vr-tf
lr-end
XP-tf
start-vr
lr-io
hb-qi
end-CI
tf-YK
end-YK
XP-lr
XP-vr
lr-EU
tf-CI
EU-vr
start-tf
YK-hb
YK-vr
start-EU
lr-CI
hb-XP
XP-io
tf-EU
""")

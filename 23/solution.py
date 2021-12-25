from copy import copy


class Room:

    @staticmethod
    def can_accept_amphipod(room, type):
        for i, space in enumerate(room):
            if space == ".":
                continue
            else:
                for j in range(i, len(room)):
                    if room[j] != type:
                        return False
        return True

    @staticmethod
    def can_leave_room(room, room_index, index):
        goal_room_index = ord(room[index]) - 65
        if goal_room_index == room_index:
            # amphipod is in right room, but does it need to move? is anything behind it?
            needs_to_move = False
            for i in range(index, len(room)):
                if room[i] != "." and room[i] != room[index]:
                    # something else is behind it that needs to get it
                    needs_to_move = True
            if not needs_to_move:
                return False

        # is there anything in front, blocking it?
        for i in range(index - 1, -1, -1):
            if room[i] != ".":
                return False
        return True

    @staticmethod
    def enter_room(room, type):
        steps = 0
        for i, space in enumerate(room):
            steps += 1
            if i == len(room) - 1:
                room[i] = type
            elif room[i + 1] != ".":
                room[i] = type
                return steps
        return steps

    @staticmethod
    def to_hallway_index(room_index):
        return (room_index + 1) * 2


class Hallway:
    @staticmethod
    def can_walk(hallway, start, destination):
        if start > destination:
            x = destination
            y = start
        else:
            x = start + 1
            y = destination + 1
        steps = 0
        for i in range(x, y):
            if hallway[i] != ".":
                return 0
            steps += 1
        return steps


class Amphipod:

    movement_energy = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000
    }

    @staticmethod
    def room_index_for_type(type):
        return ord(type) - 65


class BurrowState:

    def __init__(self, hallway, rooms):
        self.hallway = hallway
        self.rooms = rooms
        return

    def __copy__(self):
        new_hallway = [copy(room) for room in self.hallway]
        new_rooms = [room.copy() for room in self.rooms]
        return BurrowState(new_hallway, new_rooms)

    def key(self):
        return ''.join(self.hallway) + \
            ''.join([''.join(room) for room in self.rooms])

    @staticmethod
    def parse(puzzle_input):
        puzzle_input = puzzle_input.strip().replace(
            "#", "").replace(".", "").replace(" ", "").replace("\n", "")

        spaces_per_room = int(len(puzzle_input) / 4)
        rooms = []
        for room in range(0, 4):
            new_room = []
            for space in range(0, spaces_per_room):
                new_room.append(puzzle_input[(space * 4) + room])
            rooms.append(new_room)
        BurrowState.goal_rooms = [['A'] * spaces_per_room, ['B'] * spaces_per_room,
                                  ['C'] * spaces_per_room, ['D'] * spaces_per_room]

        return BurrowState(['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], rooms)


def attempt_hallway_move_to_room(burrow_state, net_energy, hallway_index, type):
    goal_room_index = Amphipod.room_index_for_type(type)
    if Room.can_accept_amphipod(burrow_state.rooms[goal_room_index], type):
        # is there a clear path?
        hallway_room_index = Room.to_hallway_index(goal_room_index)
        hallway_steps = Hallway.can_walk(
            burrow_state.hallway, hallway_index, hallway_room_index)
        if hallway_steps > 0:
            # home!
            new_burrow_state = copy(burrow_state)
            new_burrow_state.hallway[hallway_index] = '.'
            steps_in_room = Room.enter_room(
                new_burrow_state.rooms[goal_room_index], type)
            total_steps = hallway_steps + steps_in_room
            return (new_burrow_state, net_energy + (total_steps * Amphipod.movement_energy[type]))
    return None


def find_lowest_energy(burrow_state):
    frontier_states = [(burrow_state, 0, 0)]
    states_by_shortest_energy = {}

    while len(frontier_states) > 0:
        current = frontier_states.pop(0)
        burrow_state = current[0]
        net_energy = current[1]

        # print(str(len(states_by_shortest_energy.keys())) + " " + str(net_energy))

        if burrow_state.rooms == BurrowState.goal_rooms:
            return net_energy

        # determine all who can move
        movable_amphipods = []
        new_states = []

        # can anyone in hallway move back to their own room
        for i, space in enumerate(burrow_state.hallway):
            if space != '.':
                movable_amphipods.append((space, 'H', i))

        for r, room in enumerate(burrow_state.rooms):
            for s, space in enumerate(room):
                if space != ".":
                    if Room.can_leave_room(room, r, s):
                        movable_amphipods.append((space, r, s))

        if len(movable_amphipods) == 0:
            continue

        for movable_amphipod in movable_amphipods:
            if movable_amphipod[1] == 'H':
                new_state = attempt_hallway_move_to_room(
                    burrow_state, net_energy, movable_amphipod[2], movable_amphipod[0])
                if new_state is not None:
                    new_states.append(new_state)
            else:
                # move to hallway, all possible locations
                hallway_room_index = Room.to_hallway_index(movable_amphipod[1])
                potential_hallway_indeces = []

                # sweep left
                potential_hallway_index = hallway_room_index
                while True:
                    potential_hallway_index -= 1
                    if potential_hallway_index < 0 or burrow_state.hallway[potential_hallway_index] != '.':
                        # blocked, can go no further
                        break
                    else:
                        potential_hallway_indeces.append(
                            potential_hallway_index)

                # sweep right
                potential_hallway_index = hallway_room_index
                while True:
                    potential_hallway_index += 1
                    if potential_hallway_index > 10 or burrow_state.hallway[potential_hallway_index] != '.':
                        # blocked, can go no further
                        break
                    else:
                        potential_hallway_indeces.append(
                            potential_hallway_index)

                for potential_hallway_index in potential_hallway_indeces:
                    if potential_hallway_index == 2 or potential_hallway_index == 4 or potential_hallway_index == 6 or potential_hallway_index == 8:
                        continue
                    moves = movable_amphipod[2] + 1 + \
                        abs(hallway_room_index - potential_hallway_index)
                    new_burrow_state = copy(burrow_state)
                    new_burrow_state.hallway[potential_hallway_index] = movable_amphipod[0]
                    new_burrow_state.rooms[movable_amphipod[1]
                                           ][movable_amphipod[2]] = '.'
                    # distance = BurrowState.caculate_distance(new_burrow_state)
                    new_states.append(
                        (new_burrow_state, net_energy + (moves * Amphipod.movement_energy[movable_amphipod[0]])))
        for state in new_states:
            if state[0].key() not in states_by_shortest_energy or states_by_shortest_energy[state[0].key()] > state[1]:
                states_by_shortest_energy[state[0].key()] = state[1]
                frontier_states.append(state)
        frontier_states.sort(key=lambda x: x[1], reverse=False)

    return


def solve(puzzle_input):
    # part 1
    print(find_lowest_energy(BurrowState.parse(puzzle_input)))

    # part 2
    parts = puzzle_input.strip().split("\n")
    parts.insert(3,
                 """
    #D#C#B#A#
    #D#B#A#C#
    """)
    puzzle_input = '\n'.join(parts)
    print(find_lowest_energy(BurrowState.parse(puzzle_input)))

    return


solve("""
#############
#...........#
###D#C#D#B###
  #B#A#A#C#
  #########
""")

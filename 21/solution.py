def part1(positions):
    scores = [0, 0]

    rolls = 0
    die = 0
    player = 0
    while True:
        for i in range(0, 3):
            rolls += 1
            die += 1
            if die > 100:
                die %= 100
            positions[player] += die
        positions[player] %= 10
        scores[player] += positions[player] + 1
        if scores[player] >= 1000:
            break
        player += 1
        player %= 2

    # part 1
    print(min(scores) * rolls)


QUANTUM_POSITIONS_MEMO = {}


def dirac_game(positions):
    def calculate_next_quantum_positions(starting_position):
        global QUANTUM_POSITIONS_MEMO
        if starting_position in QUANTUM_POSITIONS_MEMO:
            return QUANTUM_POSITIONS_MEMO[starting_position]
        quantum_positions = []
        for x in range(0, 3):
            for y in range(0, 3):
                for z in range(0, 3):
                    quantum_position = starting_position + x + y + z + 3
                    quantum_position %= 10
                    quantum_positions.append(quantum_position)
        QUANTUM_POSITIONS_MEMO[starting_position] = quantum_positions
        return quantum_positions

    quantum_games = {
        (positions[0], positions[1], 0, 0, 0): 1
    }

    total_wins = [0, 0]

    while len(quantum_games) > 0:
        new_quantum_games = {}
        for game_state, count in quantum_games.items():
            player = game_state[4]
            next_player = (player + 1) % 2
            position = game_state[0 + player]
            quantum_positions = calculate_next_quantum_positions(position)
            for quantum_position in quantum_positions:
                new_positions = [game_state[0], game_state[1]]
                new_positions[player] = quantum_position
                new_scores = [game_state[2], game_state[3]]
                new_scores[player] += quantum_position + 1
                if new_scores[player] >= 21:
                    total_wins[player] += count
                else:
                    new_game_state = (
                        new_positions[0], new_positions[1], new_scores[0], new_scores[1], next_player)
                    if new_game_state not in new_quantum_games:
                        new_quantum_games[new_game_state] = 0
                    new_quantum_games[new_game_state] += count
        quantum_games = new_quantum_games

    print(max(total_wins))

    return


def solve(puzzle_input):
    positions = [int(x.split(": ")[1]) - 1
                 for x in puzzle_input.strip().split('\n')]
    part1(positions)

    positions = [int(x.split(": ")[1]) - 1
                 for x in puzzle_input.strip().split('\n')]
    dirac_game(positions)

    return


solve("""
Player 1 starting position: 2
Player 2 starting position: 10
""")

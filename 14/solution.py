MEMO = {}


def collapse_counts(counts_right, counts_left):
    for key, value in counts_right.items():
        if key not in counts_left:
            counts_left[key] = 0
        counts_left[key] += value
    return counts_left


def calculate_count_after_steps(sequence, steps, rules):
    if len(sequence) > 2:
        counts = {}
        for i, letter in enumerate(sequence):
            if i < len(sequence) - 1:
                next_letter = sequence[i + 1]
                partial_counts = calculate_count_after_steps(
                    letter + next_letter, steps, rules)
                if i != len(sequence) - 2:
                    partial_counts[next_letter] -= 1
                counts = collapse_counts(counts, partial_counts)
        return counts
    if steps == 0:
        counts = {}
        for letter in sequence:
            if letter not in counts:
                counts[letter] = 0
            counts[letter] += 1
        return counts
    memo_key = sequence + "_" + str(steps)
    if memo_key == "BB_1":
        x = 0
    if memo_key in MEMO:
        return MEMO[memo_key].copy()
    insert = rules[sequence]
    counts_left = calculate_count_after_steps(
        sequence[0] + insert, steps - 1, rules)
    counts_right = calculate_count_after_steps(
        insert + sequence[1], steps - 1, rules)
    # if steps == 1:
    if True:
        counts_right[insert] -= 1
    counts_left = collapse_counts(counts_left, counts_right)

    if memo_key == "BB_1":
        x = 0
    MEMO[memo_key] = counts_left
    return counts_left.copy()


def solve(puzzle_input):
    template = puzzle_input.strip().split('\n')[0]

    rules = {}
    for rule in puzzle_input.strip().split('\n\n')[1].split('\n'):
        rule = rule.split(' -> ')
        rules[rule[0]] = rule[1]

    # part 1
    counts = calculate_count_after_steps(template, 10, rules)
    print(max(counts.values()) - min(counts.values()))

    # part 2
    counts = calculate_count_after_steps(template, 40, rules)
    print(max(counts.values()) - min(counts.values()))

    return


solve("""
PKHOVVOSCNVHHCVVCBOH

NO -> B
PV -> P
OC -> K
SC -> K
FK -> P
PO -> P
FC -> V
KN -> V
CN -> O
CB -> K
NF -> K
CO -> F
SK -> F
VO -> B
SF -> F
PB -> F
FF -> C
HC -> P
PF -> B
OP -> B
OO -> V
OK -> N
KB -> H
PN -> V
PP -> N
FV -> S
BO -> O
HN -> C
FP -> F
BP -> B
HB -> N
VC -> F
PC -> V
FO -> O
OH -> S
FH -> B
HK -> B
BC -> F
ON -> K
FN -> N
NN -> O
PH -> P
KS -> H
HV -> F
BK -> O
NP -> S
CC -> H
KV -> V
NB -> C
NS -> S
KO -> V
NK -> H
HO -> C
KC -> P
VH -> C
VK -> O
CP -> K
BS -> N
BB -> F
VV -> K
SH -> O
SO -> N
VF -> K
NV -> K
SV -> O
NH -> C
VS -> N
OF -> N
SP -> C
HP -> O
NC -> V
KP -> B
KH -> O
SN -> S
CS -> N
FB -> P
OB -> H
VP -> B
CH -> O
BF -> B
PK -> S
CF -> V
CV -> S
VB -> P
CK -> H
PS -> N
SS -> C
OS -> P
OV -> F
VN -> V
BV -> V
HF -> B
FS -> O
BN -> K
SB -> N
HH -> S
BH -> S
KK -> H
HS -> K
KF -> V
""")

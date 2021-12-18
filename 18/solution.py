from typing import List


class ReduceResult:
    def __init__(self):
        self.resolved = False
        return

    def set_split(self, split):
        self.resolved = True
        self.split = split
        return self

    def set_explode(self, left, value):
        self.explode = (left, value)
        return self

    def resolve(self):
        self.resolved = True


class Pair:
    def __init__(self):
        self.left = None
        self.right = None
        return

    def set_left(self, left):
        self.left = left
        return self

    def set_right(self, right):
        self.right = right
        return self

    def push(self, item):
        if self.left is None:
            self.left = item
        else:
            self.right = item

    def __add__(self, a):
        self.right = self.right + a
        return self

    def __radd__(self, a):
        self.left = a + self.left
        return self

    def reduce(self, depth=1, do_split=False, do_explode=False):

        result = None

        # check for required split
        if do_split:
            def split(value):
                return Pair().set_left(value // 2).set_right(value - (value // 2))
            if isinstance(self.left, int) and self.left >= 10:
                self.left = split(self.left)
                return ReduceResult().set_split(True)
            elif isinstance(self.left, Pair):
                result = self.left.reduce(depth + 1, do_split, do_explode)
                if result is not None:
                    return result

            if isinstance(self.right, int) and self.right >= 10:
                self.right = split(self.right)
                return ReduceResult().set_split(True)
            elif isinstance(self.right, Pair):
                result = self.right.reduce(depth + 1, do_split, do_explode)
                if result is not None:
                    return result

        # reduce left and right, seeing if we can find an explosion. if we can, resolve explosion
        if isinstance(self.left, Pair):
            child = self.left
            if do_explode and isinstance(child.left, int) and isinstance(child.right, int) and depth >= 4:
                self.left = 0
                self.right = child.right + self.right
                return ReduceResult().set_explode(True, child.left)
            else:
                result = self.left.reduce(depth + 1, do_split, do_explode)
                if hasattr(result, "explode") and not result.resolved:
                    if result.explode[0]:
                        return result
                    else:
                        self.right = result.explode[1] + self.right
                        result.resolve()
                        return result
        if isinstance(self.right, Pair) and result is None:
            child = self.right
            if do_explode and isinstance(child.left, int) and isinstance(child.right, int) and depth >= 4:
                self.right = 0
                self.left = self.left + child.left
                return ReduceResult().set_explode(False, child.right)
            else:
                result = self.right.reduce(depth + 1, do_split, do_explode)
                if hasattr(result, "explode") and not result.resolved:
                    if not result.explode[0]:
                        return result
                    else:
                        self.left = self.left + result.explode[1]
                        result.resolve()
                        return result

        return result

    def get_magnitude(self):
        if isinstance(self.left, int):
            left = self.left
        else:
            left = self.left.get_magnitude()
        if isinstance(self.right, int):
            right = self.right
        else:
            right = self.right.get_magnitude()
        return 3*left + 2*right

    def __str__(self):
        string = ["["]
        if isinstance(self.left, int):
            string.append(str(self.left))
        else:
            string.append(str(self.left))
        string.append(",")
        if isinstance(self.right, int):
            string.append(str(self.right))
        else:
            string.append(str(self.right))
        string.append("]")
        return ''.join(string)

    @staticmethod
    def parse(input):
        pair = Pair()
        stack = []
        regular_number = ""
        for i in range(0, len(input)):
            if input[i] == "[":
                stack.append(pair)
                pair = Pair()
            elif input[i] == "]":
                if regular_number:
                    pair.push(int(regular_number))
                    regular_number = ""
                inner_pair = pair
                pair = stack.pop()
                pair.push(inner_pair)
            else:
                if input[i] == ",":
                    if regular_number:
                        pair.push(int(regular_number))
                        regular_number = ""
                else:
                    regular_number += input[i]
        return pair.left


def get_magnitude(pairs):
    while True:
        result = pairs[0].reduce(do_explode=True)
        if result is None:
            result = pairs[0].reduce(do_split=True)
        if result is None:
            if len(pairs) <= 1:
                break
            pairs[0] = Pair().set_left(pairs[0]).set_right(pairs.pop(1))
    return pairs[0].get_magnitude()


def solve(puzzle_input):

    pairs: List[Pair] = [Pair.parse(x)
                         for x in puzzle_input.strip().split("\n")]

    # part 1
    print(get_magnitude(pairs))

    pair_strings = puzzle_input.strip().split("\n")
    max_magnitude = 0
    for i in range(0, len(pair_strings)):
        for j in range(0, len(pair_strings)):
            if i != j:
                test_pairs = [Pair.parse(
                    pair_strings[i]), Pair.parse(pair_strings[j])]
                max_magnitude = max(max_magnitude, get_magnitude(test_pairs))
                test_pairs = [Pair.parse(
                    pair_strings[j]), Pair.parse(pair_strings[i])]
                max_magnitude = max(max_magnitude, get_magnitude(test_pairs))

    # part 2
    print(max_magnitude)
    return


solve("""
[[2,[[4,8],7]],[[9,7],[[2,0],9]]]
[0,[7,5]]
[[[5,[6,9]],4],[3,3]]
[[[6,[6,9]],4],[[[4,8],8],[6,5]]]
[[[[1,4],[2,1]],[6,0]],[[[9,1],[4,2]],[[0,4],0]]]
[[9,4],[[8,6],1]]
[[[[0,7],0],7],[1,[2,9]]]
[[[2,9],[[8,4],[4,0]]],[[[6,2],2],[9,5]]]
[[[0,[5,8]],[6,8]],[[[0,7],4],[[2,8],4]]]
[[3,[[4,1],[0,7]]],[[1,[5,1]],4]]
[[[[2,9],6],[[5,3],2]],[[8,[2,0]],9]]
[0,[[[2,7],9],[1,8]]]
[[[2,[6,2]],[[4,0],[9,6]]],[[6,1],[8,9]]]
[[[[9,6],9],[5,[1,8]]],[[[9,6],9],[[2,0],[3,8]]]]
[[[[4,3],[0,8]],4],[6,6]]
[[[[4,3],7],[[7,0],5]],[2,[[9,9],4]]]
[[[[4,3],[1,7]],[[3,1],[0,9]]],0]
[[5,[[2,5],[2,8]]],[[4,0],[[5,2],[9,8]]]]
[[[0,[3,5]],7],[[[5,9],2],4]]
[[9,[[4,4],8]],[[[2,8],1],[[0,9],5]]]
[[[6,8],[0,1]],[[8,2],[2,0]]]
[[[1,9],[[9,1],2]],[[6,4],[[7,7],[8,3]]]]
[[1,[5,[7,6]]],[[[4,7],4],5]]
[[[8,0],9],[[[6,0],4],1]]
[[[4,[4,2]],7],[[6,[0,9]],[[3,0],[7,6]]]]
[[[[3,4],[9,0]],[4,4]],[[9,6],7]]
[4,[[8,3],[7,1]]]
[6,[6,8]]
[[[[0,6],[7,6]],[5,3]],[[[8,9],[6,0]],[[8,5],7]]]
[[[[0,3],1],5],[[[4,3],[3,2]],[2,[5,9]]]]
[[[[3,1],0],[1,[8,4]]],[4,5]]
[[[0,[4,1]],1],[[1,6],[[4,8],[8,3]]]]
[[[1,4],6],[9,[1,2]]]
[[9,[[0,7],1]],[[0,9],[0,[4,4]]]]
[[1,[7,4]],[[2,[5,3]],[[6,6],9]]]
[0,[0,[0,[0,4]]]]
[[[[9,7],[4,9]],[9,[3,5]]],[[9,7],7]]
[5,[9,[[4,1],[2,9]]]]
[[0,[8,4]],1]
[[[9,[3,3]],[8,6]],[7,[[1,6],0]]]
[[[1,[0,7]],[[9,1],8]],[[[2,2],5],[[7,1],[2,2]]]]
[[[7,[0,3]],4],[[6,[1,6]],[8,7]]]
[[[[4,8],3],[[6,1],7]],[8,[3,[7,8]]]]
[3,[[[9,6],9],3]]
[[[5,[1,0]],[1,4]],5]
[[[[4,7],2],[[7,0],[6,7]]],[[1,[0,3]],0]]
[9,[[3,7],[6,1]]]
[[[2,5],[[0,7],[0,7]]],[[[0,3],2],8]]
[[[[4,4],7],[2,[0,7]]],[[[1,4],[6,6]],[[8,9],[5,2]]]]
[[[[0,8],5],[[3,5],7]],[[[5,6],[0,0]],[[3,8],6]]]
[4,[8,[9,[2,3]]]]
[[[[6,6],9],0],[[[2,9],[0,8]],5]]
[[[8,[4,0]],[[2,1],[7,3]]],[8,7]]
[[6,[9,[1,8]]],[[7,[7,9]],[[2,3],1]]]
[[6,[[1,7],1]],[[[5,3],[2,0]],[[4,4],9]]]
[[[[8,0],[0,3]],[[4,8],[0,9]]],[8,[7,[8,6]]]]
[6,0]
[[[[5,2],0],[3,3]],[0,4]]
[[[9,5],[6,4]],[[[7,2],0],8]]
[[[0,9],[5,[2,3]]],2]
[[[[5,4],[2,9]],[1,[9,0]]],[[9,9],[9,6]]]
[[[7,[4,8]],[9,8]],[[[1,3],0],[4,[4,7]]]]
[[7,[7,9]],0]
[[[[6,7],[8,1]],[[0,2],2]],[[[7,6],6],[[3,4],[9,9]]]]
[[7,[6,[2,2]]],[[[8,8],[0,4]],[5,[7,7]]]]
[[[[0,6],[9,2]],[8,1]],[[[0,4],2],[[5,9],[4,9]]]]
[[[[9,1],[1,7]],[[3,1],[0,7]]],[[2,[4,9]],[9,1]]]
[[[9,4],2],[[[2,3],3],[6,[5,7]]]]
[[[0,8],[[0,9],2]],[[[0,7],[4,4]],7]]
[[[5,2],4],[0,6]]
[[3,[9,[9,2]]],[8,[1,[6,8]]]]
[3,[7,[[8,0],[1,7]]]]
[[[[2,4],[7,3]],[[0,7],0]],5]
[[[[6,0],8],[1,4]],[[[3,3],[8,6]],5]]
[[5,[5,[6,2]]],4]
[[[0,7],[[4,1],4]],[[8,[3,2]],[7,7]]]
[[1,[[6,5],[2,2]]],[[6,[2,8]],[1,0]]]
[6,[4,[[2,2],[1,8]]]]
[[[[3,3],1],[[4,1],7]],[[[5,2],7],[4,[4,7]]]]
[[[[2,2],1],[[4,1],3]],[1,[[0,9],[3,8]]]]
[[0,[0,4]],[[9,[7,5]],[8,[8,0]]]]
[[[[0,3],3],[[7,3],5]],[4,[[0,1],[3,0]]]]
[[4,8],3]
[[[6,0],7],[[6,8],[8,6]]]
[[[[8,5],3],[[6,2],[2,6]]],[[[2,7],5],[[3,8],[6,9]]]]
[7,[4,2]]
[[[[6,0],[7,8]],6],[[[4,6],6],7]]
[[[0,[2,1]],[5,[3,8]]],[[[3,9],3],[[0,9],3]]]
[[[8,6],[4,0]],[2,[[4,1],8]]]
[[[0,1],[[2,0],5]],[[[0,1],[7,0]],[[1,2],[1,4]]]]
[[[8,8],[[4,4],3]],[1,[4,1]]]
[[[5,[0,7]],[7,5]],[[7,6],[5,5]]]
[[[9,[1,3]],[[3,3],6]],[4,[[5,6],8]]]
[[[9,[3,0]],[8,5]],[1,[[8,0],3]]]
[[[3,[3,9]],[[2,4],[4,6]]],[[1,2],3]]
[[[1,[3,1]],[3,[6,3]]],[1,[5,7]]]
[[[[5,5],[1,5]],3],[9,[[7,4],[9,2]]]]
[[[6,[7,1]],[[6,6],[1,6]]],7]
[[[[1,4],0],[8,3]],[[[8,2],9],[[0,3],[9,5]]]]
[[4,[1,[0,1]]],[[1,[7,3]],1]]
""")

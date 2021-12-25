# lol THIS DOESN'T WORK. I worked most of christmas eve on it and gave up. test.py is someone's solution from reddit

def test_validate(input, instructions, z):
    if isinstance(input, int):
        input = str(input)
    input_str = [int(x) for x in input]
    registers = {"x": 0, "y": 0, "w": 0}
    registers["z"] = z
    for instruction in instructions:
        op = instruction[0]
        operand1 = instruction[1]
        operand2 = None
        if len(instruction) > 2:
            operand2 = instruction[2]
        if op == "inp":
            registers[operand1] = input_str.pop(0)
        elif op == "add":
            if isinstance(operand2, int):
                registers[operand1] += operand2
            else:
                registers[operand1] += registers[operand2]
        elif op == "mul":
            if isinstance(operand2, int):
                registers[operand1] *= operand2
            else:
                registers[operand1] *= registers[operand2]
        elif op == "div":
            if isinstance(operand2, int):
                registers[operand1] = int(registers[operand1] / operand2)
            else:
                registers[operand1] = int(
                    registers[operand1] / registers[operand2])
        elif op == "mod":
            if isinstance(operand2, int):
                registers[operand1] %= operand2
            else:
                registers[operand1] %= registers[operand2]
        elif op == "eql":
            if isinstance(operand2, int):
                registers[operand1] = 1 if registers[operand1] == operand2 else 0
            else:
                registers[operand1] = 1 if registers[operand1] == registers[operand2] else 0
    return registers["z"]


class InstructionParser:
    @staticmethod
    def parse(puzzle_input):
        def parse_instruction(input):
            parts = input.split(" ")
            left = parts[1]
            if len(parts) > 2:
                right = parts[2]
                if right != "x" and right != "y" and right != "z" and right != "w":
                    right = int(right)
                return (parts[0], left, right)
            return (parts[0], left)

        instructions = [parse_instruction(x)
                        for x in puzzle_input.strip().split("\n")]

        input_sections = []
        while True:
            input_section = []
            for instruction in instructions:
                if instruction[0] == "inp":
                    # new section
                    if input_section != []:
                        input_sections.append(input_section)
                    input_section = []
                input_section.append(instruction)
            input_sections.append(input_section)
            break

        return [DigitValidator(x) for x in input_sections]


class DigitValidator:
    def __init__(self, instructions):
        self.instructions = instructions
        parameters = DigitValidator.get_instruction_parameters(
            self.instructions)
        self.parameters = parameters

    @staticmethod
    def get_instruction_parameters(instructions):
        a = instructions[4][2]
        b = instructions[5][2]
        c = instructions[15][2]
        return(a, b, c)

    def validate(self, digit, z):
        # is (z mod 26) + b == INPUT?
        x = 0 if ((z % 26) + self.parameters[0]) == digit else 1
        # divide z by a
        z = int(z / self.parameters[1])
        # multiply z by 1 or 26?
        z *= (25 * x) + 1
        # add INPUT and C to z (or not)
        z += (digit + self.parameters[2]) * x
        return z


def solve(puzzle_input):
    def parse_instruction(input):
        parts = input.split(" ")
        left = parts[1]
        if len(parts) > 2:
            right = parts[2]
            if right != "x" and right != "y" and right != "z" and right != "w":
                right = int(right)
            return (parts[0], left, right)
        return (parts[0], left)

    instructions = [parse_instruction(x)
                    for x in puzzle_input.strip().split("\n")]

    digital_validators = InstructionParser.parse(puzzle_input)

    #
    # This map tells us, for a given position in the 14 digit number,
    # and a given digit at that position,
    # and a given z register value at that point,
    # what is the z output at that point.
    #
    # Ideally, once we are done with our loop, we should be able to check foo[13][*][*] and have a value of 0 somewhere.
    #
    #
    foo = {}

    input_zs = {
        0: ''
    }
    for place in range(0, 14):
        next_input_zs = {}
        for digit in range(9, 0, -1):
            for input_z in input_zs.keys():
                # output_z = digital_validators[place].validate(digit, input_z)
                output_z = test_validate(
                    digit, digital_validators[place].instructions, input_z)
                # assert test_z == output_z
                string = input_zs[input_z] + str(digit)
                # output_z %= 26
                if place not in foo:
                    foo[place] = {}
                if digit not in foo[place]:
                    foo[place][digit] = {}
                if input_z not in foo[place][digit] or foo[place][digit][input_z][1] < string:
                    foo[place][digit][input_z] = (output_z, string)
                if output_z not in next_input_zs or next_input_zs[output_z] < string:
                    next_input_zs[output_z] = string
        input_zs = next_input_zs

    return


solve("""
inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 2
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 9
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 15
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 3
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -7
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 6
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 5
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 16
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 1
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -4
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 6
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -9
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 3
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 7
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -9
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 9
mul y x
add z y
""")

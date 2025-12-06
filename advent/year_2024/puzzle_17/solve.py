import math
import re
from collections.abc import Generator
from enum import Enum

from registry import register_solver
from advent.utils.solver import split_in_groups_separated_by_empty_line


class Operand(Enum):
    V_0 = "0"
    V_1 = "1"
    V_2 = "2"
    V_3 = "3"
    V_4 = "4"
    V_5 = "5"
    V_6 = "6"
    V_7 = "7"


class Computer:
    def __init__(self, registers: dict[str, int], instructions: list[Operand]):
        self.registers = registers
        self.output: list[str] = []
        self.register_a: int = 0
        self.register_b: int = 0
        self.register_c: int = 0
        self.instruction_pointer = 0
        self.reset(registers["A"])
        self.instructions: list[Operand] = instructions
        self.instructions_str: list[str] = [op.value for op in self.instructions]

    def literal_value_for(self, operand: Operand) -> int:
        return int(operand.value)

    def combo_value_for(self, operand: Operand) -> int:
        match operand:
            case Operand.V_0 | Operand.V_1 | Operand.V_2 | Operand.V_3:
                return self.literal_value_for(operand)
            case Operand.V_4:
                return self.register_a
            case Operand.V_5:
                return self.register_b
            case Operand.V_6:
                return self.register_c
            case Operand.V_7:
                raise ValueError("7 should not appear as a Combo operand")

    def dv(self, num: int, denom: int) -> int:
        return num // denom

    def bxor(self, v1: int, v2: int) -> int:
        return v1 ^ v2

    def possibly_jump_to(self, line_nr: int):
        if self.register_a:
            self.instruction_pointer = line_nr
            print(f"Jumping, output is now: {self.output}")
            return True
        return False

    def apply(self, op_code: Operand, operand: Operand):
        match op_code:
            case Operand.V_0:
                self.register_a = self.dv(self.register_a,
                                          pow(2,
                                              self.combo_value_for(operand)
                                              )
                                          )
            case Operand.V_1:
                self.register_b = self.bxor(self.register_b, self.literal_value_for(operand))
            case Operand.V_2:
                self.register_b = self.combo_value_for(operand) % 8
            case Operand.V_3:
                if self.possibly_jump_to(self.literal_value_for(operand)):
                    return
            case Operand.V_4:
                self.register_b = self.bxor(self.register_b, self.register_c)
            case Operand.V_5:
                self.output.append(str(self.combo_value_for(operand) % 8))
            case Operand.V_6:
                self.register_b = self.dv(self.register_a,
                                          pow(2,
                                              self.combo_value_for(operand)
                                              )
                                          )
            case Operand.V_7:
                self.register_c = self.dv(self.register_a,
                                          pow(2,
                                              self.combo_value_for(operand)
                                              )
                                          )
        self.instruction_pointer += 2

    def run(self):
        if self.register_a % 10000 == 0:
            print(f"Running for {self.register_a}")
        while self.instruction_pointer < len(self.instructions):
            op_code = self.instructions[self.instruction_pointer]
            operand = self.instructions[self.instruction_pointer + 1]
            self.apply(op_code, operand)

    def reset(self, value: int):
        self.output = []
        self.instruction_pointer = 0
        self.register_a = value
        self.register_b = self.registers["B"]
        self.register_c = self.registers["C"]

    def validate_self_loop(self) -> bool:
        return self.output == self.instructions_str


def parse(puzzle_input: list[str]) -> Computer:
    REGISTER_PATTERN = re.compile(r"Register (?P<k>[A-C]): (?P<v>\d+)")
    PROGRAM_PATTERN = re.compile(r"Program: (?P<i>[0-9,]+)")

    input_generator = split_in_groups_separated_by_empty_line(puzzle_input)
    registers: dict[str, int] = {}
    for line in next(input_generator):
        if line_match := REGISTER_PATTERN.fullmatch(line):
            registers[line_match.group("k")] = int(line_match.group("v"))
        else:
            raise ValueError(f"Invalid register definition: {line}")
    program = next(input_generator)
    if len(program) != 1:
        raise ValueError(f"Only one line expected for the program, got: {program}")
    if line_match := PROGRAM_PATTERN.fullmatch(program[0]):
        instructions = [Operand(instruction) for instruction in line_match.group("i").split(",")]
    else:
        raise ValueError(f"Invalid program definition: {program[0]}")
    return Computer(registers=registers, instructions=instructions)


@register_solver(year="2024", key="17", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    computer = parse(puzzle_input)
    computer.run()
    solution = ",".join(computer.output)
    print(f"Solution is {solution}")


class NonJumpingComputer(Computer):
    def possibly_jump_to(self, line_nr: int) -> bool:
        return False


def new_candidates_leading_to(candidate: int) -> Generator[int, None, None]:
    for i in range(0, 8):
        yield candidate * 8 + i


def generate_new_candidates(candidates: list[int]) -> Generator[int, None, None]:
    for candidate in candidates:
        yield from new_candidates_leading_to(candidate)


def verify_candidate(candidate: int, computer: Computer, expected_output: Operand) -> bool:
    computer.reset(candidate)
    computer.run()
    return computer.output[0] == expected_output.value


def solve_for_specific_input(orig_computer: Computer):
    instructions = orig_computer.instructions
    computer = NonJumpingComputer(
        registers={"A": 0, "B": 0, "C": 0},
        instructions=instructions,
    )
    # We will be using an analysis of the instruction set given that shows:
    # The only jump that might be performed is at the end, which jumps to the start
    # The amount of loops is governed by register_a = register_a // 8 per loop
    # Register_b and register_c do not carry over between loops, they are re-initialized from register_a

    # So we hack the computer to never jump (meaning it will calculate one loop), then try each candidate to see if they
    # produce the wanted output at that time, working backwards

    candidates: list[int] = [0]
    # We will be analyzing backwards
    for index_to_match in range(len(instructions) - 1, -1, -1):
        candidates = list(generate_new_candidates(candidates))
        print(f"At index_to_match: {index_to_match}, Checking {candidates}")
        candidates = [candidate for candidate in candidates if verify_candidate(candidate=candidate,
                                                                                computer=computer,
                                                                                expected_output=instructions[index_to_match]
                                                                                )]
        print(f"Valid candidates remaining: {candidates}")


def brute_force_solve_b(computer: Computer, example: bool):
    solution = 0
    while not computer.validate_self_loop():
        solution += 1
        computer.reset(solution)
        computer.run()
        if example and solution > 120000:
            raise ValueError(f"Didn't find solution at the expected value")

    print(f"Solution is {solution}")


@register_solver(year="2024", key="17", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    computer = parse(puzzle_input)
    if example:
        brute_force_solve_b(computer, example)
    else:
        solve_for_specific_input(computer)

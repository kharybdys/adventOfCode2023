import time
import datetime

from dataclasses import dataclass
from typing import Generator, Self

from advent.earlier_years.puzzle2021_24.alu import analyze_instructions, PartialALU
from registry import register_solver


@dataclass
class PartialSolution:
    """Note, solution assumes only w (input) and z are inputs for a round of instructions"""
    partial_id: str
    required_z: int

    def new_solution(self, w: str, z: int) -> Self:
        return PartialSolution(partial_id=f"{w}{self.partial_id}", required_z=z)

    def __str__(self) -> str:
        return f"PartialSolution[{self.partial_id=}, {self.required_z=}]"


def split_to_instruction_sets(puzzle_input: list[str]) -> Generator[list[str], None, None]:
    instruction_set = []
    for instruction in puzzle_input:
        if instruction.startswith("inp"):
            if instruction == "inp w":
                if instruction_set:
                    yield instruction_set
                instruction_set = []
            else:
                raise NotImplementedError("This solver cannot handle inputs other than w")
        else:
            instruction_set.append(instruction)
    if instruction_set:
        yield instruction_set


def generate_partial_alus() -> Generator[PartialALU, None, None]:
    MIN_Z = -1000000  # 1M, expected runtime for one block = 8 minutes. No valid solution remaining after block 6 of 14
    MAX_Z = +1000000
    for w in range(1, 10):
        for z in range(MIN_Z, MAX_Z+1):
            yield PartialALU(w, z=z)


def solution_step(instruction_set: list[str]) -> dict[int, PartialSolution]:
    new_solutions: dict[int, PartialSolution] = {}
    if analyze_instructions(instruction_set) != (True, False, False, True):
        raise NotImplementedError("This solver cannot handle inputs from previous instruction sets other than w (through inp) and z")
    for partial_alu in generate_partial_alus():
        partial_alu.execute_all(instruction_set)
        earlier_solution = new_solutions.get(partial_alu.z, "")
        if not earlier_solution or earlier_solution.partial_id < str(partial_alu.initial_w):
            new_solutions[partial_alu.z] = PartialSolution(partial_id=str(partial_alu.initial_w),
                                                           required_z=partial_alu.initial_z
                                                           )
    return new_solutions


def merge_solutions(old_solutions: dict[int, PartialSolution], new_solutions: dict[int, PartialSolution]) -> dict[int, PartialSolution]:
    print(f"{old_solutions=}")
    result: dict[int, PartialSolution] = {}
    for old_z, old_solution in old_solutions.items():
        if old_z in new_solutions:
            partial_solution = new_solutions[old_z]
            print(f"Looking at {old_z=}, {partial_solution=}")
            new_solution = old_solutions[old_z].new_solution(w=partial_solution.partial_id, z=partial_solution.required_z)
            print(f"{new_solution=}")
            if partial_solution.required_z not in result:
                result[partial_solution.required_z] = new_solution
                print(f"New entry to result")
            elif result[partial_solution.required_z].partial_id < new_solution.partial_id:
                print(f"Replacing entry {result[partial_solution.required_z]}")
                result[partial_solution.required_z] = new_solution

    return result


def solve_a_too_slow(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    t0 = time.time()
    print(f"Started at {datetime.datetime.now()}")
    partial_solutions = {0: PartialSolution("", 0)}
    for index, instruction_set in enumerate(reversed(list(split_to_instruction_sets(puzzle_input)))):
        new_solutions = solution_step(instruction_set)
        print(f"Processed instruction_set {index + 1}, got {len(new_solutions)} new solutions, time: {time.time() - t0}")
        partial_solutions = merge_solutions(partial_solutions, new_solutions)
        print(f"At {datetime.datetime.now()}:")
        print(f"Processed instruction_set {index + 1}, got {len(partial_solutions)} merged solutions, time: {time.time() - t0}")
        if not partial_solutions:
            raise ValueError("Increase MIN_Z/MAX_Z, no solutions to be found like this!")
    solution = max(partial_solutions.values(), key=lambda s: s.partial_id)
    print(f"Solution: {solution.partial_id}")


@register_solver(year="2021", key="24", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)


@register_solver(year="2021", key="24", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)


"""
w
x
y
z

?, ?, ?, 0
add z y
?, ?, -a, a
mul y x
?, b, -a/b, a
add y 13
?, b, -a/b-13, a
add y w
c, b, -a/b-13-c, a
mul y 0
c, b, ?, a  en -a/b-13-c = 0
mul z y
c, b, d, a/d
add y 1
c, b, d-1, a/d
mul y x
c, b, (d-1)/b, a/d
add y 25
c, b, (d-1)/b-25, a/d
mul y 0
c, b, ?, a/d en (d-1)/b-25 = 0  -> 25 = (d-1)/b -> 25b = d-1 -> 25b + 1 = d
eql x 0
c, e, ?, a/d en b in (0, 1) met e == 0 <=> b == 1
eql x w
f, e, ?, a/d en c in (0, 1) met f == e <=> c == 1
add x -14
f, e-14, ?, a/d
div z 26
f, e-14, ?, 26a/d+g met g in [0, 25]
mod x 26
f, 26h+e-14, ?, 26a/d+g
add x z
f, 26h+e-14 - (26a/d+g), ?, 26a/d+g
mul x 0
f, ?, ?, 26a/d+g met 26h+e-14 - (26a/d+g) = 0
inp w

-a/b-13-c = 0 -> a = -b(13+c)
25b + 1 = d
b in [0, 1] met e == 0 <=> b == 1
c in [0, 1] met f == e <=> c == 1
g in [0, 25]
26h+e-14 - (26a/d+g) = 0

solve a, given f in [1,9]
-a/b-13 = c
25b+1 = d -> d in {1, 26}
b in [0, 1]
c in [0, 1] -> -a/b = 13 of 14 -> a = -13b of a = -14b -> a in {0, -13, -14}
g in [0, 25]
26h+e-14 = 26a/d+g

b == 0, c == 0 -> a == 0,   d == 1,  e != 0, f == 0, g in [0, 25]   -- kan niet want f != 0
b == 0, c == 1 -> a == 0,   d == 1,  e != 0, f == e, g in [0, 25], f in [1, 9]
  26a/d+14 = 14
  14+g = 26h+e
b == 1, c == 0 -> a == -13, d == 26, e == 0, f != 0, g in [0, 25], f in [1, 9]
  26a/d+14 = 1
  1+g = 26h+e
  [1, 26] = 26h
b == 1, c == 1 -> a == -14, d == 26, e == 0, f == 0, g in [0, 25]   -- kan niet want f != 0

"""
"""
Oplossing zou moeten zijn w = 9, z = 23:

w = 9, x = ?, y = ?, z = 23
mul x 0
w = 9, x = 0, y = ?, z = 23
add x z
w = 9, x = 23, y = ?, z = 23
mod x 26
w = 9, x = 23, y = ?, z = 23
div z 26
w = 9, x = 23, y = ?, z = 0
add x -14
w = 9, x = 9, y = ?, z = 0
eql x w
w = 9, x = 1, y = ?, z = 0
eql x 0
w = 9, x = 0, y = ?, z = 0
mul y 0
w = 9, x = 0, y = 0, z = 0
add y 25
w = 9, x = 0, y = 25, z = 0
mul y x
w = 9, x = 0, y = 0, z = 0
add y 1
w = 9, x = 0, y = 1, z = 0
mul z y
w = 9, x = 0, y = 1, z = 0
mul y 0
w = 9, x = 0, y = 0, z = 0
add y w
w = 9, x = 0, y = 0, z = 0
add y 13
w = 9, x = 0, y = 13, z = 0
mul y x
w = 9, x = 0, y = 0, z = 0
add z y
w = 9, x = 0, y = 0, z = 0
"""
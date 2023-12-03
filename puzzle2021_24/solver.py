import time

from dataclasses import dataclass
from typing import Generator, Self

from puzzle2021_24.alu import analyze_instructions, PartialALU


@dataclass
class PartialSolution:
    """Note, solution assumes only w (input) and z are inputs for a round of instructions"""
    partial_id: str
    required_z: int

    def new_solution(self, w: int, z: int) -> Self:
        return PartialSolution(partial_id=f"{w}{self.partial_id}", required_z=z)


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
    MIN_Z = -10000
    MAX_Z = +10000
    for w in range(1, 10):
        for z in range(MIN_Z, MAX_Z+1):
            yield PartialALU(w, z=z)


def solution_step(partial_solutions: list[PartialSolution], instruction_set: list[str]) -> list[PartialSolution]:
    new_solutions: list[PartialSolution] = []
    if analyze_instructions(instruction_set) != (True, False, False, True):
        raise NotImplementedError("This solver cannot handle inputs from previous instruction sets other than w (through inp) and z")
    for partial_alu in generate_partial_alus():
        partial_alu.execute_all(instruction_set)
        for partial_solution in filter(lambda s: s.required_z == partial_alu.z, partial_solutions):
            new_solutions.append(partial_solution.new_solution(w=partial_alu.initial_w, z=partial_alu.initial_z))
    return new_solutions


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    t0 = time.time()
    partial_solutions = [PartialSolution("", 0)]
    for index, instruction_set in enumerate(reversed(list(split_to_instruction_sets(puzzle_input)))):
        partial_solutions = solution_step(partial_solutions, instruction_set)
        print(f"Processed instruction_set {index+1}, got {len(partial_solutions)} solutions, time: {time.time() - t0}")
    solution = max(partial_solutions, key=lambda s: s.partial_id)
    print(f"Solution: {solution.partial_id}")


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)

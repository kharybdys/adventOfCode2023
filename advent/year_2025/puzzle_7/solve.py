import re
from collections.abc import Generator

from advent.registry import register_solver

NON_STARTING_LINE_PATTERN = re.compile(r"[.^]*")


class Beam:
    def __init__(self, line: str):
        self._max_x = len(line) - 1
        start_x = self._process_start_line(line)
        self._tachyon_xs = {start_x}
        self.split_count = 0

    def _process_start_line(self, line: str) -> int:
        start_x = None
        for i, char in enumerate(line):
            if char == "S":
                if start_x is not None:
                    raise ValueError(f"Duplicate S encountered. At both {start_x} and {i}")
                start_x = i
            elif char != ".":
                raise ValueError(f"Invalid char in start line, only S and . are allowed: {char}")
        if start_x is None:
            raise ValueError(f"No S found in starting line")
        return start_x

    def _new_xs_after_split(self, x: int, existing_beam_xs: set[int]) -> Generator[int, None, None]:
        for new_x in {x-1, x+1}:
            if 0 <= new_x <= self._max_x:
                if new_x not in existing_beam_xs:
                    yield new_x

    def process_line(self, line: str):
        if not NON_STARTING_LINE_PATTERN.fullmatch(line):
            raise ValueError(f"Invalid non starting line {line}")

        splitter_indices = {i for i, char in enumerate(line) if char == "^"}
        print(f"With {self.split_count} and beams at {self._tachyon_xs}")
        print(f"Processing splitters at {splitter_indices}")
        new_tachyon_xs = set()
        for x in sorted(self._tachyon_xs):
            if x in splitter_indices:
                new_xs = set(self._new_xs_after_split(x, new_tachyon_xs))
                print(f"At splitter {x}, {new_xs=}")
                self.split_count += 1
                new_tachyon_xs.update(new_xs)
            else:
                new_tachyon_xs.add(x)
        self._tachyon_xs = new_tachyon_xs


@register_solver(year="2025", key="7", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    input_generator = iter(puzzle_input)
    beam = Beam(next(input_generator))
    for line in input_generator:
        beam.process_line(line)

    print(f"Solution is {beam.split_count}")


@register_solver(year="2025", key="7", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    solution = 0
    print(f"Solution is {solution}")

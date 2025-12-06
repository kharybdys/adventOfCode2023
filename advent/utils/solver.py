from typing import Protocol, Generator


class SolverFunction(Protocol):
    def __call__(self,
                 puzzle_input: list[str],
                 example: bool) -> None:
        pass


def split_in_groups_separated_by_empty_line(puzzle_input: list[str]) -> Generator[list[str], None, None]:
    lines = []
    for line in puzzle_input:
        if line:
            lines.append(line)
        else:
            yield lines
            lines = []
    yield lines

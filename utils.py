from itertools import groupby
from typing import Generator


def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


def split_in_groups_separated_by_empty_line(puzzle_input: list[str]) -> Generator[list[str], None, None]:
    lines = []
    for line in puzzle_input:
        if line:
            lines.append(line)
        else:
            yield lines
            lines = []
    yield lines

from dataclasses import dataclass
from itertools import starmap
from typing import Self

from registry import register_solver
from utils import split_in_groups_separated_by_empty_line


@dataclass
class LockOrKey:
    tumblers: list[list[bool]]
    lock: bool

    @classmethod
    def from_lines(cls, lines: list[str]) -> Self:
        tumblers = [[char == "#" for char in line] for line in lines]
        lock = all(tumblers[0])
        return cls(tumblers=tumblers, lock=lock)

    def fits(self, key: Self) -> bool:
        if not self.lock:
            raise ValueError("Cannot call fits on a key")
        if key.lock:
            raise ValueError("Cannot pass a lock into fits")
        print(f"Comparing lock {self}")
        print(f"With key       {key}")
        return all(
            starmap(
                lambda list_a, list_b: all(
                    not a or not b for a, b in zip(list_a, list_b)
                ),
                zip(self.tumblers, key.tumblers)
            )
        )


def parse(puzzle_input: list[str]) -> tuple[list[LockOrKey], list[LockOrKey]]:
    locks = []
    keys = []
    for lines in split_in_groups_separated_by_empty_line(puzzle_input):
        lock_or_key = LockOrKey.from_lines(lines)
        if lock_or_key.lock:
            locks.append(lock_or_key)
        else:
            keys.append(lock_or_key)
    return locks, keys


@register_solver(year="2024", key="25", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    locks, keys = parse(puzzle_input)
    solution = 0
    for lock in locks:
        for key in keys:
            if lock.fits(key):
                solution += 1
    print(f"Solution is {solution}")


@register_solver(year="2024", key="25", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(f"No puzzle for day 25, part B")

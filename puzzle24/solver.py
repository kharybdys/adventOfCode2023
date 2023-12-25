import re

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Self, ClassVar

from utils import Range


@dataclass(repr=True)
class Hail:
    x: int
    y: int
    z: int
    delta_x: int
    delta_y: int
    delta_z: int

    PATTERN: ClassVar[re.Pattern] = re.compile(r"(-?\d+),\s+(-?\d+),\s+(-?\d+)\s+@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)")

    def line_xy(self) -> tuple[float, float]:
        """
        Returns a and b such that y = ax + b
        """
        b = self.y - self.delta_y * (self.x / float(self.delta_x))
        a = (self.y - b) / float(self.x)
        return a, b

    @staticmethod
    def from_line(line: str) -> Self:
        if match := Hail.PATTERN.fullmatch(line):
            return Hail(x=int(match[1]),
                        y=int(match[2]),
                        z=int(match[3]),
                        delta_x=int(match[4]),
                        delta_y=int(match[5]),
                        delta_z=int(match[6]),
                        )
        else:
            raise ValueError(f"Invalid hail definition {line}")


def check_intersection_without_z(h1: Hail, h2: Hail) -> tuple[bool, float, float, float, float]:
    h1_a, h1_b = h1.line_xy()
    h2_a, h2_b = h2.line_xy()
    if h1_a == h2_a:
        return False, 0.0, 0.0, 0.0, 0.0
    else:
        x = (h2_b - h1_b) / float(h1_a - h2_a)
        y = h1_a * x + h1_b
        t1 = (x - h1.x) / float(h1.delta_x)
        t2 = (x - h2.x) / float(h2.delta_x)
        return True, x, y, t1, t2


def count_intersections(x_range: Range, y_range: Range, hailstones: list[Hail]) -> int:
    solution = 0
    for h1, h2 in combinations(hailstones, 2):
        intersects, x, y, t1, t2 = check_intersection_without_z(h1, h2)
        print(f"{h1}, {h2} intersect? {intersects} at {x}, {y}, with {t1}, {t2}")
        if x_range.within(x) and y_range.within(y) and t1 >= 0 and t2 >= 0:
            print("Valid intersection")
            solution += 1
    return solution


def solve_a(puzzle_input: list[str]) -> None:
    x_range = Range(start=200000000000000, stop=400000000000000 + 1)
    y_range = Range(start=200000000000000, stop=400000000000000 + 1)
    # x_range = Range(start=7, stop=27 + 1)
    # y_range = Range(start=7, stop=27 + 1)
    print(puzzle_input)
    hailstones = [Hail.from_line(line) for line in puzzle_input]
    solution = count_intersections(x_range, y_range, hailstones)
    print(solution)


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)


def read_file() -> list[str]:
    data_dir = Path(__file__).parent.parent / "data"

    with open(data_dir / f"input24.txt", "rt") as file:
        return [line.rstrip() for line in file]


if __name__ == "__main__":
    solve_a(read_file())

import re

from dataclasses import dataclass
from itertools import combinations
from typing import Self, ClassVar

from advent.registry import register_solver
from advent.utils.range import Range


@dataclass(eq=True)
class Point3D:
    x: float
    y: float
    z: float

    def __truediv__(self, other) -> Self:
        if isinstance(other, (float, int)):
            return Point3D(x=self.x / other,
                           y=self.y / other,
                           z=self.z / other
                           )
        raise ValueError(f"Cannot (true)divide by a non-scalar {other}")

    def __mul__(self, other) -> Self:
        if isinstance(other, (float, int)):
            return Point3D(x=self.x * other,
                           y=self.y * other,
                           z=self.z * other
                           )
        raise ValueError(f"Cannot multiply by a non-scalar {other}")

    def __sub__(self, other: Self) -> Self:
        if isinstance(other, Point3D):
            return Point3D(x=other.x - self.x,
                           y=other.y - self.y,
                           z=other.z - self.z
                           )
        else:
            raise ValueError(f"Cannot subtract by {other}")

    def __add__(self, other: Self) -> Self:
        if isinstance(other, Point3D):
            return Point3D(x=other.x + self.x,
                           y=other.y + self.y,
                           z=other.z + self.z
                           )
        else:
            raise ValueError(f"Cannot subtract by {other}")

    def cross(self, other: Self) -> Self:
        if isinstance(other, Point3D):
            return Point3D(x=self.y * other.z - self.z * other.y,
                           y=self.z * other.x - self.x * other.z,
                           z=self.x * other.y - self.y * other.x
                           )
        else:
            raise ValueError(f"Cannot cross with {other}")


@dataclass(repr=True)
class Hail:
    initial: Point3D
    delta: Point3D

    PATTERN: ClassVar[re.Pattern] = re.compile(r"(-?\d+),\s+(-?\d+),\s+(-?\d+)\s+@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)")

    def coords_at(self, t: int) -> Point3D:
        return self.initial + self.delta * t

    def line_xy(self) -> tuple[float, float]:
        """
        Returns a and b such that y = ax + b
        """
        b = self.initial.y - self.delta.y * (self.initial.x / float(self.delta.x))
        a = (self.initial.y - b) / float(self.initial.x)
        return a, b

    @staticmethod
    def from_line(line: str) -> Self:
        if match := Hail.PATTERN.fullmatch(line):
            initial = Point3D(x=int(match[1]),
                              y=int(match[2]),
                              z=int(match[3])
                              )
            delta = Point3D(x=int(match[4]),
                            y=int(match[5]),
                            z=int(match[6])
                            )
            return Hail(initial=initial,
                        delta=delta
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
        t1 = (x - h1.initial.x) / float(h1.delta.x)
        t2 = (x - h2.initial.x) / float(h2.delta.x)
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


def two_vectors_parallel(a: Point3D, b: Point3D) -> bool:
    return a.cross(b) == Point3D(0, 0, 0)


@register_solver(year="2023", key="24", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    if example:
        x_range = Range(start=7, stop=27 + 1)
        y_range = Range(start=7, stop=27 + 1)
    else:
        x_range = Range(start=200000000000000, stop=400000000000000 + 1)
        y_range = Range(start=200000000000000, stop=400000000000000 + 1)
    print(puzzle_input)
    hailstones = [Hail.from_line(line) for line in puzzle_input]
    solution = count_intersections(x_range, y_range, hailstones)
    print(solution)


@register_solver(year="2023", key="24", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    if example:
        LIMIT = 10
    else:
        LIMIT = 500000000000000
    print(puzzle_input)
    hailstones = [Hail.from_line(line) for line in puzzle_input]
    h0 = hailstones[0]
    h1 = hailstones[1]
    h2 = hailstones[2]
    attempts = 0
    for t0 in range(0, LIMIT):
        for t1 in range(0, LIMIT):
            for t2 in range(0, LIMIT):
                # For t0 to t2, see if the points that the three hailstones are on at that time are on one line
                p0 = h0.coords_at(t0)
                p1 = h1.coords_at(t1)
                p2 = h2.coords_at(t2)
                a = p0 - p1
                b = p0 - p2
                if two_vectors_parallel(a, b):
                    print(f"Solution: {t0=}, {t1=}, {t2=}")
                attempts += 1
                if attempts % 100000 == 0:
                    print(f"Attempts is {attempts:,}")

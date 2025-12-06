import math
import re
from collections import namedtuple, Counter
from dataclasses import dataclass
from enum import Enum
from typing import Self, ClassVar

from advent.registry import register_solver

Coords = namedtuple("Coords", ["x", "y"])


class Quadrant(Enum):
    NW = "NW"
    NE = "NE"
    SW = "SW"
    SE = "SE"
    UNKNOWN = "UNKNOWN"


@dataclass
class Robot:
    start_position: Coords
    start_velocity: Coords
    LINE_PATTERN: ClassVar[re.Pattern] = re.compile(r"p=(?P<p_x>-?\d+),(?P<p_y>-?\d+) v=(?P<v_x>-?\d+),(?P<v_y>-?\d+)")

    @classmethod
    def from_line(cls, line: str) -> Self:
        if line_match := cls.LINE_PATTERN.fullmatch(line):
            return cls(
                start_position=Coords(x=int(line_match["p_x"]), y=int(line_match["p_y"])),
                start_velocity=Coords(x=int(line_match["v_x"]), y=int(line_match["v_y"])),
            )
        else:
            raise ValueError(f"Couldn't parse: {line}")

    def calculate_position_after_steps(self, steps: int) -> Coords:
        return Coords(
            x=self.start_position.x + steps * self.start_velocity.x,
            y=self.start_position.y + steps * self.start_velocity.y,
        )

    def calculate_wrapped_position_after_steps(self, steps: int, width: int, height: int) -> Coords:
        position = self.calculate_position_after_steps(steps)
        return Coords(x=position.x % width, y=position.y % height)

    def calculate_quadrant_after_steps(self, steps: int, width: int, height: int) -> Quadrant:
        assert width % 2 != 0
        assert height % 2 != 0
        position = self.calculate_wrapped_position_after_steps(steps=steps, width=width, height=height)
        half_width = width // 2
        half_height = height // 2
        if position.x == half_width or position.y == half_height:
            return Quadrant.UNKNOWN
        if position.x < half_width and position.y < half_height:
            return Quadrant.NW
        if position.x < half_width and position.y > half_height:
            return Quadrant.SW
        if position.x > half_width and position.y < half_height:
            return Quadrant.NE
        if position.x > half_width and position.y > half_height:
            return Quadrant.SE
        raise ValueError(f"Shouldn't be able to reach this spot, got {position=} with {half_height=} and {half_width=}")


@register_solver(year="2024", key="14", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    steps = 100
    width = 7 if example else 101
    height = 11 if example else 103

    robots = [Robot.from_line(line) for line in puzzle_input]
    counter: dict[Quadrant, int] = Counter(robot.calculate_quadrant_after_steps(steps=steps, width=width, height=height) for robot in robots)
    if Quadrant.UNKNOWN in counter:
        del counter[Quadrant.UNKNOWN]
    print(f"Solution is {math.prod(counter.values())}")


def print_grid(counter: dict[Coords, int], width: int, height: int):
    def print_chr(x: int) -> str:
        if nr := counter.get(Coords(x, y)):
            return str(nr)
        else:
            return "."

    for y in range(height):
        print("".join(print_chr(x) for x in range(width)))


def contains_frame(counter: dict[Coords, int], min_size: int) -> bool:
    count_x: Counter[int, int] = Counter(map(lambda c: c[0], counter.keys()))
    if count_x.most_common(2)[-1][1] > min_size:
        count_y: Counter[int, int] = Counter(map(lambda c: c[1], counter.keys()))
        return count_y.most_common(2)[-1][1] > min_size
    else:
        return False


@register_solver(year="2024", key="14", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    width = 7 if example else 101
    height = 11 if example else 103
    min_size = 4 if example else 20

    robots = [Robot.from_line(line) for line in puzzle_input]
    steps = 0
    while True:
        counter: dict[Coords, int] = Counter(robot.calculate_wrapped_position_after_steps(steps=steps, width=width, height=height) for robot in robots)
        if contains_frame(counter, min_size):
            print(f"At step {steps}")
            print_grid(counter, width, height)
            print("XMASXMASXMASXMASXMASXMASXMASXMASXMASXMASXMASXMASXMASXMASXMAS")
        steps += 1

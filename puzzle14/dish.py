from enum import Enum
from itertools import starmap
from typing import Generator, Self


class RockStatus(Enum):
    ROUND = "ROUND", "O", 1
    CUBE = "CUBE", "#", 0
    EMPTY = "EMPTY", ".", 0

    def can_roll(self) -> bool:
        return self == RockStatus.ROUND

    def empty(self) -> bool:
        return self == RockStatus.EMPTY

    def __new__(cls, value, str_repr, load_value):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.str_repr = str_repr
        obj.load_value = load_value
        return obj

    @classmethod
    def from_char(cls, char: str) -> Self:
        for opt in cls.__members__.values():
            if opt.str_repr == char:
                return opt
        raise ValueError(f"Unknown char {char}")


class Dish:
    def __init__(self, rocks: list[list[RockStatus]]):
        self.rocks = rocks
        self.height = len(rocks)
        self.width = len(rocks[0])

    def within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def rock_at(self, x: int, y: int) -> RockStatus:
        if self.within_bounds(x, y):
            return self.rocks[y][x]

    def set_rock_at(self, x: int, y: int, value: RockStatus):
        self.rocks[y][x] = value

    def roll_north(self):
        changed = True
        while changed:
            changed = False
            for y in range(1, self.height):
                for x in range(0, self.width):
                    if self.rock_at(x, y).can_roll():
                        if self.rock_at(x, y - 1).empty():
                            rock_to_move = self.rock_at(x, y)
                            self.set_rock_at(x, y, RockStatus.EMPTY)
                            self.set_rock_at(x, y - 1, rock_to_move)
                            changed = True

    def generate_rock_with_coordinates(self) -> Generator[tuple[RockStatus, int, int], None, None]:
        for y in range(0, self.height):
            for x in range(0, self.width):
                yield self.rock_at(x, y), x, y

    def total_load_north(self) -> int:
        def to_load_value(rock: RockStatus, x: int, y: int) -> int:
            return rock.load_value * (self.height - y)
        return sum(starmap(to_load_value, self.generate_rock_with_coordinates()))

    def print_dish(self):
        print("Dish: ")
        for line in self.rocks:
            print("".join(map(lambda r: r.str_repr, line)))
        print("")

    @staticmethod
    def from_lines(lines: list[str]) -> Self:
        return Dish(rocks=[[RockStatus.from_char(char) for char in line] for line in lines])

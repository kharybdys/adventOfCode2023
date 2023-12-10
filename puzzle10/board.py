from enum import Enum
from functools import cache, cached_property
from typing import Self

DEBUG = False


class Direction(Enum):
    EAST = "EAST"
    WEST = "WEST"
    SOUTH = "SOUTH"
    NORTH = "NORTH"

    def next_coords(self, x: int, y: int) -> tuple[int, int]:
        match self:
            case Direction.EAST:
                return x + 1, y
            case Direction.WEST:
                return x - 1, y
            case Direction.NORTH:
                return x, y - 1
            case Direction.SOUTH:
                return x, y + 1
            case _:
                raise ValueError(f"Impossible, unsupported direction: {self}")

    @cached_property
    def opposite(self) -> Self:
        match self:
            case Direction.EAST:
                return Direction.WEST
            case Direction.WEST:
                return Direction.EAST
            case Direction.NORTH:
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.NORTH
            case _:
                raise ValueError(f"Impossible, unsupported direction: {self}")

    @classmethod
    def all(cls) -> list[Self]:
        return list(cls.__members__.values())


class PipeStatus(Enum):
    EASTWEST = "EASTWEST", "-"
    NORTHSOUTH = "NORTHSOUTH", "|"
    SOUTHEAST = "SOUTHEAST", "F"
    NORTHEAST = "NORTHEAST", "L"
    SOUTHWEST = "SOUTHWEST", "7"
    NORTHWEST = "NORTHWEST", "J"
    EMPTY = "EMPTY", "."
    START = "START", "S"

    def __new__(cls, value, str_repr):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.str_repr = str_repr
        return obj

    @cache
    def can_go(self, direction: Direction) -> bool:
        if self == PipeStatus.START:
            return True
        else:
            return direction.name in self.name

    @cached_property
    def directions(self) -> list[Direction]:
        return list(filter(lambda d: self.can_go(d), Direction.all()))

    @classmethod
    def from_char(cls, char: str) -> Self:
        for opt in cls.__members__.values():
            if opt.str_repr == char:
                return opt
        raise ValueError(f"Unknown char {char}")


class Board:
    def __init__(self, tiles: list[list[PipeStatus]]):
        self.tiles = tiles
        self.height = len(tiles)
        self.width = len(tiles[0])

    def status_at(self, x: int, y: int) -> PipeStatus:
        if 0 <= x < self.width:
            if 0 <= y < self.height:
                return self.tiles[y][x]
        return PipeStatus.EMPTY

    def neighbour_at(self, x: int, y: int, direction: Direction) -> PipeStatus:
        new_x, new_y = direction.next_coords(x, y)
        return self.status_at(new_x, new_y)

    @cached_property
    def start_coordinates(self) -> tuple[int, int]:
        for x in range(0, self.width):
            for y in range(0, self.height):
                if self.status_at(x, y) == PipeStatus.START:
                    return x, y
        raise ValueError("Lose the starting square, shouldn't happen!!")

    def cleanup(self):
        max_change = self.width * self.height
        total_changed = 0
        changed = 1
        while changed > 0:
            changed = 0
            for x in range(0, self.width):
                for y in range(0, self.height):
                    for direction in self.status_at(x, y).directions:
                        # Tile can have been cleaned by the previous direction. In exchange we check START too often
                        if self.status_at(x, y) not in [PipeStatus.EMPTY, PipeStatus.START]:
                            if not self.neighbour_at(x, y, direction).can_go(direction.opposite):
                                if DEBUG:
                                    print(f"Clearing tile at {x}, {y} of {self.status_at(x, y)} because neighbour {direction}, namely {self.neighbour_at(x, y, direction)} cannot connect")
                                self.tiles[y][x] = PipeStatus.EMPTY
                                changed += 1
            total_changed += changed
            print(f"Cleanup round has cleaned {changed} tiles. Total_changed: {total_changed} of {max_change}")
            if DEBUG:
                self.print()

    def print(self):
        print("Board: ")
        for line in self.tiles:
            print("".join(tile.str_repr for tile in line))
        print("")

    @staticmethod
    def from_lines(lines: list[str]) -> Self:
        tiles = [[PipeStatus.from_char(char) for char in line] for line in lines]
        return Board(tiles)

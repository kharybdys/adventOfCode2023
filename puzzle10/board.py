from collections import Counter
from enum import Enum
from functools import cache, cached_property
from typing import Self, Generator

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


class InsideOutsideStatus(Enum):
    INSIDE = "INSIDE", "I"
    OUTSIDE = "OUTSIDE", "O"
    LOOP = "LOOP", "."
    UNKNOWN = "UNKNOWN", " "

    def __new__(cls, value, str_repr):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.str_repr = str_repr
        return obj


class Board:
    def __init__(self, tiles: list[list[PipeStatus]]):
        self.tiles = tiles
        self.height = len(tiles)
        self.width = len(tiles[0])
        self.categorization_width = 2 * self.width + 1
        self.categorization_height = 2 * self.height + 1
        self.categorization: list[list[InsideOutsideStatus]] = [[InsideOutsideStatus.UNKNOWN for _ in range(0, self.categorization_width)] for _ in range(0, self.categorization_height)]

    def status_at(self, x: int, y: int) -> PipeStatus:
        if 0 <= x < self.width:
            if 0 <= y < self.height:
                return self.tiles[y][x]
        return PipeStatus.EMPTY

    def categorization_status_at(self, x: int, y: int) -> InsideOutsideStatus:
        if 0 <= x < self.categorization_width:
            if 0 <= y < self.categorization_height:
                return self.categorization[y][x]
        return InsideOutsideStatus.UNKNOWN

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

    def record_loop(self, loop_coordinates: list[tuple[int, int]]):
        for x, y in loop_coordinates:
            new_x = 2 * x + 1
            new_y = 2 * y + 1
            self.categorization[new_y][new_x] = InsideOutsideStatus.LOOP
            if self.status_at(x, y) != PipeStatus.START:
                for new_x_2, new_y_2 in self.generate_new_categorization_coordinates_for_directions(new_x, new_y, self.status_at(x, y).directions):
                    self.categorization[new_y_2][new_x_2] = InsideOutsideStatus.LOOP
        self.print_categorization()
        # Validate. All coordinates marked loop should have at least two coordinates marked loop as neighbours
        for x in range(0, self.categorization_width):
            for y in range(0, self.categorization_height):
                if self.categorization_status_at(x, y) == InsideOutsideStatus.LOOP:
                    neighbours = Counter(self.categorization[new_y][new_x] for new_x, new_y in self.generate_new_categorization_coordinates_for_directions(x, y, Direction.all()))
                    if neighbours.get(InsideOutsideStatus.LOOP, 0) < 2:
                        raise ValueError(f"Incorrect loop recorded, all loop elements should have at least two loop neighbours. Failing at coordinate {x}, {y} with neighbours {neighbours}")

    def generate_new_coordinates_for_directions(self, x: int, y: int, directions: list[Direction]) -> Generator[tuple[int, int], None, None]:
        for direction in directions:
            new_x, new_y = direction.next_coords(x, y)
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                yield new_x, new_y

    def generate_new_categorization_coordinates_for_directions(self, x: int, y: int, directions: list[Direction]) -> Generator[tuple[int, int], None, None]:
        for direction in directions:
            new_x, new_y = direction.next_coords(x, y)
            if 0 <= new_x < self.categorization_width and 0 <= new_y < self.categorization_height:
                yield new_x, new_y

    def list_all_real_categorization_elements(self) -> Generator[InsideOutsideStatus, None, None]:
        for x in range(1, self.categorization_width, 2):
            for y in range(1, self.categorization_height, 2):
                yield self.categorization[y][x]

    def count_categorizations(self) -> dict[InsideOutsideStatus, int]:
        return Counter(self.list_all_real_categorization_elements())

    def categorize_board(self):
        total_changed = 0
        changed = 1
        while changed > 0:
            changed = 0
            for x in range(0, self.categorization_width):
                for y in range(0, self.categorization_height):
                    match self.categorization_status_at(x, y):
                        case InsideOutsideStatus.UNKNOWN:
                            # If this one is unknown but it's on the edge of the board, mark as outside
                            if x == 0 or y == 0 or x == self.categorization_width - 1 or y == self.categorization_height - 1:
                                self.categorization[y][x] = InsideOutsideStatus.OUTSIDE
                                changed += 1
                        case InsideOutsideStatus.OUTSIDE:
                            # neighbours on UNKNOWN can be marked the same
                            for new_x, new_y in self.generate_new_categorization_coordinates_for_directions(x, y, Direction.all()):
                                if self.categorization_status_at(new_x, new_y) == InsideOutsideStatus.UNKNOWN:
                                    self.categorization[new_y][new_x] = InsideOutsideStatus.OUTSIDE
                                    changed += 1
            total_changed += changed
            print(f"Categorizing has changed {changed} elements, for a total of {total_changed}")

    def print(self):
        print("Board: ")
        for line in self.tiles:
            print("".join(tile.str_repr for tile in line))
        print("")

    def print_categorization(self):
        print("Categorization board: ")
        for line in self.categorization:
            print("".join(tile.str_repr for tile in line))
        print("")

    @staticmethod
    def from_lines(lines: list[str]) -> Self:
        tiles = [[PipeStatus.from_char(char) for char in line] for line in lines]
        return Board(tiles)

from enum import Enum
from typing import Optional, Self


class FloorStatus(Enum):
    EAST = "EAST", ">"
    SOUTH = "SOUTH", "v"
    EMPTY = "EMPTY", "."

    def __new__(cls, value, str_repr):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.str_repr = str_repr
        return obj

    def __bool__(self) -> bool:
        return not self == FloorStatus.EMPTY

    def next_coords(self, x: int, y: int) -> tuple[int, int]:
        match self:
            case FloorStatus.SOUTH:
                return x, y+1
            case FloorStatus.EAST:
                return x+1, y
            case _:
                raise NotImplementedError("Cannot provide next coordinates for an empty floor slot")

    @classmethod
    def from_char(cls, char: str) -> Self:
        for opt in cls.__members__.values():
            if opt.str_repr == char:
                return opt
        raise ValueError(f"Unknown char {char}")


class SeaFloor:
    def __init__(self, floor: list[list[FloorStatus]]):
        self.floor = floor

    @staticmethod
    def parse(puzzle_input: list[str]) -> Self:
        return SeaFloor(floor=[[FloorStatus.from_char(char) for char in line] for line in puzzle_input])

    def _move_only(self, floor: list[list[FloorStatus]], new_floor: list[list[FloorStatus]], restrict_to: FloorStatus) -> bool:
        moved = False
        for y, line in enumerate(floor):
            for x, element in enumerate(line):
                if cucumber := self.status_at(x, y, self.floor):
                    if cucumber == restrict_to:
                        next_x, next_y = self.wrap(*cucumber.next_coords(x, y))
                        if not self.status_at(next_x, next_y, floor) and not self.status_at(next_x, next_y, new_floor):
                            new_floor[next_y][next_x] = cucumber
                            moved = True
                        else:
                            new_floor[y][x] = cucumber
        return moved

    def move(self) -> bool:
        new_floor: list[list[FloorStatus]] = [[FloorStatus.EMPTY] * len(self.floor[0]) for _ in range(len(self.floor))]
        moved_east = self._move_only(floor=self.floor, new_floor=new_floor, restrict_to=FloorStatus.EAST)
        moved_south = self._move_only(floor=self.floor, new_floor=new_floor, restrict_to=FloorStatus.SOUTH)
        self.floor = new_floor
        return moved_east or moved_south

    def print(self):
        print("Seafloor: ")
        for floor_line in self.floor:
            print("".join(tile.str_repr for tile in floor_line))

    def wrap(self, x: int, y: int) -> tuple[int, int]:
        new_x, new_y = x, y
        if new_y >= len(self.floor):
            new_y -= len(self.floor)
        line_length = len(self.floor[y])
        if new_x >= line_length:
            new_x -= line_length
        return new_x, new_y

    def status_at(self, x: int, y: int, floor: Optional[list[list[FloorStatus]]] = None) -> FloorStatus:
        if not floor:
            floor = self.floor
        return floor[y][x]

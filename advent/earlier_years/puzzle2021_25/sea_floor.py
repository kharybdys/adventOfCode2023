from typing import Optional, Self

from utils import PrintEnum


class FloorStatus(PrintEnum):
    EAST = "EAST", ">"
    SOUTH = "SOUTH", "v"
    EMPTY = "EMPTY", "."

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

    @staticmethod
    def _keep(floor_element: FloorStatus,  restrict_to: FloorStatus) -> FloorStatus:
        if floor_element == restrict_to:
            return floor_element
        else:
            return FloorStatus.EMPTY

    def _empty_but_keep(self, restrict_to: FloorStatus):
        return [[self._keep(floor_element=self.status_at(x, y),
                            restrict_to=restrict_to)
                 for x, new_floor_element in enumerate(new_line)]
                for y, new_line in enumerate(self.floor)]

    def _move_east(self) -> bool:
        new_floor: list[list[FloorStatus]] = self._empty_but_keep(restrict_to=FloorStatus.SOUTH)
        moved = self._move_only(floor=self.floor, new_floor=new_floor, restrict_to=FloorStatus.EAST)
        self.floor = new_floor
        return moved

    def _move_south(self) -> bool:
        new_floor: list[list[FloorStatus]] = self._empty_but_keep(restrict_to=FloorStatus.EAST)
        moved = self._move_only(floor=self.floor, new_floor=new_floor, restrict_to=FloorStatus.SOUTH)
        self.floor = new_floor
        return moved

    def move(self) -> bool:
        moved_east = self._move_east()
        moved_south = self._move_south()
        return moved_east or moved_south

    def print(self):
        print("Seafloor: ")
        for floor_line in self.floor:
            print("".join(tile.str_repr for tile in floor_line))

    def wrap(self, x: int, y: int) -> tuple[int, int]:
        new_x, new_y = x, y
        if new_y >= len(self.floor):
            new_y -= len(self.floor)
        line_length = len(self.floor[new_y])
        if new_x >= line_length:
            new_x -= line_length
        return new_x, new_y

    def status_at(self, x: int, y: int, floor: Optional[list[list[FloorStatus]]] = None) -> FloorStatus:
        if not floor:
            floor = self.floor
        return floor[y][x]

    def __eq__(self, other):
        if isinstance(other, SeaFloor):
            return self.floor == other.floor
        else:
            return False

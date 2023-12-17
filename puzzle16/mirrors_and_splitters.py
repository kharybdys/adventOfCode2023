from collections import deque, defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Self

from utils import Direction, Grid

DEBUG = False


@dataclass
class Beam:
    x: int
    y: int
    entry: Direction


class TileStatus(Enum):
    EMPTY = "EMPTY", "."
    MIRROR_TOPLEFT = "MIRROR_TOPLEFT", "\\"
    MIRROR_TOPRIGHT = "MIRROR_TOPRIGHT", "/"
    SPLITTER_HORIZONTAL = "SPLITTER_HORIZONTAL", "|"
    SPLITTER_VERTICAL = "SPLITTER_VERTICAL", "-"

    def __new__(cls, value, str_repr):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.str_repr = str_repr
        return obj

    def empty(self) -> bool:
        return self == TileStatus.EMPTY

    def beam_to(self, entry: Direction) -> list[Direction]:
        match self:
            case TileStatus.EMPTY:
                return [entry.opposite]
            case TileStatus.SPLITTER_VERTICAL if entry in [Direction.EAST, Direction.WEST]:
                return [entry.opposite]
            case TileStatus.SPLITTER_VERTICAL:
                return [Direction.EAST, Direction.WEST]
            case TileStatus.SPLITTER_HORIZONTAL if entry in [Direction.SOUTH, Direction.NORTH]:
                return [entry.opposite]
            case TileStatus.SPLITTER_HORIZONTAL:
                return [Direction.SOUTH, Direction.NORTH]
            case TileStatus.MIRROR_TOPRIGHT:
                return [self.handle_topright_mirror(entry)]
            case TileStatus.MIRROR_TOPLEFT:
                return [self.handle_topleft_mirror(entry)]
            case _:
                raise ValueError(f"Unknown TileStatus {self}, shouldn't be possible!")

    @staticmethod
    def handle_topleft_mirror(entry: Direction):
        match entry:
            case Direction.NORTH:
                return Direction.EAST
            case Direction.EAST:
                return Direction.NORTH
            case Direction.SOUTH:
                return Direction.WEST
            case Direction.WEST:
                return Direction.SOUTH
            case _:
                raise ValueError(f"Unknown Direction {entry}, shouldn't be possible!")

    @staticmethod
    def handle_topright_mirror(entry: Direction):
        match entry:
            case Direction.NORTH:
                return Direction.WEST
            case Direction.WEST:
                return Direction.NORTH
            case Direction.SOUTH:
                return Direction.EAST
            case Direction.EAST:
                return Direction.SOUTH
            case _:
                raise ValueError(f"Unknown Direction {entry}, shouldn't be possible!")

    @classmethod
    def from_char(cls, char: str) -> Self:
        for opt in cls.__members__.values():
            if opt.str_repr == char:
                return opt
        raise ValueError(f"Unknown char {char}")


def generate_beams_by_coords(grid: Grid, initial_beam: Beam) -> dict[tuple[int, int], set[Direction]]:
    result: dict[tuple[int, int], set[Direction]] = defaultdict(set)
    current_beams = deque()
    current_beams.append(initial_beam)
    while current_beams:
        beam = current_beams.popleft()
        if beam.entry in result.get((beam.x, beam.y), set()):
            if DEBUG:
                print(f"Detecting cycle, already got {beam.entry} at {beam.x}, {beam.y}")
        else:
            result[(beam.x, beam.y)].add(beam.entry)
            for exit_direction in grid.value_at(beam.x, beam.y).beam_to(beam.entry):
                new_x, new_y = exit_direction.next_coords(beam.x, beam.y)
                if grid.within_bounds(new_x, new_y):
                    new_beam = Beam(new_x, new_y, exit_direction.opposite)
                    current_beams.append(new_beam)
                    if DEBUG:
                        print(f"Beam from {beam.entry} at {beam.x}, {beam.y}, causes new beam from {new_beam.entry} at {new_beam.x}, {new_beam.y}")
    return result

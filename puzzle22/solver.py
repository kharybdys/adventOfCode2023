import re

from collections import namedtuple, defaultdict
from dataclasses import dataclass, field
from functools import cached_property
from typing import Generator, Self, ClassVar

DEBUG = False

Point3D = namedtuple("Point3D", ["x", "y", "z"])


@dataclass
class Brick:
    ident: int
    start_x: int
    start_y: int
    start_z: int
    end_x: int
    end_y: int
    end_z: int
    held_up_by: set[Self] = field(default_factory=set)
    PATTERN: ClassVar[re.Pattern] = re.compile(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)")

    def generate_coords(self) -> Generator[Point3D, None, None]:
        for x in range(self.start_x, self.end_x + 1):
            for y in range(self.start_y, self.end_y + 1):
                for z in range(self.start_z, self.end_z + 1):
                    yield Point3D(x=x, y=y, z=z)

    # Can be cached because it is only used after dropping the brick down
    @cached_property
    def coords(self) -> set[Point3D]:
        return set(self.generate_coords())

    @property
    def min_z(self) -> int:
        return min(self.start_z, self.end_z)

    def __repr__(self) -> str:
        return f"Brick(ident={self.ident}, start=({self.start_x}, {self.start_y}, {self.start_z}), end=({self.end_x}, {self.end_y}, {self.end_z}), held_up_by={[b.ident for b in self.held_up_by]}"

    def __hash__(self):
        return hash(self.ident)

    def __eq__(self, other):
        if isinstance(other, Brick):
            return self.ident == other.ident
        else:
            raise ValueError(f"Cannot compare with {other}")

    @staticmethod
    def from_line(ident: int, line: str) -> Self:
        if match := Brick.PATTERN.fullmatch(line):
            return Brick(ident=ident,
                         start_x=int(match[1]),
                         start_y=int(match[2]),
                         start_z=int(match[3]),
                         end_x=int(match[4]),
                         end_y=int(match[5]),
                         end_z=int(match[6])
                         )
        else:
            raise ValueError(f"Invalid line {line}")


def get_lower_bricks(bricks_per_min_z: dict[int, list[Brick]], max_z: int) -> Generator[Brick, None, None]:
    for z in bricks_per_min_z.keys():
        if z < max_z:
            yield from bricks_per_min_z[z]


def parse(puzzle_input: list[str]) -> dict[int, list[Brick]]:
    bricks_per_min_z = defaultdict(list)
    for ident, line in enumerate(puzzle_input):
        brick = Brick.from_line(ident, line)
        bricks_per_min_z[brick.min_z].append(brick)
    return bricks_per_min_z


def drop_down_and_determine_held_up_by(bricks_per_min_z: dict[int, list[Brick]]):
    # Do the dropping down but also fill the held_up_by
    for min_z in sorted(bricks_per_min_z.keys()):
        if DEBUG:
            print(f"Dropping down bricks at original min_z: {min_z}, length of bricks to check: {len(bricks_per_min_z[min_z])}")
        for brick in bricks_per_min_z[min_z].copy():
            bricks_per_min_z[min_z].remove(brick)
            dropped_down = True
            while dropped_down:
                lower_bricks = list(get_lower_bricks(bricks_per_min_z, brick.min_z))
                if lower_bricks:
                    dropped_down_coords = set(Point3D(x, y, z-1) for x, y, z in brick.generate_coords())
                    for lower_brick in lower_bricks:
                        if not lower_brick.coords.isdisjoint(dropped_down_coords):
                            brick.held_up_by.add(lower_brick)
                            dropped_down = False
                else:
                    dropped_down = False
                if dropped_down:
                    brick.start_z = brick.start_z - 1
                    brick.end_z = brick.end_z - 1
            if DEBUG:
                if brick.min_z < min_z:
                    print(f"Dropped down brick to {brick}")
                else:
                    print(f"Cannot drop down {brick}")
            bricks_per_min_z[brick.min_z].append(brick)
    return bricks_per_min_z


def split_bricks_on_removable(bricks_per_min_z: dict[int, list[Brick]]) -> tuple[set[Brick], set[Brick], set[Brick]]:
    all_bricks = set()
    non_removable_bricks = set()
    for min_z in sorted(bricks_per_min_z.keys()):
        if DEBUG:
            print(f"Listing bricks at min_z {min_z}")
        for brick in bricks_per_min_z[min_z]:
            if DEBUG:
                print(f"{brick}")
            all_bricks.add(brick)
            if len(brick.held_up_by) == 1:
                non_removable_bricks.update(brick.held_up_by)
    return all_bricks, all_bricks - non_removable_bricks, non_removable_bricks


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    bricks_per_min_z = parse(puzzle_input)

    bricks_per_min_z = drop_down_and_determine_held_up_by(bricks_per_min_z)

    _, removable_bricks, _ = split_bricks_on_removable(bricks_per_min_z)
    print(len(removable_bricks))


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    bricks_per_min_z = parse(puzzle_input)

    bricks_per_min_z = drop_down_and_determine_held_up_by(bricks_per_min_z)

    all_bricks, _, non_removable_bricks = split_bricks_on_removable(bricks_per_min_z)
    print(f"Got {len(non_removable_bricks)} non_removable_bricks to check")
    solution = 0
    for start_brick in non_removable_bricks:
        removed_bricks: set[Brick] = set()
        removed_bricks.add(start_brick)
        new_collapses = True
        while new_collapses:
            new_collapses = False
            for brick in all_bricks - removed_bricks:
                if brick.held_up_by and brick.held_up_by.issubset(removed_bricks):
                    removed_bricks.add(brick)
                    new_collapses = True
        print(f"Removing brick {start_brick} results in a chain reaction of {len(removed_bricks) - 1}")
        solution += len(removed_bricks) - 1
    print(solution)

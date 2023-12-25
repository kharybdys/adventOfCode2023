from dataclasses import dataclass
from itertools import combinations
from typing import Generator, Iterable, Self, Counter


@dataclass
class Galaxy:
    id: int
    x: int
    y: int

    def distance(self, other: Self) -> int:
        if isinstance(other, Galaxy):
            return abs(self.x - other.x) + abs(self.y - other.y)
        else:
            raise ValueError("Cannot calculate a distance between Galaxy and something else")


def generate_galaxies(lines: list[str]) -> Generator[Galaxy, None, None]:
    ident = 1
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                yield Galaxy(ident, x, y)
                ident += 1


def galaxies_to_dict(galaxies: Iterable[Galaxy]) -> tuple[dict[tuple[int, int], Galaxy], int, int]:
    galaxies_by_coordinate: dict[tuple[int, int], Galaxy] = {}
    width = 0
    height = 0
    for g in galaxies:
        galaxies_by_coordinate[(g.x, g.y)] = g
        width = max(width, g.x)
        height = max(height, g.y)
    return galaxies_by_coordinate, width, height


def coordinates_to_corrections(coords: list[int], max_coord: int) -> dict[int, int]:
    result: dict[int, int] = {}
    counter = Counter(coords)
    correction = 0
    for i in range(0, max_coord):
        result[i] = correction
        if not counter.get(i):
            correction += 1
    return result


def expand_galaxies(galaxies: Iterable[Galaxy], increase_factor: int) -> Generator[Galaxy, None, None]:
    galaxies_by_coordinate, width, height = galaxies_to_dict(galaxies)
    x_coords, y_coords = zip(*galaxies_by_coordinate.keys())
    x_correction: dict[int, int] = coordinates_to_corrections(x_coords, width + 1)
    y_correction: dict[int, int] = coordinates_to_corrections(y_coords, height + 1)
    for g in galaxies_by_coordinate.values():
        yield Galaxy(id=g.id,
                     x=g.x + x_correction[g.x] * (increase_factor - 1),
                     y=g.y + y_correction[g.y] * (increase_factor - 1)
                    )


def print_galaxies(galaxies: Iterable[Galaxy]):
    galaxies_by_coordinate, width, height = galaxies_to_dict(galaxies)
    for y in range(0, height + 1):
        line: list[Galaxy] = []
        for x in range(0, width + 1):
            line.append(galaxies_by_coordinate.get((x, y), None))
        print("".join(map(lambda g: str(g.id) if g else ".", line)))


def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    galaxies = list(expand_galaxies(generate_galaxies(puzzle_input), 2))
    print_galaxies(galaxies)
    solution = 0
    for g1, g2 in combinations(galaxies, 2):
        distance = g1.distance(g2)
        print(f"Distance between galaxies {g1.id} and {g2.id} is {distance}")
        solution += distance
    print(solution)


def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    galaxies = list(expand_galaxies(generate_galaxies(puzzle_input), 1000000))
    solution = 0
    for g1, g2 in combinations(galaxies, 2):
        distance = g1.distance(g2)
        print(f"Distance between galaxies {g1.id} and {g2.id} is {distance}")
        solution += distance
    print(solution)

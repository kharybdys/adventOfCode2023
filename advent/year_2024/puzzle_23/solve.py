from collections.abc import Generator
from itertools import combinations
from typing import Self

from registry import register_solver


class Vertex:
    def __init__(self, key: str):
        self.key = key
        self.connections: set[Vertex] = set()

    def add_connection(self, other: Self):
        self.connections.add(other)

    @property
    def reachable_from(self) -> set["Vertex"]:
        return self.connections.union({self})

    def __hash__(self) -> int:
        return hash(self.key)

    def __eq__(self, other) -> bool:
        if isinstance(other, Vertex):
            return self.key == other.key
        else:
            return False

    def __repr__(self) -> str:
        return f"Vertex[key={self.key}, connections={[connection.key for connection in self.connections]}"


def parse(lines: list[str]) -> dict[str, Vertex]:
    result = {}
    for line in lines:
        line_split = line.split("-")
        if len(line_split) != 2:
            raise ValueError(f"Invalid initial value line: {line}")
        if line_split[0] not in result:
            result[line_split[0]] = Vertex(line_split[0])
        if line_split[1] not in result:
            result[line_split[1]] = Vertex(line_split[1])
        result[line_split[0]].add_connection(result[line_split[1]])
        result[line_split[1]].add_connection(result[line_split[0]])
    return result


def find_threesomes_with(vertex: Vertex) -> Generator[tuple[str], None, None]:
    print(f"Checking threesome for {vertex=}")
    for connection in vertex.connections:
        print(f"Verifying {connection=}")
        if shared := connection.connections.intersection(vertex.connections):
            print("Threesome found!")
            for value in shared:
                yield tuple(sorted([vertex.key, connection.key, value.key]))


@register_solver(year="2024", key="23", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    vertices = parse(puzzle_input)
    ord_a = ord("a")
    solutions: set[tuple[str]] = set()
    for ord_key in range(ord_a, ord_a + 26):
        key = f"t{chr(ord_key)}"
        if key in vertices:
            solutions.update(find_threesomes_with(vertices[key]))
    print(f"Solution is {len(solutions)}")


def find_biggest_connected_subgraph_with(vertex: Vertex) -> tuple[Vertex, ...]:
    for size in range(len(vertex.reachable_from), 2, -1):
        for connected in combinations(vertex.reachable_from, size):
            if all(connection.reachable_from.issuperset(connected) for connection in connected):
                return connected
    return ()


@register_solver(year="2024", key="23", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    vertices = parse(puzzle_input)
    solution: tuple[Vertex, ...] = ()
    # Destructively iterate
    while vertices:
        _, vertex = vertices.popitem()
        new_solution = find_biggest_connected_subgraph_with(vertex)
        if len(new_solution) > len(solution):
            solution = new_solution
        print(f"Solution {solution} after checking {vertex}")
        for connection in vertex.connections:
            connection.connections.remove(vertex)
    password = ",".join(sorted(vertex.key for vertex in solution))
    print(f"Solution is {password}")

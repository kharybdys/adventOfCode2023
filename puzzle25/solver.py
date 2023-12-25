import re
from collections import deque
from itertools import combinations
from pathlib import Path
from typing import Generator

from graph.base import Vertex, Edge


def parse(puzzle_input: list[str]) -> list[Vertex]:
    PATTERN = re.compile(r"(\w+): (.*)")
    vertices: dict[str, Vertex] = {}
    connections_by_vertex: dict[Vertex, str] = {}
    for line in puzzle_input:
        if match := PATTERN.fullmatch(line):
            vertex = Vertex(ident=match[1], x=0, y=0)
            vertices[vertex.ident] = vertex
            connections_by_vertex[vertex] = match[2]
    for vertex, connections in connections_by_vertex.items():
        for connection in connections.split():
            if connection not in vertices:
                new_vertex = Vertex(ident=connection, x=0, y=0)
                vertices[new_vertex.ident] = new_vertex
            end_vertex = vertices[connection]
            edge = Edge(start_vertex=vertex, end_vertex=end_vertex, weight=1)
            vertex.edges.append(edge)
            end_vertex.edges.append(edge)
    return list(vertices.values())


def generate_connected_vertices(edges: set[Edge]) -> Generator[list[Vertex], None, None]:
    if not edges:
        return None
    start_edge = edges.pop()
    vertices: set[Vertex] = {start_edge.start_vertex, start_edge.end_vertex}
    to_process: deque[Vertex] = deque()
    to_process.append(start_edge.start_vertex)
    to_process.append(start_edge.end_vertex)
    while to_process:
        vertex = to_process.pop()
        for edge in vertex.edges:
            if edge in edges:
                edges.remove(edge)
                if edge.start_vertex not in vertices:
                    vertices.add(edge.start_vertex)
                    to_process.append(edge.start_vertex)
                if edge.end_vertex not in vertices:
                    vertices.add(edge.end_vertex)
                    to_process.append(edge.end_vertex)
    yield vertices
    yield from generate_connected_vertices(edges)


def solve_a(puzzle_input: list[str]) -> None:
    # Disconnect 3 wires
    print(puzzle_input)
    vertices = parse(puzzle_input)
    edges: set[Edge] = set()
    for vertex in vertices:
        edges.update(vertex.edges)
    for e1, e2, e3 in combinations(edges, 3):
        # Remove e1, e2, e3 and check connectiveness
        new_edges = edges.copy()
        new_edges.difference_update({e1, e2, e3})
        connected_vertices = list(generate_connected_vertices(new_edges))
        if len(connected_vertices) == 2:
            lengths = [len(conn) for conn in connected_vertices]
            print(f"{lengths=}, {lengths[0] * lengths[1]}")


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    print("No Part Two on day 25")


def read_file() -> list[str]:
    data_dir = Path(__file__).parent.parent / "data"

    with open(data_dir / f"input25.txt", "rt") as file:
        return [line.rstrip() for line in file]


if __name__ == "__main__":
    solve_a(read_file())

import re

from advent.registry import register_solver
from advent.utils.graph import Vertex, VertexPath, find_all_paths

INPUT_PATTERN = re.compile(r"(?P<start>\w+):\s*(?P<ends>.*)\s*")


def build_graph(puzzle_input: list[str]) -> list[Vertex]:
    vertices: dict[str, Vertex] = {}
    for line in puzzle_input:
        match = INPUT_PATTERN.fullmatch(line)
        start_ident = match.group("start")
        end_idents = match.group("ends").split(" ")
        if start_ident not in vertices:
            vertices[start_ident] = Vertex(ident=start_ident, x=-1, y=-1)
        start_vertex = vertices[start_ident]
        for end_ident in end_idents:
            if end_ident not in vertices:
                vertices[end_ident] = Vertex(ident=end_ident, x=-1, y=-1)
            start_vertex.add_unidirectional_edge(other_vertex=vertices[end_ident], weight=1)
    return list(vertices.values())


def path_finished(path: VertexPath):
    return path.current_vertex.ident == "out"


@register_solver(year="2025", key="11", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    vertices = build_graph(puzzle_input)
    start_vertex = next(vertex for vertex in vertices if vertex.ident == "you")

    start_path = VertexPath(current_vertex=start_vertex)
    solution = len(list(find_all_paths(start_path, path_finished)))
    print(f"Solution is {solution}")


@register_solver(year="2025", key="11", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    solution = 0
    print(f"Solution is {solution}")

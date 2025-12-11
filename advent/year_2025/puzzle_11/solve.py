import re
from collections import defaultdict
from functools import partial

from advent.registry import register_solver
from advent.utils.graph import Vertex, VertexPath, find_all_paths, Edge

INPUT_PATTERN = re.compile(r"(?P<start>\w+):\s*(?P<ends>.*)\s*")


def build_graph(puzzle_input: list[str], ignore_vertices: set[str]) -> list[Vertex]:
    vertices: dict[str, Vertex] = {}
    for line in puzzle_input:
        match = INPUT_PATTERN.fullmatch(line)
        start_ident = match.group("start")
        if start_ident in ignore_vertices:
            continue
        end_idents = match.group("ends").split(" ")
        if start_ident not in vertices:
            vertices[start_ident] = Vertex(ident=start_ident, x=-1, y=-1)
        start_vertex = vertices[start_ident]
        for end_ident in end_idents:
            if end_ident not in vertices:
                vertices[end_ident] = Vertex(ident=end_ident, x=-1, y=-1)
            start_vertex.add_unidirectional_edge(other_vertex=vertices[end_ident], weight=1)
    return list(vertices.values())


def path_finished(path: VertexPath, target_idents: set[str]):
    return path.current_vertex.ident in target_idents


@register_solver(year="2025", key="11", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    vertices = build_graph(puzzle_input)
    start_vertex = next(vertex for vertex in vertices if vertex.ident == "you")

    start_path = VertexPath(current_vertex=start_vertex)
    solution = len(list(find_all_paths(start_path, partial(path_finished, target_idents={"out"}))))
    print(f"Solution is {solution}")


def calculate_path_count_to_vertex(start_vertex: Vertex, vertices: set[Vertex]) -> dict[Vertex, int]:
    edges_by_endpoint: dict[Vertex, set[Edge]] = defaultdict(set)
    for vertex in vertices:
        for edge in vertex.edges:
            edges_by_endpoint[edge.end_vertex].add(edge)

    print("edges_by_endpoint keys " + str({vertex.ident for vertex in edges_by_endpoint.keys()}))
    path_count_to_vertex: dict[Vertex, int] = {}

    path_count_to_vertex[start_vertex] = 1
    if start_vertex in edges_by_endpoint:
        del edges_by_endpoint[start_vertex]
    while edges_by_endpoint:
        next_vertex = next((vertex for vertex, edges in edges_by_endpoint.items() if all(edge.start_vertex in path_count_to_vertex for edge in edges)), None)
        if next_vertex is None:
            break
        path_count_to_vertex[next_vertex] = sum(path_count_to_vertex[edge.start_vertex] for edge in edges_by_endpoint[next_vertex])
        del edges_by_endpoint[next_vertex]

    print({vertex.ident: count for vertex, count in path_count_to_vertex.items()})
    return path_count_to_vertex


def get_vertices_reachable_from(start_vertex: Vertex) -> set[Vertex]:
    reachable_vertices: set[Vertex] = set()
    boundary_vertices: set[Vertex] = set()
    boundary_vertices.add(start_vertex)
    while boundary_vertices:
        current_vertex = boundary_vertices.pop()
        reachable_vertices.add(current_vertex)
        boundary_vertices.update(edge.end_vertex for edge in current_vertex.edges)

    return reachable_vertices


@register_solver(year="2025", key="11", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    vertices = build_graph(puzzle_input, ignore_vertices={"out", "dac", "fft"})
    start_vertex = next(vertex for vertex in vertices if vertex.ident == "svr")
    dac_vertex = next(vertex for vertex in vertices if vertex.ident == "dac")
    fft_vertex = next(vertex for vertex in vertices if vertex.ident == "fft")
    path_count_to_vertex = calculate_path_count_to_vertex(start_vertex=start_vertex, vertices=get_vertices_reachable_from(start_vertex))
    svr_to_dac_count = path_count_to_vertex.get(dac_vertex, 0)
    svr_to_fft_count = path_count_to_vertex.get(fft_vertex, 0)

    # Step two, DAC to FFT and OUT
    vertices = build_graph(puzzle_input, ignore_vertices={"svr", "out", "fft"})
    start_vertex = next(vertex for vertex in vertices if vertex.ident == "dac")
    fft_vertex = next(vertex for vertex in vertices if vertex.ident == "fft")
    out_vertex = next(vertex for vertex in vertices if vertex.ident == "out")
    path_count_to_vertex = calculate_path_count_to_vertex(start_vertex=start_vertex, vertices=get_vertices_reachable_from(start_vertex))
    dac_to_fft_count = path_count_to_vertex.get(fft_vertex, 0)
    dac_to_out_count = path_count_to_vertex.get(out_vertex, 0)

    # Step three, FFT to DAC and OUT
    vertices = build_graph(puzzle_input, ignore_vertices={"svr", "out", "dac"})
    start_vertex = next(vertex for vertex in vertices if vertex.ident == "fft")
    dac_vertex = next(vertex for vertex in vertices if vertex.ident == "dac")
    out_vertex = next(vertex for vertex in vertices if vertex.ident == "out")
    path_count_to_vertex = calculate_path_count_to_vertex(start_vertex=start_vertex, vertices=get_vertices_reachable_from(start_vertex))
    fft_to_dac_count = path_count_to_vertex.get(dac_vertex, 0)
    fft_to_out_count = path_count_to_vertex.get(out_vertex, 0)
    solution = svr_to_dac_count * dac_to_fft_count * fft_to_out_count + svr_to_fft_count * fft_to_dac_count * dac_to_out_count
    print(f"Solution is {solution}")

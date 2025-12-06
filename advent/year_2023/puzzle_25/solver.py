import re
from collections import deque
from copy import copy
from dataclasses import dataclass, field
from functools import cached_property
from itertools import combinations
from typing import Generator, Self

from advent.utils.graph import Vertex, Edge, print_graph
from registry import register_solver


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


def check_cuts(edges: set[Edge]) -> Generator[tuple[int, int], None, None]:
    # Far too naive
    attempts = 0
    for e1, e2, e3 in combinations(edges, 3):
        # Disconnect 3 wires
        # Remove e1, e2, e3 and check connectiveness
        new_edges = edges.copy()
        new_edges.difference_update({e1, e2, e3})
        connected_vertices = list(generate_connected_vertices(new_edges))
        if len(connected_vertices) == 2:
            lengths = [len(conn) for conn in connected_vertices]
            yield lengths[0], lengths[1]
        attempts += 1
        if attempts % 100 == 0:
            print(f"Attempts: {attempts:,}")


@dataclass
class PartitionAttempt:
    group_1: set[Vertex] = field(default_factory=set)
    group_2: set[Vertex] = field(default_factory=set)
    edges: set[Edge] = field(default_factory=set)

    def add_to_group_1(self, vertex: Vertex) -> Self:
        new_group_1 = copy(self.group_1)
        new_group_1.add(vertex)
        return PartitionAttempt(group_1=new_group_1, group_2=self.group_2, edges=self.edges)

    def add_to_group_2(self, vertex: Vertex) -> Self:
        new_group_2 = copy(self.group_2)
        new_group_2.add(vertex)
        return PartitionAttempt(group_1=self.group_1, group_2=new_group_2, edges=self.edges)

    @cached_property
    def cut_size(self) -> int:
        def in_cut(edge: Edge) -> bool:
            if edge.start_vertex in self.group_1 and edge.end_vertex in self.group_2:
                return True
            if edge.start_vertex in self.group_2 and edge.end_vertex in self.group_1:
                return True
            return False
        return len([edge for edge in self.edges if in_cut(edge)])


def form_partitions(vertices: set[Vertex], edges: set[Edge], max_cut_size: int) -> Generator[tuple[int, int], None, None]:
    # Also far too slow, the first "other_vertex" doesn't complete in hours of calculation
    start_vertex = vertices.pop()
    print(f"{start_vertex=}")
    for other_vertex in vertices:
        start_attempt = PartitionAttempt(group_1={start_vertex}, group_2={other_vertex}, edges=edges)
        attempts: deque[PartitionAttempt] = deque()
        max_size_attempts = 0
        attempts.append(start_attempt)
        print(f"Trying with {other_vertex=}")
        while attempts:
            attempt = attempts.pop()
            remaining_vertices = vertices.difference(attempt.group_1).difference(attempt.group_2)
            if attempt.cut_size <= max_cut_size:
                if remaining_vertices:
                    next_vertex = remaining_vertices.pop()
                    attempts.appendleft(attempt.add_to_group_1(next_vertex))
                    attempts.appendleft(attempt.add_to_group_2(next_vertex))
                else:
                    print(f"Found solution: {len(attempt.group_1), len(attempt.group_2)} with cut_size: {attempt.cut_size}")
                    yield len(attempt.group_1), len(attempt.group_2)
            else:
                print(f"Length remaining vertices: {len(remaining_vertices)}, stopping because cut_size: {attempt.cut_size}, attempts to check: {len(attempts)}")
            if len(attempts) > max_size_attempts:
                max_size_attempts = len(attempts)
            else:
                print(f"Reached {max_size_attempts=} without increasing further")


@dataclass
class GroupAttempt:
    vertices: set[Vertex]

    def add(self, vertex: Vertex) -> Self:
        new_vertices = copy(self.vertices)
        new_vertices.add(vertex)
        return GroupAttempt(vertices=new_vertices)

    def calculate_edge(self) -> tuple[set[Edge], set[Vertex]]:
        edges_on_edge = set()
        vertices_on_edge = set()
        for vertex in self.vertices:
            for edge in vertex.edges:
                if edge.start_vertex not in self.vertices:
                    edges_on_edge.add(edge)
                    vertices_on_edge.add(edge.start_vertex)
                if edge.end_vertex not in self.vertices:
                    edges_on_edge.add(edge)
                    vertices_on_edge.add(edge.end_vertex)
        return edges_on_edge, vertices_on_edge

    @property
    def primary_key(self) -> tuple:
        vertex_ids = [vertex.ident for vertex in self.vertices]
        return tuple(sorted(vertex_ids))


def form_groups(vertices: set[Vertex], edges: set[Edge], max_cut_size: int) -> Generator[tuple[int, int], None, None]:
    # Goes out of memory probably
    attempts: deque[GroupAttempt] = deque()
    tried_attempts: set[tuple] = set()
    for vertex in vertices:
        attempt = GroupAttempt(vertices={vertex})
        attempts.append(attempt)
        tried_attempts.add(attempt.primary_key)
    vertex_size = 1
    while attempts:
        attempt = attempts.pop()
        if len(attempt.vertices) > vertex_size:
            vertex_size = len(attempt.vertices)
            print(f"Starting on the next vertex size: {vertex_size}, attempts to check: {len(attempts)}")
        edges_on_edge, vertices_on_edge = attempt.calculate_edge()
        if 0 < len(edges_on_edge) <= max_cut_size:
            remaining_edges = edges.copy()
            remaining_edges.difference_update(edges_on_edge)
            connected_vertices = list(generate_connected_vertices(remaining_edges))
            if len(connected_vertices) == 2:
                lengths = [len(conn) for conn in connected_vertices]
                print(f"Answer: {lengths[0]}, {lengths[1]}, {lengths[0] * lengths[1]}")
                yield lengths[0], lengths[1]
            else:
                print(f"Edges {remaining_edges} do not result in a clean partition, namely {len(connected_vertices)}")
        else:
            for vertex in vertices_on_edge:
                new_attempt = attempt.add(vertex)
                if new_attempt.primary_key not in tried_attempts:
                    tried_attempts.add(new_attempt.primary_key)
                    attempts.appendleft(new_attempt)


@register_solver(year="2023", key="25", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    vertices = parse(puzzle_input)
    print_graph(vertices)
    edges: set[Edge] = set()
    for vertex in vertices:
        edges.update(vertex.edges)
    solutions = list(form_groups(set(vertices), edges, 3))
    print(f"{[(a, b, a * b) for a, b in solutions]}")


@register_solver(year="2023", key="25", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    print("No Part Two on day 25")

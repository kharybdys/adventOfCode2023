from dataclasses import dataclass, field
from typing import Self


class Vertex:
    def __init__(self, ident: str, x: int, y: int):
        self.ident = ident
        self.edges: list["Edge"] = []
        self.coords = (x, y)

    def add_unidirectional_edge(self, other_vertex: Self, weight: int):
        if not any(edge.end_vertex == other_vertex for edge in self.edges):
            new_edge = Edge(start_vertex=self, end_vertex=other_vertex, weight=weight)
            self.edges.append(new_edge)

    def add_bidirectional_edge(self, other_vertex: Self, weight: int):
        if not any(edge.between(self, other_vertex) for edge in self.edges):
            new_edge = Edge(start_vertex=self, end_vertex=other_vertex, weight=weight)
            self.edges.append(new_edge)
            other_vertex.edges.append(~new_edge)

    def __repr__(self) -> str:
        return f"Vertex(id={self.ident}, coords={self.coords}, edges: {self.edges})"

    def __hash__(self):
        return hash(self.ident)

    def __eq__(self, other):
        if isinstance(other, Vertex):
            return self.ident == other.ident
        else:
            raise ValueError(f"Cannot compare with {other}")


@dataclass
class Edge:
    start_vertex: Vertex
    end_vertex: Vertex
    weight: int

    def between(self, v1: Vertex, v2: Vertex) -> bool:
        return (v1 == self.start_vertex and v2 == self.end_vertex) or (v1 == self.end_vertex and v2 == self.start_vertex)

    def __repr__(self) -> str:
        return f"Edge(start={self.start_vertex.ident}, end={self.end_vertex.ident}, weight={self.weight})"

    def __invert__(self) -> Self:
        return Edge(start_vertex=self.end_vertex, end_vertex=self.start_vertex, weight=self.weight)

    def __hash__(self):
        return hash((self.start_vertex, self.end_vertex, self.weight))


@dataclass
class VertexPath:
    current_vertex: Vertex
    length: int = 0
    visited: set[Vertex] = field(default_factory=set)

    def move_to(self, vertex: Vertex) -> Self:
        for edge in self.current_vertex.edges:
            if edge.end_vertex == vertex:
                new_visited = self.visited.copy()
                new_visited.add(self.current_vertex)
                return VertexPath(current_vertex=vertex, length=self.length + edge.weight, visited=new_visited)
        raise ValueError(f"No path from {self.current_vertex} to {vertex}")


def print_graph(vertices: list[Vertex]):
    for vertex in vertices:
        edge_info = ", ".join(f"{edge.start_vertex.ident if edge.end_vertex == vertex else edge.end_vertex.ident}: {edge.weight}" for edge in vertex.edges)
        print(f"{vertex.ident}: {edge_info}")

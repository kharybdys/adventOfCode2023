from dataclasses import dataclass, field
from typing import Self


class Vertex:
    def __init__(self, ident: int, x: int, y: int):
        self.ident = ident
        self.edges: list["Edge"] = []
        self.coords = (x, y)

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

    def __repr__(self) -> str:
        return f"Edge(start={self.start_vertex.ident}, end={self.end_vertex.ident}, weight={self.weight})"

    def __invert__(self) -> Self:
        return Edge(start_vertex=self.end_vertex, end_vertex=self.start_vertex, weight=self.weight)


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

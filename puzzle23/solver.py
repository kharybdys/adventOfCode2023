from collections import deque
from dataclasses import field, dataclass
from typing import Generator, Self

from graph.base import Vertex, Edge, VertexPath
from utils import Grid, PrintEnum, Direction


class AbstractTile(PrintEnum):
    @property
    def can_move_to(self) -> bool:
        return not self.value == "FOREST"

    def allowed_exits(self) -> list[Direction]:
        match self.value:
            case "PATH":
                return Direction.all()
            case "FOREST":
                return Direction.all()
            case "SLOPE_SOUTH":
                return [Direction.SOUTH]
            case "SLOPE_NORTH":
                return [Direction.NORTH]
            case "SLOPE_EAST":
                return [Direction.EAST]
            case "SLOPE_WEST":
                return [Direction.WEST]
            case _:
                raise ValueError(f"Unsupported tile {self}")


class TileStatus(AbstractTile):
    PATH = "PATH", "."
    FOREST = "FOREST", "#"
    SLOPE_EAST = "SLOPE_EAST", ">"
    SLOPE_WEST = "SLOPE_WEST", "<"
    SLOPE_NORTH = "SLOPE_NORTH", "^"
    SLOPE_SOUTH = "SLOPE_SOUTH", "v"


class FreeTileStatus(AbstractTile):
    PATH = "PATH", "."
    FOREST = "FOREST", "#"
    SLOPE_EAST = "SLOPE_EAST", ">"
    SLOPE_WEST = "SLOPE_WEST", "<"
    SLOPE_NORTH = "SLOPE_NORTH", "^"
    SLOPE_SOUTH = "SLOPE_SOUTH", "v"

    def allowed_exits(self) -> list[Direction]:
        return Direction.all()


TileGrid = Grid[AbstractTile]
FreeTileGrid = Grid[FreeTileStatus]


@dataclass
class Path:
    x: int
    y: int
    visited: set[tuple[int, int]] = field(default_factory=set)

    @property
    def length(self) -> int:
        return len(self.visited)

    def move_to(self, new_x: int, new_y: int) -> Self:
        new_visited = self.visited.copy()
        new_visited.add((self.x, self.y))
        return Path(x=new_x, y=new_y, visited=new_visited)


def find_all_paths(start: Path, grid: TileGrid) -> Generator[Path, None, None]:
    paths = deque()
    paths.append(start)
    while paths:
        path = paths.pop()
        if path.y == grid.height - 1:
            yield path
        for direction in grid.value_at(path.x, path.y).allowed_exits():
            new_x, new_y = direction.next_coords(path.x, path.y)
            if grid.within_bounds(new_x, new_y) and grid.value_at(new_x, new_y).can_move_to and (new_x, new_y) not in path.visited:
                paths.append(path.move_to(new_x, new_y))


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    start_path = Path(0, 0)
    for x in range(0, grid.width):
        if grid.value_at(x, 0).can_move_to:
            start_path = Path(x, 0)
    solution = max(find_all_paths(start_path, grid), key=lambda p: p.length)
    print(f"Found max path with length {solution.length}")


def generate_graph(start_vertex: Vertex, grid: TileGrid) -> list[Vertex]:
    def valid_direction(direction: Direction, x: int, y: int) -> bool:
        new_x, new_y = direction.next_coords(x, y)
        within = grid.within_bounds(new_x, new_y)
        can_move_to = within and grid.value_at(new_x, new_y).can_move_to
        not_visited = (new_x, new_y) not in visited_coords
        return within and can_move_to and not_visited

    vertices: dict[tuple[int, int], Vertex] = {start_vertex.coords: start_vertex}
    current_ident = 1

    to_process: set[tuple[Direction, Vertex]] = set()
    to_process.add((Direction.SOUTH, start_vertex))
    while to_process:
        start_direction, vertex = to_process.pop()
        visited_coords: set[tuple[int, int]] = set()
        x, y = vertex.coords
        # Do the first step
        visited_coords.add((x, y))
        x, y = start_direction.next_coords(x, y)
        # Start the pathing
        allowed_exits = list(filter(lambda d: valid_direction(d, x, y), [direction for direction in grid.value_at(x, y).allowed_exits()]))
        while len(allowed_exits) == 1:
            visited_coords.add((x, y))
            x, y = allowed_exits[0].next_coords(x, y)
            allowed_exits = list(filter(lambda d: valid_direction(d, x, y),
                                        [direction for direction in grid.value_at(x, y).allowed_exits()]))
        if len(allowed_exits) > 1:
            # Create a vertex
            if (x, y) in vertices:
                new_vertex = vertices[(x, y)]
            else:
                new_vertex = Vertex(current_ident, x, y)
                vertices[new_vertex.coords] = new_vertex
                current_ident += 1
                for direction in allowed_exits:
                    to_process.add((direction, new_vertex))
            new_edge = Edge(start_vertex=vertex, end_vertex=new_vertex, weight=len(visited_coords))
            vertex.edges.append(new_edge)
            new_vertex.edges.append(~new_edge)
        else:
            new_vertex = Vertex(current_ident, x, y)
            vertices[new_vertex.coords] = new_vertex
            current_ident += 1
            new_edge = Edge(start_vertex=vertex, end_vertex=new_vertex, weight=len(visited_coords))
            vertex.edges.append(new_edge)
            new_vertex.edges.append(~new_edge)
    return list(vertices.values())


def find_all_paths_graph(start_path: VertexPath, target_y: int) -> Generator[VertexPath, None, None]:
    paths: deque[VertexPath] = deque()
    paths.append(start_path)
    while paths:
        path = paths.pop()
        if path.current_vertex.coords[1] == target_y:
            yield path
        for edge in path.current_vertex.edges:
            if edge.end_vertex not in path.visited:
                paths.append(path.move_to(edge.end_vertex))


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    grid: FreeTileGrid = Grid.from_lines(puzzle_input, FreeTileStatus.from_char)
    start_x = 0
    for x in range(0, grid.width):
        if grid.value_at(x, 0).can_move_to:
            start_x = x
    start_vertex = Vertex(ident=0, x=start_x, y=0)
    vertices = generate_graph(start_vertex, grid)
    print(f"Graph generated, {vertices=}")
    solution = max(find_all_paths_graph(VertexPath(current_vertex=start_vertex), target_y=grid.height - 1), key=lambda p: p.length)
    print(f"Found max path with length {solution.length}")

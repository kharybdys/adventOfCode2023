from collections import deque
from typing import Generator, Callable

from graph.base import Vertex, VertexPath, print_graph
from utils import Grid, PrintEnum, Direction, T

DEBUG = False

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


def generate_graph(start_vertex: Vertex, grid: TileGrid) -> list[Vertex]:
    def valid_direction(direction: Direction, this_x: int, this_y: int, allow_return: bool = False) -> bool:
        new_x, new_y = direction.next_coords(this_x, this_y)
        within = grid.within_bounds(new_x, new_y)
        can_move_to = within and grid.value_at(new_x, new_y).can_move_to
        not_visited = allow_return or (new_x, new_y) not in visited_coords
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
                new_vertex = Vertex(str(current_ident), x, y)
                if DEBUG:
                    print(f"Crossroads: created new vertex {new_vertex}")
                    print(f"Came from vertex {vertex}")
                    print(f"{allowed_exits=}")
                vertices[new_vertex.coords] = new_vertex
                current_ident += 1
                for direction in list(filter(lambda d: valid_direction(d, x, y, allow_return=True),
                                        [direction for direction in grid.value_at(x, y).allowed_exits()])):
                    to_process.add((direction, new_vertex))
            vertex.add_unidirectional_edge(other_vertex=new_vertex, weight=len(visited_coords))
        else:
            new_vertex = Vertex(str(current_ident), x, y)
            if DEBUG:
                print(f"Dead end: created new vertex {new_vertex}")
                print(f"{allowed_exits=}")
                print(f"{visited_coords=}")
                print(f"{grid.value_at(x, y)}")
            vertices[new_vertex.coords] = new_vertex
            current_ident += 1
            vertex.add_unidirectional_edge(other_vertex=new_vertex, weight=len(visited_coords))
    return list(vertices.values())


def find_all_paths(start_path: VertexPath, target_y: int) -> Generator[VertexPath, None, None]:
    paths: deque[VertexPath] = deque()
    paths.append(start_path)
    while paths:
        path = paths.pop()
        if path.current_vertex.coords[1] == target_y:
            if DEBUG:
                print(f"Found path with length {path.length}")
            yield path
        for edge in path.current_vertex.edges:
            if edge.end_vertex not in path.visited:
                paths.append(path.move_to(edge.end_vertex))


def solve_for_grid(grid: TileGrid) -> int:
    start_x = 0
    for x in range(0, grid.width):
        if grid.value_at(x, 0).can_move_to:
            start_x = x
    start_vertex = Vertex(ident="0", x=start_x, y=0)
    vertices = generate_graph(start_vertex, grid)
    print(f"Graph generated, {vertices}")
    print_graph(vertices)
    solution = max(find_all_paths(VertexPath(current_vertex=start_vertex), target_y=grid.height - 1), key=lambda p: p.length)
    return solution.length


def ignore_certain_chars_converter(char: str, converter: Callable[[str], T]) -> T:
    match char:
        case "A" | "S" | "Q" | "T" | "R" | "D" | "E" | "Z" | "H":
            return converter(".")
        case _:
            return converter(char)


def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    grid: TileGrid = Grid.from_lines(puzzle_input, lambda c: ignore_certain_chars_converter(c, TileStatus.from_char))
    print(f"Found max path with length {solve_for_grid(grid)}")


def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    grid: FreeTileGrid = Grid.from_lines(puzzle_input, lambda c: ignore_certain_chars_converter(c, FreeTileStatus.from_char))
    print(f"Found max path with length {solve_for_grid(grid)}")

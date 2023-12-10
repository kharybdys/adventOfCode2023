from collections import deque
from dataclasses import dataclass

from puzzle10.board import Board, Direction, PipeStatus


@dataclass
class Step:
    x: int
    y: int
    step: 0

    def to_coords(self) -> tuple[int, int]:
        return self.x, self.y


def steps_furthest_loop(board: Board) -> int:
    progress: dict[tuple[int, int], Step] = {}
    current_coordinates = deque()
    start_x, start_y = board.start_coordinates
    start_step = Step(x=start_x, y=start_y, step=0)
    progress[start_step.to_coords()] = start_step
    for direction in Direction.all():
        if board.neighbour_at(start_x, start_y, direction).can_go(direction.opposite):
            current_coordinates.append(direction.next_coords(start_x, start_y))
    while current_coordinates:
        x, y = current_coordinates.popleft()
        previous_step = None
        previous_direction = None
        for direction in board.status_at(x, y).directions:
            if direction.next_coords(x, y) in progress:
                previous_step = progress[direction.next_coords(x, y)]
                previous_direction = direction
        if (x, y) in progress:
            if progress[(x, y)].step != previous_step.step + 1:
                raise ValueError(f"Invalid solution, one direction says {progress[(x,y)].step} the other {previous_step.step + 1}")
            return previous_step.step + 1
        else:
            progress[(x, y)] = Step(x=x, y=y, step=previous_step.step + 1)
            for direction in board.status_at(x, y).directions:
                if direction != previous_direction:
                    current_coordinates.append(direction.next_coords(x, y))


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    board = Board.from_lines(puzzle_input)
    board.print()
    # Cleanup not really needed
    board.cleanup()
    board.print()
    print(steps_furthest_loop(board))


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)

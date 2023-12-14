from puzzle14.dish import Dish


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    dish = Dish.from_lines(puzzle_input)
    dish.print_dish()
    dish.roll_north()
    dish.print_dish()
    print(dish.total_load_north())


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)

from puzzle2021_25.sea_floor import SeaFloor


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    moved = True
    steps = 0
    sea_floor = SeaFloor.parse(puzzle_input)
    while moved:
        moved = sea_floor.move()
        sea_floor.print()
        if moved:
            steps += 1
    print(f"Steps: {steps}")


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)

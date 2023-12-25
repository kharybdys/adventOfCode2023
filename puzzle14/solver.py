from puzzle14.dish import Dish, RockStatus


def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    dish = Dish.from_lines(puzzle_input)
    dish.print_dish()
    dish.roll_north()
    dish.print_dish()
    print(dish.total_load_north())


def run_cycles(dish: Dish, cycles: int) -> int:
    snapshots_to_cycle: dict[tuple[tuple[RockStatus]], int] = {dish.snapshot(): 0}
    load_by_cycle: dict[int, int] = {0: dish.total_load_north()}
    for cycle in range(1, cycles + 1):
        dish.spin_cycle()
        snapshot = dish.snapshot()
        # We can short-circuit
        if snapshot in snapshots_to_cycle:
            previous_cycle = snapshots_to_cycle[snapshot]
            cycles_to_go = cycles - cycle
            cycle_offset = cycles_to_go % (cycle - previous_cycle)
            end_cycle = previous_cycle + cycle_offset
            return load_by_cycle[end_cycle]
        snapshots_to_cycle[dish.snapshot()] = cycle
        load_by_cycle[cycle] = dish.total_load_north()
        if cycle % 10000 == 0:
            print(f"Just processed cycle {cycle} of {cycles}")
    return dish.total_load_north()


def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    CYCLES = 1000000000
    dish = Dish.from_lines(puzzle_input)
    print(run_cycles(dish, CYCLES))

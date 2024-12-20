from advent.year_2023.puzzle_20.cycle_analyzer import analyze
from advent.year_2023.puzzle_20.modules import Module, parse_module, OutputModule, Pulse, WatcherModule, send_pulse
from registry import register_solver

DEBUG = False


def parse(puzzle_input: list[str]) -> dict[str, Module]:
    modules_by_name: dict[str, Module] = {}
    all_destinations: set[str] = set()
    for line in puzzle_input:
        module = parse_module(line)
        modules_by_name[module.identifier] = module
        all_destinations.update(module.destination_strings)
    # Add OutputModules for those destinations not having a specifier line
    for dest in all_destinations.difference(modules_by_name.keys()):
        output = OutputModule(identifier=dest, destination_strings=[])
        modules_by_name[output.identifier] = output
    # Link all destinations
    for module in modules_by_name.values():
        module.destinations = [modules_by_name[dest] for dest in module.destination_strings if dest in modules_by_name]
        for dest in module.destinations:
            dest.register_receiver(module)
    return modules_by_name


def sum_low_high_pulse(pulse_tuples: list[tuple[int, int]]) -> tuple[int, int]:
    if DEBUG:
        print(f"{pulse_tuples}")
    if pulse_tuples:
        return tuple(map(sum, zip(*pulse_tuples)))
    else:
        return 0, 0


def count_pulses(max_cycle: int, modules_by_name: dict[str, Module]) -> tuple[int, int]:
    cycle_to_pulses: dict[int, tuple[int, int]] = {}
    for cycle in range(0, max_cycle):
        if DEBUG:
            print(f"Starting a cycle by pressing the button")
        elif cycle % 100000 == 0:
            print(f"Starting cycle {cycle:,}")
        high_pulse_count, low_pulse_count = send_pulse(Pulse(high_pulse=False, cycle=cycle, source="button", destination=modules_by_name["broadcaster"]))
        if DEBUG:
            print(f"{high_pulse_count}, {low_pulse_count} after cycle {cycle}")
        cycle_to_pulses[cycle] = high_pulse_count, low_pulse_count
    return sum_low_high_pulse(list(cycle_to_pulses.values()))


@register_solver(year="2023", key="20", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    modules_by_name = parse(puzzle_input)
    high_pulse_count, low_pulse_count = count_pulses(1000, modules_by_name)
    print(f"{high_pulse_count=}, {low_pulse_count=}, solution is {high_pulse_count * low_pulse_count}")


@register_solver(year="2023", key="20", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    modules_by_name = parse(puzzle_input)
    target_module = "rx"
    modules_by_name[target_module] = WatcherModule(identifier=target_module, destination_strings=[])
    if example:
        raise ValueError("This solution is tailored to the real input")
    analyze(
        modules_by_name=modules_by_name,
        start_module="broadcaster",
        target_module=target_module,
    )

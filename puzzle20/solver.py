from collections import deque

from puzzle20.modules import Module, parse_module, Pulse, OutputModule


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


def send_pulse(initial_pulse: Pulse) -> tuple[int, int]:
    high_pulse_count = 0
    low_pulse_count = 0
    pulses: deque[Pulse] = deque()
    pulses.append(initial_pulse)
    while pulses:
        pulse = pulses.popleft()
        if pulse.high_pulse:
            high_pulse_count += 1
        else:
            low_pulse_count += 1
        print(f"Sending pulse from {pulse.source}, high? {pulse.high_pulse} to {pulse.destination.identifier}")
        pulses.extend(pulse.process())
    return high_pulse_count, low_pulse_count


def sum_low_high_pulse(pulse_tuples: list[tuple[int, int]]) -> tuple[int, int]:
    print(f"{pulse_tuples}")
    if pulse_tuples:
        return tuple(map(sum, zip(*pulse_tuples)))
    else:
        return 0, 0


def count_pulses(max_cycle: int, puzzle_input: list[str]) -> tuple[int, int]:
    modules_by_name = parse(puzzle_input)
    cycle_to_pulses: dict[int, tuple[int, int]] = {}
    snapshot_to_cycle: dict[tuple[bool], int] = {}
    for cycle in range(0, max_cycle):
        snapshot = tuple(module.status for module in modules_by_name.values())
        if snapshot in snapshot_to_cycle:
            # Short-circuit
            previous_cycle = snapshot_to_cycle[snapshot]
            start_high, start_low = sum_low_high_pulse([v for k, v in cycle_to_pulses.items() if k < previous_cycle])
            sum_high, sum_low = sum_low_high_pulse([v for k, v in cycle_to_pulses.items() if previous_cycle <= k < cycle])
            repeats_for, extra_steps = divmod(max_cycle - previous_cycle, cycle - previous_cycle)
            extra_high, extra_low = sum_low_high_pulse([v for k, v in cycle_to_pulses.items() if previous_cycle <= k < previous_cycle + extra_steps])
            print(f"{previous_cycle=}, {cycle=}")
            print(f"{repeats_for=}, {extra_steps=}")
            print(f"{start_high=}, {start_low=}")
            print(f"{sum_high=}, {sum_low=}")
            print(f"{extra_high=}, {extra_low=}")
            return start_high + sum_high * repeats_for + extra_high, start_low + sum_low * repeats_for + extra_low
        snapshot_to_cycle[snapshot] = cycle
        print(f"Starting a cycle by pressing the button")
        high_pulse_count, low_pulse_count = send_pulse(Pulse(high_pulse=False, source="button", destination=modules_by_name["broadcaster"]))
        print(f"{high_pulse_count}, {low_pulse_count} after cycle {cycle}")
        cycle_to_pulses[cycle] = high_pulse_count, low_pulse_count
    return sum_low_high_pulse(list(cycle_to_pulses.values()))


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    high_pulse_count, low_pulse_count = count_pulses(1000, puzzle_input)
    print(f"{high_pulse_count=}, {low_pulse_count=}, solution is {high_pulse_count * low_pulse_count}")


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)

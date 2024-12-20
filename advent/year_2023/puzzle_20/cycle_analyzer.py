import math
from collections.abc import Generator
from dataclasses import dataclass
from functools import cached_property
from itertools import combinations

from advent.year_2023.puzzle_20.modules import Module, ConjunctionModule, send_pulse, Pulse, WatcherModule
from utils import Range


@dataclass
class Cycle:
    size: int
    high_signals: list[Range]


@dataclass
class ModuleArea:
    start_module: Module
    end_module: Module
    other_modules: dict[str, Module]

    @cached_property
    def size(self) -> int:
        return len(self.module_names)

    @cached_property
    def module_names(self) -> set[str]:
        return {self.start_module.identifier, self.end_module.identifier}.union(set(self.other_modules.keys()))

    @property
    def modules(self) -> Generator[Module, None, None]:
        yield self.start_module
        yield from self.other_modules.values()
        yield self.end_module


# Analysis of my input shows that each of the targets of the broadcaster is the start of a self-contained network
# that ends at ns (which is what leads to rx, the goal)
# So if we can figure out the cycle time of each of the four parts of this puzzle and at which times in that cycle
# ns gets a high signal, we can calculate a solution

def analyze(modules_by_name: dict[str, Module],
            start_module: str,
            target_module: str):
    cycles: list[Cycle] = []
    final_modules = list(module for module in modules_by_name.values() if target_module in module.destination_strings)
    if len(final_modules) != 1:
        raise ValueError("This analysis method can only work if there's one module leading to the target")
    if not isinstance(final_modules[0], ConjunctionModule):
        raise ValueError("This analysis method can only work if the one module leading to the target is a conjunction module")

    final_module = final_modules[0]
    module_areas = list(split_modules(modules_by_name[start_module], final_module))

    if sum(module_area.size for module_area in module_areas) != len(modules_by_name) - 3:
        raise ValueError("Failure at splitting the given modules in areas, we have leftovers")
    if any(not area_1.module_names.isdisjoint(area_2.module_names) for area_1, area_2 in combinations(module_areas, 2)):
        raise ValueError("Failure at splitting the given modules in areas, the areas are not distinct")

    for module_area in module_areas:
        cycles.append(calculate_cycle(module_area))
    print(f"{cycles}")

    if any(len(cycle.high_signals) != 1 for cycle in cycles):
        raise ValueError("Logic to draw a conclusion from the provided cycles needs every cycle to have only one high_signals Range")
    if any(cycle.high_signals[0].start + 1 != cycle.size for cycle in cycles):
        raise ValueError(
            "Logic to draw a conclusion from the provided cycles needs the start of the only high_signals Range to be size - 1")
    if any(cycle.high_signals[0].stop != cycle.size for cycle in cycles):
        raise ValueError(
            "Logic to draw a conclusion from the provided cycles needs the stop of the only high_signals Range to be size")

    solution = math.lcm(*[cycle.size for cycle in cycles])
    print(f"Solution is {solution}")


def split_modules(
        start_module: Module,
        end_module: Module,
) -> Generator[ModuleArea, None, None]:
    for area_start in start_module.destinations:
        print(f"Creating area starting at {area_start.identifier}")
        area_end: Module | None = None
        area_modules: set[Module] = set()
        new_area_modules: set[Module] = set(area_start.destinations)
        while new_area_modules:
            print(f"Adding modules with identifiers to area: {[module.identifier for module in new_area_modules]}")
            if area_ends := [module for module in new_area_modules if end_module in module.destinations]:
                if len(area_ends) != 1:
                    raise ValueError(f"Cannot handle multiple modules leading to {end_module.identifier} for this area")
                if area_end:
                    if area_end.identifier != area_ends[0].identifier:
                        raise ValueError(f"Found multiple area_ends: {area_end.identifier} and {area_ends[0].identifier}")
                else:
                    area_end = area_ends[0]
                new_area_modules.remove(area_end)

            area_modules.update(new_area_modules)
            new_area_modules = set(destination for module in new_area_modules for destination in module.destinations
                                   if destination not in area_modules)
        yield ModuleArea(
            start_module=area_start,
            end_module=area_end,
            other_modules={module.identifier: module for module in area_modules},
        )


def calculate_cycle(module_area: ModuleArea) -> Cycle:
    watcher = WatcherModule(identifier="watcher", destination_strings=[])
    module_area.end_module.destinations.append(watcher)
    cycle = 1
    send_pulse(
        Pulse(
            high_pulse=False,
            cycle=cycle,
            source="button",
            destination=module_area.start_module
        )
    )
    while any(module.status for module in module_area.modules):
        send_pulse(
            Pulse(
                high_pulse=False,
                cycle=cycle,
                source="button",
                destination=module_area.start_module
            )
        )
        cycle += 1
    return Cycle(size=cycle,
                 high_signals=watcher.high_signal_ranges,
                 )

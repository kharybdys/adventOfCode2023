import re
import traceback
from collections import deque
from collections.abc import Generator
from copy import deepcopy, copy
from typing import Self

from advent.registry import register_solver


class Lights:
    def __init__(
            self,
            target_lights: str,
            status: list[int] | None = None,
            presses: int | None = None,
    ):
        self.target = target_lights
        self.presses = presses or 0
        if status:
            self.status = status
        else:
            self.status = [0 for _ in range(len(target_lights))]

    def __repr__(self) -> str:
        return f"Lights[target={self.target}, presses={self.presses}, status={self.status}]"

    def switch(self, light_numbers: tuple[int], times: int = 1):
        for light_number in light_numbers:
            self.status[light_number] += times
        self.presses += times

    @property
    def lights(self) -> list[bool]:
        return [light % 2 == 1 for light in self.status]

    @property
    def lights_str(self) -> str:
        return "".join("#" if light else "." for light in self.lights)

    @property
    def done_lights(self) -> bool:
        return self.target == self.lights_str

    def __copy__(self) -> Self:
        return self.__class__(self.target, self.status, self.presses)


class Joltages(Lights):
    def __init__(
            self,
            target_lights: str,
            joltages: list[int],
            buttons: set[tuple[int]],
            status: list[int] | None = None,
            presses: int | None = None,
    ):
        super().__init__(target_lights=target_lights, status=status, presses=presses)
        self.joltages = joltages
        self.buttons = buttons

    def __repr__(self) -> str:
        return f"Joltages[target={self.target}, joltages={self.joltages}, buttons={self.buttons}, presses={self.presses}, status={self.status}]"

    @property
    def next_index_to_clear(self) -> int | None:
        """ Index with the least amount of buttons left referring it. """
        min_index, button_count = min(((index, sum(1 for button in self.buttons if index in button)) for index in self.remaining_indices), key=lambda t: t[1], default=None)
        return min_index

    @property
    def remaining_joltages(self) -> tuple[int]:
        return tuple(joltage - status for status, joltage in zip(self.status, self.joltages, strict=True))

    @property
    def remaining_indices(self) -> tuple[int]:
        return tuple(index for index, joltage in enumerate(self.remaining_joltages) if joltage > 0)

    @property
    def joltages_tuple(self) -> tuple[int]:
        return tuple(self.status)

    @property
    def done_joltages(self) -> bool:
        return self.status == self.joltages

    @property
    def invalid_joltages(self) -> bool:
        if any(joltage < 0 for joltage in self.remaining_joltages):
            return True
        for index in self.remaining_indices:
            if not any(button for button in self.buttons if index in button):
                return True

        return False

    @classmethod
    def from_lights(cls, lights: Lights, target_joltages: list[int], buttons: set[tuple[int]]):
        return cls(
            target_lights=lights.target,
            status=lights.status,
            presses=lights.presses,
            joltages=target_joltages,
            buttons=buttons,
        )

    def __copy__(self) -> Self:
        lights = super().__copy__()
        return self.from_lights(lights, deepcopy(self.joltages), deepcopy(self.buttons))


INPUT_PATTERN = re.compile(r"\[(?P<target>[.#]+)\]\s*\((?P<buttons>.*)\)\s*\{(?P<joltages>[\d,]+)\}")
BUTTON_SPLIT_PATTERN = re.compile(r"\)? \(?")


def parse_input_line(line: str) -> tuple[Lights, list[tuple[int]], list[int]]:
    match = INPUT_PATTERN.fullmatch(line)
    lights = Lights(target_lights=match.group("target"))
    buttons = [tuple(int(number) for number in button.split(",")) for button in BUTTON_SPLIT_PATTERN.split(match.group("buttons"))]
    joltages = [int(number) for number in match.group("joltages").split(",")]
    return lights, buttons, joltages


def solve_line_for_lights(line: str) -> int:
    print(f"Solving {line}")
    seen_stages: set[str] = set()
    lights, buttons, joltages = parse_input_line(line)
    attempts: deque[Lights] = deque()
    current_attempt = lights
    seen_stages.add(current_attempt.lights_str)
    while current_attempt and not current_attempt.done_lights:
        print(f"{current_attempt=}, {current_attempt.presses=}, {seen_stages=}")
        for button in buttons:
            print(f"Applying {button}")
            new_attempt = deepcopy(current_attempt)
            new_attempt.switch(button)
            if new_attempt.lights_str not in seen_stages:
                print(f"Adding {new_attempt=} coming from {current_attempt=} with {button}")
                seen_stages.add(new_attempt.lights_str)
                # Breadth-first search, so appendleft
                attempts.appendleft(new_attempt)
        current_attempt = attempts.pop() if len(attempts) > 0 else None
    return current_attempt.presses


def generate_splits(total: int, limits: list[int]) -> Generator[tuple[int, ...], None, None]:
    if len(limits) <= 0:
        raise ValueError(f"Invalid limits, got {total=}, {limits=}")
    elif len(limits) == 1:
        yield total,
    else:
        for i in range(0, total + 1):
            for split in generate_splits(total=total - i, limits=limits[1:]):
                yield tuple([i] + list(split))


def solve_line_for_joltages(line: str) -> int:
    print(f"Solving {line}")
    lights, buttons, target_joltages = parse_input_line(line)
    joltages = Joltages.from_lights(lights, target_joltages, set(buttons))
    attempts: deque[Joltages] = deque()
    solution = sum(target_joltages) + 1  # Solution cannot be this high

    current_attempt = joltages
    while current_attempt:
        print(f"{current_attempt=}")

        next_index_to_clear = current_attempt.next_index_to_clear
        if next_index_to_clear is None:
            raise ValueError(f"Got no buttons remaining for {current_attempt=}")
        print(f"Going to process all buttons referring {next_index_to_clear}")

        remaining_presses = current_attempt.joltages[next_index_to_clear] - current_attempt.status[next_index_to_clear]
        buttons_with_index = {
            button: max((current_attempt.remaining_joltages[index] for index in button if index != next_index_to_clear), default=remaining_presses)
            for button
            in current_attempt.buttons
            if next_index_to_clear in button
        }
        if len(buttons_with_index) > 0:
            for split in generate_splits(total=remaining_presses, limits=list(buttons_with_index.values())):
                new_attempt = deepcopy(current_attempt)
                for button, presses in zip(buttons_with_index, split):
                    new_attempt.switch(button, times=presses)
                if not new_attempt.invalid_joltages and new_attempt.presses < solution:
                    if new_attempt.done_joltages:
                        solution = min(solution, new_attempt.presses)
                        print(f"New solution is {solution}")
                    else:
                        new_attempt.buttons.difference_update(buttons_with_index)
                        # Depth first, we loop everything anyways, save on memory
                        attempts.append(new_attempt)

        current_attempt = attempts.pop() if len(attempts) > 0 else None
    return solution


@register_solver(year="2025", key="10", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    solution = 0
    for line in puzzle_input:
        solution += solve_line_for_lights(line)
    print(f"Solution is {solution}")


@register_solver(year="2025", key="10", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    solution = 0
    for line in puzzle_input:
        try:
            solution += solve_line_for_joltages(line)
        except Exception as e:
            print(f"Exception at line {line}")
            traceback.print_exception(e)
    print(f"Solution is {solution}")

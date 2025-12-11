import re
from collections import deque
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
            self._status = status
        else:
            self._status = [0 for _ in range(len(target_lights))]

    def __repr__(self) -> str:
        return f"Lights[target={self.target}, presses={self.presses}, status={self._status}]"

    def switch(self, light_numbers: list[int], times: int = 1):
        for light_number in light_numbers:
            self._status[light_number] += times
        self.presses += times

    @property
    def lights(self) -> list[bool]:
        return [light % 2 == 1 for light in self._status]

    @property
    def lights_str(self) -> str:
        return "".join("#" if light else "." for light in self.lights)

    @property
    def done_lights(self) -> bool:
        return self.target == self.lights_str

    def __copy__(self) -> Self:
        return self.__class__(self.target, self._status, self.presses)


class Joltages(Lights):
    def __init__(
            self,
            target_lights: str,
            status: list[int] | None = None,
            presses: int | None = None,
            joltages: list[int] | None = None
    ):
        super().__init__(target_lights=target_lights, status=status, presses=presses)
        self.joltages = joltages

    def __repr__(self) -> str:
        return f"Joltages[target={self.target}, joltages={self.joltages}, presses={self.presses}, status={self._status}]"

    @property
    def remaining_indices(self) -> tuple[int]:
        return tuple(index for index, joltage in enumerate(self.joltages) if self._status[index] < joltage)

    @property
    def joltages_tuple(self) -> tuple[int]:
        return tuple(self._status)

    @property
    def done_joltages(self) -> bool:
        return self._status == self.joltages

    @property
    def invalid_joltages(self) -> bool:
        return any(status > joltage for status, joltage in zip(self._status, self.joltages, strict=True))

    @classmethod
    def from_lights(cls, lights: Lights, target_joltages: list[int]):
        return cls(
            target_lights=lights.target,
            status=lights._status,
            presses=lights.presses,
            joltages=target_joltages,
        )

    def __copy__(self) -> Self:
        lights = super().__copy__()
        return self.from_lights(lights, copy(self.joltages))


INPUT_PATTERN = re.compile(r"\[(?P<target>[.#]+)\]\s*\((?P<buttons>.*)\)\s*\{(?P<joltages>[\d,]+)\}")
BUTTON_SPLIT_PATTERN = re.compile(r"\)? \(?")


def parse_input_line(line: str) -> tuple[Lights, list[list[int]], list[int]]:
    match = INPUT_PATTERN.fullmatch(line)
    lights = Lights(target_lights=match.group("target"))
    buttons = [[int(number) for number in button.split(",")] for button in BUTTON_SPLIT_PATTERN.split(match.group("buttons"))]
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


def solve_line_for_joltages(line: str) -> int:
    print(f"Solving {line}")
    lights, buttons, target_joltages = parse_input_line(line)
    joltages = Joltages.from_lights(lights, target_joltages)
    attempts: deque[Joltages] = deque()
    solution = sum(target_joltages) + 1  # Solution cannot be this high

    current_attempt = lights
    while current_attempt:
        # See if any number left to do only appears in one button:
        for index in current_attempt.remaining_indices:
            buttons_with_index = [button for button in buttons if index in button]
            if len(buttons_with_index) == 1:
                # Press it the expected amount of times
                lights.switch(buttons_with_index[0], target_joltages[index])
                buttons.remove(buttons_with_index[0])
                print(f"Removed {buttons_with_index[0]}, got {lights}")

        for button in buttons:
            new_attempt = deepcopy(current_attempt)
            new_attempt.switch(button)
            if not new_attempt.invalid_joltages:
                # Breadth-first search, so appendleft
                attempts.appendleft(new_attempt)
        current_attempt = attempts.pop() if len(attempts) > 0 else None
    return current_attempt.presses


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
        solution += solve_line_for_joltages(line)
    print(f"Solution is {solution}")

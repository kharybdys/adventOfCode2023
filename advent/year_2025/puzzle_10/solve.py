import re
from collections import deque
from copy import deepcopy
from typing import Self

from advent.registry import register_solver


class Lights:
    def __init__(self, target_lights: str, status: list[int] | None = None, presses: int | None = None):
        self.target = target_lights
        self.presses = presses or 0
        if status:
            self._status = status
        else:
            self._status = [0 for _ in range(len(target_lights))]

    def switch(self, light_numbers: list[int]):
        for light_number in light_numbers:
            self._status[light_number] += 1
        self.presses += 1

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


INPUT_PATTERN = re.compile(r"\[(?P<target>[.#]+)\]\s*\((?P<buttons>.*)\)\s*\{(?P<joltages>[\d,]+)\}")
BUTTON_SPLIT_PATTERN = re.compile(r"\)? \(?")


def parse_input_line(line: str) -> tuple[Lights, list[list[int]], list[int]]:
    match = INPUT_PATTERN.fullmatch(line)
    lights = Lights(match.group("target"))
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


@register_solver(year="2025", key="10", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    solution = 0
    for line in puzzle_input:
        solution += solve_line_for_lights(line)
    print(f"Solution is {solution}")


@register_solver(year="2025", key="10", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    solution = 0
    print(f"Solution is {solution}")

import re


def my_hash(string: str) -> int:
    result = 0
    for char in string:
        result += ord(char)
        result *= 17
        result = result % 256
    return result


def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    print(sum(my_hash(string) for string in puzzle_input[0].split(",")))


class LensBox:
    def __init__(self, identifier: int):
        self.identifier: int = identifier
        self.lenses: dict[str, int] = {}

    def remove_lens(self, label: str):
        if label in self.lenses:
            del self.lenses[label]

    def add_lens(self, label: str, strength: int):
        self.lenses[label] = strength

    def total_lens_power(self) -> int:
        result = 0
        for index, strength in enumerate(self.lenses.values(), 1):
            result += self.identifier * index * strength
        return result


def solve_b(puzzle_input: list[str], example: bool) -> None:
    REMOVE_PATTERN = re.compile(r"([a-z]+)-")
    ADD_PATTERN = re.compile(r"([a-z]+)=(\d)")
    print(puzzle_input)
    lens_boxes: dict[int, LensBox] = {}
    for i in range(1, 257):
        lens_boxes[i - 1] = LensBox(i)
    for instruction in puzzle_input[0].split(","):
        if match := REMOVE_PATTERN.fullmatch(instruction):
            lens_label = match[1]
            lens_boxes[my_hash(lens_label)].remove_lens(lens_label)
        elif match := ADD_PATTERN.fullmatch(instruction):
            lens_label = match[1]
            lens_strength = int(match[2])
            lens_boxes[my_hash(lens_label)].add_lens(lens_label, lens_strength)
    print(sum(lens_box.total_lens_power() for lens_box in lens_boxes.values()))

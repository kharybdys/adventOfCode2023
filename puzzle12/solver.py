import re
from collections import deque
from typing import Generator

from puzzle12.nonogram import to_nonogram_pattern, NonogramPattern


def extend_unknown_to_part_cache(max_length: int):
    for length in range(2, max_length + 1):
        current_key = "?" * length
        if current_key not in UNKNOWN_TO_PART_CACHE:
            result = []
            for previous_option in UNKNOWN_TO_PART_CACHE["?" * (length - 1)]:
                result.append(previous_option + ".")
                result.append(previous_option + "#")
            UNKNOWN_TO_PART_CACHE[current_key] = result


UNKNOWN_TO_PART_CACHE: dict[str, list[str]] = {"?": [".", "#"]}
PART_TO_POSSIBLE_PATTERN_CACHE: dict[str, list[list[int]]] = {}
STRING_TO_PATTERN_PATTERN: re.Pattern = re.compile(r"\.+")


def convert_string_to_pattern(line: str) -> list[int]:
    parts = STRING_TO_PATTERN_PATTERN.split(line)
    return list(filter(bool, map(len, parts)))


def _fill_in_splitted_part(splitted_part: list[str]) -> Generator[str, None, None]:
    if not splitted_part:
        yield ""
    else:
        current_part = splitted_part[0]
        if "?" in current_part:
            if current_part not in UNKNOWN_TO_PART_CACHE:
                extend_unknown_to_part_cache(len(current_part))
            for possible_part in UNKNOWN_TO_PART_CACHE[current_part]:
                yield from map(lambda s: possible_part + s, _fill_in_splitted_part(splitted_part[1:]))
        else:
            yield from map(lambda s: current_part + s, _fill_in_splitted_part(splitted_part[1:]))


SPLIT_ON_UNKNOWN_PATTERN = re.compile(r"(\?+)")


def fill_in_part(part: str) -> Generator[str, None, None]:
    yield from _fill_in_splitted_part(SPLIT_ON_UNKNOWN_PATTERN.split(part))


def part_to_possible_patterns(part: str) -> Generator[list[int], None, None]:
    for possible_part in fill_in_part(part):
        yield convert_string_to_pattern(possible_part)


def combinations_parts_to_pattern(parts: list[str], pattern: list[int]) -> int:
    total = 0
    if not parts and not pattern:
        return 1
    elif not parts:
        return 0
    else:
        part = parts[0]
        if part not in PART_TO_POSSIBLE_PATTERN_CACHE:
            PART_TO_POSSIBLE_PATTERN_CACHE[part] = list(part_to_possible_patterns(part))
        for part_pattern in PART_TO_POSSIBLE_PATTERN_CACHE[part]:
            if len(pattern) >= len(part_pattern) and all(a == b for a, b in zip(pattern, part_pattern)):
                used_up = len(part_pattern)
                total += combinations_parts_to_pattern(parts[1:], pattern[used_up:])

    return total


def parse_line(line: str, multiplier: int) -> tuple[list[str], list[int]]:
    parts_string, pattern_string = line.split()
    parts_string = "?".join([parts_string] * multiplier)
    pattern_string = ",".join([pattern_string] * multiplier)
    parts = STRING_TO_PATTERN_PATTERN.split(parts_string)
    pattern = list(map(int, pattern_string.split(",")))
    return parts, pattern


def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    solution = 0
    for line in puzzle_input:
        parts, pattern = parse_line(line, 1)
        combination_count = combinations_parts_to_pattern(parts, pattern)
        print(f"Line {line} results in combinations {combination_count}")
        solution += combination_count
    print(solution)


# TODO: Solution is far too slow with the increased input.
def solve_b_too_naive(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    solution = 0
    for line in puzzle_input:
        parts, pattern = parse_line(line, 5)
        combination_count = combinations_parts_to_pattern(parts, pattern)
        print(f"Line {line} results in combinations {combination_count}")
        solution += combination_count
    print(solution)


def solve_nonogram(initial_pattern: NonogramPattern, example: bool) -> int:
    combinations = 0
    patterns_to_check: deque[NonogramPattern] = deque()
    patterns_to_check.append(initial_pattern)
    while patterns_to_check:
        current_pattern = patterns_to_check.pop()
        if current_pattern.completed:
            if example:
                print(f"Completed pattern: {current_pattern}")
            if current_pattern.valid:
                combinations += 1
        else:
            white_counted = 0 if current_pattern.first_or_last else 1
            if example:
                print(f"Range from {current_pattern.remaining_whites_possible + white_counted} to {-1 + white_counted}")
            for new_white in range(current_pattern.remaining_whites_possible + white_counted, -1 + white_counted, -1):
                new_pattern = current_pattern.copy_and_next_white_length(new_white)
                if example:
                    print(f"Checking: {new_pattern=}")
                if new_pattern.matches:
                    if example:
                        print(f"Matches")
                    patterns_to_check.append(new_pattern)
    return combinations


def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    solution = 0
    for line in puzzle_input:
        initial_pattern = to_nonogram_pattern(line, 5)
        print(f"Initial pattern: {initial_pattern}")
        print(f"{initial_pattern.total_whites_possible=}")
        combination_count = solve_nonogram(initial_pattern, example)
        print(f"Line {line} results in combinations {combination_count}")
        solution += combination_count
    print(solution)

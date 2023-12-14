import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Self, Generator


def fill_unknown_to_part_cache(max_length: int) -> dict[str, list[str]]:
    result: dict[str, list[str]] = defaultdict(list)
    result["?"] = [".", "#"]
    for length in range(2, max_length + 1):
        current_key = "?" * length
        for previous_option in result["?" * (length - 1)]:
            result[current_key].append(previous_option + ".")
            result[current_key].append(previous_option + "#")
    return result


UNKNOWN_TO_PART_CACHE: dict[str, list[str]] = fill_unknown_to_part_cache(17)  # 17 is the max length of ?'s in the given input
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


def parse_line(line: str) -> tuple[list[str], list[int]]:
    parts_string, pattern_string = line.split()
    parts = STRING_TO_PATTERN_PATTERN.split(parts_string)
    pattern = list(map(int, pattern_string.split(",")))
    return parts, pattern


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    solution = 0
    for line in puzzle_input:
        parts, pattern = parse_line(line)
        combination_count = combinations_parts_to_pattern(parts, pattern)
        print(f"Line {line} results in combinations {combination_count}")
        solution += combination_count
    print(solution)


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)

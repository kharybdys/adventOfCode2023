import re
from collections import defaultdict
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


def solve_nonogram(pattern: NonogramPattern, example: bool) -> int:
    # dict blacks_covered to extra_whites_covered to combinations
    combinations_found: dict[int, dict[int, int]] = defaultdict(dict)
    for blacks_to_cover in range(0, len(pattern.black_pattern)):
        # print(f"{blacks_to_cover=}")
        for subtotal_extra_whites in range(0, pattern.total_whites_possible + 1):
            if blacks_to_cover == len(pattern.black_pattern) - 1 and not pattern.ends_empty(pattern.total_whites_possible - subtotal_extra_whites):
                # Final bit cannot be completely empty so impossible anyway
                continue
            is_first = blacks_to_cover == 0
            correction = 0 if is_first else 1
            combinations = 0
            # print(f"{subtotal_extra_whites=}, {correction=}")
            for next_extra_white_length in range(correction, subtotal_extra_whites + 1 + correction):
                previous_extra_white_length = subtotal_extra_whites - next_extra_white_length + correction
                if is_first and previous_extra_white_length != 0:
                    continue
                length_covered = pattern.minimum_length(blacks_to_cover) + previous_extra_white_length
                # print(f"{next_extra_white_length=}, {previous_extra_white_length=}, {length_covered=}")
                # Is this a valid setup
                if pattern.matches(start=length_covered,
                                   current_black_index=blacks_to_cover,
                                   extra_white_length=next_extra_white_length):
                    if blacks_to_cover == 0:
                        combinations += 1
                    else:
                        combinations += combinations_found[blacks_to_cover - 1][previous_extra_white_length]
                # print(f"{combinations=}")
            combinations_found[blacks_to_cover][subtotal_extra_whites] = combinations
    print(f"{combinations_found=}")
    return sum(combinations_found[len(pattern.black_pattern) - 1].values())


def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    solution = 0
    for line in puzzle_input:
        pattern = to_nonogram_pattern(line, 5)
        print(f"Pattern: {pattern}")
        print(f"{pattern.total_whites_possible=}")
        combination_count = solve_nonogram(pattern, example)
        print(f"Line {line} results in combinations {combination_count}")
        solution += combination_count
    print(solution)

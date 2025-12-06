from collections import defaultdict

from advent.registry import register_solver


def line_to_positions_dict(line: str) -> dict[int, list[int]]:
    result = defaultdict(list)
    for index, char in enumerate(line):
        result[int(char)].append(index)

    for key in result:
        result[key].sort(reverse=True)

    return result


def find_current_best_joltage(
    line: str,
) -> tuple[int, int]:
    line_to_positions = line_to_positions_dict(line)
    best_joltage = max(line_to_positions.keys())
    position = min(line_to_positions[best_joltage])
    return best_joltage, position


def calculate_max_joltage(line: str, joltage_length: int) -> int:
    min_position = 0
    result = 0
    line_len = len(line)
    for remaining in sorted(range(0, joltage_length), reverse=True):
        joltage, joltage_position = find_current_best_joltage(
            line[min_position:line_len - remaining],
        )
        min_position += joltage_position + 1
        result = result * 10 + joltage

    return result


@register_solver(year="2025", key="3", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    solution = 0
    for line in puzzle_input:
        solution += calculate_max_joltage(line, joltage_length=2)

    print(f"Solution is {solution}")


@register_solver(year="2025", key="3", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    solution = 0
    for line in puzzle_input:
        solution += calculate_max_joltage(line, joltage_length=12)

    print(f"Solution is {solution}")

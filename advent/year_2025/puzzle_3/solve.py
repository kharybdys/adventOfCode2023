from collections import defaultdict

from advent.registry import register_solver


def line_to_positions_dict(line: str) -> dict[int, list[int]]:
    result = defaultdict(list)
    for index, char in enumerate(line):
        result[int(char)].append(index)

    for key in result:
        result[key].sort(reverse=True)

    return result


def calculate_max_joltage(line: str) -> int:
    line_to_positions = line_to_positions_dict(line)
    first_digit = max(line_to_positions.keys())
    first_digit_position = min(line_to_positions[first_digit])
    # Ugly but works
    if first_digit_position == len(line) - 1:
        first_digit = max(key for key in line_to_positions.keys() if key != first_digit)
        first_digit_position = min(line_to_positions[first_digit])

    second_digit = max(key for key, positions in line_to_positions.items() if positions[0] > first_digit_position)

    return first_digit * 10 + second_digit


@register_solver(year="2025", key="3", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    solution = 0
    for line in puzzle_input:
        solution += calculate_max_joltage(line)

    print(f"Solution is {solution}")


@register_solver(year="2025", key="3", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(f"Solution is TBD")

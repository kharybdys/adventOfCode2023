from utils import split_in_groups_separated_by_empty_line


def validate_mirror_after(lines: list[str], mirror_after: int, expected_diffs: int) -> bool:
    total_diff = 0
    for i in range(0, min(mirror_after + 1, len(lines) - mirror_after - 1)):
        total_diff += diff_two_lines(lines[mirror_after - i], lines[mirror_after + 1 + i])
        if total_diff > expected_diffs:
            return False
    return total_diff == expected_diffs


def find_mirror_number(lines: list[str], factor: int, expected_diffs: int) -> int:
    for index, line in enumerate(lines[1:], start=1):
        if validate_mirror_after(lines, index - 1, expected_diffs):
            return index * factor
    return 0


def transpose(lines: list[str]) -> list[str]:
    return list(map(lambda l: "".join(l), zip(*lines)))


def print_lines(lines: list[str]):
    print("Header:")
    for line in lines:
        print(line)
    print("")


def diff_two_lines(l1: str, l2: str) -> int:
    return sum(1 for a, b in zip(l1, l2) if a != b)


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    solution = 0
    for lines in split_in_groups_separated_by_empty_line(puzzle_input):
        answer = find_mirror_number(lines, 100, 0) or find_mirror_number(transpose(lines), 1, 0)
        if not answer:
            raise ValueError("Cannot find mirror_number for current lines")
        print(f"Answer for next lines is {answer}: ")
        print_lines(lines)
        solution += answer
    print(solution)


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    solution = 0
    for lines in split_in_groups_separated_by_empty_line(puzzle_input):
        answer = find_mirror_number(lines, 100, 1) or find_mirror_number(transpose(lines), 1, 1)
        if not answer:
            raise ValueError("Cannot find mirror_number for current lines")
        print(f"Answer for next lines is {answer}: ")
        print_lines(lines)
        solution += answer
    print(solution)

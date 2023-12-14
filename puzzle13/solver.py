from utils import split_in_groups_separated_by_empty_line


def validate_mirror_after(lines: list[str], mirror_after: int) -> bool:
    for i in range(0, min(mirror_after + 1, len(lines) - mirror_after - 1)):
        if lines[mirror_after - i] != lines[mirror_after + 1 + i]:
            return False
    return True


def find_mirror_number(lines: list[str], factor: int) -> int:
    previous_line = lines[0]
    for index, line in enumerate(lines[1:], start=1):
        if line == previous_line:
            print(f"Validating mirror_after: {index - 1}")
            if validate_mirror_after(lines, index - 1):
                return index * factor
        previous_line = line
    return 0


def transpose(lines: list[str]) -> list[str]:
    return list(map(lambda l: "".join(l), zip(*lines)))


def print_lines(lines: list[str]):
    print("Header:")
    for line in lines:
        print(line)
    print("")


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    solution = 0
    for lines in split_in_groups_separated_by_empty_line(puzzle_input):
        answer = find_mirror_number(lines, 100) or find_mirror_number(transpose(lines), 1)
        if not answer:
            raise ValueError("Cannot find mirror_number for current lines")
        print(f"Answer for next lines is {answer}: ")
        print_lines(lines)
        solution += answer
    print(solution)


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)

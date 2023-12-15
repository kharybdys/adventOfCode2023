def my_hash(string: str) -> int:
    result = 0
    for char in string:
        result += ord(char)
        result *= 17
        result = result % 256
    return result


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    print(sum(my_hash(string) for string in puzzle_input[0].split(",")))

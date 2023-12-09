def calculate_next_element(elements: list[int]) -> int:
    if not any(elements):
        return 0
    elif len(elements) <= 1:
        raise ValueError("Cannot calculate next element, list too short!")
    else:
        divs = [b-a for a, b in zip(elements, elements[1:])]
        result = elements[-1] + calculate_next_element(divs)
        print(f"Returning {result} as next_element for {elements}")
        return result


def line_to_elements(line: str) -> list[int]:
    return list(map(int, line.split()))


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    solution = sum(calculate_next_element(line_to_elements(line)) for line in puzzle_input)
    print(solution)


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)

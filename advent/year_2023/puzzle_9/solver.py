from registry import register_solver


def calculate_previous_element(elements: list[int]) -> int:
    if not any(elements):
        return 0
    elif len(elements) <= 1:
        raise ValueError("Cannot calculate previous element, list too short!")
    else:
        divs = [b-a for a, b in zip(elements, elements[1:])]
        result = elements[0] - calculate_previous_element(divs)
        print(f"Returning {result} as previous_element for {elements}")
        return result


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


@register_solver(year="2023", key="9", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    solution = sum(calculate_next_element(line_to_elements(line)) for line in puzzle_input)
    print(solution)


@register_solver(year="2023", key="9", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    solution = sum(calculate_previous_element(line_to_elements(line)) for line in puzzle_input)
    print(solution)

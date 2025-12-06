import re
from collections import defaultdict
from collections.abc import Generator
from itertools import filterfalse

from advent.registry import register_solver
from advent.utils.solver import split_in_groups_separated_by_empty_line

# key needs to be before any of the set
_BEFORE_RULES: dict[int, set[int]] = defaultdict(set)
# key needs to be after any of the set
_AFTER_RULES: dict[int, set[int]] = defaultdict(set)


class Page:
    def __init__(self, value: str):
        self.value = int(value)

    def __lt__(self, other) -> bool:
        if isinstance(other, Page):
            if other.value in _BEFORE_RULES[self.value]:
                return False
            if self.value in _AFTER_RULES[other.value]:
                return False
            return True
        else:
            return False


def parse_rules(lines: list[str]):
    RULE_PATTERN = re.compile(r"(\d+)\|(\d+)")
    for line in lines:
        if result := RULE_PATTERN.fullmatch(line):
            _BEFORE_RULES[int(result[1])].add(int(result[2]))
            _AFTER_RULES[int(result[2])].add(int(result[1]))
        else:
            raise ValueError(f"Invalid rule pattern for {line}")


def parse_prints(lines: list[str]) -> Generator[list[Page], None, None]:
    PART_SEP = re.compile(r",")
    for line in lines:
        yield list(map(Page, PART_SEP.split(line)))


def parse(puzzle_input: list[str]) -> Generator[list[Page], None, None]:
    input_generator = split_in_groups_separated_by_empty_line(puzzle_input)
    parse_rules(next(input_generator))
    yield from parse_prints(next(input_generator))


def valid_line(line: list[Page]) -> bool:
    for i in range(len(line)):
        before = set(page.value for page in line[:i])
        this = line[i]
        after = set(page.value for page in line[i+1:])
        if before.intersection(_BEFORE_RULES[this.value]):
            return False
        if after.intersection(_AFTER_RULES[this.value]):
            return False
    return True


def find_middle(line: list[Page]) -> int:
    return line[len(line) // 2].value


def correct_ordering(line: list[Page]) -> list[Page]:
    return sorted(line)


@register_solver(year="2024", key="5", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    solution = sum(map(find_middle, filter(valid_line, parse(puzzle_input))))
    print(f"Solution is {solution}")


@register_solver(year="2024", key="5", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    solution = sum(map(find_middle, map(correct_ordering, filterfalse(valid_line, parse(puzzle_input)))))
    print(f"Solution is {solution}")

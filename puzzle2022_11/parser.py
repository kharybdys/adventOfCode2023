import re
from typing import Iterator, Optional

from puzzle2022_11.logger import LogStreamer
from puzzle2022_11.monkey import Monkey, ThrowTest
from puzzle2022_11.operation import parse_operation


def parse_puzzle_lines(puzzle_lines: list[str], logger: LogStreamer, monkey_cls: type) -> dict[int, Monkey]:
    result = {}
    lines_iterator = iter(puzzle_lines)
    while True:
        monkey = parse_monkey(lines_iterator, logger, monkey_cls)
        if monkey:
            result[monkey.monkey_id] = monkey
        else:
            return result


def parse_monkey(lines_iterator: Iterator[str], logger: LogStreamer, monkey_cls: type) -> Optional[Monkey]:
    MONKEY_PATTERN = re.compile(r"Monkey (\d+):")
    STARTING_ITEMS_PREFIX = "  Starting items: "
    OPERATION_PREFIX = "  Operation: "
    TEST_PATTERN = re.compile(r"\s+Test: divisible by (\d+)\s+If true: throw to monkey (\d+)\s+If false: throw to monkey (\d+)", re.MULTILINE)
    monkey_id = -1
    items = []
    operation = None
    test = None
    while line := next(lines_iterator, ""):
        if match := MONKEY_PATTERN.fullmatch(line):
            monkey_id = int(match[1])
        elif line.startswith(STARTING_ITEMS_PREFIX):
            items = list(map(int, [item.strip() for item in line.removeprefix(STARTING_ITEMS_PREFIX).split(",")]))
        elif line.startswith(OPERATION_PREFIX):
            operation = parse_operation(line.removeprefix(OPERATION_PREFIX), logger)
        else:
            lines = "\n".join([line, next(lines_iterator), next(lines_iterator)])
            if match := TEST_PATTERN.fullmatch(lines):
                test = ThrowTest(test_divisor=int(match[1]), to_monkey_id_on_true=int(match[2]), to_monkey_id_on_false=int(match[3]), logger=logger)
            else:
                raise ValueError(f"Invalid input for Monkey, {lines=}")
    if monkey_id >= 0 and items and operation and test:
        return monkey_cls(monkey_id=monkey_id, items=items, throw_test=test, operation=operation, logger=logger)
    else:
        return None

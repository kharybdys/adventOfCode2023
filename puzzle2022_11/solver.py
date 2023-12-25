from math import prod
from pathlib import Path

from puzzle2022_11.logger import LogStreamer
from puzzle2022_11.monkey import Monkey, WorrisomeMonkey
from puzzle2022_11.parser import parse_puzzle_lines


def expected_output(example: bool, postfix: str = "") -> list[str]:
    example_postfix = "_example" if example else ""
    with open(Path(__file__).parent / f"expected_output{postfix}{example_postfix}.txt", "rt") as file:
        return [line.strip() for line in file]


def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    logger = LogStreamer()
    monkeys: dict[int, Monkey] = parse_puzzle_lines(puzzle_input, logger, Monkey)
    for monkey in monkeys.values():
        monkey.register_monkeys(monkeys)
    print(f"Preparation done, monkeys are: {monkeys}")

    for i in range(1, 21):
        for monkey in monkeys.values():
            monkey.play_turn(i == 1)
        if i == 1:
            logger.log("")
        if i in [11, 16]:
            logger.log("...")
            logger.log("")
        if i in [15, 20] or i <= 10:
            logger.log(f"After round {i}, the monkeys are holding items with these worry levels:")
            for monkey in monkeys.values():
                monkey.report_items()
            logger.log("")
    if example:
        for log_line, expected_line in zip(logger.log_lines, expected_output(example)):
            if log_line != expected_line:
                print(f"Mismatch, {expected_line=}, {log_line=}")
    items_inspected = sorted([monkey.items_inspected for monkey in monkeys.values()], reverse=True)
    print(str(items_inspected[0] * items_inspected[1]))


def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    log_at = [1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    logger = LogStreamer()
    monkeys: dict[int, Monkey] = parse_puzzle_lines(puzzle_input, logger, WorrisomeMonkey)
    limit = prod(monkey.throw_test.test_divisor for monkey in monkeys.values())
    for monkey in monkeys.values():
        monkey.register_monkeys(monkeys)
        monkey.register_limit(limit)

    print(f"Preparation done, monkeys are: {monkeys}")

    for i in range(1, 10001):
        for monkey in monkeys.values():
            monkey.play_turn(False)
        if i in log_at:
            logger.log(f"== After round {i} ==")
            for monkey in monkeys.values():
                monkey.report_inspections()
            logger.log("")
    if example:
        for log_line, expected_line in zip(logger.log_lines, expected_output(example, postfix="_b")):
            if log_line != expected_line:
                print(f"Mismatch, {expected_line=}, {log_line=}")
    items_inspected = sorted([monkey.items_inspected for monkey in monkeys.values()], reverse=True)
    print(str(items_inspected[0] * items_inspected[1]))

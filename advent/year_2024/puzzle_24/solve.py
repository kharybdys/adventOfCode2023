import re
from collections.abc import Generator
from copy import copy, deepcopy
from dataclasses import dataclass
from enum import Enum
from itertools import permutations, batched
from typing import Self

from registry import register_solver
from utils import split_in_groups_separated_by_empty_line


class RuleType(Enum):
    AND = "AND"
    OR = "OR"
    XOR = "XOR"

    def apply(self, value_1: bool, value_2: bool) -> bool:
        match self:
            case RuleType.AND:
                return value_1 and value_2
            case RuleType.OR:
                return value_1 or value_2
            case RuleType.XOR:
                return value_1 ^ value_2
            case _:
                raise ValueError(f"Invalid RuleType: {self}")


@dataclass
class Rule:
    input_gate_strs: list[str]
    output_gate_str: str
    type: RuleType

    def applicable(self, values: dict[str, bool]) -> bool:
        return all(input_gate in values for input_gate in self.input_gate_strs)

    def apply(self, values: dict[str, bool]) -> bool:
        return self.type.apply(*[values[input_gate] for input_gate in self.input_gate_strs])

    def __copy__(self) -> Self:
        return Rule(input_gate_strs=self.input_gate_strs.copy(),
                    output_gate_str=self.output_gate_str,
                    type=self.type)


def parse_initial_values(lines: list[str]) -> dict[str, bool]:
    result = {}
    for line in lines:
        line_split = line.split(": ")
        if len(line_split) != 2:
            raise ValueError(f"Invalid initial value line: {line}")
        result[line_split[0]] = bool(int(line_split[1]))
    return result


def parse_rules(lines: list[str]) -> Generator[Rule, None, None]:
    rule_pattern = re.compile(r"(?P<input_1>\w+) (?P<type>(AND)|(OR)|(XOR)) (?P<input_2>\w+) -> (?P<output>\w+)")
    for line in lines:
        if line_match := rule_pattern.fullmatch(line):
            yield Rule(input_gate_strs=[line_match.group("input_1"), line_match.group("input_2")],
                       output_gate_str=line_match.group("output"),
                       type=RuleType(line_match.group("type")),
                       )
        else:
            raise ValueError(f"Invalid rule line: {line}")


def wire_values_to_value(wire_values: dict[str, bool], prefix: str) -> int:
    solution_digits = []
    for index in range(100):
        gate = f"{prefix}{index:02d}"
        if gate in wire_values:
            solution_digits.append(str(int(wire_values[gate])))
    solution_binary = "".join(reversed(solution_digits))
    return int(solution_binary, 2)


def run(initial_values: dict[str, bool], rules: list[Rule]) -> int:
    while rules:
        rule = next(filter(lambda r: r.applicable(initial_values), rules))
        if rule.output_gate_str in initial_values:
            raise ValueError(f"Already calculated a value for {rule.output_gate_str}")
        initial_values[rule.output_gate_str] = rule.apply(initial_values)
        rules.remove(rule)
    return wire_values_to_value(initial_values, "z")


@register_solver(year="2024", key="24", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    input_generator = split_in_groups_separated_by_empty_line(puzzle_input)
    initial_values = parse_initial_values(next(input_generator))
    rules = list(parse_rules(next(input_generator)))
    solution = run(initial_values, rules)
    print(f"Solution is {solution}")


def value_to_wire_values(value: int, prefix: str, digits: int) -> dict[str, bool]:
    result = {}
    for index, char in enumerate(reversed(f"{value:0{digits}b}")):
        result[f"{prefix}{index:02d}"] = bool(int(char))
    return result


def generate_initial_values(input_gates: set[str], example: bool) -> Generator[tuple[dict[str, bool], int], None, None]:
    highest_x_digit = max(int(gate[1:]) for gate in input_gates if gate.startswith("x")) + 1
    highest_y_digit = max(int(gate[1:]) for gate in input_gates if gate.startswith("y")) + 1
    for x in range(pow(2, highest_x_digit)):
        x_values = value_to_wire_values(x, "x", highest_x_digit)
        for y in range(pow(2, highest_y_digit)):
            y_values = value_to_wire_values(y, "y", highest_y_digit)
            initial_values = y_values.copy()
            initial_values.update(x_values)
            yield initial_values, x & y if example else x + y


def verify_rules(rules: list[Rule], example: bool) -> bool:
    input_gates = set()
    for rule in rules:
        input_gates.update(rule.input_gate_strs)
    for initial_values, z in generate_initial_values(input_gates, example):
        # print(f"{initial_values=}, {z=}, {rules=}")
        try:
            solution = run(initial_values, copy(rules))
            if solution != z:
                return False
        except StopIteration:
            return False
    return True


def swap_outputs(rules: list[Rule], index_1: int, index_2: int):
    output_gate = rules[index_1].output_gate_str
    rules[index_1].output_gate_str = rules[index_2].output_gate_str
    rules[index_2].output_gate_str = output_gate


@register_solver(year="2024", key="24", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    input_generator = split_in_groups_separated_by_empty_line(puzzle_input)
    # Skip the initial values
    _ = next(input_generator)
    rules = list(parse_rules(next(input_generator)))
    for indices in permutations(range(len(rules)), 4 if example else 8):
        print(f"Trying swaps: {indices}")
        swapped_rules = deepcopy(rules)
        for i_1, i_2 in batched(indices, 2):
            swap_outputs(swapped_rules, i_1, i_2)
        if verify_rules(swapped_rules, example):
            output_gates = [rules[index].output_gate_str for index in indices]
            solution = ",".join(sorted(output_gates))
            print(f"Solution is {solution}")
            return

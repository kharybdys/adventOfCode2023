import re
from collections import deque
from collections.abc import Generator
from copy import copy, deepcopy
from dataclasses import dataclass
from enum import Enum
from itertools import permutations, batched, chain, count
from typing import Self

from registry import register_solver
from advent.utils.solver import split_in_groups_separated_by_empty_line


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

    def __hash__(self):
        return hash(self.output_gate_str)

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
    print(f"{initial_values=}")
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


def generate_initial_values(input_gates: set[str], example: bool, barrier: int) -> Generator[tuple[dict[str, bool], int], None, None]:
    z_limit = pow(2, barrier)
    highest_x_digit = max(int(gate[1:]) for gate in input_gates if gate.startswith("x")) + 1
    highest_y_digit = max(int(gate[1:]) for gate in input_gates if gate.startswith("y")) + 1
    for x in range(pow(2, highest_x_digit)):
        x_values = value_to_wire_values(x, "x", highest_x_digit)
        for y in range(pow(2, highest_y_digit)):
            y_values = value_to_wire_values(y, "y", highest_y_digit)
            initial_values = y_values.copy()
            initial_values.update(x_values)
            z_value = x & y if example else x + y
            # if z_value < z_limit or True:
            print(f"{x=}, {y=}, {z_value=}")
            yield initial_values, z_value


def verify_rules(rules: list[Rule], example: bool, barrier: int) -> bool:
    input_gates = set()
    for rule in rules:
        input_gates.update(rule.input_gate_strs)
    for initial_values, z in generate_initial_values(input_gates, example, barrier):
        try:
            solution = run(initial_values, copy(rules))
            # print(f"{initial_values=}, {z=}, {rules=}, {solution=}")
            if solution != z and False:
                return False
        except StopIteration:
            return False
    return True


def swap_outputs(rules: list[Rule], index_1: int, index_2: int):
    output_gate = rules[index_1].output_gate_str
    rules[index_1].output_gate_str = rules[index_2].output_gate_str
    rules[index_2].output_gate_str = output_gate


@dataclass
class Attempt:
    barrier: int
    frozen_outputs: set[str]
    outputs_at_risk: set[str]
    rules: list[Rule]
    swaps_done: list[tuple[str, str]]

    @property
    def all_outputs(self) -> set[str]:
        return {rule.output_gate_str for rule in self.rules}

    @property
    def open_to_swap_with(self) -> Generator[str, None, None]:
        yield from self.all_outputs - self.frozen_outputs - self.swap_set

    @property
    def swap_set(self) -> set[str]:
        return set(chain(*self.swaps_done))

    @property
    def at_risk_without_swaps(self) -> Generator[str, None, None]:
        yield from self.outputs_at_risk - self.swap_set

    def perform_swap(self, swap_1: str, swap_2: str) -> Self:
        new_rules = {rule.output_gate_str: copy(rule) for rule in self.rules}
        new_rules[swap_1].output_gate_str = swap_2
        new_rules[swap_2].output_gate_str = swap_1
        return Attempt(
            barrier=self.barrier,
            frozen_outputs=self.frozen_outputs,
            outputs_at_risk=set(),
            rules=list(new_rules.values()),
            swaps_done=self.swaps_done + [(swap_1, swap_2)]
        )


def generate_new_attempts_by_swapping(base: Attempt) -> Generator[Attempt, None, None]:
    for output_str in base.outputs_at_risk.difference(base.swaps_done):
        for swap_with in base.open_to_swap_with:
            yield base.perform_swap(output_str, swap_with)


def find_highest_barrier(attempt: Attempt, example: bool) -> Attempt | None:
    barrier = attempt.barrier + 1
    frozen_outputs: set[str] = set()
    while True:
        # Keep all rules leading to z<barrier> or lower
        pruned_rules: dict[str, Rule] = {}
        inputs_to_satisfy: set[str] = set()
        for rule in attempt.rules:
            if rule.output_gate_str.startswith("z") and int(rule.output_gate_str[1:]) < barrier:
                pruned_rules[rule.output_gate_str] = rule
                inputs_to_satisfy.update(rule.input_gate_strs)

        while inputs_to_satisfy:
            new_inputs_to_satisfy = set()
            for rule in attempt.rules:
                if rule.output_gate_str in inputs_to_satisfy and rule.output_gate_str not in pruned_rules:
                    pruned_rules[rule.output_gate_str] = rule
                    new_inputs_to_satisfy.update(rule.input_gate_strs)
            inputs_to_satisfy = new_inputs_to_satisfy
        print(f"{barrier=}: {[rule.output_gate_str for rule in pruned_rules.values()]}")
        if verify_rules(list(pruned_rules.values()), example, barrier):
            if len(attempt.rules) == len(pruned_rules):
                attempt.barrier = barrier
                # Success!
                solution = ",".join(sorted(attempt.swap_set))
                print(f"Solution is {solution}")
                return None
            else:
                frozen_outputs = {rule.output_gate_str for rule in pruned_rules.values()}
                barrier += 1
        else:
            max_swaps = 4 if example else 8
            if len(attempt.swap_set) < max_swaps and barrier > attempt.barrier + 1:
                return Attempt(barrier=barrier - 1,
                               frozen_outputs=frozen_outputs,
                               outputs_at_risk={rule.output_gate_str for rule in pruned_rules.values()} - frozen_outputs,
                               rules=attempt.rules,  # Maybe copy
                               swaps_done=attempt.swaps_done,
                               )
            else:
                return None


def tryouts(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    input_generator = split_in_groups_separated_by_empty_line(puzzle_input)
    # Skip the initial values
    _ = next(input_generator)
    rules = list(parse_rules(next(input_generator)))
    base_attempt = Attempt(
        barrier=0,
        frozen_outputs=set(),
        outputs_at_risk=set(),
        rules=rules,
        swaps_done=[],
    )
    attempts = deque()
    attempts.append(base_attempt)
    while attempts:
        print(f"XXX: {len(attempts)}")
        attempt = attempts.pop()
        updated_attempt = find_highest_barrier(attempt, example)
        if updated_attempt:
            attempts.extend(generate_new_attempts_by_swapping(updated_attempt))


def extract_rules_for_rule(start_rule: Rule, rules_to_check: list[Rule]) -> list[Rule]:
    result = {start_rule}
    rules_done: set[str] = {start_rule.output_gate_str}
    inputs_to_satisfy: set[str] = set(start_rule.input_gate_strs)
    while inputs_to_satisfy:
        new_inputs_to_satisfy: set[str] = set()
        for rule in rules_to_check:
            if rule.output_gate_str in inputs_to_satisfy and rule.output_gate_str not in rules_done:
                result.add(rule)
                new_inputs_to_satisfy.update(rule.input_gate_strs)
        inputs_to_satisfy = new_inputs_to_satisfy
    rule_added = True
    while rule_added:
        rule_added = False
        all_inputs = set(chain.from_iterable(rule.input_gate_strs for rule in result))
        for rule in rules_to_check:
            if rule not in result and set(rule.input_gate_strs).issubset(all_inputs):
                result.add(rule)
                rule_added = True
    return list(result)


@register_solver(year="2024", key="24", variation="b")
def tryouts_2(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    input_generator = split_in_groups_separated_by_empty_line(puzzle_input)
    # Skip the initial values
    _ = next(input_generator)
    rules = list(parse_rules(next(input_generator)))
    rules_per_z: dict[str, list[Rule]] = {}
    for rule in rules:
        if rule.output_gate_str.startswith("z"):
            rules_per_z[rule.output_gate_str] = [rule]
    known_outputs: set[str] = set()
    for index in count():
        if index > 1:
            return
        target_rule = f"z{index:02d}"
        if target_rule in rules_per_z:
            rules_per_z[target_rule] = extract_rules_for_rule(
                start_rule=rules_per_z[target_rule][0],
                rules_to_check=[rule for rule in rules if rule.output_gate_str not in known_outputs],
            )
            known_outputs.update(rule.output_gate_str for rule in rules_per_z[target_rule])
            print(f"{target_rule}: {[rule.output_gate_str for rule in rules_per_z[target_rule]]}")
            print(f"{known_outputs=}")
            rules_to_verify = rules_per_z[target_rule]
            if target_rule == "z01":
                rules_to_verify.extend(rules_per_z["z00"])
            print(verify_rules(rules=rules_to_verify, example=example, barrier=index))
        else:
            # Ensure we stop the infinite loop
            return



# Good enough for the example but too slow for the real thing
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
        if verify_rules(swapped_rules, example, 100):
            output_gates = [rules[index].output_gate_str for index in indices]
            solution = ",".join(sorted(output_gates))
            print(f"Solution is {solution}")
            return

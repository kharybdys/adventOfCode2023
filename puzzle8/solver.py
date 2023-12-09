import re
from dataclasses import dataclass
from itertools import groupby

from puzzle8.analyzer import AnalyzedNode, analyze_nodes


@dataclass
class Location:
    current_node: AnalyzedNode
    steps: int


class Attempt:
    def __init__(self, instructions: str, nodes_list: list[AnalyzedNode], current_node: AnalyzedNode):
        self.instructions = instructions
        self.nodes_dict = {node.src: node for node in nodes_list}
        self.locations = [Location(current_node=current_node, steps=0)]

    def can_finish(self) -> bool:
        return all(location.current_node.is_ending_node() for location in self.locations)

    def progress_one_step(self):
        result = []
        for location in self.locations:
            instruction = self.instructions[self.get_instruction_pos(location.steps)]
            result.append(Location(current_node=self.nodes_dict[location.current_node.go(instruction)], steps=location.steps + 1))
        self.locations = result

    def get_instruction_pos(self, steps: int) -> int:
        return steps % len(self.instructions)

    def extensive_instructions(self, steps: int) -> str:
        COPIES = 10
        return "".join([self.instructions[self.get_instruction_pos(steps):]] + [self.instructions] * COPIES)

    def process_lead_time(self):
        result = []
        for location in self.locations:
            extra_steps, target = location.current_node.lead_time
            if extra_steps:
                result.append(Location(current_node=self.nodes_dict[target], steps=location.steps + extra_steps))
            else:
                raise ValueError(f"Lead time expected on current_node {location.current_node}")
        self.locations = result

    def earliest_location(self) -> Location:
        return min(self.locations, key=lambda l: l.steps)

    def process_paths(self):
        earliest_location = self.earliest_location()
        self.locations.remove(earliest_location)
        for target, partial_instructions in earliest_location.current_node.paths:
            if match := re.match(partial_instructions, self.extensive_instructions(earliest_location.steps)):
                self.locations.append(Location(current_node=self.nodes_dict[target], steps=earliest_location.steps + len(match[0])))

    def __lt__(self, other) -> True:
        if isinstance(other, Attempt):
            return self.earliest_location().steps < other.earliest_location().steps
        else:
            raise ValueError(f"Cannot compare Attempts with other objects: {other}")


def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    instructions = puzzle_input[0]
    if puzzle_input[1] != "":
        raise ValueError("Missing separation line between instructions and nodes in the input")
    nodes_list = [AnalyzedNode.from_string(line) for line in puzzle_input[2:]]
    nodes = {node.src: node for node in nodes_list}
    attempt = Attempt(instructions=instructions, nodes_list=nodes_list, current_node=nodes["AAA"])
    while not attempt.can_finish():
        attempt.progress_one_step()
    print(attempt.earliest_location().steps)


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    instructions = puzzle_input[0]
    if puzzle_input[1] != "":
        raise ValueError("Missing separation line between instructions and nodes in the input")
    nodes_list = [AnalyzedNode.from_string(line) for line in puzzle_input[2:]]
    attempts = [Attempt(instructions=instructions, nodes_list=nodes_list, current_node=node) for node in nodes_list if node.src.endswith("A")]
    # Extra in part b, analyze the nodes for extra info
    analyze_nodes(nodes_dict={node.src: node for node in nodes_list}, instructions=instructions)
    for attempt in attempts:
        attempt.process_lead_time()
    while not all_equal(attempt.earliest_location().steps for attempt in attempts):
        earliest_attempt = min(attempts)
        earliest_attempt.process_paths()
    print(attempts[0].earliest_location().steps)

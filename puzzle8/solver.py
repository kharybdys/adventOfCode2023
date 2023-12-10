import datetime
import re
from collections import defaultdict

from puzzle8.analyzer import AnalyzedNode, analyze_nodes
from utils import all_equal


class Attempt:
    def __init__(self, instructions: str, nodes_list: list[AnalyzedNode], current_node: AnalyzedNode):
        self.instructions = instructions
        self.nodes_dict = {node.src: node for node in nodes_list}
        self.locations: dict[int, set[AnalyzedNode]] = defaultdict(set)
        self.locations[0].add(current_node)

    def can_finish(self) -> bool:
        return all(node.is_ending_node() for nodes in self.locations.values() for node in nodes)

    def progress_one_step(self):
        result: dict[int, set[AnalyzedNode]] = defaultdict(set)
        for steps, nodes in self.locations.items():
            instruction = self.instructions[self.get_instruction_pos(steps)]
            for node in nodes:
                result[steps + 1].add(self.nodes_dict[node.go(instruction)])
        self.locations = result

    def get_instruction_pos(self, steps: int) -> int:
        return steps % len(self.instructions)

    def extensive_instructions(self, steps: int) -> str:
        COPIES = 10
        return "".join([self.instructions[self.get_instruction_pos(steps):]] + [self.instructions] * COPIES)

    def process_lead_time(self):
        result: dict[int, set[AnalyzedNode]] = defaultdict(set)
        for steps, nodes in self.locations.items():
            for node in nodes:
                extra_steps, target = node.lead_time
                if extra_steps:
                    result[steps + extra_steps].add(self.nodes_dict[target])
                else:
                    raise ValueError(f"Lead time expected on current_node {node}")
        self.locations = result

    def lowest_steps(self) -> int:
        return min(self.locations)

    def process_paths(self):
        lowest_steps = self.lowest_steps()
        further_extended_instruction = self.extensive_instructions(lowest_steps)
        nodes_to_process = self.locations.pop(lowest_steps)
        for node in nodes_to_process:
            for target, partial_instructions in node.paths:
                if match := re.match(partial_instructions, further_extended_instruction):
                    self.locations[lowest_steps + len(match[0])].add(self.nodes_dict[target])

    def __lt__(self, other) -> True:
        if isinstance(other, Attempt):
            return self.lowest_steps() < other.lowest_steps()
        else:
            raise ValueError(f"Cannot compare Attempts with other objects: {other}")


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
    print(attempt.lowest_steps())


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    print(f"Started at {datetime.datetime.now()}")
    instructions = puzzle_input[0]
    if puzzle_input[1] != "":
        raise ValueError("Missing separation line between instructions and nodes in the input")
    nodes_list = [AnalyzedNode.from_string(line) for line in puzzle_input[2:]]
    attempts = [Attempt(instructions=instructions, nodes_list=nodes_list, current_node=node) for node in nodes_list if node.src.endswith("A")]
    print(f"Created attempts at {datetime.datetime.now()}")
    # Extra in part b, analyze the nodes for extra info
    # TODO: analyzing nodes goes out of memory, specifically already the finding cycles - check algorithms for cycle detection!
    analyze_nodes(nodes_dict={node.src: node for node in nodes_list}, instructions=instructions)
    print(f"Finished analyzing nodes at {datetime.datetime.now()}")
    for attempt in attempts:
        attempt.process_lead_time()
    print(f"Finished processing lead times at {datetime.datetime.now()}")
    while not all_equal(attempt.lowest_steps() for attempt in attempts):
        earliest_attempt = min(attempts)
        furthest_steps = max(attempts).lowest_steps()
        print(f"Currently processing an attempt with {earliest_attempt.lowest_steps()} steps. Furthest is on {furthest_steps}, time {datetime.datetime.now()}")
        earliest_attempt.process_paths()
    print(attempts[0].lowest_steps())

import datetime
from collections import defaultdict
from functools import reduce

from puzzle8.analyzer import AnalyzedNode, analyze_nodes, generate_possible_instructions
from puzzle8.instructor import InstructedNode, instruct_nodes
from utils import all_equal


class Attempt:
    def __init__(self, instructions: str, nodes_list: list[AnalyzedNode], current_node: AnalyzedNode):
        self.instructions = instructions
        self.nodes_dict = {node.node_id: node for node in nodes_list}
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
        nodes_to_process = self.locations.pop(lowest_steps)
        for node in nodes_to_process:
            for path in node.paths.get(self.get_instruction_pos(lowest_steps), []):
                self.locations[lowest_steps + path.length].add(self.nodes_dict[path.target])

    def __lt__(self, other) -> True:
        if isinstance(other, Attempt):
            return self.lowest_steps() < other.lowest_steps()
        else:
            raise ValueError(f"Cannot compare Attempts with other objects: {other}")


def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    instructions = puzzle_input[0]
    if puzzle_input[1] != "":
        raise ValueError("Missing separation line between instructions and nodes in the input")
    nodes_list = [AnalyzedNode.from_string(line) for line in puzzle_input[2:]]
    nodes = {node.node_id: node for node in nodes_list}
    attempt = Attempt(instructions=instructions, nodes_list=nodes_list, current_node=nodes["AAA"])
    while not attempt.can_finish():
        attempt.progress_one_step()
    print(attempt.lowest_steps())


def solve_b_with_reduction_of_graph(puzzle_input: list[str], example: bool) -> None:
    # Constraint on the solution, arbitrarily chosen. Should be much bigger
    MAX_PATH_LENGTH = 2000

    print(puzzle_input)
    print(f"Started at {datetime.datetime.now()}")
    instructions = puzzle_input[0]
    if puzzle_input[1] != "":
        raise ValueError("Missing separation line between instructions and nodes in the input")
    nodes_list = [AnalyzedNode.from_string(line) for line in puzzle_input[2:]]
    partial_instructions_list = list(generate_possible_instructions(instructions, max_length=MAX_PATH_LENGTH))
    print(f"Length of partial_instructions_list is: {len(partial_instructions_list)}")
    attempts = [Attempt(instructions=instructions, nodes_list=nodes_list, current_node=node) for node in nodes_list if node.node_id.endswith("A")]
    print(f"Created attempts at {datetime.datetime.now()}")
    # Extra in part b, analyze the nodes for extra info
    analyze_nodes(nodes_dict={node.node_id: node for node in nodes_list}, instructions=instructions, partial_instructions_list=partial_instructions_list)
    print(f"Finished analyzing nodes at {datetime.datetime.now()}")
    for attempt in attempts:
        attempt.process_lead_time()
    print(f"Finished processing lead times at {datetime.datetime.now()}")
    for attempt in attempts:
        print(f"At {attempt.locations}")
    while not all_equal(attempt.lowest_steps() for attempt in attempts):
        earliest_attempt = min(attempts)
        furthest_steps = max(attempts).lowest_steps()
        print(f"Currently processing an attempt with {earliest_attempt.lowest_steps()} steps. Furthest is on {furthest_steps}, time {datetime.datetime.now()}")
        earliest_attempt.process_paths()
        print(f"After processing paths, locations are now: {earliest_attempt.locations}")
    print(attempts[0].lowest_steps())


def reach_end(current_nodes: list[InstructedNode], nodes_dict: dict[str, InstructedNode], cycle_size: int) -> int:
    current_iteration_start = 1
    while True:
        if all(node.is_ending_node() for node in current_nodes):
            return current_iteration_start
        else:
            if all(node.can_finish_at for node in current_nodes):
                intersected_can_finish_at = reduce(lambda a, b: a.intersection(b), [node.can_finish_at for node in current_nodes])
                if intersected_can_finish_at:
                    print(f"Returning with {intersected_can_finish_at} and {current_iteration_start}")
                    return min(intersected_can_finish_at) + current_iteration_start
        current_iteration_start += cycle_size
        current_nodes = [nodes_dict[node.end_node] for node in current_nodes]
        if current_iteration_start % (cycle_size * 100000) == 1:
            print(f"At {current_iteration_start:,} at {datetime.datetime.now()}")


def solve_b_with_instructions(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    print(f"Started at {datetime.datetime.now()}")
    instructions = puzzle_input[0]
    copies = 1 if example else 1000
    instructions = "".join([instructions] * copies)
    if puzzle_input[1] != "":
        raise ValueError("Missing separation line between instructions and nodes in the input")
    nodes_list = [InstructedNode.from_string(line) for line in puzzle_input[2:]]
    nodes_dict = {node.node_id: node for node in nodes_list}
    instruct_nodes(nodes_dict, instructions)
    print(f"Finished instructing nodes at {datetime.datetime.now()}")
    current_nodes = [node for node in nodes_dict.values() if node.node_id.endswith("A")]
    print(reach_end(current_nodes, nodes_dict, len(instructions)))


def solve_b(puzzle_input: list[str], example: bool) -> None:
    solve_b_with_instructions(puzzle_input, example)

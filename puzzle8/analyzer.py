import datetime

from collections import deque, defaultdict
from dataclasses import field, dataclass
from typing import Generator

from puzzle8.node import Node


@dataclass
class Path:
    start_position: int
    length: int
    target: str


@dataclass
class PartialInstruction:
    instr: str
    start_positions: list[int] = field(default_factory=list)

    @property
    def length(self):
        return len(self.instr)


class AnalyzedNode(Node):
    def __init__(self, src: str, left: str, right: str):
        super().__init__(src, left, right)
        self.lead_time: tuple[int, str] = (-1, "")
        self.paths: dict[int, list[Path]] = defaultdict(list)

    def add_to_paths(self, path: Path):
        self.paths[path.start_position].append(path)

    def __str__(self) -> str:
        return f"AnalyzedNode[{self.node_id}"


def analyze_nodes(nodes_dict: dict[str, AnalyzedNode], instructions: str, partial_instructions_list: list[PartialInstruction]):
    for node in nodes_dict.values():
        if node.is_ending_node():
            print(f"Starting node {node.node_id} at {datetime.datetime.now()}")
            for path in generate_paths(node, nodes_dict, partial_instructions_list):
                node.add_to_paths(path)
                print(f"Found a path from {node.node_id} to {path.target} with length {path.length}")
            print(f"Got paths for {node.node_id} at {datetime.datetime.now()}")
        elif node.node_id.endswith("A"):
            print(f"Starting node {node.node_id} at {datetime.datetime.now()}")
            node.lead_time = generate_lead_time(node, nodes_dict, instructions)
            print(f"Got lead time for {node.node_id}, namely {node.lead_time} at {datetime.datetime.now()}")


def generate_paths(node: AnalyzedNode, nodes_dict: [str, AnalyzedNode], partial_instructions_list: list[PartialInstruction]) -> Generator[Path, None, None]:
    """Returns a list of instructions that result in a path to an end node. Allows repetition,
     but has an inherent maximum length (from generating the partial_instructions_list)
       """
    for partial_instruction in partial_instructions_list:
        dest = walk_path(node, nodes_dict, partial_instruction.instr)
        if dest.is_ending_node():
            for start_position in partial_instruction.start_positions:
                yield Path(start_position=start_position, length=partial_instruction.length, target=dest.node_id)


def walk_path(node: AnalyzedNode, nodes_dict: [str, AnalyzedNode], partial_instruction: str) -> AnalyzedNode:
    dest = node
    for instruction in partial_instruction:
        dest = nodes_dict[dest.go(instruction)]
    return dest


def position_wrapped(position: int, wrap_at: int) -> int:
    return position % wrap_at


def generate_lead_time(node: AnalyzedNode, nodes_dict: [str, AnalyzedNode], instructions: str) -> tuple[int, str]:
    steps = 0
    while not node.is_ending_node():
        instruction = instructions[position_wrapped(steps, len(instructions))]
        node = nodes_dict[node.go(instruction)]
        steps += 1
    return steps, node.node_id


def generate_possible_instructions(instructions: str, max_length: int) -> Generator[PartialInstruction, None, None]:
    partial_instructions = deque()
    partial_instructions.append(PartialInstruction(instr="R", start_positions=[index for index, char in enumerate(instructions) if char == "R"]))
    partial_instructions.append(PartialInstruction(instr="L", start_positions=[index for index, char in enumerate(instructions) if char == "L"]))
    while partial_instructions:
        partial_instruction = partial_instructions.pop()
        yield partial_instruction
        if len(partial_instruction.instr) < max_length:
            if len(partial_instruction.start_positions) == 1:
                yield from extend_partial_instruction(partial_instruction, instructions, max_length)
            else:
                next_instructions_dict = defaultdict(list)
                for start_position in partial_instruction.start_positions:
                    next_char = instructions[position_wrapped(start_position + len(partial_instruction.instr) + 1, len(instructions))]
                    next_instructions_dict[next_char].append(start_position)
                for next_char, start_positions in next_instructions_dict.items():
                    partial_instructions.append(PartialInstruction(instr=partial_instruction.instr + next_char, start_positions=start_positions))


def extend_partial_instruction(partial_instruction: PartialInstruction, instructions: str, max_length: int) -> Generator[PartialInstruction, None, None]:
    instruction = partial_instruction.instr
    for i in range(len(partial_instruction.instr), max_length + 1):
        instruction += instructions[position_wrapped(partial_instruction.start_positions[0] + i, len(instructions))]
        yield PartialInstruction(instr=instruction, start_positions=partial_instruction.start_positions)

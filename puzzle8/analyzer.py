import datetime
import re

from collections import deque, namedtuple, defaultdict
from dataclasses import field, dataclass
from typing import Generator

from puzzle8.node import Node


class AnalyzedNode(Node):
    def __init__(self, src: str, left: str, right: str):
        super().__init__(src, left, right)
        self.lead_time: tuple[int, str] = (-1, "")
        self.paths: list[tuple[str, str]] = []


Path = namedtuple("Path", ["partial_instr", "nodes_sofar"])


def analyze_nodes(nodes_dict: dict[str, AnalyzedNode], instructions: str, partial_instructions_list: list[str]):
    for node in nodes_dict.values():
        print(f"Starting node {node.src} at {datetime.datetime.now()}")
        if node.is_ending_node():
            node.paths = list(generate_paths(node, nodes_dict, partial_instructions_list))
            print(f"Got paths for {node.src} at {datetime.datetime.now()}")
        if node.src.endswith("A"):
            node.lead_time = generate_lead_time(node, nodes_dict, instructions)
            print(f"Got lead time for {node.src} at {datetime.datetime.now()}")


def generate_paths(node: AnalyzedNode, nodes_dict: [str, AnalyzedNode], partial_instructions_list: list[str]) -> Generator[tuple[str, str], None, None]:
    """Returns a list of instructions that result in a path to an end node. Allows repetition,
     but has an inherent maximum length (from generating the partial_instructions_list)
       """
    for partial_instruction in partial_instructions_list:
        dest = walk_path(node, nodes_dict, partial_instruction)
        if dest.is_ending_node():
            yield partial_instruction, dest.src


def walk_path(node: AnalyzedNode, nodes_dict: [str, AnalyzedNode], partial_instruction: str) -> AnalyzedNode:
    dest = node
    for instruction in partial_instruction:
        dest = nodes_dict[dest.go(instruction)]
    return dest


ZERO_PATH_PATTERN = re.compile(r"\([^()]+\)\*\?")


def ensure_non_zero_path_length(instruction: str) -> str:
    if ZERO_PATH_PATTERN.fullmatch(instruction):
        return instruction.replace("*", "+")
    else:
        return instruction


def generate_lead_time(node: AnalyzedNode, nodes_dict: [str, AnalyzedNode], instructions: str) -> tuple[int, str]:
    instruction_pos = 0
    steps = 0
    while not node.is_ending_node():
        instruction = instructions[instruction_pos]
        node = nodes_dict[node.go(instruction)]
        steps += 1
        instruction_pos += 1
        if instruction_pos >= len(instructions):
            instruction_pos = 0
    return steps, node.src


@dataclass
class PartialInstruction:
    instr: str
    start_positions: list[int] = field(default_factory=list)


def position_wrapped(position: int, wrap_at: int) -> int:
    return position % wrap_at


def generate_possible_instructions(instructions: str, max_length: int) -> Generator[str, None, None]:
    partial_instructions = deque()
    partial_instructions.append(PartialInstruction(instr="R", start_positions=[index for index, char in enumerate(instructions) if char == "R"]))
    partial_instructions.append(PartialInstruction(instr="L", start_positions=[index for index, char in enumerate(instructions) if char == "L"]))
    while partial_instructions:
        partial_instruction = partial_instructions.pop()
        yield partial_instruction.instr
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


def extend_partial_instruction(partial_instruction: PartialInstruction, instructions: str, max_length: int):
    instruction = partial_instruction.instr
    for i in range(len(partial_instruction.instr), max_length + 1):
        instruction += instructions[position_wrapped(partial_instruction.start_positions[0] + i, len(instructions))]
        yield instruction

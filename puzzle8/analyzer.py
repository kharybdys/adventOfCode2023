# Graph analysis
from collections import deque, namedtuple
from typing import Generator

from puzzle8.node import Node


# I need time from start node (with A) to first node with Z
# instruction patterns from node with Z to another node with Z (and thus their length)
# Cycle analysis

class AnalyzedNode(Node):
    def __init__(self, src: str, left: str, right: str):
        super().__init__(src, left, right)
        self.cycles: list[str] = []
        self.lead_time: tuple[int, str] = (0, src)
        self.paths: list[tuple[str, str]] = []


Path = namedtuple("Path", ["partial_instr", "nodes_sofar"])


def analyze_nodes(nodes_dict: dict[str, AnalyzedNode], instructions: str):
    for node in nodes_dict.values():
        node.cycles = list(generate_self_cycles(node, nodes_dict))
        if node.src.endswith("A"):
            node.lead_time = generate_lead_time(node, nodes_dict, instructions)
    # path analysis needs completed cycle analysis on the entire graph
    for node in nodes_dict.values():
        if node.src.endswith("Z"):
            node.paths = list(generate_paths(node, nodes_dict))


def generate_self_cycles(node: AnalyzedNode, nodes_dict: [str, AnalyzedNode]) -> Generator[str, None, None]:
    """Returns a list of instructions that result in a cycle to self, without repetition?
       (what if A to B, then B cycles, then B to A?)
       Without repetition to ensure end to finding cycles, so how to guarantee that otherwise?
       """
    current_paths = deque()
    # instruction, list of nodes passed
    current_paths.append(Path("", [node]))
    while current_paths:
        partial_instr, nodes_sofar = current_paths.popleft()
        current_node = nodes_sofar[-1]
        node_left = nodes_dict[current_node.left]
        if node_left not in nodes_sofar:
            current_paths.append(Path(partial_instr + "L", nodes_sofar + node_left))
        elif node_left == node:
            yield partial_instr + "L"
        node_right = nodes_dict[current_node.left]
        if node_right not in nodes_sofar:
            current_paths.append(Path(partial_instr + "R", nodes_sofar + node_right))
        elif node_right == node:
            yield partial_instr + "R"


def generate_paths(node: AnalyzedNode, nodes_dict: [str, AnalyzedNode]) -> Generator[tuple[str, str], None, None]:
    """ Returns a list of instructions that result in a path from a Z node to a different Z node.
        Assumes cycles have already been found and described. """
    current_paths = deque()
    # instruction, list of nodes passed
    current_paths.append(Path("", [node]))
    while current_paths:
        partial_instr, nodes_sofar = current_paths.popleft()
        current_node = nodes_sofar[-1]
        if current_node.cycles:
            partial_instructions = [f"{partial_instr}({cycle})*" for cycle in current_node.cycles]
        else:
            partial_instructions = [partial_instr]
        node_left = nodes_dict[current_node.left]
        if node_left.src.endswith("Z"):
            for instruction in partial_instructions:
                yield node_left.src, instruction + "L"
        elif node_left not in nodes_sofar:
            for instruction in partial_instructions:
                current_paths.append(Path(instruction + "L", nodes_sofar + node_left))
        node_right = nodes_dict[current_node.left]
        if node_right.src.endswith("Z"):
            for instruction in partial_instructions:
                yield node_right.src, instruction + "R"
        elif node_right not in nodes_sofar:
            for instruction in partial_instructions:
                current_paths.append(Path(instruction + "R", nodes_sofar + node_right))


def generate_lead_time(node: AnalyzedNode, nodes_dict: [str, AnalyzedNode], instructions: str) -> tuple[int, str]:
    instruction_pos = 0
    steps = 0
    while not node.src.endswith("Z"):
        instruction = instructions[instruction_pos]
        node = nodes_dict[node.go(instruction)]
        steps += 1
        instruction_pos += 1
        if instruction_pos >= len(instructions):
            instruction_pos = 0
    return steps, node.src

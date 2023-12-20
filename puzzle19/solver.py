import re
from typing import Generator

from puzzle19.base import Part, PartRange, Watcher
from puzzle19.nodes import Node, parse_node, LinkToTreeNode
from utils import split_in_groups_separated_by_empty_line, Range


def parse_nodes(lines: list[str], watcher: Watcher) -> Node:
    TREE_PATTERN = re.compile(r"(\w+)\{(.*)}")
    trees: dict[str, Node] = {}
    nodes_to_link: list[LinkToTreeNode] = []
    for line in lines:
        if tree_match := TREE_PATTERN.fullmatch(line):
            key = tree_match[1]
            root_node = None
            for node_line in reversed(tree_match[2].split(",")):
                root_node, to_link_nodes = parse_node(node_line, root_node, watcher)
                nodes_to_link.extend(to_link_nodes)
            trees[key] = root_node
        else:
            raise ValueError(f"Invalid tree pattern for {line}")
    # Link the trees
    for node in nodes_to_link:
        node.target_node = trees[node.target_tree]
    return trees["in"]


def parse_parts(lines: list[str]) -> Generator[Part, None, None]:
    PART_PATTERN = re.compile(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}")
    for line in lines:
        if match := PART_PATTERN.fullmatch(line):
            yield Part(x=int(match[1]), m=int(match[2]), a=int(match[3]), s=int(match[4]))
        else:
            raise ValueError(f"Invalid part pattern for {line}")


def parse(puzzle_input: list[str], watcher: Watcher) -> tuple[Node, list[Part]]:
    input_generator = split_in_groups_separated_by_empty_line(puzzle_input)
    root_node = parse_nodes(next(input_generator), watcher)
    parts = list(parse_parts(next(input_generator)))
    return root_node, parts


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    watcher = Watcher()
    root_node, parts = parse(puzzle_input, watcher)
    solution = 0
    for part in parts:
        root_node.process(part)
        if part.accepted:
            solution += part.value
    print(solution)


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    watcher = Watcher()
    root_node, parts = parse(puzzle_input, watcher)
    initial_range = PartRange(x=Range(1, 4001), m=Range(1, 4001), a=Range(1, 4001), s=Range(1, 4001))
    root_node.process_range(initial_range)
    print(watcher.combinations)

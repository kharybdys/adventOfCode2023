import re
from abc import ABC, abstractmethod
from typing import Optional

from puzzle19.base import Part, Watcher, PartRange


class Node(ABC):
    @abstractmethod
    def process(self, part: Part):
        pass

    @abstractmethod
    def process_range(self, part_range: PartRange):
        pass


class RejectNode(Node):
    def process(self, part: Part):
        part.reject()

    def process_range(self, part_range: PartRange):
        # Rejected, nothing to do with this
        pass


class AcceptNode(Node):
    def __init__(self, watcher: Watcher):
        self.watcher = watcher

    def process(self, part: Part):
        part.accept()

    def process_range(self, part_range: PartRange):
        self.watcher.accept(part_range)


class LinkToTreeNode(Node):
    def __init__(self, target_tree: str):
        self.target_tree = target_tree
        # Can only link the trees to each other once parsing is complete
        self.target_node = None

    def process(self, part: Part):
        self.target_node.process(part)

    def process_range(self, part_range: PartRange):
        self.target_node.process_range(part_range)


class DecisionNode(Node):
    def __init__(self, true_node: Node, false_node: Node, attribute: str, operator: str, value: int):
        self.true_node = true_node
        self.false_node = false_node
        self.attribute = attribute
        self.value = value
        if operator == ">":
            self.greater_than = True
        elif operator == "<":
            self.greater_than = False
        else:
            raise ValueError(f"Unsupported operator {operator}")

    def decide(self, part: Part) -> bool:
        if self.greater_than:
            return getattr(part, self.attribute) > self.value
        else:
            return getattr(part, self.attribute) < self.value

    def process(self, part: Part):
        if self.decide(part):
            self.true_node.process(part)
        else:
            self.false_node.process(part)

    def split_range(self, part_range: PartRange) -> tuple[PartRange, PartRange]:
        if self.greater_than:
            return part_range.split_on_greater_then(self.attribute, self.value)
        else:
            return part_range.split_on_less_then(self.attribute, self.value)

    def process_range(self, part_range: PartRange):
        true_range, false_range = self.split_range(part_range)
        if true_range:
            self.true_node.process_range(true_range)
        if false_range:
            self.false_node.process_range(false_range)


NODE_PATTERN = re.compile(r"(\w)(<|>)(\d+):(\w+)")
SIMPLE_NODE_PATTERN = re.compile(r"(\w+)")


def parse_node(node_line: str, false_node: Optional[Node], watcher: Watcher) -> tuple[Node, list[LinkToTreeNode]]:
    if node_match := NODE_PATTERN.fullmatch(node_line):
        attribute = node_match[1]
        operator = node_match[2]
        value = int(node_match[3])
        result_node, to_link_nodes = end_node(node_match[4], watcher)
        if not false_node:
            raise ValueError(f"Cannot process node pattern {node_line} without a false_node")
        decision = DecisionNode(true_node=result_node,
                                false_node=false_node,
                                attribute=attribute,
                                operator=operator,
                                value=value)
        return decision, to_link_nodes
    elif simple_node_match := SIMPLE_NODE_PATTERN.fullmatch(node_line):
        return end_node(simple_node_match[1], watcher)
    else:
        raise ValueError(f"Invalid node pattern for {node_line}")


def end_node(target: str, watcher: Watcher) -> tuple[Node, list[LinkToTreeNode]]:
    if target == "R":
        return RejectNode(), []
    elif target == "A":
        return AcceptNode(watcher), []
    else:
        link_node = LinkToTreeNode(target)
        return link_node, [link_node]

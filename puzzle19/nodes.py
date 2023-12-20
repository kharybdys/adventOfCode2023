import re
from abc import ABC, abstractmethod
from typing import Optional

from puzzle19.base import Part


class Node(ABC):
    @abstractmethod
    def process(self, part: Part):
        pass


class RejectNode(Node):
    def process(self, part: Part):
        part.reject()


class AcceptNode(Node):
    def process(self, part: Part):
        part.accept()


class LinkToTreeNode(Node):
    def __init__(self, target_tree: str):
        self.target_tree = target_tree
        # Can only link the trees to each other once parsing is complete
        self.target_node = None

    def process(self, part: Part):
        self.target_node.process(part)


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


NODE_PATTERN = re.compile(r"(\w)(<|>)(\d+):(\w+)")
SIMPLE_NODE_PATTERN = re.compile(r"(\w+)")


def parse_node(node_line: str, false_node: Optional[Node]) -> tuple[Node, list[Node]]:
    if node_match := NODE_PATTERN.fullmatch(node_line):
        attribute = node_match[1]
        operator = node_match[2]
        value = int(node_match[3])
        result_node, to_link_nodes = end_node(node_match[4])
        if not false_node:
            raise ValueError(f"Cannot process node pattern {node_line} without a false_node")
        decision = DecisionNode(true_node=result_node,
                                false_node=false_node,
                                attribute=attribute,
                                operator=operator,
                                value=value)
        return decision, to_link_nodes
    elif simple_node_match := SIMPLE_NODE_PATTERN.fullmatch(node_line):
        return end_node(simple_node_match[1])
    else:
        raise ValueError(f"Invalid node pattern for {node_line}")


def end_node(target: str) -> tuple[Node, list[Node]]:
    if target == "R":
        return RejectNode(), []
    elif target == "A":
        return AcceptNode(), []
    else:
        link_node = LinkToTreeNode(target)
        return link_node, [link_node]

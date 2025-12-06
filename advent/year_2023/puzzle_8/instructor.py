from advent.year_2023.puzzle_8.node import Node


class InstructedNode(Node):
    def __init__(self, src: str, left: str, right: str):
        super().__init__(src, left, right)
        self.end_node = ""
        self.can_finish_at: set[int] = set()


def instruct_nodes(nodes_dict: dict[str, InstructedNode], instructions: str):
    for node in nodes_dict.values():
        current_node = node
        can_finish_at: set[int] = set()
        for i, instruction in enumerate(instructions):
            current_node = nodes_dict[current_node.go(instruction)]
            if current_node.is_ending_node():
                can_finish_at.add(i)
        node.can_finish_at = can_finish_at
        node.end_node = current_node.node_id

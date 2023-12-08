from puzzle8.analyzer import AnalyzedNode


class Attempt:
    def __init__(self, instructions: str, nodes_list: list[AnalyzedNode], current_node: AnalyzedNode):
        self.instructions = instructions
        self.instruction_pos = 0
        self.nodes_dict = {node.src: node for node in nodes_list}
        self.current_node = current_node
        self.steps = 0

    def can_finish(self) -> bool:
        return self.current_node.src.endswith("Z")

    def progress_one_step(self):
        instruction = self.instructions[self.instruction_pos]
        self.current_node = self.nodes_dict[self.current_node.go(instruction)]
        self.steps += 1
        self.increase_instruction_pos()

    def increase_instruction_pos(self):
        self.instruction_pos += 1
        if self.instruction_pos >= len(self.instructions):
            self.instruction_pos = 0


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
    print(attempt.steps)


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    instructions = puzzle_input[0]
    if puzzle_input[1] != "":
        raise ValueError("Missing separation line between instructions and nodes in the input")
    nodes_list = [AnalyzedNode.from_string(line) for line in puzzle_input[2:]]
    attempts = [Attempt(instructions=instructions, nodes_list=nodes_list, current_node=node) for node in nodes_list if node.src.endswith("A")]
    while not all(attempt.can_finish() for attempt in attempts):
        for attempt in attempts:
            attempt.progress_one_step()
    print(attempts[0].steps)

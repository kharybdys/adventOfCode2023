from puzzle8.node import Node


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    instructions = puzzle_input[0]
    if puzzle_input[1] != "":
        raise ValueError("Missing separation line between instructions and nodes in the input")
    nodes_list = [Node.from_string(line) for line in puzzle_input[2:]]
    nodes = {node.src: node for node in nodes_list}
    instruction_pos = 0
    steps = 0
    node = nodes["AAA"]
    while node.src != "ZZZ":
        instruction = instructions[instruction_pos]
        node = nodes[node.go(instruction)]
        steps += 1
        instruction_pos += 1
        if instruction_pos >= len(instructions):
            instruction_pos = 0
    print(steps)


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)

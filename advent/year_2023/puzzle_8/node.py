import re
from typing import Self


class Node:
    PATTERN = re.compile(r"([0-9A-Z]{3}) = \(([0-9A-Z]{3}), ([0-9A-Z]{3})\)")

    def __init__(self, src: str, left: str, right: str):
        self.node_id = src
        self.left = left
        self.right = right

    def go(self, instruction: str) -> str:
        match instruction:
            case "L":
                return self.left
            case "R":
                return self.right
            case _:
                raise ValueError(f"Invalid instruction {instruction}")

    def is_ending_node(self) -> bool:
        return self.node_id.endswith("Z")

    @classmethod
    def from_string(cls, line: str) -> Self:
        if match := cls.PATTERN.fullmatch(line):
            return cls(src=match[1], left=match[2], right=match[3])
        else:
            raise ValueError(f"Invalid node definition: {line}")

from operator import floordiv, mul, mod, add
from typing import Callable

from puzzle2021_24.constraints import ConstraintsWatcher
from puzzle2021_24.variable import Variable, SetPossibilitiesGenerator


def analyze_instructions(instructions: list[str]) -> tuple[bool, bool, bool, bool]:
    """Returns whether w, x, y and z are used as inputs for this set of instructions (4x bool)"""
    writes: dict[str, bool] = {}
    inputs: dict[str, bool] = {}
    for instruction in instructions:
        instr_split = instruction.split()
        if len(instr_split) == 3:
            instr_type, param1, param2 = instr_split
        else:
            raise ValueError(f"Invalid instruction {instruction}")
        if not param2.isdecimal() and not writes.get(param2, False):
            inputs[param2] = True
        writes[param1] = True

    return inputs.get("w", False), inputs.get("x", False), inputs.get("y", False), inputs.get("z", False)


class PartialALU:

    def __init__(self, w: int, x: int = 0, y: int = 0, z: int = 0):
        self.w = w
        self.x = x
        self.y = y
        self.z = z
        self.initial_w = self.w
        self.initial_x = self.x
        self.initial_y = self.y
        self.initial_z = self.z

    @staticmethod
    def eq(x: int, y: int) -> int:
        if x == y:
            return 1
        else:
            return 0

    def parse_instruction(self, instruction: str) -> tuple[Callable, int, int, str]:
        instr_split = instruction.split()
        if len(instr_split) == 3:
            instr_type, param1, param2 = instr_split
        else:
            raise ValueError(f"Invalid instruction {instruction}")

        match instr_type:
            case "inp":
                raise NotImplementedError("input not supported by this ALU")
            case "add":
                return add, self.value(param1), self.value(param2), param1
            case "mul":
                return mul, self.value(param1), self.value(param2), param1
            case "div":
                return floordiv, self.value(param1), self.value(param2), param1
            case "mod":
                return mod, self.value(param1), self.value(param2), param1
            case "eql":
                return self.eq, self.value(param1), self.value(param2), param1
            case _:
                raise NotImplementedError(f"Unknown instruction {instruction}")

    def execute_all(self, instructions: list[str]):
        for instruction in instructions:
            self.execute(instruction)

    def execute(self, instruction: str):
        instr_func, param1, param2, output = self.parse_instruction(instruction)
        self.store(output, instr_func(param1, param2))

    def store(self, attrib: str, value: int):
        match attrib:
            case "w":
                self.w = value
            case "x":
                self.x = value
            case "y":
                self.y = value
            case "z":
                self.z = value
            case _:
                raise ValueError(f"Invalid attribute {attrib}")

    def value(self, attrib: str) -> int:
        match attrib:
            case "w":
                return self.w
            case "x":
                return self.x
            case "y":
                return self.y
            case "z":
                return self.z
            case a:
                try:
                    return int(a)
                except:
                    raise ValueError(f"Invalid attribute {attrib}")


class ReverseALU:
    def __init__(self):
        self.watcher = ConstraintsWatcher()
        self.w = Variable(watcher=self.watcher)
        self.x = Variable(watcher=self.watcher)
        self.y = Variable(watcher=self.watcher)
        self.z = Variable(watcher=self.watcher, possibilities=SetPossibilitiesGenerator([0]))
        self.no_longer_referred_variables: list[Variable] = []

    def parse_instruction(self, instruction: str) -> None:
        instr_split = instruction.split()
        if len(instr_split) == 3:
            instr_type, param1, param2 = instr_split
        else:
            raise ValueError(f"Invalid instruction {instruction}")

        match instr_type:
            case "inp":
                raise NotImplementedError("input not supported by this ALU")
            case "add":
                pass
            case "mul":
                pass
            case "div":
                pass
            case "mod":
                pass
            case "eql":
                pass
            case _:
                raise NotImplementedError(f"Unknown instruction {instruction}")

    def execute_all(self, instructions: list[str]):
        for instruction in instructions:
            self.execute(instruction)

    def execute(self, instruction: str):
        instr_func, param1, param2, output = self.parse_instruction(instruction)

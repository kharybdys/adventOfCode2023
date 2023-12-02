import re
from dataclasses import dataclass
from functools import reduce
from operator import mul
from typing import ClassVar, Self


@dataclass
class Draw:
    cubes_by_color: dict[str, int]
    DRAW_SPLIT_PATTERN: ClassVar[re.Pattern] = re.compile(r"\s*;\s*")
    COLOR_SPLIT_PATTERN: ClassVar[re.Pattern] = re.compile(r"\s*,\s*")

    @staticmethod
    def from_string(line: str) -> list[Self]:
        result: list[Self] = []
        for draw in Draw.DRAW_SPLIT_PATTERN.split(line):
            cubes_by_color = {}
            for colored_cubes in Draw.COLOR_SPLIT_PATTERN.split(draw):
                sep = r"\w+"
                cubes, color = colored_cubes.split()
                cubes_by_color[color] = int(cubes)
            result.append(Draw(cubes_by_color=cubes_by_color))
        return result

    def possible(self, sack: dict[str, int]) -> bool:
        for color, cubes in self.cubes_by_color.items():
            if color not in sack:
                return False
            if cubes > sack[color]:
                return False
        return True


@dataclass
class Game:
    id: int
    draws: list[Draw]

    PATTERN: ClassVar[re.Pattern] = re.compile(r"Game (\d+): (.*)")

    @staticmethod
    def from_string(line: str) -> Self:
        match = Game.PATTERN.fullmatch(line)
        return Game(id=int(match[1]),
                    draws=Draw.from_string(match[2])
                    )

    def possible(self, sack: dict[str, int]) -> bool:
        return all(map(lambda d: d.possible(sack), self.draws))

    def power_value(self) -> int:
        return reduce(mul, self._minimum_sack().values())

    def _minimum_sack(self) -> dict[str, int]:
        sack = {}
        for draw in self.draws:
            for color, cubes in draw.cubes_by_color.items():
                if cubes > sack.get(color, 0):
                    sack[color] = cubes
        return sack

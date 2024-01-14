from dataclasses import dataclass, field
from functools import cached_property
from typing import ClassVar


@dataclass(frozen=True)
class NonogramPattern:
    target_pattern: str
    black_pattern: list[int] = field(default_factory=list)
    EMPTY: ClassVar[str] = "."
    UNKNOWN: ClassVar[str] = "?"
    FILLED: ClassVar[str] = "#"

    @cached_property
    def total_whites_possible(self) -> int:
        return len(self.target_pattern) - self.minimum_length(len(self.black_pattern))

    def minimum_length(self, blacks_covered: int):
        if blacks_covered == 0:
            return 0
        else:
            return sum(self.black_pattern[0:blacks_covered]) + blacks_covered - 1

    def matches(self, start: int, current_black_index: int, extra_white_length: int) -> bool:
        stop = start + extra_white_length + self.black_pattern[current_black_index]
        # print(f"Checking matches for {start=}, {stop=}, {self.target_pattern[start:stop + 1]}, whites_length: {extra_white_length}")
        for index, char in enumerate(self.target_pattern[start:stop + 1], start=start):
            if index == stop:
                if char == self.FILLED:
                    # print(f"Doesn't match because final char is filled, {index=}")
                    return False
            elif index < start + extra_white_length:
                if char == self.FILLED:
                    # print(f"Doesn't match because initial whites has a filled space, {index=}")
                    return False
            elif char == self.EMPTY:
                # print(f"Doesn't match because an empty block is in the wanted blacks space, {index=}")
                return False
        return True

    def ends_empty(self, final_white_length: int) -> bool:
        start = len(self.target_pattern) - final_white_length
        return all(char != self.FILLED for char in self.target_pattern[start:])


def to_nonogram_pattern(line: str, multiplier: int) -> NonogramPattern:
    parts_string, pattern_string = line.split()
    parts_string = "?".join([parts_string] * multiplier)

    pattern_string = ",".join([pattern_string] * multiplier)
    pattern = list(map(int, pattern_string.split(",")))
    return NonogramPattern(target_pattern=parts_string, black_pattern=pattern)

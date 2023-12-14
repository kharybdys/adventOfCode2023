import re
from abc import abstractmethod, ABC

from dataclasses import dataclass
from itertools import batched
from typing import Self, Generator

from utils import split_in_groups_separated_by_empty_line


@dataclass(order=True)
class Range:
    start: int
    stop: int  # Exclusive
    correction: int = 0

    def partial_overlap(self, rng: Self) -> bool:
        return rng.start < self.stop and self.start <= rng.stop

    def apply_ranges(self, ranges: list[Self]) -> Generator[Self, None, None]:
        local_start = self.start
        for rng in sorted(filter(self.partial_overlap, ranges)):
            if rng.start > local_start:
                yield Range(start=local_start, stop=rng.start)
            yield Range(start=max(rng.start, self.start) + rng.correction, stop=min(rng.stop, self.stop) + rng.correction)
            local_start = rng.stop
        if local_start < self.stop:
            yield Range(start=local_start, stop=self.stop)

    def __repr__(self):
        return f"Range[{self.start=}, {self.stop=}, {self.correction=}]"

    @staticmethod
    def from_string(line: str) -> Self:
        start_dest, start_source, range_size = map(int, line.split())
        correction = start_dest - start_source
        stop = start_source + range_size
        return Range(start=start_source, stop=stop, correction=correction)


class Converter:
    def __init__(self, src: str, dest: str, ranges: list[Range]):
        self.src = src
        self.dest = dest
        self.ranges = ranges

    def convert(self, ranges: list[Range]) -> list[Range]:
        result = []
        for rng in ranges:
            result.extend(rng.apply_ranges(self.ranges))
        return result

    def __repr__(self):
        return f"Converter[{self.src=}, {self.dest=}, # ranges {len(self.ranges)}]"

    @staticmethod
    def from_string(lines: list[str], src: str, dest: str) -> Self:
        ranges = [Range.from_string(line) for line in lines]
        return Converter(src=src, dest=dest, ranges=ranges)


class Problem(ABC):
    SEEDS_PREFIX = "seeds: "
    CONVERTER_PATTERN = re.compile(r"(\w+)-to-(\w+) map:")

    def __init__(self, seeds_line: str, converters: list[Converter]):
        self.seeds_line = seeds_line
        self.converters = list(self.special_sort(converters, "seed", "location"))

    @staticmethod
    def special_sort(converters: list[Converter], src: str, dest: str) -> Generator[Converter, None, None]:
        while src != dest:
            converter = next(filter(lambda c: c.src == src, converters))
            yield converter
            src = converter.dest

    def convert(self, rng: Range) -> list[Range]:
        result = [rng]
        for converter in self.converters:
            result = converter.convert(result)
        return result

    def solve(self) -> int:
        ranges = []
        for seed_range in self.generate_seeds():
            ranges.extend(self.convert(seed_range))
        min_range = min(ranges)
        return min_range.start

    @abstractmethod
    def generate_seeds(self) -> Generator[Range, None, None]:
        pass

    @classmethod
    def from_string(cls, lines: list[str]) -> Self:
        seeds_line = ""
        converters = []
        for block in split_in_groups_separated_by_empty_line(lines):
            if block[0].startswith(Problem.SEEDS_PREFIX):
                seeds_line = block[0].removeprefix(Problem.SEEDS_PREFIX)
            else:
                if match := Problem.CONVERTER_PATTERN.fullmatch(block[0]):
                    src, dest = match[1], match[2]
                    converters.append(Converter.from_string(block[1:], src, dest))
                else:
                    raise ValueError(f"Invalid start to converter block: {block}")
        return cls(seeds_line=seeds_line, converters=converters)


class ProblemA(Problem):
    def generate_seeds(self) -> Generator[Range, None, None]:
        for seed_str in self.seeds_line.split():
            seed = int(seed_str)
            yield Range(seed, seed + 1, 0)


class ProblemB(Problem):
    def generate_seeds(self) -> Generator[Range, None, None]:
        for start, range_size in batched(map(int, self.seeds_line.split()), 2):
            yield Range(start, start + range_size, 0)

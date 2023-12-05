import re

from dataclasses import dataclass
from typing import Self, Generator


@dataclass
class Range:
    start: int
    stop: int  # Exclusive
    correction: int

    def convert(self, num: int) -> int:
        if self.valid_for(num):
            return num + self.correction
        else:
            raise ValueError("Invalid range applied")

    def valid_for(self, num: int) -> bool:
        return self.start <= num < self.stop

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

    def convert(self, num: int) -> int:
        for single_range in self.ranges:
            if single_range.valid_for(num):
                return single_range.convert(num)
        return num

    def __repr__(self):
        return f"Converter[{self.src=}, {self.dest=}, # ranges {len(self.ranges)}]"

    @staticmethod
    def from_string(lines: list[str], src: str, dest: str) -> Self:
        ranges = [Range.from_string(line) for line in lines]
        print(f"Making converter with ranges: {ranges}, for {src=} and {dest=}")
        return Converter(src=src, dest=dest, ranges=ranges)


class Problem:
    SEEDS_PREFIX = "seeds: "
    CONVERTER_PATTERN = re.compile(r"(\w+)-to-(\w+) map:")

    def __init__(self, seeds: list[int], converters: list[Converter]):
        self.seeds = seeds
        self.converters = list(self.special_sort(converters, "seed", "location"))

    @staticmethod
    def special_sort(converters: list[Converter], src: str, dest: str) -> Generator[Converter, None, None]:
        print(f"Called special_sort with {converters=}, {src=}, {dest=}")
        while src != dest:
            converter = next(filter(lambda c: c.src == src, converters))
            print(f"Found converter {converter}")
            yield converter
            src = converter.dest

    def convert(self, num: int) -> int:
        result = num
        print(f"Entered convert with {result}")
        for converter in self.converters:
            result = converter.convert(result)
            print(f"After converter {converter} this is now {result}")
        return result

    def solve(self) -> int:
        return min(self.convert(seed) for seed in self.seeds)

    @staticmethod
    def split_on_empty_line(lines: list[str]) -> Generator[list[str], None, None]:
        result = []
        for line in lines:
            if line:
                result.append(line)
            else:
                yield result
                result = []
        yield result

    @staticmethod
    def from_string(lines: list[str]) -> Self:
        seeds = []
        converters = []
        for block in Problem.split_on_empty_line(lines):
            if block[0].startswith(Problem.SEEDS_PREFIX):
                seeds = [int(seed) for seed in block[0].removeprefix(Problem.SEEDS_PREFIX).split()]
            else:
                if match := Problem.CONVERTER_PATTERN.fullmatch(block[0]):
                    src, dest = match[1], match[2]
                    converters.append(Converter.from_string(block[1:], src, dest))
                else:
                    raise ValueError(f"Invalid start to converter block: {block}")
        return Problem(seeds=seeds, converters=converters)

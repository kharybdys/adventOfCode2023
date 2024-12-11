from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import Self

from registry import register_solver


@dataclass(order=True)
class Stone:
    value: int = field(compare=False)
    min_depth_encountered: int
    follow_up_stones: list[Self] = field(default_factory=list, compare=False)
    steps_to_follow_up: int = field(compare=False, default=-1)
    count_cache: dict[int, int] = field(default_factory=dict, compare=False)

    def merge(self, other: Self):
        assert isinstance(other, Stone)
        assert other.value == self.value
        self.min_depth_encountered = min(self.min_depth_encountered, other.min_depth_encountered)

    def fill_cache(self, depth: int, max_depth: int, count: int):
        for key in range(depth, max_depth + 1):
            self.count_cache[depth] = count

    def __repr__(self) -> str:
        return f"Stone[value={self.value}, min_depth={self.min_depth_encountered}, follow_up_stones=Stones: {[stone.value for stone in self.follow_up_stones]}, steps_to_follow_up={self.steps_to_follow_up}]"


def find_follow_up_stones(start_stone: Stone, max_depth: int):
    print(f"Finding follow_up_stones for {start_stone}")
    assert len(start_stone.follow_up_stones) == 0, "Shouldn't find follow_up_stones for a stone that already knows!"
    depth = 0
    value = start_stone.value
    while len(str(value)) % 2 != 0 and start_stone.min_depth_encountered + depth <= max_depth:
        if value == 0:
            value = 1
        else:
            value *= 2024
        depth += 1
    print(f"Value after {depth} steps is {value}")
    depth += 1
    start_stone.steps_to_follow_up = depth
    if len(str(value)) % 2 == 0:
        print(f"Going to split {value}")
        # Do the split action if we haven't reached max_depth
        string_value = str(value)
        start_stone.follow_up_stones = [
            Stone(
                value=int(string_value[:len(string_value) // 2]),
                min_depth_encountered=start_stone.min_depth_encountered + depth,
            ),
            Stone(
                value=int(string_value[len(string_value) // 2:]),
                min_depth_encountered=start_stone.min_depth_encountered + depth,
            ),
        ]
    print(f"Result of finding follow_up_stones: {start_stone.follow_up_stones} at {start_stone.steps_to_follow_up}")


def walk(stone: Stone, depth: int, max_depth: int) -> int:
    if depth not in stone.count_cache:
        if stone.steps_to_follow_up + depth > max_depth:
            stone.fill_cache(depth, max_depth, 1)
        elif not stone.follow_up_stones:
            raise ValueError(f"No follow-up stones while steps_to_follow_up is not big enough, this should not happen. {stone=}, {depth=}, {max_depth=}")
        else:
            count = sum(
                walk(
                    stone=follow_up_stone,
                    depth=depth + stone.steps_to_follow_up,
                    max_depth=max_depth
                ) for follow_up_stone in stone.follow_up_stones
            )
            stone.count_cache[depth] = count
    return stone.count_cache[depth]


def solve(puzzle_input: list[str], max_depth: int):
    print(puzzle_input)
    assert len(puzzle_input) == 1, "Day 11 can only work with a single line of input"
    encountered_stones: dict[int, Stone] = {
        int(nr): Stone(
            value=int(nr),
            min_depth_encountered=0,
        ) for nr in puzzle_input[0].split(" ")
    }
    stones_to_parse = PriorityQueue()
    for stone in encountered_stones.values():
        stones_to_parse.put(stone)

    while not stones_to_parse.empty():
        stone = stones_to_parse.get_nowait()
        find_follow_up_stones(stone, max_depth=max_depth)
        new_follow_up_stones: list[Stone] = []
        for index, follow_up_stone in enumerate(stone.follow_up_stones[:]):
            if follow_up_stone.value in encountered_stones:
                print(f"Need to merge {follow_up_stone} with {encountered_stones[follow_up_stone.value]}")
                encountered_stones[follow_up_stone.value].merge(follow_up_stone)
                new_follow_up_stones.append(encountered_stones[follow_up_stone.value])
            else:
                encountered_stones[follow_up_stone.value] = follow_up_stone
                stones_to_parse.put_nowait(follow_up_stone)
                new_follow_up_stones.append(follow_up_stone)
        stone.follow_up_stones = new_follow_up_stones

    print(f"All encountered stones: {encountered_stones}")
    print("Going to calculate the solution:")
    solution = sum(walk(stone=stone, depth=0, max_depth=max_depth) for stone in encountered_stones.values() if stone.min_depth_encountered == 0)
    print(f"Solution is {solution}")


@register_solver(year="2024", key="11", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    solve(puzzle_input, max_depth=6 if example else 25)


@register_solver(year="2024", key="11", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    solve(puzzle_input, max_depth=6 if example else 75)

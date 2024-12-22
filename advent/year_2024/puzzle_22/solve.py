from collections import deque, defaultdict
from collections.abc import Generator

from registry import register_solver


def mix_and_prune(secret: int, step: int) -> int:
    mix = secret ^ step
    return mix % 16777216


def next_secret_number(secret: int) -> int:
    secret = mix_and_prune(secret, secret * 64)
    secret = mix_and_prune(secret, secret // 32)
    return mix_and_prune(secret, secret * 2048)


class Monkey:
    PRICES_AMOUNT = 2000
    CHANGES_BY_AMOUNT = 4

    def __init__(self, starting_secret: int):
        self.starting_secret = starting_secret
        self.prices = [self.starting_secret % 10]
        secret = self.starting_secret
        for _ in range(0, self.PRICES_AMOUNT):
            secret = next_secret_number(secret)
            self.prices.append(secret % 10)

    @property
    def price_changes(self) -> Generator[tuple[tuple[int, ...], int], None, None]:
        changes: deque[int] = deque()
        previous_price = self.prices[0]
        for price in self.prices[1:]:
            changes.append(price - previous_price)
            if len(changes) == self.CHANGES_BY_AMOUNT:
                yield tuple(changes.copy()), price
                changes.popleft()
            previous_price = price


@register_solver(year="2024", key="22", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)

    solution = 0
    for line in puzzle_input:
        secret = int(line)
        for _ in range(0, 2000):
            secret = next_secret_number(secret)
        solution += secret
    print(f"Solution is {solution}")


@register_solver(year="2024", key="22", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    rewards: dict[tuple[int, ...], int] = defaultdict(int)
    for line in puzzle_input:
        monkey = Monkey(int(line))
        price_changes_done: set[tuple[int, ...]] = set()
        for price_change, value in monkey.price_changes:
            if price_change not in price_changes_done:
                rewards[price_change] += value
                price_changes_done.add(price_change)
    print(f"Solution is {max(rewards.values())}")

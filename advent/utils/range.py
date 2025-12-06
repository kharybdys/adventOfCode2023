from dataclasses import dataclass
from functools import cached_property


@dataclass
class Range:
    start: int
    stop: int

    @cached_property
    def size(self) -> int:
        return self.stop - self.start

    def within(self, value: float) -> bool:
        return self.start <= value < self.stop

    def before(self, value: float | int) -> bool:
        return self.stop <= value

    def after(self, value: float | int) -> bool:
        return self.start > value


@dataclass
class InclusiveRange(Range):
    @cached_property
    def size(self) -> int:
        return self.stop - self.start + 1

    def within(self, value: float | int) -> bool:
        return self.start <= value <= self.stop

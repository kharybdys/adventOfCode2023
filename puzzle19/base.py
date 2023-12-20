from dataclasses import dataclass
from enum import Enum
from typing import Self, Optional

from utils import Range


class Status(Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    PENDING = "PENDING"


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int
    status: Status = Status.PENDING

    def reject(self):
        self.status = Status.REJECTED

    def accept(self):
        self.status = Status.ACCEPTED

    @property
    def accepted(self) -> bool:
        return self.status == Status.ACCEPTED

    @property
    def value(self) -> int:
        return self.x + self.m + self.a + self.s


@dataclass
class PartRange:
    x: Range
    m: Range
    a: Range
    s: Range

    @property
    def value(self) -> int:
        return self.x.size * self.m.size * self.a.size * self.s.size

    def get_range(self, attribute: str) -> Range:
        match attribute:
            case "x":
                return self.x
            case "m":
                return self.m
            case "a":
                return self.a
            case "s":
                return self.s
            case _:
                raise ValueError(f"Unknown attribute for get_range {attribute}")

    def copy_and_replace(self, attribute: str, rng: Range):
        match attribute:
            case "x":
                return PartRange(x=rng, m=self.m, a=self.a, s=self.s)
            case "m":
                return PartRange(x=self.x, m=rng, a=self.a, s=self.s)
            case "a":
                return PartRange(x=self.x, m=self.m, a=rng, s=self.s)
            case "s":
                return PartRange(x=self.x, m=self.m, a=self.a, s=rng)
            case _:
                raise ValueError(f"Unknown attribute for get_range {attribute}")

    def split_on_greater_then(self, attribute: str, value: int) -> tuple[Optional[Self], Optional[Self]]:
        rng = self.get_range(attribute)
        greater_equal_value = value + 1
        if rng.within(greater_equal_value):
            before_range = Range(rng.start, greater_equal_value)
            after_range = Range(greater_equal_value, rng.stop)
            return self.copy_and_replace(attribute, after_range), self.copy_and_replace(attribute, before_range)
        elif rng.before(greater_equal_value):
            return None, self
        elif rng.after(greater_equal_value):
            return self, None
        else:
            raise ValueError(f"Unknown comparison result between range {rng} and value {value}")

    def split_on_less_then(self, attribute: str, value: int) -> tuple[Optional[Self], Optional[Self]]:
        rng = self.get_range(attribute)
        less_equal_value = value
        if rng.within(less_equal_value):
            before_range = Range(rng.start, less_equal_value)
            after_range = Range(less_equal_value, rng.stop)
            return self.copy_and_replace(attribute, before_range), self.copy_and_replace(attribute, after_range)
        elif rng.before(less_equal_value):
            return self, None
        elif rng.after(less_equal_value):
            return None, self


class Watcher:
    def __init__(self):
        self.combinations = 0

    def accept(self, accepted_range: PartRange):
        self.combinations += accepted_range.value

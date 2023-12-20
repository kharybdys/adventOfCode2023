from dataclasses import dataclass
from enum import Enum


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

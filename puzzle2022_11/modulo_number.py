from typing import Self


class ModuloNumber:
    def __init__(self, num: int, limit: int):
        self.limit = limit
        self.num = num % self.limit

    def __mul__(self, other) -> Self:
        return ModuloNumber(num=self.num * int(other), limit=self.limit)

    def __add__(self, other) -> Self:
        return ModuloNumber(num=self.num + int(other), limit=self.limit)

    def __floordiv__(self, other) -> Self:
        return ModuloNumber(num=self.num // int(other), limit=self.limit)

    def __mod__(self, other) -> int:
        return self.num % int(other)

    def __int__(self) -> int:
        return self.num

    def __repr__(self) -> str:
        return f"ModuloNumber[{self.num=}, {self.limit=}]"

from itertools import zip_longest
from typing import Self


class SNAFUNumber:
    def __init__(self, digits: list[int]):
        if all(map(lambda d: -2 <= d <= 2, digits)):
            self.digits = digits
        else:
            raise ValueError(f"Invalid SNAFUNumber: {digits}")

    def __str__(self) -> str:
        return "".join(map(self._digit_to_char, self.digits))

    def __add__(self, other: Self):
        new_digits: list[int] = []
        remainder = 0
        for self_digit, other_digit in zip_longest(reversed(self.digits), reversed(other.digits), fillvalue=0):
            local_sum = remainder + self_digit + other_digit
            local_sum, remainder = self._to_base_5(local_sum)
            new_digits.append(local_sum)
        if remainder != 0:
            new_digits.extend(self._to_base_5(remainder))
        return SNAFUNumber(list(reversed(new_digits)))

    @staticmethod
    def _to_base_5(digit: int) -> tuple[int, int]:
        remainder = 0
        while digit > 2:
            digit -= 5
            remainder += 1
        while digit < -2:
            digit += 5
            remainder -= 1
        return digit, remainder

    @staticmethod
    def parse(string: str) -> Self:
        return SNAFUNumber(digits=list(map(SNAFUNumber._char_to_digit, string)))

    @staticmethod
    def _char_to_digit(char: str) -> int:
        match char:
            case "2":
                return 2
            case "1":
                return 1
            case "0":
                return 0
            case "-":
                return -1
            case "=":
                return -2
            case _:
                raise ValueError(f"Invalid SNAFUNumber digit: {char}")

    @staticmethod
    def _digit_to_char(digit: int) -> str:
        match digit:
            case 2:
                return "2"
            case 1:
                return "1"
            case 0:
                return "0"
            case -1:
                return "-"
            case -2:
                return "="
            case _:
                raise ValueError(f"Invalid SNAFUNumber digit: {digit}")

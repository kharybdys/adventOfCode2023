from advent.registry import register_solver


class Dial:
    def __init__(self, during: bool):
        self._position = 50
        self._count_zeroes = 0
        self._during = during

    def move_dial(self, code: str):
        diff = self._code_to_diff(code)

        if self._during:
            roundtrips = int(diff / 100)
            self._count_zeroes += abs(roundtrips)
            diff -= roundtrips * 100

        original_position = self._position
        self._position += diff
        position_before_correction = self._position
        self._position = self._position % 100

        if self._position == 0:
            self._count_zeroes += 1
        elif original_position != 0 and self._during:
            if position_before_correction != self._position:
                self._count_zeroes += 1

    def _code_to_diff(self, code: str) -> int:
        if code.startswith("L"):
            return int(code[1:]) * -1
        if code.startswith("R"):
            return int(code[1:])
        raise ValueError(f"Unsupported code: {code}")

    @property
    def count_zeroes(self) -> int:
        return self._count_zeroes


@register_solver(year="2025", key="1", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    dial = Dial(during=False)
    for line in puzzle_input:
        dial.move_dial(line)

    print(f"Solution is {dial.count_zeroes=}")


@register_solver(year="2025", key="1", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    dial = Dial(during=True)
    for line in puzzle_input:
        dial.move_dial(line)

    print(f"Solution is {dial.count_zeroes=}")

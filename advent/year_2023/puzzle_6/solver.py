from math import prod, isqrt, comb

from registry import register_solver


def inverse_choose(result: int, choices: int) -> int:
    STOP = 10000000
    previous_result = 0
    for i in range(choices, STOP):
        choose = comb(i, choices)
        if choose <= result:
            previous_result = i
        else:
            print(f"inverse_choose({result}, {choices}) = {previous_result}")
            return previous_result


def ways_to_win(time: int, distance: int) -> int:
    # (x-a)(y+a) - xy = xy -ay + ax - a^2 -xy = a(x-y)-a^2
    # 3 * 3 = 9, 2 * 4 = 8, 1 * 5 = 5 -> 0, 1, 4, 9 = quadratics
    # 4 * 5 = 20, 3 * 6 = 18, 2 * 7 = 14, 1 * 8 = 8  -> 0, 2, 6, 12, 20 = 2 * (n choose 2)
    half_time_low = time // 2
    half_time_high = time - half_time_low
    overshoot = half_time_high * half_time_low - distance
    print(f"overshoot = {half_time_high} * {half_time_low} - {distance} = {overshoot}")
    init_diff = half_time_high - half_time_low
    # solve overshoot >= a * init_diff - a * a
    if init_diff == 0:
        print(f"isqrt: {isqrt(overshoot)}")
        return 2 * isqrt(overshoot-1) + 1  # -1 to remove equality as an option
    else:
        # overshoot >= 2 * a choose 2
        return 2 * inverse_choose(overshoot // 2, 2)


def ways_to_win_with_log(time: int, distance: int) -> int:
    result = ways_to_win(time, distance)
    print(f"{time=}, {distance=}, {result=}")
    return result


def parse(puzzle_input: list[str]) -> list[tuple[int, int]]:
    """list of time, distance pairs"""
    times_prefix = "Time:"
    distances_prefix = "Distance:"
    times: list[int] = []
    distances: list[int] = []
    for line in puzzle_input:
        if line.startswith(times_prefix):
            times = [int(time) for time in line.removeprefix(times_prefix).split()]
        if line.startswith(distances_prefix):
            distances = [int(distance) for distance in line.removeprefix(distances_prefix).split()]
    if len(times) != len(distances):
        raise ValueError("Invalid input, times & distances are expected to be equal length")
    return list(zip(times, distances))


def parse_ignore_spaces(puzzle_input: list[str]) -> tuple[int, int]:
    """list of time, distance pairs"""
    times_prefix = "Time:"
    distances_prefix = "Distance:"
    time: int = 0
    distance: int = 0
    for line in puzzle_input:
        if line.startswith(times_prefix):
            time = int(line.removeprefix(times_prefix).replace(" ", ""))
        if line.startswith(distances_prefix):
            distance = int(line.removeprefix(distances_prefix).replace(" ", ""))
    return time, distance


@register_solver(year="2023", key="6", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    solution = prod(ways_to_win_with_log(time, distance) for time, distance in parse(puzzle_input))
    # time 53, distance 275: 6 * 47 to 47 * 6 = 42 options
    # time 78, distance 1215: 22 * 56 to 56 * 22 = 35 options
    # time 30, distance 200: 11 * 19 to 19 * 11 = 9 options
    print(solution)


@register_solver(year="2023", key="6", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    solution = ways_to_win_with_log(*parse_ignore_spaces(puzzle_input))
    print(solution)

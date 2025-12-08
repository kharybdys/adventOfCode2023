from functools import cached_property
from itertools import combinations
from math import prod
from typing import Self

from advent.registry import register_solver


class Connection:
    def __init__(self, from_str: str, to_str: str):
        self.from_str = from_str
        self._from_x, self._from_y, self._from_z = self._parse(from_str)

        self.to_str = to_str
        self._to_x, self._to_y, self._to_z = self._parse(to_str)

    def __repr__(self) -> str:
        return f"Connection[from={self.from_str}, to={self.to_str}]"

    def _parse(self, line: str) -> tuple[int, int, int]:
        parts = line.split(",")
        if len(parts) != 3:
            raise ValueError(f"Invalid line, no three parts: {line}")
        return int(parts[0]), int(parts[1]), int(parts[2])

    @cached_property
    def distance(self) -> float:
        temp = pow(self._to_x - self._from_x, 2)
        temp += pow(self._to_y - self._from_y, 2)
        temp += pow(self._to_z - self._from_z, 2)
        return pow(temp, 0.5)


class Circuit(list[Connection]):
    @property
    def junctions(self) -> set[str]:
        result = set()
        for item in self:
            result.update((item.from_str, item.to_str))
        return result

    @property
    def junction_count(self) -> int:
        return len(self.junctions)

    def is_connected(self, connection: Connection) -> bool:
        juncs = self.junctions
        return connection.from_str in juncs or connection.to_str in juncs

    def is_contained(self, connection: Connection) -> bool:
        juncs = self.junctions
        return connection.from_str in juncs and connection.to_str in juncs


@register_solver(year="2025", key="8", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    connections: list[Connection] = []
    for line_1, line_2 in combinations(puzzle_input, 2):
        connections.append(Connection(from_str=line_1, to_str=line_2))

    connections.sort(key=lambda c: c.distance)

    circuits: list[Circuit] = []
    for index in range(0, 10 if example else 1000):
        current_connection = connections[index]
        print(f"Finding a home for {current_connection}, with distance {current_connection.distance}")
        matching_circuits = [circuit for circuit in circuits if circuit.is_connected(current_connection)]
        if len(matching_circuits) == 2:
            # need to merge circuits
            circuits.remove(matching_circuits[0])
            other_circuit = matching_circuits[1]
            other_circuit.append(current_connection)
            other_circuit.extend(matching_circuits[0])
        elif len(matching_circuits) == 1:
            if not matching_circuits[0].is_contained(current_connection):
                matching_circuits[0].append(current_connection)
        elif len(matching_circuits) == 0:
            new_circuit = Circuit()
            new_circuit.append(current_connection)
            circuits.append(new_circuit)
        else:
            raise ValueError(f"For {current_connection=}, got an unexpected number of {matching_circuits=}")

    for circuit in circuits:
        print(f"{circuit=}, {circuit.junction_count=}")

    solution = prod(sorted((circuit.junction_count for circuit in circuits), reverse=True)[0:3])
    print(f"Solution is {solution}")


@register_solver(year="2025", key="8", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    solution = 0
    print(f"Solution is {solution}")

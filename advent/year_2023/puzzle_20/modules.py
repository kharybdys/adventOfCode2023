import re
from collections import deque
from dataclasses import dataclass
from typing import Self, Generator

from advent.utils.range import Range


@dataclass
class Pulse:
    high_pulse: bool
    cycle: int
    source: str
    destination: "Module"

    def process(self) -> Generator[Self, None, None]:
        yield from self.destination.receive_pulse(self.high_pulse, self.cycle, self.source)


class Module:
    _PRINT_CHAR = ""

    def __init__(self, identifier: str, destination_strings: list[str]):
        self.identifier = identifier
        self.destination_strings = destination_strings
        self.destinations: list[Module] = []

    @property
    def status(self) -> bool:
        return False

    def register_receiver(self, module: Self):
        pass

    def send_pulse(self, cycle: int, high_pulse: bool) -> Generator[Pulse, None, None]:
        for dest in self.destinations:
            yield Pulse(high_pulse, cycle, self.identifier, dest)

    def receive_pulse(self, high_pulse: bool, cycle: int, source_identifier: str) -> Generator[Pulse, None, None]:
        yield from self.send_pulse(cycle, high_pulse)

    def __repr__(self) -> str:
        return f"{self._PRINT_CHAR}{self.identifier}"


class OutputModule(Module):
    def send_pulse(self, cycle: int, high_pulse: bool) -> Generator[Pulse, None, None]:
        yield from ()


class WatcherModule(Module):
    _PRINT_CHAR = "@"

    def __init__(self, identifier: str, destination_strings: list[str]):
        super().__init__(identifier, destination_strings)
        self.high_signal_ranges = []
        self.latest_high_signal: int | None = None

    def receive_pulse(self, high_pulse: bool, cycle: int, source_identifier: str) -> Generator[Pulse, None, None]:
        if not high_pulse:
            if self.latest_high_signal:
                self.high_signal_ranges.append(Range(self.latest_high_signal, cycle + 1))
                self.latest_high_signal = None
        else:
            if not self.latest_high_signal:
                self.latest_high_signal = cycle
        yield from ()

    def reset(self):
        self.high_signal_ranges = []


class FlipFlopModule(Module):
    _PRINT_CHAR = "%"

    def __init__(self, identifier: str, destination_strings: list[str]):
        super().__init__(identifier, destination_strings)
        self.on = False

    @property
    def status(self) -> bool:
        return self.on

    def receive_pulse(self, high_pulse: bool, cycle: int, source_identifier: str) -> Generator[Pulse, None, None]:
        if high_pulse:
            pass
        else:
            self.on = not self.on
            yield from self.send_pulse(cycle, self.on)


class ConjunctionModule(Module):
    _PRINT_CHAR = "&"

    def __init__(self, identifier: str, destination_strings: list[str]):
        super().__init__(identifier, destination_strings)
        self.last_pulses: dict[str, bool] = {}

    def register_receiver(self, module: Self):
        self.last_pulses[module.identifier] = False

    def receive_pulse(self, high_pulse: bool, cycle: int, source_identifier: str) -> Generator[Pulse, None, None]:
        self.last_pulses[source_identifier] = high_pulse
        yield from self.send_pulse(cycle, not all(self.last_pulses.values()))


def parse_module(module_line: str) -> Module:
    MODULE_PATTERN = re.compile(r"([%&])?([a-z]+) -> (.*)")
    if match := MODULE_PATTERN.fullmatch(module_line):
        type_string = match[1] if match[1] else " "
        identifier = match[2]
        destination_strings = match[3].split(", ")
        match type_string:
            case "%":
                return FlipFlopModule(identifier, destination_strings)
            case "&":
                return ConjunctionModule(identifier, destination_strings)
            case " ":
                return Module(identifier, destination_strings)
            case _:
                raise ValueError(f"Invalid module type from {module_line}, namely {type_string}")


def send_pulse(initial_pulse: Pulse, debug: bool = False) -> tuple[int, int]:
    high_pulse_count = 0
    low_pulse_count = 0
    pulses: deque[Pulse] = deque()
    pulses.append(initial_pulse)
    while pulses:
        pulse = pulses.popleft()
        if pulse.high_pulse:
            high_pulse_count += 1
        else:
            low_pulse_count += 1
        if debug:
            print(f"Sending pulse from {pulse.source}, high? {pulse.high_pulse} to {pulse.destination.identifier}")
        pulses.extend(pulse.process())
    return high_pulse_count, low_pulse_count

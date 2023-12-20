import re
from dataclasses import dataclass
from typing import Self, Generator


@dataclass
class Pulse:
    high_pulse: bool
    source: str
    destination: "Module"

    def process(self) -> Generator[Self, None, None]:
        yield from self.destination.receive_pulse(self.high_pulse, self.source)


class Module:
    def __init__(self, identifier: str, destination_strings: list[str]):
        self.identifier = identifier
        self.destination_strings = destination_strings
        self.destinations: list[Module] = []

    @property
    def status(self) -> bool:
        return False

    def register_receiver(self, module: Self):
        pass

    def send_pulse(self, high_pulse: bool) -> Generator[Pulse, None, None]:
        for dest in self.destinations:
            yield Pulse(high_pulse, self.identifier, dest)

    def receive_pulse(self, high_pulse: bool, source_identifier: str) -> Generator[Pulse, None, None]:
        yield from self.send_pulse(high_pulse)


class OutputModule(Module):
    def send_pulse(self, high_pulse: bool) -> Generator[Pulse, None, None]:
        yield from ()


class FlipFlopModule(Module):
    def __init__(self, identifier: str, destination_strings: list[str]):
        super().__init__(identifier, destination_strings)
        self.on = False

    @property
    def status(self) -> bool:
        return self.on

    def receive_pulse(self, high_pulse: bool, source_identifier: str) -> Generator[Pulse, None, None]:
        if high_pulse:
            pass
        else:
            self.on = not self.on
            yield from self.send_pulse(self.on)


class ConjunctionModule(Module):
    def __init__(self, identifier: str, destination_strings: list[str]):
        super().__init__(identifier, destination_strings)
        self.last_pulses: dict[str, bool] = {}

    def register_receiver(self, module: Self):
        self.last_pulses[module.identifier] = False

    def receive_pulse(self, high_pulse: bool, source_identifier: str) -> Generator[Pulse, None, None]:
        self.last_pulses[source_identifier] = high_pulse
        yield from self.send_pulse(not all(self.last_pulses.values()))


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

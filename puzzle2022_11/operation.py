import re

from abc import ABC, abstractmethod
from typing import Self

from puzzle2022_11.logger import LogStreamer
from puzzle2022_11.number import ANumber


class Operation(ABC):
    def __init__(self, logger: LogStreamer):
        self.logger = logger

    @abstractmethod
    def apply(self, num: ANumber, detail_log: bool) -> ANumber:
        pass

    @abstractmethod
    def log(self, result: ANumber, do_log: bool):
        pass

    @classmethod
    @abstractmethod
    def from_match(cls, match: re.Match, logger: LogStreamer) -> Self:
        pass


class AddOperation(Operation):
    PATTERN = re.compile(r"new = old \+ (\d+)")

    def __init__(self, logger: LogStreamer, constant: int):
        super().__init__(logger)
        self.constant = constant

    def apply(self, num: ANumber, detail_log: bool) -> ANumber:
        result = num + self.constant
        self.log(result=result, do_log=detail_log)
        return result

    def log(self, result: ANumber, do_log: bool):
        if do_log:
            self.logger.log("Worry level increases by # to |.".replace("#", str(self.constant)).replace("|", str(result)))

    @classmethod
    def from_match(cls, match: re.Match, logger: LogStreamer) -> Self:
        return AddOperation(logger, int(match[1]))


class MultiplyOperation(Operation):
    PATTERN = re.compile(r"new = old \* (\d+)")

    def __init__(self, logger: LogStreamer, constant: int):
        super().__init__(logger)
        self.constant = constant

    def apply(self, num: ANumber, detail_log: bool) -> ANumber:
        result = num*self.constant
        self.log(result=result, do_log=detail_log)
        return result

    def log(self, result: ANumber, do_log: bool):
        if do_log:
            self.logger.log("Worry level is multiplied by # to |.".replace("#", str(self.constant)).replace("|", str(result)))

    @classmethod
    def from_match(cls, match: re.Match, logger: LogStreamer) -> Self:
        return MultiplyOperation(logger, int(match[1]))


class SquareOperation(Operation):
    PATTERN = re.compile(r"new = old \* old")

    def apply(self, num: ANumber, detail_log: bool) -> ANumber:
        result = num * num
        self.log(result=result, do_log=detail_log)
        return result

    def log(self, result: ANumber, do_log: bool):
        if do_log:
            self.logger.log("Worry level is multiplied by itself to |.".replace("|", str(result)))

    @classmethod
    def from_match(cls, match: re.Match, logger: LogStreamer) -> Self:
        return SquareOperation(logger)


def parse_operation(operation: str, logger: LogStreamer) -> Operation:
    operation_classes = [AddOperation, MultiplyOperation, SquareOperation]
    for operation_cls in operation_classes:
        if match := operation_cls.PATTERN.fullmatch(operation):
            return operation_cls.from_match(match, logger)
    raise ValueError(f"Unsupported operation {operation}")

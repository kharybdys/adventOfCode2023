import sys
from abc import ABC, abstractmethod
from typing import Generator, Self, Optional

from puzzle2021_24.constraints import ConstraintsWatcher


class PossibilitiesGenerator(ABC):
    @abstractmethod
    def generate(self) -> Generator[int, None, None]:
        pass

    @abstractmethod
    def apply_add(self, by: int) -> Self:
        pass

    @abstractmethod
    def apply_add_var(self, by: Self) -> Self:
        pass

    @abstractmethod
    def apply_div(self, by: int) -> Self:
        pass

    @abstractmethod
    def apply_mul(self, by: Self) -> Self:
        pass

    @abstractmethod
    def apply_mod(self, by: int) -> Self:
        pass

    @abstractmethod
    def apply_eql(self, by: int) -> Self:
        pass

    @abstractmethod
    def apply_eql_var(self, by: Self) -> Self:
        pass


class Variable:
    def __init__(self, watcher: ConstraintsWatcher, possibilities: Optional[PossibilitiesGenerator] = None):
        self.negated = False
        self.possibilities_generator = possibilities or EverythingPossibilitiesGenerator()
        self.watcher = watcher

    def apply_mul(self, by: int | Self) -> Self:
        if by == 0:
            # This resets stuff
            pass
        elif isinstance(by, int):
            raise NotImplementedError("Operation <mul by non-zero> not supported by this solver")
        else:
            self.possibilities_generator = self.possibilities_generator.apply_mul(by)
        return self

    def apply_div(self, by: int | Self) -> Self:
        if isinstance(by, int):
            if by < 0:
                raise NotImplementedError("Operation <div by negative int> not supported by this solver")
            else:
                self.possibilities_generator = self.possibilities_generator.apply_div(by)
        else:
            raise NotImplementedError("Operation <div variable> not supported by this solver")
        return self

    def apply_add(self, by: int | Self) -> Self:
        if isinstance(by, int):
            self.possibilities_generator = self.possibilities_generator.apply_add(by)
        else:
            self.possibilities_generator = self.possibilities_generator.apply_add_var(by)
        return self

    def apply_mod(self, by: int | Self) -> Self:
        if isinstance(by, int):
            self.possibilities_generator = self.possibilities_generator.apply_mod(by)
        else:
            raise NotImplementedError("Operation <mod variable> not supported by this solver")
        return self

    def apply_eql(self, by: int | Self) -> Self:
        if isinstance(by, int):
            self.possibilities_generator = self.possibilities_generator.apply_eql(by)
        else:
            self.possibilities_generator = self.possibilities_generator.apply_eql_var(by)
        return self


class EverythingPossibilitiesGenerator(PossibilitiesGenerator):
    def __init__(self):
        self.step_size = 1

    def apply_add(self, by: int) -> PossibilitiesGenerator:
        # TODO: Can't be entirely right
        return self

    def apply_div(self, by: int) -> PossibilitiesGenerator:
        self.step_size *= by
        return self

    def generate(self) -> Generator[int, None, None]:
        # TODO: Not sure this is smart
        yield from range(-sys.maxsize-1, sys.maxsize, self.step_size)


class RangePossibilitiesGenerator(PossibilitiesGenerator):
    """Inclusive"""

    def __init__(self, min_value: int, max_value: int, step_size: int = 1):
        self.min_value = min_value
        self.max_value = max_value
        self.step_size = step_size

    def apply_add(self, by: int) -> PossibilitiesGenerator:
        self.min_value -= by
        self.max_value -= by
        return self

    def apply_div(self, by: int) -> Self:
        pass

    def apply_mod(self, by: int) -> Self:
        pass

    def apply_eql(self, by: int) -> Self:
        pass

    def apply_add_var(self, by: Self) -> Self:
        pass

    def apply_mul(self, by: Self) -> Self:
        pass

    def apply_eql_var(self, by: Self) -> Self:
        pass

    def generate(self) -> Generator[int, None, None]:
        yield from range(self.min_value, self.max_value+1, self.step_size)


class SetPossibilitiesGenerator(PossibilitiesGenerator):
    def __init__(self, values: list[int]):
        self.values = values

    def apply_add(self, by: int) -> PossibilitiesGenerator:
        self.values = [value - by for value in self.values]
        return self

    def apply_div(self, by: int) -> Self:
        # div by results in new possibilities being by *
        pass

    def apply_mod(self, by: int) -> Self:
        pass

    def apply_eql(self, by: int) -> Self:
        pass

    def apply_add_var(self, by: Self) -> Self:
        pass

    def apply_mul(self, by: Self) -> Self:
        pass

    def apply_eql_var(self, by: Self) -> Self:
        pass

    def generate(self) -> Generator[int, None, None]:
        for value in self.values:
            yield value


class BooleanPossibilitiesGenerator(SetPossibilitiesGenerator):
    # TODO: Note somehow the restraint from the equality that generated this
    def __init__(self):
        super().__init__(values=[0, 1])

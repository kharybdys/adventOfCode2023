from abc import ABC


class Constraint(ABC):
    pass


class ConstraintsWatcher:
    def __init__(self):
        self.constraints: list[Constraint] = []

from typing import Self

from puzzle2022_11.logger import LogStreamer
from puzzle2022_11.operation import Operation
from puzzle2022_11.prime_factorization_number import PrimeFactorizationNumber


class ThrowTest:
    LOG_TEXT = "Current worry level is?divisible by #."

    def __init__(self,  test_divisor: int, to_monkey_id_on_true: int, to_monkey_id_on_false: int, logger: LogStreamer):
        self.test_divisor = test_divisor
        self.monkeys: dict[bool, int] = {True: to_monkey_id_on_true,
                                         False: to_monkey_id_on_false}
        self.logger = logger

    def throws_to_monkey(self, num: PrimeFactorizationNumber, detail_log: bool) -> int:
        test_result = num % self.test_divisor == 0
        if detail_log:
            self.logger.log(self.log_text(test_result))
        return self.monkeys[test_result]

    def log_text(self, test_success: bool) -> str:
        test_text = " " if test_success else " not "
        return self.LOG_TEXT.replace("?", test_text).replace("#", str(self.test_divisor))


class Monkey:
    RELIEF_FACTOR: int = 3

    def __init__(self, monkey_id: int, items: list[PrimeFactorizationNumber], operation: Operation, throw_test: ThrowTest, logger: LogStreamer):
        self.monkey_id = monkey_id
        self.items = items
        self.operation = operation
        self.throw_test = throw_test
        self.logger = logger
        self.items_inspected = 0
        self.monkeys: dict[int, Self] = {}

    def report_items(self):
        self.logger.log(f"Monkey {self.monkey_id}: " + ", ".join(map(str, self.items)))

    def report_inspections(self):
        self.logger.log(f"Monkey {self.monkey_id} inspected items {self.items_inspected} times.")

    def register_monkeys(self, monkeys: dict[int, Self]):
        self.monkeys = monkeys

    def add(self, item: PrimeFactorizationNumber):
        self.items.append(item)

    def log(self, do_log: bool, message: str):
        if do_log:
            self.logger.log(message)

    def play_turn(self, detail_log: bool):
        self.log(detail_log, f"Monkey {self.monkey_id}: ")
        for item in self.items:
            self.log(detail_log, f"Monkey inspects an item with a worry level of {item}.")
            self.items_inspected += 1
            item = self.operation.apply(item, detail_log)
            item = item // self.RELIEF_FACTOR
            self.log(detail_log, f"Monkey gets bored with item. Worry level is divided by 3 to {item}.")
            target_monkey = self.throw_test.throws_to_monkey(item, detail_log)
            self.log(detail_log, f"Item with worry level {item} is thrown to monkey {target_monkey}.")
            self.monkeys[target_monkey].add(item)
        # All items will have been thrown to some other monkey
        self.items = []


class WorrisomeMonkey(Monkey):
    RELIEF_FACTOR: int = 1

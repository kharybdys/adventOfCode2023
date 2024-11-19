from collections import defaultdict
from copy import copy
from math import prod
from typing import Self

FIRST_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 91, 97]


def extend_first_primes(limit: int):
    max_prime = max(FIRST_PRIMES)
    for i in range(max_prime + 1, min(limit + 1, max_prime ** 2 + 1)):
        if not any(i % prime == 0 for prime in FIRST_PRIMES):
            FIRST_PRIMES.append(i)


# Assumes given numbers have prime factors at most < 100 except for possibly the last one
def factorize(num: int) -> dict[int, int]:
    result: dict[int, int] = defaultdict(int)
    for prime in FIRST_PRIMES:
        while num % prime == 0 and num > 1:
            result[prime] += 1
            num = num // prime
    if num != 1:
        extend_first_primes(num)
        print(f"Just extended first primes to {max(FIRST_PRIMES)} because of {num}")
        # Recurse
        new_result = factorize(num)
        for prime, factor in new_result.items():
            result[prime] += factor
    return result


class PrimeFactorizationNumber:
    @staticmethod
    def from_int(num: int) -> Self:
        return PrimeFactorizationNumber(factorize(num))

    @staticmethod
    def from_str(num: str) -> Self:
        return PrimeFactorizationNumber.from_int(int(num))

    def __init__(self, prime_factors: dict[int, int]):
        self.prime_factors = prime_factors

    def __mul__(self, other) -> Self:
        new_prime_factors = copy(self.prime_factors)
        if isinstance(other, int):
            new_prime_factors[other] += 1
            return PrimeFactorizationNumber(new_prime_factors)
        elif isinstance(other, PrimeFactorizationNumber):
            for prime, factor in other.prime_factors.items():
                new_prime_factors[prime] += factor
            return PrimeFactorizationNumber(new_prime_factors)
        else:
            raise ValueError(f"Multiplication is unsupported between {self} and {other}")

    def __add__(self, other) -> Self:
        if isinstance(other, int):
            return PrimeFactorizationNumber.from_int(int(self) + other)
        else:
            raise ValueError(f"Addition is unsupported between {self} and {other}")

    def __floordiv__(self, other) -> Self:
        new_prime_factors = copy(self.prime_factors)
        if isinstance(other, int):
            if other == 1:
                return PrimeFactorizationNumber(new_prime_factors)
            elif other in self.prime_factors and self.prime_factors[other] > 1:
                new_prime_factors[other] -= 1
                return PrimeFactorizationNumber(new_prime_factors)
            else:
                return PrimeFactorizationNumber.from_int(int(self) // other)
        else:
            raise ValueError(f"Addition is unsupported between {self} and {other}")

    def __mod__(self, other) -> int:
        new_prime_factors = copy(self.prime_factors)
        if isinstance(other, int):
            if other in new_prime_factors:
                return 0
            else:
                return int(self) % other
        else:
            raise ValueError(f"Modulo is unsupported between {self} and {other}")

    def __int__(self) -> int:
        return prod(prime ** factor for prime, factor in self.prime_factors.items())

    def __repr__(self) -> str:
        return str(int(self))

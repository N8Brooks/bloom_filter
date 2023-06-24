"""Bloom filter implementation"""

from __future__ import annotations

from itertools import chain
from math import log, log1p
from random import Random
from sys import maxsize
from typing import Generic, Iterable, Set, TypeVar

T = TypeVar("T")


class BloomFilter(Generic[T]):
    """Space efficient probabilistic estimation of a set"""

    def __init__(self, k: int, m: int):
        self._bits: Set[int] = set()
        self._k = k
        self._m = m

    @staticmethod
    def from_approximate_epsilon(n: int, epsilon: float) -> BloomFilter:
        """Computes the optimal length of a bit array for an approximate error rate"""
        m = m_with_approximate_epsilon(n, epsilon)
        k = optimal_k(m, n)
        return BloomFilter(k, m)

    @staticmethod
    def from_epsilon_upper_bound(n: int, k: int, epsilon: float) -> BloomFilter:
        """Computes the optimal length of a bit array for an error upper bound"""
        m = m_with_epsilon_upper_bound(n, k, epsilon)
        return BloomFilter(k, m)

    def __contains__(self, element: T) -> bool:
        """Test `element` for inclusion in the bloom filter"""
        return all(i in self._bits for i in self._hash_k(element))

    def add(self, element: T):
        """Inserts the `element` into the bloom filter"""
        self._bits.update(self._hash_k(element))

    def update(self, elements: Iterable[T]):
        """Update this `BloomFilter` with each element of `elements`"""
        iterable = chain.from_iterable(map(self._hash_k, elements))
        self._bits.update(iterable)

    def _hash_k(self, element: T) -> Iterable[int]:
        seed = hash(element)
        random = Random(seed)
        for _ in range(self._k):
            yield random.randrange(self._m)

    def __len__(self) -> int:
        """Approximates the length of the bloom filter"""
        if len(self._bits) == self._m:
            return maxsize
        return round(-(self._m / self._k) * log(1 - len(self._bits) / self._m))


def optimal_k(m: int, n: int) -> int:
    """Computes k that minimizes the false positive probability"""
    return max(1, round(m / n * log(2)))


def m_with_approximate_epsilon(n: int, epsilon: float) -> int:
    """Computes the optimal length of a bit array for an approximate error rate"""
    numerator = n * log(epsilon)
    denominator = log(2) ** 2
    return max(1, round(-(numerator / denominator)))


def m_with_epsilon_upper_bound(n: int, k: int, epsilon: float) -> int:
    """Computes the optimal length of a bit array for an error upper bound"""
    minuend = log1p(-(epsilon ** (1 / k)))
    subtrahend = k * (n + 0.5)
    return max(1, round((minuend - subtrahend) / minuend))

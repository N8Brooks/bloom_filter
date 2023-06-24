"""Bloom filter implementation"""

from __future__ import annotations

from itertools import chain
from math import log
from random import Random
from sys import maxsize
from typing import Generic, Iterable, Set, TypeVar

T = TypeVar("T")


class BloomFilter(Generic[T]):
    """Space efficient probabilistic estimation of a set"""

    def __init__(self, num_hash_functions: int, len_bit_set: int):
        self._bits: Set[int] = set()
        self._k = num_hash_functions
        self._m = len_bit_set

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

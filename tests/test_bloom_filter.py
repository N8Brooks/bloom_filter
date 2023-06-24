"""Tests for `BloomFilter`"""

from random import shuffle
from sys import maxsize

from bloom_filter.bloom_filter import (
    BloomFilter,
    m_with_approximate_epsilon,
    m_with_epsilon_upper_bound,
    optimal_k,
)

# pylint: disable=invalid-name,missing-function-docstring,protected-access


def test_not_contains():
    bloom_filter = BloomFilter(10, 100)
    for i in range(10):
        assert i not in bloom_filter


def test_contains():
    elements = set()
    bloom_filter = BloomFilter(10, 100)
    pool = list(range(10)) * 2
    shuffle(pool)
    for element in pool:
        a = element in elements
        b = element in bloom_filter
        falseNegative = a and not b
        assert not falseNegative
        elements.add(element)
        bloom_filter.add(element)


def test_update():
    bloom_filter_1 = BloomFilter(10, 100)
    bloom_filter_2 = BloomFilter(10, 100)
    n = 10
    for i in range(n):
        bloom_filter_1.add(i)
    bloom_filter_2.update(range(n))
    assert bloom_filter_1._bits == bloom_filter_2._bits


def test_len():
    bloom_filter = BloomFilter(10, 10**9)
    for i in range(10):
        bloom_filter.add(i)
    assert len(bloom_filter) == 10


def test_max_len():
    m = 10
    bloom_filter = BloomFilter(100, m)
    bloom_filter._bits = set(range(m))
    assert len(bloom_filter) == maxsize


def test_optimal_k():
    assert optimal_k(100, 1) == 69


def test_m_with_approximate_epsilon():
    assert m_with_approximate_epsilon(1e6, 1e-2) == 9_585_058


def test_m_with_epsilon_upper_bound():
    assert m_with_epsilon_upper_bound(1e6, 10, 1e-2) == 10_031_676

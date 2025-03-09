import numpy as np
import pytest
from max_density_segment_bruteforce import find_max_density_segment_bruteforce
from max_density_segment_optimal import find_max_density_segment_optimal

from max_density_segment import find_max_density_segment


def test_single():
    a = [5]
    w = [1]
    w_min = 1
    i, j, d = find_max_density_segment(a, w, w_min)
    assert (i, j, d) == (0, 0, 5)


def test_example():
    a = np.array([2, 7, -1, 9, 0], dtype=np.float32)
    w = np.array([1, 1, 1, 1, 1], dtype=np.float32)
    i, j, d = find_max_density_segment(a, w, w_min=2)
    assert (i, j, d) == (1, 3, pytest.approx(5))


def test_non_uniform_weights():
    a = [4, 5, 1, 3]
    w = [2, 1, 1, 2]
    w_min = 3
    i, j, d = find_max_density_segment(a, w, w_min)
    assert (i, j, d) == (0, 1, pytest.approx((4 + 5) / 3))


def test_various():
    tests_list = [
        {'a': [1, 2, 3, 4, 5], 'w_min': 1, 'expected': (4, 4, 5)},
        {'a': [1, 2, 3, 4, 5], 'w_min': 2, 'expected': (3, 4, 4.5)},
        {'a': [5, 4, 3, 2, 1], 'w_min': 1, 'expected': (0, 0, 5)},
        {'a': [5, 4, 3, 2, 1], 'w_min': 2, 'expected': (0, 1, 4.5)},
        {'a': [1, 1, 1, 1, 1], 'w_min': 1, 'expected': (0, 0, 1)},
        {'a': [1, 1, 1, 1, 1], 'w_min': 2, 'expected': (0, 1, 1)},
        {'a': [1, 1, 1, 1, 1], 'w_min': 5, 'expected': (0, 4, 1)},
    ]
    for test in tests_list:
        a, w_min, expected = test['a'], test['w_min'], test['expected']
        i, j, d = find_max_density_segment(a, np.ones_like(a), w_min)
        assert (i, j, d) == expected


def test_random_brute_force():
    rng = np.random.default_rng(0)
    n = 200
    a = rng.standard_normal(n).astype(np.float32)
    w = np.ones(n).astype(np.float32)
    w_min = n // 5
    (i1, j1, d1) = find_max_density_segment(a, w, w_min)
    (i2, j2, d2) = find_max_density_segment_bruteforce(a, w, w_min)
    assert (i1, j1, d1) == (i2, j2, pytest.approx(d2))


def test_random_large():
    rng = np.random.default_rng(0)
    for n in [1, 10, 100, 1000, 10000]:
        for w_ratio in [0, 0.1, 0.5, 0.9, 1]:
            a = rng.standard_normal(n).astype(np.float32)
            w = rng.uniform(0.5, 2, n).astype(np.float32)
            w_sum = np.sum(w)
            w_min = max(int(w_sum * w_ratio), w.min())
            (i1, j1, d1) = find_max_density_segment(a, w, w_min)
            (i2, j2, d2) = find_max_density_segment_optimal(a, w, w_min)
            assert (i1, j1, d1) == (i2, j2, pytest.approx(d1))


def test_empty_array():
    with pytest.raises(ValueError):
        find_max_density_segment([], [], 1)


def test_incorrect_w():
    with pytest.raises(ValueError):
        find_max_density_segment([1, 2, 3], [1, -1, 1], 1)


def test_incorrect_w_min():
    with pytest.raises(ValueError):
        find_max_density_segment([1, 2, 3], [1, 1, 1], 4)

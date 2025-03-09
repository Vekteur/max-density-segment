import numpy as np
import pytest
from max_density_segment_optimal import find_max_density_segment_optimal

from max_density_segment import find_max_density_segment


def benchmark_args(n, dtype):
    rng = np.random.default_rng(0)
    a = rng.standard_normal(n).astype(dtype)
    w = np.ones(n).astype(dtype)
    w_min = n // 5
    return a, w, w_min

def benchmark_args_small(dtype):
    return benchmark_args(10_000, dtype)

@pytest.mark.slow
def test_cpp_float_small(benchmark):
    benchmark(find_max_density_segment, *benchmark_args_small(np.float32))

@pytest.mark.slow
def test_cpp_double_small(benchmark):
    benchmark(find_max_density_segment, *benchmark_args_small(np.float64))

@pytest.mark.slow
def test_python_small(benchmark):
    benchmark(find_max_density_segment_optimal, *benchmark_args_small(np.float32))


def benchmark_args_large(dtype):
    return benchmark_args(10_000_000, dtype)

@pytest.mark.slow
def test_cpp_float_large(benchmark):
    benchmark(find_max_density_segment, *benchmark_args_large(np.float32))

@pytest.mark.slow
def test_cpp_double_large(benchmark):
    benchmark(find_max_density_segment, *benchmark_args_large(np.float64))

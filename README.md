# Maximum Density Segment

This Python package provides an algorithm to solve the Maximum Density Segment problem in O(n) based on the [following paper](https://arxiv.org/abs/cs/0311020):
> Chung, K. M., & Lu, H. I. (2005). An optimal algorithm for the maximum-density segment problem. SIAM Journal on Computing, 34(2), 373-387.

The algorithm is implemented in C++ for efficiency.

Let $S$ be a sequence of $n$ pairs $\bigl(a_i, w_i\bigr)$ where $w_i > 0$ for $i = 1, 2, \dots, n$. Define the width of any consecutive subsequence $S(i,j)$ (where $1 \le i \le j \le n$) as

$$
w(i,j) = w_i + \cdots + w_j
$$

and the corresponding density as

$$
d(i,j) = \frac{a_i + \cdots + a_j}{w(i,j)}.
$$

Given a minimum width $w_\text{min}$, the **Maximum Density Segment** problem is to find a segment $S(i,j)$ such that $w(i,j) \geq w_\text{min}$ and $d(i,j)$ is maximized.

Note that the algorithm can be extended to support an upper bound for $w(i,j)$ or to support sparse arrays.

## Installation

To install the package, use
```sh
pip install max-density-segment
```

To install the package in development mode, use
```sh
pip install -e .
```

## Usage

The function `max_density_segment` returns the indices of the maximum density segment and its density. 

```python
from max_density_segment import find_max_density_segment
import numpy as np

a = np.array([2, 7, -1, 9, 0], dtype=np.float32)
w = np.ones(5, dtype=np.float32)
i, j, density = find_max_density_segment(a, w, w_min=2)
assert (i, j) == (1, 3)
assert density == 5
```

## Testing

To run the tests, use
```sh
pytest
```

The tests include benchmarks, showing a 200x speedup for the C++ implementation compared to a pure Python implementation.

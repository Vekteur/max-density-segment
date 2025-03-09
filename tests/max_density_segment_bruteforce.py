"""
Maximum density segment problem solved by brute force in O(n^2).

The algorithm uses 1-based indexing.
"""

class MaxDensitySegmentBruteForce:
    def __init__(self, a, w, w_min):
        assert len(a) == len(w), "Arrays 'a' and 'w' must have the same length."
        assert w_min <= sum(w), "w_min must be less than or equal to the total width."
        self.n = len(a)
        self.w_min = w_min
        self.prefixA, self.prefixW, self.j0 = self.precompute(a, w)

    def precompute(self, a, w):
        n = self.n
        prefixA = [0] * (n + 1)
        for i in range(1, n + 1):
            prefixA[i] = prefixA[i - 1] + a[i - 1]

        prefixW = [0] * (n + 1)
        for i in range(1, n + 1):
            prefixW[i] = prefixW[i - 1] + w[i - 1]
        
        j0 = 1
        for j in range(n + 1):
            if prefixW[j] >= self.w_min:
                j0 = j
                break
        else:
            raise ValueError("No j found with w(1, j) >= w_min")

        return prefixA, prefixW, j0
    
    def width(self, i, j):
        return self.prefixW[j] - self.prefixW[i - 1]
    
    def density(self, i, j):
        assert 0 <= i <= j <= self.n
        return (self.prefixA[j] - self.prefixA[i - 1]) / self.width(i, j)

    def find_all_best(self):
        for j in range(self.j0, self.n + 1):
            best_density = -float('inf')
            best_indices = None
            for i in range(1, j + 1):
                if self.width(i, j) < self.w_min:
                    break
                density = self.density(i, j)
                if density > best_density:
                    best_density = density
                    best_indices = (i, j)
            assert best_indices is not None
            yield best_indices

    def compute(self):
        best_indices = None
        best_density = -float('inf')
        for ij, j in self.find_all_best():
            density = self.density(ij, j)
            if density > best_density:
                best_density = density
                best_indices = ij, j
        return *best_indices, best_density


"""
Convenience function to run the algorithm with 0-based indexing.
"""
def find_max_density_segment_bruteforce(a, w, w_min):
    i, j, density = MaxDensitySegmentBruteForce(a, w, w_min).compute()
    return i - 1, j - 1, density

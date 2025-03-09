class MaxDensitySegmentOptimal:
    def __init__(self, a, w, w_min):
        assert len(a) == len(w), "Arrays 'a' and 'w' must have the same length."
        assert w_min <= sum(w), "w_min must be less than or equal to the total width."
        self.precompute(a, w, w_min)

    def precompute(self, a, w, w_min):
        n = len(a)
        self.prefixA = [0] * (n + 1)
        for i in range(1, n + 1):
            self.prefixA[i] = self.prefixA[i - 1] + a[i - 1]

        self.prefixW = [0] * (n + 1)
        for i in range(1, n + 1):
            self.prefixW[i] = self.prefixW[i - 1] + w[i - 1]
        
        self.j0 = 0
        for j in range(n + 1):
            if self.prefixW[j] >= w_min:
                self.j0 = j
                break

        self.r = [0] * (n + 1)
        i = 1
        for j in range(self.j0, n + 1):
            while i < j and self.width(i + 1, j) >= w_min:
                i += 1
            self.r[j] = i
    
    def width(self, i, j):
        assert 1 <= i <= j < len(self.prefixA)
        return self.prefixW[j] - self.prefixW[i - 1]

    def density(self, i, j):
        return (self.prefixA[j] - self.prefixA[i - 1]) / self.width(i, j)

    def update(self, j):
        """
        Runs the 'UPDATE(j)' procedure from Figure 5.
        """
        start_r, end_r = self.r[j - 1] + 1, self.r[j]

        # Add each new candidate r
        for r in range(start_r, end_r + 1):
            # Pop from the right if it doesn't improve density
            while self.p < self.q and self.density(
                self.Phi[self.q - 1], self.Phi[self.q] - 1
            ) >= self.density(self.Phi[self.q - 1], r - 1):
                self.q -= 1

            self.q += 1
            self.Phi[self.q] = r

    def find_best(self, j):
        """
        Runs the 'LBEST(j)' from Figure 5.
        Returns the chosen starting index i_j.
        """
        # Move p forward if that helps improve density
        while self.p < self.q and self.density(
            self.Phi[self.p], self.Phi[self.p + 1] - 1
        ) <= self.density(self.Phi[self.p], j):
            self.p += 1

        return self.Phi[self.p]

    def find_all_best(self):
        """
        Runs the 'LMAIN' logic from Figure 5 for the w_max-infinite case.
        """
        self.p = 1  # Index of leftmost candidate
        self.q = 0  # Index of rightmost candidate
        self.Phi = [0] * len(self.prefixA)  # Candidate starting positions
        self.Phi[1] = 1 # Initialize with the first candidate

        for j in range(self.j0, len(self.r)):
            self.update(j)
            i_j = self.find_best(j)
            yield (i_j, j)

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
def find_max_density_segment_optimal(a, w, w_min):
    i, j, density = MaxDensitySegmentOptimal(a, w, w_min).compute()
    return i - 1, j - 1, density

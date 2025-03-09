#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <cassert>
#include <limits>
#include <stdexcept>
#include <vector>

namespace py = pybind11;


// Max density segment algorithm solved in O(n) as defined in:
// Chung, K. M., & Lu, H. I. (2005). An optimal algorithm for the maximum-density segment problem. 
// SIAM Journal on Computing, 34(2), 373-387.

// The key is that for any real numbers a1, a2 and w1, w2 > 0:
// a1 / w1 <= a2 / w2
// <=>
// a1 / w1 <= (a1 + a2) / (w1 + w2)

// The algorithm uses 1-based indexing.
template <typename T>
class MaxDensitySegment {
   public:
    MaxDensitySegment(const T* a, const T* w, int length, T w_min)
        : n_(length) {
        prefixA_.resize(n_ + 1, T(0));
        prefixW_.resize(n_ + 1, T(0));

        // Compute prefix sums
        for (int i = 1; i <= n_; ++i) {
            prefixA_[i] = prefixA_[i - 1] + a[i - 1];
            prefixW_[i] = prefixW_[i - 1] + w[i - 1];
        }

        // Check w > 0
        for (int i = 0; i < n_; ++i) {
            if (w[i] <= 0) {
                throw std::invalid_argument("All w values must be positive.");
            }
        }
        // Check w_min <= total width
        T total_w = prefixW_[n_];
        if (w_min > total_w) {
            throw std::invalid_argument("w_min must be <= sum of w.");
        }

        // Find j0 such that prefixW_[j0] >= w_min
        j0_ = 0;
        for (int j = 0; j <= n_; ++j) {
            if (prefixW_[j] >= w_min) {
                j0_ = j;
                break;
            }
        }

        // Precompute r_[j]
        r_.resize(n_ + 1, 0);
        {
            int i = 1;
            for (int j = j0_; j <= n_; ++j) {
                while (i < j && width(i + 1, j) >= w_min) {
                    i++;
                }
                r_[j] = i;
            }
        }
    }

    // Find best overall
    std::tuple<int, int, T> compute_best() {
        auto candidates = find_all_best();
        T best_density = -std::numeric_limits<T>::infinity();
        std::pair<int, int> best_ij(0, 0);

        for (auto& ij : candidates) {
            int i = ij.first;
            int j = ij.second;
            T d = density(i, j);
            if (d > best_density) {
                best_density = d;
                best_ij = {i, j};
            }
        }
        return {best_ij.first, best_ij.second, best_density};
    }

   private:
    // Data
    int n_;
    int j0_;
    std::vector<T> prefixA_;
    std::vector<T> prefixW_;
    std::vector<int> r_;

    // For the "candidate" logic
    int p_ = 0;
    int q_ = 0;
    std::vector<int> Phi_;

    T width(int i, int j) const {
        return prefixW_[j] - prefixW_[i - 1];
    }

    T density(int i, int j) const {
        T num = prefixA_[j] - prefixA_[i - 1];
        T den = width(i, j);
        return num / den;
    }

    // Runs the 'UPDATE(j)' procedure from Figure 5.
    void update(int j) {
        // start_r = r_[j-1] + 1, end_r = r_[j]
        // watch out for j == 0 edge, but typically j loops from j0_..n_
        int start_r = (j == 0) ? 1 : (r_[j - 1] + 1);
        int end_r = r_[j];

        for (int candidate = start_r; candidate <= end_r; ++candidate) {
            while ((p_ < q_) &&
                   (density(Phi_[q_ - 1], Phi_[q_] - 1) >=
                    density(Phi_[q_ - 1], candidate - 1))) {
                q_--;
            }
            q_++;
            Phi_[q_] = candidate;
        }
    }

    // Runs the 'LBEST(j)' from Figure 5.
    int find_best(int j) {
        while ((p_ < q_) &&
               (density(Phi_[p_], Phi_[p_ + 1] - 1) <= density(Phi_[p_], j))) {
            p_++;
        }
        return Phi_[p_];
    }

    std::vector<std::pair<int, int>> find_all_best() {
        std::vector<std::pair<int, int>> results;
        p_ = 1;
        q_ = 0;
        Phi_.resize(n_ + 1, 0);
        Phi_[1] = 1;  // first candidate

        for (int j = j0_; j <= n_; ++j) {
            update(j);
            int i_j = find_best(j);
            results.emplace_back(i_j, j);
        }
        return results;
    }
};

// A templated wrapper with 0-based indexing
template <typename T>
py::tuple find_max_density_segment_template(py::array_t<T> a,
                                       py::array_t<T> w,
                                       T w_min) {
    auto bufA = a.request();
    auto bufW = w.request();
    if (bufA.size != bufW.size) {
        throw std::runtime_error("Arrays 'a' and 'w' must have the same length.");
    }
    if (bufA.ndim != 1 || bufW.ndim != 1) {
        throw std::runtime_error("Input arrays must be 1D.");
    }

    int n = static_cast<int>(bufA.size);
    auto* ptrA = static_cast<const T*>(bufA.ptr);
    auto* ptrW = static_cast<const T*>(bufW.ptr);

    MaxDensitySegment<T> mds(ptrA, ptrW, n, w_min);
    int left, right;
    T density;
    std::tie(left, right, density) = mds.compute_best();
    // Convert to 0-based indexing
    return py::make_tuple(left - 1, right - 1, density);
}

// A single function that decides at runtime whether to use float or double
py::tuple find_max_density_segment_dispatch(py::object a_obj,
                                       py::object w_obj,
                                       py::object w_min_obj) {
    py::array a = py::array::ensure(a_obj);
    py::array w = py::array::ensure(w_obj);
    // Check if either array is float64:
    bool a_is_double = (a.dtype().kind() == 'f' && a.dtype().itemsize() == 8);
    bool w_is_double = (w.dtype().kind() == 'f' && w.dtype().itemsize() == 8);
    double w_min_as_double = w_min_obj.cast<double>();

    // If either array is double, pick double
    if (a_is_double || w_is_double) {
        // Double version
        return find_max_density_segment_template<double>(
            a.cast<py::array_t<double>>(),
            w.cast<py::array_t<double>>(),
            static_cast<double>(w_min_as_double));
    } else {
        // Float version
        return find_max_density_segment_template<float>(
            a.cast<py::array_t<float>>(),
            w.cast<py::array_t<float>>(),
            static_cast<float>(w_min_as_double));
    }
}

PYBIND11_MODULE(_core, m) {
    m.doc() = "Maximum density segment algorithm";

    m.def("find_max_density_segment",
          &find_max_density_segment_dispatch,
          py::arg("a"), py::arg("w"), py::arg("w_min"),
          R"pbdoc(
            Find the segment with the maximum density.
            If at least one input array is float64, the algorithm will use double precision.
            Otherwise, it will use single precision.
          )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
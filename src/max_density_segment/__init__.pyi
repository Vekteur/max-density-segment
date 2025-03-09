# Add the doc of max_density_segment
def find_max_density_segment(a: list[float], w: list[float], w_min: float) -> tuple[int, int, float]:
    """
    Find the segment of a with the maximum density.

    Parameters
    ----------
    a : List[float]
        The input array.
    w : List[float]
        The weights of each element in a.
    w_min : float
        The minimum weight of the segment.

    Returns
    -------
    Tuple[int, int, float]
        The starting index, ending index, and the density of the segment.
    """

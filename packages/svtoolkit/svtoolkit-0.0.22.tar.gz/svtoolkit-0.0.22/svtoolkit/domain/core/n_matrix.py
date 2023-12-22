import numpy as np
import numba as nb


@nb.jit(nopython=True)
def n_matrix(points):
    """
    This function computes the N matrix
    for the given points. By default, the
    N matrix is computed using a radial
    basis function with a degree of 3.

    Parameters
    ----------
        points : ndarray
            The points defining the D-1 manifold embedded
            in D-dimensional space.
    Returns
    -------
        n_ : ndarray
            The N matrix. This matrix is a Nx4 matrix.
            Where N is the number of points defining
            the D-1 manifold embedded in D-dimensional
            space.
    """
    n = points.shape[0]
    d = points.shape[1]
    n_ = np.zeros(((d + 1) * n, (d + 1)))
    for i in range(n):
        for j in range(d):
            n_[i, j] = points[i, j]
        n_[i, -1] = 1
    for i in range(n):
        n_[n + i * d:n + i * d + d, :d] = np.eye(d)
    return n_

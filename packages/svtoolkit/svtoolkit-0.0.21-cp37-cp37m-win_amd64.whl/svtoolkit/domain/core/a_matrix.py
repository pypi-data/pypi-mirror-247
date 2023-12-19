import numpy as np
from .m_matrix import m_matrix
from .n_matrix import n_matrix


def a_matrix(points, rbf_degree=3):
    """
    Build the full interpolation matrix
    for the points defining the domain
    of interest. This is accomplished
    by first constructing the sub-matrices
    M and N.

    Parameters
    ----------
         points : ndarray
            The points defining the D-1 manifold
            embedded in D-dimensional space.
        rbf_degree : float  (default=3)
            The degree of the Duchon interpolant function.
            Default is 3.
    Returns
    -------
        a_ : ndarray
            The full interpolation matrix for the
            points defining the D-1 manifold
            embedded in D-dimensional space.
    """
    n = points.shape[0]
    d = points.shape[1]
    m_ = m_matrix(points, rbf_degree=rbf_degree)
    n_ = n_matrix(points)
    a_ = np.zeros(((n + 1) * (d + 1), (n + 1) * (d + 1)))
    a_[:n * (d + 1), :n * (d + 1)] = m_
    a_[:n * (d + 1), n * (d + 1):] = n_
    a_[n * (d + 1):, :n * (d + 1)] = n_.T
    return a_

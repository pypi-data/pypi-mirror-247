import numpy as np
import numba as nb
from scipy.spatial.distance import cdist


def m00(points, rbf_degree=3):
    """
    This function computes the M00
    sub-matrix of the M matrix. By
    default, the M00 sub-matrix is
    computed using a radial basis
    function with a degree of 3.

    Parameters
    ----------
        points : ndarray
            The points defining the D-1 manifold embedded
            in D-dimensional space.
        rbf_degree : float  (default=3)
            The degree of the radial basis function (rbf).
            Default is 3.
    Returns
    -------
        m00_ : ndarray
            The M00 sub-matrix of the M matrix. This
            sub-matrix is an NxN matrix. Where N is
            the number of points defining the D-1
            manifold embedded in D-dimensional space.
    """
    return cdist(points, points) ** rbf_degree


@nb.jit(nopython=True)
def m01(points, rbf_degree=3):
    """
    This function computes the M01
    sub-matrix of the M matrix. By
    default, the M01 sub-matrix is
    computed using a radial basis
    function with a degree of 3.

    Parameters
    ----------
        points : ndarray
            The points defining the D-1 manifold embedded
            in D-dimensional space.
        rbf_degree : float  (default=3)
            The degree of the radial basis function (rbf).
            Default is 3.
    Returns
    -------
        m01_ : ndarray
            The M01 sub-matrix of the M matrix. This
            sub-matrix is an Nx3N matrix. Where N is
            the number of points defining the D-1
            manifold embedded in D-dimensional space.
    """
    n = points.shape[0]
    d = points.shape[1]
    m01_ = np.zeros((n, n * d))
    for i in range(n):
        for j in range(n):
            diff = points[i, :] - points[j, :]
            diff_sum = np.sum(diff ** 2)
            if diff_sum == 0 and (rbf_degree/2 - 1) < 0:
                norm1 = np.inf
            else:
                norm1 = diff_sum**(rbf_degree / 2 - 1)
            for k in range(d):
                if i == j:
                    m01_[i, j * d + k] = 0
                else:
                    m01_[i, j * d + k] = -rbf_degree * (points[i, k] - points[j, k]) * norm1
    return m01_


@nb.jit(nopython=True)
def m11(points, rbf_degree=3):
    """
    This function computes the M11
    sub-matrix of the M matrix. By
    default, the M11 sub-matrix is
    computed using a radial basis
    function with a degree of 3.

    Parameters
    ----------
        points : ndarray
            The points defining the D-1 manifold embedded
            in D-dimensional space.
        rbf_degree : float  (default=3)
            The degree of the radial basis function (rbf).
            Default is 3.
    Returns
    -------
        m11_ : ndarray
            The M11 sub-matrix of the M matrix. This
            sub-matrix is an D*NxD*N matrix. Where N is
            the number of points defining the D-1
            manifold embedded in D-dimensional space.
    """
    n = points.shape[0]
    d = points.shape[1]
    m11_ = np.zeros((n * d, n * d))
    for i in range(n):
        for j in range(i, n):
            diff = points[i, :] - points[j, :]
            diff_sum = np.sum(diff ** 2)
            if i == j:
                if (rbf_degree / 2 - 1) < 0:
                    norm1 = np.inf
                else:
                    norm1 = diff_sum ** (rbf_degree / 2 - 1)
                if (rbf_degree / 2 - 2) < 0:
                    norm2 = np.inf
                else:
                    norm2 = diff_sum ** (rbf_degree / 2 - 2)
            else:
                if diff_sum == 0 and (rbf_degree / 2 - 1) < 0:
                    norm1 = np.inf
                else:
                    norm1 = diff_sum ** (rbf_degree / 2 - 1)
                if diff_sum == 0 and (rbf_degree / 2 - 2) < 0:
                    norm2 = np.inf
                else:
                    norm2 = diff_sum ** (rbf_degree / 2 - 2)
            for k in range(d):
                for l in range(d):
                    if i == j:
                        m11_[j * d + l, i * d + k] = 0
                    elif k == l:
                        m11_[j * d + l, i * d + k] = -2 * (rbf_degree / 2 - 1) * rbf_degree * diff[k] ** 2 * norm2 - \
                                                     rbf_degree * norm1
                    else:
                        m11_[j * d + l, i * d + k] = -2 * (rbf_degree / 2 - 1) * rbf_degree * diff[k] * diff[l] * norm2
    return m11_



def m_matrix(points, rbf_degree=3):
    """
    This function constructs the M
    matrix for the D-1 manifold
    embedded in D-dimensional space.
    By default, the M matrix is
    computed using a radial basis
    function with a degree of 3.

    Parameters
    ----------
        points : ndarray
            The points defining the D-1 manifold embedded
            in D-dimensional space.
        rbf_degree : float  (default=3)
            The degree of the radial basis function (rbf).
            Default is 3.
    Returns
    -------
        m_ : ndarray
            The M matrix. This matrix is an (3N+1)x(3N+1)
            matrix. Where N is the number of points
            defining the D-1 manifold embedded in
            D-dimensional space.
    """
    n = points.shape[0]
    d = points.shape[1]
    m_ = np.zeros((n * (d + 1), n * (d + 1)))
    m00_ = m00(points, rbf_degree)
    m01_ = m01(points, rbf_degree)
    m11_ = m11(points, rbf_degree)
    m_[:n, :n] = m00_
    m_[:n, n:] = m01_
    m_[n:, :n] = m01_.T
    m_[n:, n:] = m11_
    m_[n:, n:] += m11_.T
    return m_

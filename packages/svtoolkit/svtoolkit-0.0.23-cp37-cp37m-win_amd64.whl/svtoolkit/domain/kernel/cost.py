import numpy as np
#import numba as nb
from .coordinate_system import sph2cart


#@nb.jit(nopython=True, fastmath=True)
def cost(x, h_, n, d):
    """
    This function is used to calculate the cost function of the optimization problem
    posed for the energy minimization of the implicit surface.

    Parameters
    ----------
        x : numpy.ndarray
            The vector of parameters to be optimized. These are generally in the form
            of spherical coordinates of normalized magnitude. Thus, the first radial
            coordinate is not included and assumed to be 1.
        h_ : numpy.ndarray
            The h matrix is a D*N x D*N matrix representing the linear system of
            equations forming the energy minimization problem.
        n : int
            The number of points defining the D-1 manifold.
        d : int
            The dimension of the domain in which the D-1 manifold is embedded.
    Returns
    -------
        cost : float
            The cost function of the optimization problem.
    """
    g = np.ones((n, d))
    g[:, 1:] = x.reshape(n, d - 1)
    a = sph2cart(g)
    a = a.reshape((n * d, 1))
    c = a.T @ h_ @ a
    c = c.flatten()
    return c

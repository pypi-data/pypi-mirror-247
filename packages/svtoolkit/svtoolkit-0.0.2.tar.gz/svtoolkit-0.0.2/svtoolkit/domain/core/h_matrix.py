import numpy as np



def h_matrix(a_, n, d, lam):
    """
    This function computes the h matrix
    which is Duchon's matrix. Which form
    the linear system of equations to
    minimize for the variational
    problem. Of note, h_ should be
    positive semi-definite.

    Parameters
    ----------
        a_ : ndarray
            The A matrix is the (d+1)N x (d+1)N
            full interpolation matrix for the
            points defining the D-1 manifold.
        n : int
            The number of points defining the
            D-1 manifold.
        d : int
            The dimension of the domain in which
            the D-1 manifold is embedded.
        lam : float
            The regularization parameter or thin
            -plate relaxation parameter. This
            determines how well the D-1 manifold
            will fit through its set of control
            points.
    Returns
    -------
        h_ : ndarray
            The h matrix is a D*N x D*N matrix
            representing the linear system of
            equations forming the bending energy
            minimization problem.
    """
    a_inv = np.linalg.inv(a_)
    j_ = a_inv[:n * (d + 1), :n * (d + 1)]
    j00_ = j_[:n, :n]
    j01_ = j_[:n, n:].copy()
    j11_ = j_[n:, n:]
    if lam > 0:
        inv = np.linalg.inv(np.eye(j00_.shape[0]) + lam * j00_)
        h_ = j11_ - (lam * j01_.T) @ inv @ j01_
    else:
        h_ = j11_
    return h_, j00_, j01_, j11_, a_inv

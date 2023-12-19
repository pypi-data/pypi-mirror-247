import numpy as np
import mpmath as mp

# @nb.jit(nopython=True)
def cart2sph(cart):
    """
    This function converts cartesian coordinates to spherical coordinates
    for any given vector of points in a d-dimensional space.

    Parameters
    ----------
        cart : ndarray
            The points within the d-dimensional space.
    Return
    ------
        sph : ndarray
            The spherical coordinates for the given points.
    """
    n = cart.shape[0]
    d = cart.shape[1]
    sph = np.zeros((n, d))
    for i in range(n):
        sph[i, 0] = np.linalg.norm(cart[i, :])
        for j in range(d - 2):
            sph[i, j + 1] = np.arccos(cart[i, j] / np.linalg.norm(cart[i, j:]))
        if np.linalg.norm(cart[i, -2:]) == 0:
            sph[i, -1] = 0
        elif cart[i, -1] >= 0:
            sph[i, -1] = np.arccos(cart[i, -2] / np.linalg.norm(cart[i, -2:]))
        else:
            sph[i, -1] = 2 * np.pi - np.arccos(cart[i, -2] / np.linalg.norm(cart[i, -2:]))
    return sph


# @nb.jit(nopython=True)
def sph2cart(sph):
    """
    This function converts spherical coordinates to cartesian coordinates
    for any given spherical vector of points in a d-dimensional space.
    Parameters
    ----------
        sph : ndarray
            The spherical coordinates for the given points.
    Return
    ------
        cart : ndarray
            The cartesian coordinates for the given points.
    """
    n = sph.shape[0]
    d = sph.shape[1]
    cart = np.zeros((n, d))
    for i in range(n):
        if np.isclose(sph[i, 1], np.pi/2) or np.isclose(sph[i, 1], -np.pi/2) or np.isclose(sph[i, 1], (3/2)*np.pi):
            cart[i, 0] = 0
        else:
            cart[i, 0] = sph[i, 0] * np.cos(sph[i, 1])
        for j in range(max(d - 2, 0)):
            if np.any(np.isclose(sph[i, 1:j + 2], np.pi)) or np.any(np.isclose(sph[i, 1:j + 2], -np.pi)) or np.any(np.isclose(sph[i, 1:j + 2], 0)):
                cart[i, j + 1] = 0
            elif np.isclose(sph[i, j + 2], np.pi/2) or np.isclose(sph[i, j + 2], -np.pi/2) or np.isclose(sph[i, j + 2], (3/2)*np.pi):
                cart[i, j + 1] = 0
            else:
                p_ones = np.isclose(sph[i, 1:j+2], np.pi/2)
                n_ones = np.logical_or(np.isclose(sph[i, 1:j+2], -np.pi/2), np.isclose(sph[i, 1:j+2], (3/2)*np.pi))
                sins = np.sin(sph[i, 1:j+2])
                sins[p_ones] = 1
                sins[n_ones] = -1
                if np.isclose(sph[i, j + 2], 0):
                    cos = 1
                elif np.isclose(sph[i, j + 2], np.pi) or np.isclose(sph[i, j + 2], -np.pi):
                    cos = -1
                else:
                    cos = np.cos(sph[i, j + 2])
                cart[i, j + 1] = sph[i, 0] * np.prod(sins) * cos
        if np.any(np.isclose(sph[i, 1:], np.pi)) or np.any(np.isclose(sph[i, 1:], -np.pi)):
            cart[i, -1] = 0
        else:
            p_ones = np.isclose(sph[i, 1:], np.pi/2)
            n_ones = np.isclose(sph[i, 1:], -np.pi/2)
            sins = np.sin(sph[i, 1:])
            sins[p_ones] = 1
            sins[n_ones] = -1
            cart[i, -1] = sph[i, 0] * np.prod(sins)
    return cart

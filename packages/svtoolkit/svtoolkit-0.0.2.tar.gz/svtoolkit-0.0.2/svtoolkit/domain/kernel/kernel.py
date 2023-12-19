import numpy as np
from ..core.a_matrix import a_matrix
from ..core.h_matrix import h_matrix
from .cost import cost
from .coordinate_system import cart2sph


class Kernel:
    """
    This class defines the minimization kernel for
    the implicit domain object. If a kernel contains
    all the points in the domain, then the kernel
    becomes the classic implementation of the
    variational implicit point set surface As
    described in [Huang et al. 2019. ACM Transactions
    on Graphics (TOG) 38, 4 (2019), 1-14.].

    This class object is used to set up the minimization
    problem for the implicit domain object.
    """

    def __init__(self, points, rbf_degree=3, lam=0):
        self.n = points.shape[0]
        self.d = points.shape[1]
        self.a_ = a_matrix(points, rbf_degree)
        self.h_, self.j00_, self.j01_, self.j11_, self.a_inv = h_matrix(self.a_, self.n, self.d, lam)
        self.__cost__ = lambda x: cost(x, self.h_, self.n, self.d)
        self.__costs__ = None
        self.__grad__ = None
        self.__hess__ = None
        self.x0 = None
        self.lam = lam
        self.h0 = None

    def set_initial_values(self, *args, **kwargs):
        """
        Set the initial values for the variational minimization.

        Parameters
        ----------
            x0: (optional) ndarray
                The initial values for the variational minimization.
                These values must be given in reference to the
                cartesian coordinate system. The shape of the initial
                values array must be (n,d) where n is the number of
                points defining the manifold patch and d is the
                dimension of the space in which the manifold is
                embedded.
            lambda_parameters: (optional) list -> shape: (3,)
                The parameters for the variational minimization.
                Which linearly vary the thin plate relaxation parameter
                (lambda). The first parameter is the minimum value,
                the second parameter is the maximum value, and the
                third parameter is the number of values to generate
                between the minimum and maximum values.
        Return
        ------
            None
        """
        if len(args) > 0:
            normals = args[0]
            normals = normals / np.linalg.norm(normals, axis=1).reshape(-1, 1)
            spherical_coordinates = cart2sph(normals)
            x0 = spherical_coordinates[:, 1:]
            h0 = [self.h_]
            x0 = [x0.flatten()]
            funcs = [lambda x: cost(x, self.h_, self.n, self.d)]
        else:
            lam_params = kwargs.get("lambda_parameters", [0.001, 1, 5])
            lams = np.linspace(self.lam + lam_params[0], self.lam + lam_params[1], lam_params[2])
            h0 = []
            x0 = []
            funcs = []
            for lam in lams:
                h_, _, _, _, _ = h_matrix(self.a_, self.n, self.d, lam)
                h0.append(h_)
                eigen_values, eigen_vectors = np.linalg.eig(h_)
                eh = np.argmin(eigen_values)
                x0_init = eigen_vectors[:, eh].real
                x0_init = x0_init.reshape(self.n, self.d)
                x0_init = x0_init / np.linalg.norm(x0_init, axis=1).reshape(-1, 1)
                x0_init = cart2sph(x0_init)
                x0_init = x0_init[:, 1:]
                x0_init = x0_init.flatten()
                x0.append(x0_init)
                func = lambda x: cost(x, h_, self.n, self.d)
                funcs.append(func)
        self.x0 = x0
        self.h0 = h0
        self.__costs__ = funcs
        return None

    def get_bounds(self):
        bounds = []
        lb = []
        ub = []
        for i in range(self.n):
            for j in range(self.d - 1):
                if j < self.d - 2:
                    lb.append(0)
                    ub.append(np.pi)
                else:
                    lb.append(0)
                    ub.append(2 * np.pi)
        bounds.append(lb)
        bounds.append(ub)
        return tuple(bounds)

    def eval(self, x):
        return self.__cost__(x)

    def gradient(self, x):
        return self.__grad__(x)

    def hessian(self, x):
        return self.__hess__(x)

import numpy as np
from .kernel.kernel import Kernel
from .solver.solver import Solver


class Patch:
    """
    Patch class decomposes a domain into a set of interpolation sub-problems which
    can be solved independently and then blended together to form the final
    domain interpolation function.
    """
    def __init__(self, lam=0):
        self.points = None
        self.normals = None
        self.kernel = None
        self.solver = None
        self.constants = None
        self.rbf_degree = 3
        self.lam = lam

    def set_data(self, *args):
        """
        Set the data for the domain.
        """
        if len(args) > 1:
            self.points = args[0]
            self.normals = args[1]
            self.kernel = Kernel(self.points, lam=self.lam)
            self.kernel.set_initial_values(self.normals)
        elif len(args) > 0:
            self.points = args[0]
            self.kernel = Kernel(self.points, lam=self.lam)
            self.kernel.set_initial_values()
        else:
            print("Error: No data provided.")
        return None

    def solve(self, method="L-BFGS-B", precision=9):
        """
        Solve the interpolation problem for the patch object

        Parameters:
        -----------
        method : str
            The method to use for the solver. Default is L-BFGS-B.
            (Limited-memory Broyden-Fletcher-Goldfarb-Shanno Bounded)

        precision : int
            The number of decimal places to round the constants to.
            Default is 9.

        Returns:
        --------
        None
        """
        self.solver = Solver(self.kernel)
        self.solver.set_solver(method=method)
        if isinstance(self.normals, type(None)):
            self.solver.solve()
        else:
            self.solver.solve(skip=True)
        self.constants = np.round(self.solver.get_constants(), decimals=precision)
        return None

    def build(self):
        """
        Build the interpolation function for the patch object
        :return:
        """
        a = self.constants[:self.kernel.n]
        b = self.constants[self.kernel.n:self.kernel.n * (self.kernel.d + 1)].reshape(self.kernel.n, self.kernel.d)
        c = self.constants[self.kernel.n * (self.kernel.d + 1):self.kernel.n * (self.kernel.d + 1) + self.kernel.d]
        d = self.constants[-1]

        def f(x, a_=a, b_=b, c_=c, d_=d):
            """
            Interpolation function for a patch of the domain.

            Parameters:
            -----------
            x : array_like
                The point(s) at which to evaluate the interpolation function. Given as an
                ndarray of shape (..., d), where d is the dimension of the domain.

            a_ : array_like
                The coefficients for the Duchon interpolation function.

            b_ : array_like
                The coefficients for the gradient of the Duchon interpolation function.

            c_ : array_like
                The coefficients for the Hessian of the Duchon interpolation function.

            d_ : float
                The constant term for the Duchon interpolation function.

            Returns:
            --------
            value : array_like
                The value of the interpolation function at the given point(s). Given as an
                ndarray of shape (..., 1).
            """
            value = 0
            diff = x - self.points.reshape(
                tuple([self.points.shape[0]]) + (1,) * self.kernel.d + tuple([self.points.shape[1]]))
            a_ = a_.reshape(a_.shape + (1,) * self.kernel.d)
            b_ = b_.reshape(tuple([b_.shape[0]]) + (1,) * self.kernel.d + tuple([b_.shape[1]]))
            c_ = c_.reshape((1,) * self.kernel.d + c_.shape)
            a_value = np.sum(a_ * np.sum(diff ** 2, axis=-1) ** (self.rbf_degree / 2), axis=0)
            value += a_value
            b_value = np.sum(self.rbf_degree * np.sum((-b_) * diff, axis=-1) * np.sum(diff ** 2, axis=-1) ** (
                        self.rbf_degree / 2 - 1), axis=0)
            value += b_value
            c_value = np.sum(c_ * x, axis=-1)
            value += c_value
            value += d_
            return value
        f.points = self.points
        if self.normals is not None:
            f.normals = self.normals
        else:
            f.normals = self.solver.get_normals()
        f.dimensions = self.kernel.d
        f.min = np.min(self.points, axis=0)
        f.max = np.max(self.points, axis=0)
        f.centroid = np.mean(self.points, axis=0)
        f.first = self.points[0, :]
        return f

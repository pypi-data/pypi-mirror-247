import numpy as np
from scipy.spatial import cKDTree
from .patch import Patch
from .routines.allocate import allocate
from .routines.discretize import contour
from .io.read_pyvista import read_pyvista


class Domain(object):
    def __init__(self, *args, **kwargs):
        """
        The Domain class defines the region in space that
        will be recognized by svtoolkit when generating
        vascular networks. The class abstracts the physical
        representation of the space to allow for efficient
        interrogation and data manipulation.

        Parameters
        ----------
        args : list
            A list of arguments to be passed to the Domain
            object. The arguments can be a single numpy array
            of points, a single numpy array of points and
            normals, or a PyVista object.
        kwargs : dict
            A dictionary of keyword arguments to be passed
            to the Domain object.
        """
        self.patches = []
        self.functions = []
        self.function_tree = None
        self.points = None
        self.normals = None
        self.duplicate_number = 1 # plan to remove this
        if len(args) > 0:
            self.set_data(*args, **kwargs)

    def set_data(self, *args, **kwargs):
        """
        Set the data for the domain from point-wise data
        or a PyVista object.
        """
        if len(args) == 0:
            raise ValueError("No data provided.")
        elif len(args) == 1:
            if isinstance(args[0], np.ndarray):
                self.points = args[0]
                self.n = self.points.shape[0]
                self.d = self.points.shape[1]
            elif 'pyvista' in str(args[0].__class__):
                points, normals, n, d = read_pyvista(args[0], **kwargs)
                self.points = points
                self.normals = normals
                self.n = n
                self.d = d
        elif len(args) == 2:
            self.points = args[0]
            self.normals = args[1]
            self.n = self.points.shape[0]
            self.d = self.points.shape[1]
        else:
            raise ValueError("Too many arguments.")
        return None

    def create(self, **kwargs):
        """
        Create the patches for the domain. This is the first step in the process.
        :param kwargs:
        :return:
        """
        self.patches = []
        if self.normals is None:
            patch_data = allocate(self.points, **kwargs)
        else:
            patch_data = allocate(self.points, self.normals, **kwargs)
        for i in range(len(patch_data)):
            self.patches.append(Patch())
            if self.normals is None:
                self.patches[-1].set_data(patch_data[i][0])
            else:
                self.patches[-1].set_data(patch_data[i][0], patch_data[i][1])
        return None

    def solve(self, **kwargs):
        """
        Solve the individual patch interpolation problems prior to blending.

        Parameters
        ----------
            None

        Returns
        -------
            None
        """
        for patch in self.patches:
            patch.solve(**kwargs)
        return None

    def build(self):
        """
        Build the implicit function describing the domain.
        :return:
        """
        functions = []
        firsts = []
        for patch in self.patches:
            func = patch.build()
            firsts.append(func.first)
            functions.append(func)
        self.function_tree = cKDTree(np.array(firsts))
        #nominal_exterior_point = np.max(self.points, axis=0) + 1
        function_list = set(tuple(list(range(len(functions)))))
        #current_function = self.function_tree.query(nominal_exterior_point, k=1)[1]
        #if not np.sign(functions[current_function](nominal_exterior_point)) > 0:
        #    def func(x):
        #        return -1 * functions[current_function](x)
        #    func.dimensions = functions[current_function].dimensions
        #    func.min = functions[current_function].min
        #    func.max = functions[current_function].max
        #    func.centroid = functions[current_function].centroid
        #    func.first = functions[current_function].first
        #    func.normals = -1 * functions[current_function].normals
        #    func.points = functions[current_function].points
        #    functions[current_function] = func
        self.functions = functions
        return None

    def evaluate(self, points, k=1, tolerance=np.finfo(float).eps * 4):
        """
        Evaluate the implicit function at a point or set of points.
        :param points:
        :param k:
        :param tolerance:
        :return:
        """
        if self.function_tree is None:
            raise ValueError("Domain not built.")
        values = np.zeros((points.shape[0], 1))
        dists, indices_first = self.function_tree.query(points, k=1)
        dists_first = dists.reshape(-1, 1)[:, -1].flatten()
        indices = self.function_tree.query_ball_point(points, dists_first + tolerance)
        if k > 1:
            extra_dists, extra_indices_first = self.function_tree.query(points, k=k)
            extra_dists = extra_dists.reshape(-1, k)[:, -1].flatten()
            extra_indices = self.function_tree.query_ball_point(points, extra_dists + tolerance)
        else:
            extra_indices_first = None
            extra_indices = None
        for i in range(len(indices)):
            tmp_value = []
            weights = []
            if len(indices[i]) == 0:
                indices[i].append(indices_first[i])
            for j in range(len(indices[i])):
                func = self.functions[indices[i][j]](points[i, :])
                tmp_value.append(func.flatten()[0])
            tmp_value = np.array(tmp_value)
            sign = np.sign(np.max(tmp_value))
            tmp_value_sign = np.argwhere(np.sign(tmp_value) == sign).flatten()
            tmp_sum = np.sum(tmp_value[tmp_value_sign])
            if np.any(np.isclose(tmp_value, 0)):
                weights.append(np.inf)
            else:
                weights.append(1 / np.min(abs(tmp_sum)))
            tmp_value = [tmp_sum]
            weights = [weights]
            if k > 1:
                if len(extra_indices[i]) == 0:
                    extra_indices[i].extend(extra_indices_first[i, :].tolist())
                for j in range(len(indices[i]), len(extra_indices[i])):
                    func = self.functions[extra_indices[i][j]](points[i, :])
                    if np.isclose(func.flatten()[0], 0):
                        weights.append(np.inf)
                        tmp_value.append(tmp_sum)
                    else:
                        weights.append(1 / abs(func.flatten()[0]))
                        tmp_value.append(func.flatten()[0])
            tmp_value = np.array(tmp_value)
            weights = np.array(weights)
            signs = np.sign(tmp_value)
            idx = np.argwhere(signs == sign).flatten()
            if np.any(np.isinf(weights[idx])):
                idx = np.argwhere(np.isinf(weights[idx])).flatten()
                values[i] = np.mean(tmp_value[idx])
            else:
                partition = weights[idx] / np.sum(weights[idx])
                value = np.tanh(np.sum(np.tanh(tmp_value[idx]) * partition))
                values[i] = value
        return values

    def __call__(self, points, **kwargs):
        """
        Evaluate the implicit function at a point or set of points.
        :param points:
        :param k:
        :param tolerance:
        :return:
        """
        return self.evaluate(points, **kwargs)

    def within(self, points, level=0, **kwargs):
        """
        Determine if a point or set of points is within the domain.

        """
        values = self.__call__(points, **kwargs)
        return values < level

    def __sub__(self, other):
        """
        Subtract two domains. This is the set difference operation.

        """
        new_domain = Domain()
        def evaluate(x):
            self_object = self.__call__(x)
            other_object = other.__call__(x)
            values = (np.logical_and(self_object < 0, other_object < 0)*(abs(self_object) + abs(other_object)) +
                      self_object)
            return values
        new_domain.evaluate = evaluate
        #new_domain.evaluate = lambda x: np.logical_and(self.__call__(x) < 0, other.__call__(x) < 0)*(abs(self.__call__(x)) + abs(other.__call__(x))) + self.__call__(x)
        return new_domain

    def __add__(self, other):
        """
        Add two domains. This is the set union operation.
        """
        new_domain = Domain()
        new_domain.evaluate = lambda x: np.logical_and(self.__call__(x) > 0, other.__call__(x) > 0)*(abs(self.__call__(x)) + abs(other.__call__(x))) + (self.__call__(x) < 0)*self.__call__(x) + (other.__call__(x) < 0)*other.__call__(x)
        return new_domain

    def descretize(self, resolution):
        """
        Descretize the domain into a set of points.
        """
        self.boundary, self.mesh = contour(self.evaluate, self.points, resolution)


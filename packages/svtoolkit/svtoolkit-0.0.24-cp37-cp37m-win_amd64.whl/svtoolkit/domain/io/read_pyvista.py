import numpy as np
import pyvista as pv
from ..remeshing.remesh import remesh_surface

def read_pyvista(pyvista_object, **kwargs):
    """
    Read a PyVista object into a Domain object.

    Parameters
    ----------
    pyvista_object : pyvista object
        A PyVista object to be read into a Domain object.
    kwargs : dict
        A dictionary of keyword arguments to be passed

    """
    feature_angle = kwargs.get("feature_angle", 30.0)
    remesh = kwargs.get("remesh", False)
    pyvista_object = pyvista_object.compute_normals(split_vertices=True, feature_angle=feature_angle)
    points = pyvista_object.points.astype(np.float64)
    normals = pyvista_object.point_normals.astype(np.float64)
    n = points.shape[0]
    d = points.shape[1]
    return points, normals, n, d


def read_stl():
    pass


def read_vtk():
    pass
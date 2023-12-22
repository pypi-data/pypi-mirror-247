import numpy as np
from skimage import measure
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go

def grid(mins, maxs, nums):
    """
    This function creates a grid of points
    within the unit cube.
    """
    dim = []
    for i in range(len(mins)):
        dim.append(np.linspace(mins[i], maxs[i], nums[i]))
    meshgrid = np.meshgrid(*dim)
    for i in range(len(meshgrid)):
        meshgrid[i] = meshgrid[i].flatten()
    return np.array([*meshgrid]).T



def plot_3d_volume(function, resolution=20, cmin=-1, cmax=0, number_surfaces=10, buffer=1):
    ranges = function.max - function.min
    center = (function.max + function.min)/2
    buffer = (np.linalg.norm(ranges)*buffer)/2
    mins = center - buffer
    maxs = center + buffer
    nums = [resolution]*function.dimensions
    grid_points = grid(mins, maxs, nums)
    values = function(grid_points).flatten()
    fig = go.Figure(data=go.Isosurface(
        x=grid_points[:, 0],
        y=grid_points[:, 1],
        z=grid_points[:, 2],
        value=values,
        isomin=cmin,
        isomax=cmax,
        surface_count=number_surfaces)
    )
    fig.show()
    return None


def plot_3d_domain(domain, resolution=20, k=1, cmin=-1, cmax=0, number_surfaces=10, buffer=1):
    domain_max = np.max(domain.points, axis=0)
    domain_min = np.min(domain.points, axis=0)
    domain_dimensions = domain.points.shape[1]
    ranges = domain_max - domain_min
    center = (domain_max + domain_min)/2
    buffer = (np.linalg.norm(ranges)*buffer)/2
    mins = center - buffer
    maxs = center + buffer
    nums = [resolution]*domain_dimensions
    grid_points = grid(mins, maxs, nums)
    values = domain.evaluate(grid_points, k=k).flatten()
    fig = go.Figure(data=go.Isosurface(
        x=grid_points[:, 0],
        y=grid_points[:, 1],
        z=grid_points[:, 2],
        value=values,
        isomin=cmin,
        isomax=cmax,
        opacity=0.2,
        surface_count=number_surfaces)
    )
    fig.show()
    return None
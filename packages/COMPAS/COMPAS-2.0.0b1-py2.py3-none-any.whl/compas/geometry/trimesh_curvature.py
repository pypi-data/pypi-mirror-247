from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import pluggable


@pluggable(category="trimesh")
def trimesh_gaussian_curvature(M):
    """Compute the discrete gaussian curvature of a triangle mesh.

    Parameters
    ----------
    M : tuple[sequence[[float, float, float] | :class:`compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    list[float]
        The discrete gaussian curvature per vertex.

    Examples
    --------
    >>>

    """
    raise NotImplementedError


trimesh_gaussian_curvature.__pluggable__ = True


@pluggable(category="trimesh")
def trimesh_principal_curvature(M):
    """Compute the principal curvature directions of a triangle mesh.

    Parameters
    ----------
    M : tuple[sequence[[float, float, float] | :class:`compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    list[tuple[[float, float, float], [float, float]]]
        The curvature directions per vertex.

    Examples
    --------
    >>>

    """
    raise NotImplementedError


trimesh_principal_curvature.__pluggable__ = True


@pluggable(category="trimesh")
def trimesh_mean_curvature(M):
    """Compute the discrete mean curvature of a triangle mesh.

    Parameters
    ----------
    M : tuple[sequence[[float, float, float] | :class:`compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    list[float]
        The discrete mean curvature per vertex.

    Examples
    --------
    >>>

    """
    raise NotImplementedError


trimesh_mean_curvature.__pluggable__ = True

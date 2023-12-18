from math import tan
from math import radians

from compas.geometry import Transformation
from compas.geometry import normalize_vector
from compas.geometry import subtract_vectors
from compas.geometry import cross_vectors


def ortho(left, right, bottom, top, near, far):
    """Construct an orthogonal projection matrix.

    Parameters
    ----------
    left : float
        Location of the left clipping plane.
    right : float
        Location of the right clipping plane.
    bottom : float
        Location of the bottom clipping plane.
    top : float
        Location of the top clipping plane.
    near : float
        Location of the near clipping plane.
    far : float
        Location of the far clipping plane.

    Returns
    -------
    :class:`compas.geometry.Transformation`

    """
    dx = right - left
    dy = top - bottom
    dz = far - near
    rx = -(right + left) / dx
    ry = -(top + bottom) / dy
    rz = -(far + near) / dz
    matrix = [
        [2.0 / dx, 0, 0, rx],
        [0, 2.0 / dy, 0, ry],  # noqa: E201
        [0, 0, -2.0 / dz, rz],  # noqa: E201
        [0, 0, 0, 1],  # noqa: E201
    ]
    return Transformation.from_matrix(matrix)


def perspective(fov, aspect, near, far):
    """Construct a perspective projection matrix.

    Parameters
    ----------
    fov : float
        The field of view in degrees.
    aspect : float
        The aspect ratio of the view.
    near : float
        Location of the near clipping plane.
    far : float
        Location of the far clipping plane.

    Returns
    -------
    :class:`compas.geometry.Transformation`

    """
    sy = 1.0 / tan(radians(fov) / 2.0)
    sx = sy / aspect
    zz = (far + near) / (near - far)
    zw = 2 * far * near / (near - far)
    matrix = [[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, zz, zw], [0, 0, -1, 0]]  # noqa: E201  # noqa: E201  # noqa: E201
    return Transformation.from_matrix(matrix)


def lookat(eye, target, up):
    """Construct a "look at" transformation matrix.

    Parameters
    ----------
    eye : [float, float, float] or :class:`compas.geometry.Point`
        Location of the "eye" of the camera.
    target : [float, float, float] or :class:`compas.geometry.Point`
        Location of the target to look at.
    up : [float, float, float] or :class:`compas.geometry.Vector`
        Direction indicating which way is "up".

    Returns
    -------
    :class:`compas.geometry.Transformation`

    """
    d = normalize_vector(subtract_vectors(target, eye))
    r = cross_vectors(d, normalize_vector(up))
    u = cross_vectors(r, d)
    matrix = [
        [+r[0], +r[1], +r[2], -eye[0]],
        [+u[0], +u[1], +u[2], -eye[1]],
        [-d[0], -d[1], -d[2], -eye[2]],
        [0, 0, 0, 1],  # noqa: E201
    ]
    return Transformation.from_matrix(matrix)

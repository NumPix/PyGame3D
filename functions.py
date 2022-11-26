from __future__ import annotations

from math import sin, cos
import numpy as np

from numba import njit


@njit(fastmath=True)
def clamp(value, min_value, max_value) -> float | int:
    return min_value if value < min_value else max_value if value > max_value else value


@njit(fastmath=True)
def length(vector: np.ndarray) -> float:
    res = 0
    for elem in vector:
        res += elem ** 2
    return np.sqrt(res)


@njit(fastmath=True)
def normalize(vector: np.ndarray) -> np.ndarray:
    return vector / length(vector)


@njit(fastmath=True)
def dot(vector1: np.ndarray, vector2: np.ndarray) -> float:
    return sum(vector1 * vector2)


@njit(fastmath=True)
def step_float(edge, x):
    return 1 if x > edge else 0


@njit(fastmath=True)
def step(edge: np.ndarray, x: np.ndarray):
    return np.array([step_float(edge[0], x[0]), step_float(edge[1], x[1]), step_float(edge[2], x[2])])


@njit(fastmath=True)
def reflect(ray: np.ndarray, normal: np.ndarray):
    return ray - normal * (2 * dot(normal, ray))


@njit(fastmath=True)
def sphere(camera: np.ndarray, ray: np.ndarray,  radius: float):
    b = dot(camera, ray)
    c = dot(camera, camera) - radius ** 2
    h = b ** 2 - c
    if h < 0:
        return np.array([-1.0, -1.0])
    h = np.sqrt(h)
    return np.array([-b - h, -b + h])


@njit(fastmath=True)
def box(camera: np.ndarray, ray: np.ndarray, position: np.ndarray, size: np.ndarray):
    b_camera = camera - position
    m = np.array([1, 1, 1]) / ray
    n = m * b_camera
    k = np.abs(m) * size
    t1 = -n - k
    t2 = -n + k
    tN = np.max(t1)
    tF = np.min(t2)

    if tN > tF or tF < 0:
        return np.array([-1.0, -1.0])

    return np.array([tN, tF])


def box_normal(camera: np.ndarray, ray: np.ndarray, position: np.ndarray, size: np.ndarray):
    b_camera = camera - position
    m = np.array([1, 1, 1]) / ray
    n = m * b_camera
    k = np.abs(m) * size
    t1 = -n - k
    yzx = np.array([t1[1], t1[2], t1[0]])
    zxy = np.array([t1[2], t1[0], t1[1]])

    return -np.sign(ray) * step(yzx, t1) * step(zxy, t1)


@njit(fastmath=True)
def plane(camera: np.ndarray, ray: np.ndarray, p, w):
    return -(dot(camera, p) + w) / dot(ray, p)


@njit(fastmath=True)
def rotate_x(vector: np.ndarray, angle: float):
    return np.array([vector[0],
                    vector[2] * sin(angle) + vector[1] * cos(angle),
                    vector[2] * cos(angle) - vector[1] * sin(angle)])


@njit(fastmath=True)
def rotate_y(vector: np.ndarray, angle: float):
    return np.array([vector[0] * cos(angle) - vector[2] * sin(angle),
                    vector[1],
                    vector[0] * sin(angle) + vector[2] * cos(angle)])


@njit(fastmath=True)
def rotate_z(vector: np.ndarray, angle: float):
    return np.array([vector[0] * cos(angle) - vector[1] * sin(angle),
                    vector[0] * sin(angle) + vector[1] * cos(angle),
                    vector[2]])

from __future__ import annotations

from math import sqrt, sin, cos
from Vector3 import Vector3
from Vector2 import Vector2


def clamp(value, min_value, max_value) -> float | int:
    return min_value if value < min_value else max_value if value > max_value else value


def sign(n: float | int | Vector3 | Vector2) -> int | Vector3 | Vector2:
    if type(n) == int or type(n) == float:
        return -1 if n < 0 else 1 if n > 0 else 0
    elif type(n) == Vector2:
        return Vector2(sign(n.x), sign(n.y))
    elif type(n) == Vector3:
        return Vector3(sign(n.x), sign(n.y), sign(n.z))


def length(vector: Vector2 | Vector3) -> float:
    if type(vector) == Vector2:
        return sqrt(vector.x ** 2 + vector.y ** 2)
    elif type(vector) == Vector3:
        return sqrt(vector.x ** 2 + vector.y ** 2 + vector.z ** 2)


def normalize(vector: Vector2 | Vector3) -> Vector2 | Vector3:
    if type(vector) == Vector2:
        try:
            return Vector2(vector.x / length(vector), vector.y / length(vector))
        except ZeroDivisionError:
            return Vector2(0, 0)
    elif type(vector) == Vector3:
        try:
            return Vector3(vector.x / length(vector), vector.y / length(vector), vector.z / length(vector))
        except ZeroDivisionError:
            return Vector3(0, 0, 0)


def dot(vector1: Vector2 | Vector3, vector2: Vector2 | Vector3) -> float:
    if type(vector1) == Vector2 and type(vector2 == Vector2):
        return vector1.x * vector2.x + vector1.y * vector2.y
    elif type(vector1) == Vector3 and type(vector2 == Vector3):
        return vector1.x * vector2.x + vector1.y * vector2.y + vector1.z * vector2.z


def step(edge: int | float | Vector2 | Vector3, x: int | float | Vector2 | Vector3):
    if type(edge) in [float, int] and type(x) in [float, int]:
        return 1 if x > edge else 0
    elif type(edge) == Vector2 and type(x) == Vector2:
        return Vector2(step(edge.x, x.x), step(edge.y, x.y))
    elif type(edge) == Vector3 and type(x) == Vector3:
        return Vector3(step(edge.x, x.x), step(edge.y, x.y), step(edge.z, x.z))


def reflect(ray: Vector3, normal: Vector3):
    return ray - normal * (2 * dot(normal, ray))


def sphere(camera: Vector3, ray: Vector3,  radius: float):
    b = dot(camera, ray)
    c = dot(camera, camera) - radius ** 2
    h = b ** 2 - c
    if h < 0:
        return Vector2(-1, -1)
    h = sqrt(h)
    return Vector2(-b - h, -b + h)


def box(camera: Vector3, ray: Vector3, position: Vector3, size: Vector3):
    camera -= position
    m = Vector3(1, 1, 1) / ray
    n = m * camera
    k = abs(m) * size
    t1 = -n - k
    t2 = -n + k
    tN = max(t1.x, t1.y, t1.z)
    tF = min(t2.x, t2.y, t2.z)

    if tN > tF or tF < 0:
        return Vector2(-1, -1), Vector2(0, 0)

    yzx = Vector3(t1.y, t1.z, t1.x)
    zxy = Vector3(t1.z, t1.x, t1.y)

    normal_angle = -sign(ray) * step(yzx, t1) * step(zxy, t1)

    return Vector2(tN, tF), normal_angle


def plane(camera: Vector3, ray: Vector3, p, w):
    return -(dot(camera, p) + w) / dot(ray, p)


def rotate_x(vector: Vector3, angle: float):
    return Vector3(vector.x,
                   vector.z * sin(angle) + vector.y * cos(angle),
                   vector.z * cos(angle) - vector.y * sin(angle))


def rotate_y(vector: Vector3, angle: float):
    return Vector3(vector.x * cos(angle) - vector.z * sin(angle),
                   vector.y,
                   vector.x * sin(angle) + vector.z * cos(angle))


def rotate_z(vector: Vector3, angle: float):
    return Vector3(vector.x * cos(angle) - vector.y * sin(angle),
                   vector.x * sin(angle) + vector.y * cos(angle),
                   vector.z)


def vec2tup(vector: Vector2 | Vector3):
    if type(vector) == Vector2:
        return vector.x, vector.y
    if type(vector) == Vector3:
        return vector.x, vector.y, vector.z

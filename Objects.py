from Vector3 import Vector3


class Sphere:
    def __init__(self, position: Vector3, radius: float, color: Vector3 = Vector3(255, 255, 255)):
        self.position = position
        self.radius = radius
        self.color = color


class Box:
    def __init__(self, position: Vector3, size: Vector3, color: Vector3 = Vector3(255, 255, 255)):
        self.position = position
        self.size = size
        self.color = color


class Plane:
    def __init__(self, p: Vector3, w: float, color: Vector3 = Vector3(255, 255, 255)):
        self.p = p
        self.w = w
        self.color = color

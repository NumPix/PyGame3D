import numpy as np


class Sphere:
    def __init__(self, position, radius: float, color=np.array([255, 255, 255])):
        self.position = position
        self.radius = radius
        self.color = color


class Box:
    def __init__(self, position, size, color=np.array([255, 255, 255])):
        self.position = position
        self.size = size
        self.color = color


class Plane:
    def __init__(self, p, w: float, color=np.array([255, 255, 255])):
        self.p = p
        self.w = w
        self.color = color

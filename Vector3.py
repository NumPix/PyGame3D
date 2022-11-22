class Vector3:
    def __init__(self, x, y, z):
        if (type(x) == float or type(x) == int) and (type(y) == float or type(y) == int) and (
                type(z) == float or type(z) == int):
            self.x = x
            self.y = y
            self.z = z

    def __add__(self, other):
        if type(other) == float or type(other) == int:
            return Vector3(self.x + other, self.y + other, self.z + other)
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        if type(other) == float or type(other) == int:
            return Vector3(self.x - other, self.y - other, self.z - other)
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if type(other) == float or type(other) == int:
            return Vector3(self.x * other, self.y * other, self.z * other)
        return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __truediv__(self, other):
        if type(other) == float or type(other) == int:
            return Vector3(self.x / other, self.y / other, self.z / other)

        if other.x == 0:
            other.x = 0.001

        if other.y == 0:
            other.y = 0.001

        if other.z == 0:
            other.z = 0.001

        return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)

    def __abs__(self):
        return Vector3(abs(self.x), abs(self.y), abs(self.z))

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __str__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"
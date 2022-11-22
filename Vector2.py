class Vector2:
    def __init__(self, x, y):
        if (type(x) == float or type(x) == int) and (type(y) == float or type(y) == int):
            self.x = x
            self.y = y
        elif type(x) == Vector2 and type(y) == Vector2:
            self.x = y.x - x.x
            self.y = y.y - x.y

    def __add__(self, other):
        if type(other) == float or type(other) == int:
            return Vector2(self.x + other, self.y + other)
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if type(other) == float or type(other) == int:
            return Vector2(self.x - other, self.y - other)
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if type(other) == float or type(other) == int:
            return Vector2(self.x * other, self.y * other)
        return Vector2(self.x * other.x, self.y * other.y)

    def __truediv__(self, other):
        if type(other) == float or type(other) == int:
            return Vector2(self.x / other, self.y / other)

        if other.x == 0:
            other.x = 0.001

        if other.y == 0:
            other.y = 0.001

        return Vector2(self.x / other.x, self.y / other.y)

    def __abs__(self):
        return Vector2(abs(self.x), abs(self.y))

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __str__(self):
        return f"Vector2({self.x}, {self.y})"
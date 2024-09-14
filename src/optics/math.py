import math
from dataclasses import dataclass


@dataclass
class Vec2:
    x: float
    y: float

    def __neg__(self):
        return -1 * self

    def __mul__(self, other) -> float or 'Vec2':
        if hasattr(other, 'x') and hasattr(other, 'y'):
            return self.x * other.x + self.y * other.y
        return Vec2(other * self.x, other * self.y)

    def __rmul__(self, other) -> 'Vec2':
        return self * other

    def __add__(self, other) -> 'Vec2':
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> 'Vec2':
        return Vec2(self.x - other.x, self.y - other.y)

    def __getitem__(self, item):
        if not 0 <= item <= 1:
            raise ValueError("no value at " + item)
        return self.x if item == 0 else self.y

    def normalize(self):
        if self.length() == 0:
            raise ValueError("cannot normalize a zero vector")
        length = math.sqrt(self.x ** 2 + self.y ** 2)
        return Vec2(self.x / length, self.y / length)

    def rotate(self, angle: float) -> 'Vec2':
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        return Vec2(self.x * cos_a - self.y * sin_a, self.x * sin_a + self.y * cos_a)

    def rotate_cw(self) -> 'Vec2':
        return Vec2(self.y, -self.x)

    def rotate_ccw(self) -> 'Vec2':
        return Vec2(-self.y, self.x)

    def length(self):
        return math.sqrt(self * self)


class Mat:
    def __init__(self, n, m=None):
        if m is None:
            m = n
        self.n = n  # Number of columns
        self.m = m if m is not None else n  # Number of rows
        self.data = [[0] * self.m for _ in range(self.n)]  # Column-major order (list of columns)

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, i, value):
        self.data[i] = value

    def __mul__(self, other):
        if hasattr(other, 'n'):
            if self.n != other.m:
                raise ValueError("matrix dimensions do not match for multiplication")
            result = Mat(other.n, self.m)
            for i in range(other.n):
                for j in range(self.m):
                    result[i][j] = sum(self[k][j] * other[i][k] for k in range(self.n))
            return result
        else:
            if len(other) != self.n:
                raise ValueError("vector size does not match the number of columns in the matrix")
            result = [0] * self.m
            for j in range(self.m):
                result[j] = sum(self[i][j] * other[i] for i in range(self.n))
            return result

    def __repr__(self):
        res = ""
        for col in self.data[:self.n - 1]:
            res += repr(col)
            res += "\n"
        for col in self.data[self.n-1:self.n]:
            res += repr(col)
        return res


@dataclass
class Segment:
    a: Vec2
    b: Vec2

    def a_to_b(self) -> Vec2:
        return self.b - self.a

    def length(self) -> float:
        return self.a_to_b().length()

    def normal(self) -> Vec2:
        return self.a_to_b().rotate_ccw().normalize()

import math

class Vector2d:
    def __init__(self, x: int=0, y: int=0):
        if type(x) not in [int, float] or type(y) not in [int, float]:
            raise TypeError("x and y must be float or int")
        self.x = x
        self.y = y
    
    def norm(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)
    
    def normalize(self) -> None:
        norm = self.norm()
        if norm == 0:
            raise ZeroDivisionError("Cannot normalize a zero vector")
        self.x /= norm
        self.y /= norm
    
    def dot(self, other) -> float:
        if type(other) != Vector2d:
            raise TypeError("Cannot dot a Vector2d with a non-Vector2d")
        return self.x * other.x + self.y * other.y
    
    def rotate(self, angle: float) -> None:
        angle = math.radians(angle)
        self.x = self.x * math.cos(angle) - self.y * math.sin(angle)
        self.y = self.x * math.sin(angle) + self.y * math.cos(angle)
    
    def copy(self) -> "Vector2d":
        return Vector2d(self.x, self.y)
    
    def __add__(self, other) -> "Vector2d":
        if type(other) != Vector2d:
            raise TypeError("Cannot add a Vector2d to a non-Vector2d")
        return Vector2d(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other) -> "Vector2d":
        if type(other) != Vector2d:
            raise TypeError("Cannot subtract a Vector2d from a non-Vector2d")
        return Vector2d(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other) -> "Vector2d":
        if type(other) in [int, float]:
            return Vector2d(self.x * other, self.y * other)
        raise TypeError("Cannot multiply a Vector2d by a non-Vector2d")
        
    def __rmul__(self, other) -> "Vector2d":
        if type(other) in [int, float]:
            return Vector2d(self.x * other, self.y * other)
        raise TypeError("Cannot multiply a Vector2d by a non-Vector2d")
    
    def __div__(self, other) -> "Vector2d":
        if type(other) in [int, float]:
            if other == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            return Vector2d(self.x / other, self.y / other)
        raise TypeError("Cannot divide a Vector2d by a non-Vector2d")
    
    def __str__(self) -> str:
        return f"Vector2d({self.x}, {self.y})"
    
    def __repr__(self) -> str:
        return f"Vector2d({self.x}, {self.y})"
    
    def __eq__(self, other) -> bool:
        if type(other) != Vector2d:
            raise TypeError("Cannot compare a Vector2d with a non-Vector2d")
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other) -> bool:
        return not self == other
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __getitem__(self, key: int) -> float:
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        raise IndexError("Vector2d index out of range")
    
    def __setitem__(self, key: int, value: float) -> None:
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Vector2d index out of range")
        
    def __iter__(self):
        yield self.x
        yield self.y

    def __len__(self):
        return 2
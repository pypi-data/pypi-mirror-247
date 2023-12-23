import math

class Vector3d:
    def __init__(self, x: int=0, y: int=0, z: int=0):
        if type(x) not in [int, float] or type(y) not in [int, float] or type(z) not in [int, float]:
            raise TypeError("x, y and z must be float or int")
        self.x = x
        self.y = y
        self.z = z
    
    def norm(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self) -> None:
        norm = self.norm()
        if norm == 0:
            raise ZeroDivisionError("Cannot normalize a zero vector")
        self.x /= norm
        self.y /= norm
        self.z /= norm
    
    def dot(self, other) -> float:
        if type(other) != Vector3d:
            raise TypeError("Cannot dot a Vector3d with a non-Vector3d")
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def copy(self) -> "Vector3d":
        return Vector3d(self.x, self.y, self.z)
    
    def __add__(self, other) -> "Vector3d":
        if type(other) != Vector3d:
            raise TypeError("Cannot add a Vector3d to a non-Vector3d")
        return Vector3d(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other) -> "Vector3d":
        if type(other) != Vector3d:
            raise TypeError("Cannot subtract a Vector3d from a non-Vector3d")
        return Vector3d(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other) -> "Vector3d":
        if type(other) in [int, float]:
            return Vector3d(self.x * other, self.y * other, self.z * other)
        return Vector3d(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)
        
    def __rmul__(self, other) -> "Vector3d":
        if type(other) in [int, float]:
            return Vector3d(self.x * other, self.y * other, self.z * other)
        return self * other
    
    def __truediv__(self, other) -> "Vector3d":
        if type(other) in [int, float]:
            if other == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            return Vector3d(self.x / other, self.y / other, self.z / other)
        raise TypeError("Cannot divide a Vector3d by a non-Vector3d")
    
    def __str__(self) -> str:
        return f"Vector2d({self.x}, {self.y}, {self.z})"
    
    def __repr__(self) -> str:
        return f"Vector2d({self.x}, {self.y}, {self.z})"
    
    def __eq__(self, other) -> bool:
        if type(other) != Vector3d:
            raise TypeError("Cannot compare a Vector3d with a non-Vector3d")
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __ne__(self, other) -> bool:
        return not self == other
    
    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))
    
    def __getitem__(self, key: int) -> float:
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        if key == 2:
            return self.z
        raise IndexError("Vector3d index out of range")
    
    def __setitem__(self, key: int, value: float) -> None:
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        else:
            raise IndexError("Vector3d index out of range")
        
    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z
    
    def __len__(self):
        return 3
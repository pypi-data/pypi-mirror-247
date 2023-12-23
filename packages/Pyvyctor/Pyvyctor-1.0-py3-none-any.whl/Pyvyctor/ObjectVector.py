class ObjectVector:
    def __init__(self, *args):
        self._vector = list(args)
        self._length = len(self._vector)

    def __add__(self, other):
        if type(other) != ObjectVector:
            raise TypeError("Cannot add a ObjectVector to a non-ObjectVector")
        if self._length != other._length:
            raise ValueError("Cannot add ObjectVectors of different lengths")
        if type(self._vector[0]) != type(other._vector[0]):
            raise TypeError("Cannot add ObjectVectors of different types")
        return ObjectVector(*[self._vector[i] + other._vector[i] for i in range(self._length)])
    
    def __sub__(self, other):
        if type(other) != ObjectVector:
            raise TypeError("Cannot subtract a ObjectVector from a non-ObjectVector")
        if self._length != other._length:
            raise ValueError("Cannot subtract ObjectVectors of different lengths")
        if type(self._vector[0]) != type(other._vector[0]):
            raise TypeError("Cannot subtract ObjectVectors of different types")
        return ObjectVector(*[self._vector[i] - other._vector[i] for i in range(self._length)])
    
    def __dot__(self, other):
        if type(other) in [int, float]:
            return ObjectVector(*[self._vector[i] * other for i in range(self._length)])
        if type(other) == ObjectVector:
            if self._length != other._length:
                raise ValueError("Cannot multiply ObjectVectors of different lengths")
            if type(self._vector[0]) != type(other._vector[0]):
                raise TypeError("Cannot multiply ObjectVectors of different types")
            return sum([self._vector[i] * other._vector[i] for i in range(self._length)])
        raise TypeError("Cannot multiply a ObjectVector by a non-ObjectVector")
    
    def __mul__(self, other):
        if type(other) in [int, float]:
            return ObjectVector(*[self._vector[i] * other for i in range(self._length)])
        if type(other) == ObjectVector:
            raise TypeError("Cannot multiply a ObjectVector by a non-ObjectVector")
    
    def __rmul__(self, other):
        if type(other) in [int, float]:
            return ObjectVector(*[self._vector[i] * other for i in range(self._length)])
        if type(other) == ObjectVector:
            raise TypeError("Cannot multiply a ObjectVector by a non-ObjectVector")
    
    def __div__(self, other):
        return ObjectVector(*[self._vector[i] / other for i in range(self._length)])
    
    def __str__(self):
        return f"ObjectVector({', '.join([str(i) for i in self._vector])})"
    
    def __repr__(self):
        return f"ObjectVector({', '.join([str(i) for i in self._vector])})"
    
    def __eq__(self, other):
        if type(other) != ObjectVector:
            raise TypeError("Cannot compare a ObjectVector to a non-ObjectVector")
        if self._length != other._length:
            raise ValueError("Cannot compare ObjectVectors of different lengths")
        if type(self._vector[0]) != type(other._vector[0]):
            raise TypeError("Cannot compare ObjectVectors of different types")
        return all([self._vector[i] == other._vector[i] for i in range(self._length)])
    
    def __getitem__(self, index):
        return self._vector[index]
    
    def __setitem__(self, index, value):
        self._vector[index] = value

    def __len__(self):
        return self._length
    
    def __hash__(self):
        return hash(tuple(self._vector))
    
    def __iter__(self):
        return iter(self._vector)
    
    def __contains__(self, item):
        return item in self._vector
    
    def __copy__(self):
        return ObjectVector(*self._vector)
    
    def __deepcopy__(self, memo):
        return ObjectVector(*self._vector)
    
    def __neg__(self):
        return ObjectVector(*[-i for i in self._vector])
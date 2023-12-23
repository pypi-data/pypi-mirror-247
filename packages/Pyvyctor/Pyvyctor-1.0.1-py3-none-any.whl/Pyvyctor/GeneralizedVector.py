class GeneralVector:
    def __init__(self, *args):
        self._vector = list(args)
        self._length = len(self._vector)

    def __add__(self, other):
        if type(other) != GeneralVector:
            raise TypeError("Cannot add a GeneralVector to a non-GeneralVector")
        if self._length != other._length:
            raise ValueError("Cannot add GeneralVectors of different lengths")
        if type(self._vector[0]) != type(other._vector[0]):
            raise TypeError("Cannot add GeneralVectors of different types")
        return GeneralVector(*[self._vector[i] + other._vector[i] for i in range(self._length)])
    
    def __sub__(self, other):
        if type(other) != GeneralVector:
            raise TypeError("Cannot subtract a GeneralVector from a non-GeneralVector")
        if self._length != other._length:
            raise ValueError("Cannot subtract GeneralVectors of different lengths")
        if type(self._vector[0]) != type(other._vector[0]):
            raise TypeError("Cannot subtract GeneralVectors of different types")
        return GeneralVector(*[self._vector[i] - other._vector[i] for i in range(self._length)])
    
    def __dot__(self, other):
        if type(other) in [int, float]:
            return GeneralVector(*[self._vector[i] * other for i in range(self._length)])
        if type(other) == GeneralVector:
            if self._length != other._length:
                raise ValueError("Cannot multiply GeneralVectors of different lengths")
            if type(self._vector[0]) != type(other._vector[0]):
                raise TypeError("Cannot multiply GeneralVectors of different types")
            return sum([self._vector[i] * other._vector[i] for i in range(self._length)])
        raise TypeError("Cannot multiply a GeneralVector by a non-GeneralVector")
    
    def __mul__(self, other):
        if type(other) in [int, float]:
            return GeneralVector(*[self._vector[i] * other for i in range(self._length)])
        if type(other) == GeneralVector:
            raise TypeError("Cannot multiply a GeneralVector by a non-GeneralVector")
    
    def __rmul__(self, other):
        if type(other) in [int, float]:
            return GeneralVector(*[self._vector[i] * other for i in range(self._length)])
        if type(other) == GeneralVector:
            raise TypeError("Cannot multiply a GeneralVector by a non-GeneralVector")
    
    def __div__(self, other):
        return GeneralVector(*[self._vector[i] / other for i in range(self._length)])
    
    def __str__(self):
        return f"GeneralVector({', '.join([str(i) for i in self._vector])})"
    
    def __repr__(self):
        return f"GeneralVector({', '.join([str(i) for i in self._vector])})"
    
    def __eq__(self, other):
        if type(other) != GeneralVector:
            raise TypeError("Cannot compare a GeneralVector to a non-GeneralVector")
        if self._length != other._length:
            raise ValueError("Cannot compare GeneralVectors of different lengths")
        if type(self._vector[0]) != type(other._vector[0]):
            raise TypeError("Cannot compare GeneralVectors of different types")
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
        return GeneralVector(*self._vector)
    
    def __deepcopy__(self, memo):
        return GeneralVector(*self._vector)
    
    def __neg__(self):
        return GeneralVector(*[-i for i in self._vector])
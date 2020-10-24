class WeightTuple(tuple):
    def __add__(self, other):
        return WeightTuple(x + y for x, y in zip(self, other))

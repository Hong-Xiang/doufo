__all__ = ['FunctorArithmeticMixin']

class FunctorArithmeticMixin:
    def __eq__(self, t):
        return self.fmap(lambda d: d == t)

    def __req__(self, t):
        return self.fmap(lambda d: t == d)

    def __mul__(self, t):
        return self.fmap(lambda d: d * t)

    def __rmul__(self, t):
        return self.fmap(lambda d: t * d)
    
    def __add__(self, t):
        return self.fmap(lambda d: d + t)

    def __radd__(self, t):
        return self.fmap(lambda d: t + d)

    def __sub__(self, t):
        return self.fmap(lambda d: d - t)

    def __rsub__(self, t):
        return self.fmap(lambda d: t - d)

    def __truediv__(self, t):
        return self.fmap(lambda d: d / t)

    def __rtruediv__(self, t):
        return self.fmap(lambda d: t / d)

    def __floordiv__(self, t):
        return self.fmap(lambda d: d // t)

    def __rfloordiv__(self, t):
        return self.fmap(lambda d: t // d)

    def __mod__(self, t):
        return self.fmap(lambda d: d % t)

    def __rmod__(self, t):
        return self.fmap(lambda d: t % d)

    def __neg__(self):
        return self.fmap(lambda d: -d)
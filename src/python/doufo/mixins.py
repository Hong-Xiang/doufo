from functools import partial

__all__ = ['FunctorArithmeticMixin', 'GetItemSingleBatchMixin']


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

# TODO desigin: is this a mixin or abstract class? 
# TODO refactor: refactor List/Tensor/Table to use this class
class GetItemSingleBatchMixin:
    def __getitem__(self, s):
        if is_get_single_item(s):
            return self._getitem_single(s)
        else:
            return self._getitem_batch(s)

def is_get_single_item(s):
    if isinstance(s, int):
        return True
    if isinstance(s, tuple) and all(map(lambda x: isinstance(x, int))):
        return True
    return False
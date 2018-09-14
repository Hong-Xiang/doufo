"""
Quick lambda creator, useful for use in fmap, filter, etc.

e.g. List([1,2]).fmap(x + 1)
"""
from doufo import WrappedFunction, identity, Functor, FunctorArithmeticMixin
import operator

__all__ = ['QuickLambda', 'x']


class QuickLambda(WrappedFunction, FunctorArithmeticMixin):
    """
    QuickLambda constructor.
    """

    def fmap(self, f):
        return QuickLambda(lambda o: f(self.__call__(o)))

    def __getattr__(self, *args, **kwargs):
        return self.fmap(operator.attrgetter(*args, **kwargs))

    def __getitem__(self, *args, **kwargs):
        return self.fmap(operator.itemgetter(*args, **kwargs))

    def __hash__(self):
        return hash(id(self))


x = QuickLambda(identity)

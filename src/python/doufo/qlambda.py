"""
Quick lambda creator, useful for use in fmap, filter, etc.

e.g. List([1,2]).fmap(x + 1)
"""
from doufo import PureFunction, identity, Functor, FunctorArithmeticMixin
import operator
from functools import partial

__all__ = ['QuickLambda', 'x']


class QuickLambda(PureFunction, FunctorArithmeticMixin):
    """
    QuickLambda constructor.
    """

    def fmap(self, f):
        return QuickLambda(lambda x: f(self.__call__(x)))


    def __getattr__(self, *args, **kwargs):
        return self.fmap(operator.attrgetter(*args, **kwargs))

    def __getitem__(self, *args, **kwargs):
        return self.fmap(operator.itemgetter(*args, **kwargs))

    def __hash__(self):
        return hash(id(self))


x = QuickLambda(identity)

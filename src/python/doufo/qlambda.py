from doufo import PureFunction, identity

__all__ = ['QuickLambda', 'x']


class QuickLambda(PureFunction):

    def __eq__(self, v):
        return QuickLambda(lambda x: self.__call__(x) == v)

    def __getattr__(self, *args, **kwargs):
        return QuickLambda(lambda x: getattr(self.__call__(x), *args, **kwargs))

    def __getitem__(self, *args, **kwargs):
        return QuickLambda(lambda x: self.__call__(x).__getitem__(*args, **kwargs))

    def __add__(self, v):
        return QuickLambda(lambda x: self.__call__(x) + v)

    def __sub__(self, v):
        return QuickLambda(lambda x: self.__call__(x) - v)

    def __hash__(self):
        return hash(id(self))


x = QuickLambda(identity)

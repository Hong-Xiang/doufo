"""

"""


from .function import func
from functools import wraps, cmp_to_key
from multipledispatch import Dispatcher

__all__ = ['converters', 'convert_to', 'convert']

class ConvertersDict:
    def __init__(self):
        self.converters = {}

    def sorted_converters_keys(self):
        keys = sorted(self.converters.keys(),
                      key=cmp_to_key(tuple_type_compare))
        return {k: self.converters[k] for k in keys}

    def register(self, src, tar):
        def deco(f):
            self.converters[(src, tar)] = f
            self.converters = self.sorted_converters_keys()
            return f
        return deco


    def convert(self, t0, t1):
        return self.converters[(t0, t1)]


converters = ConvertersDict()


@func
def convert_to(o, target_type):
    return converters.convert(type(o), target_type)(o)


@func
def convert(target_type, o):
    return converters.convert(type(o), target_type)(o)


def tuple_type_compare(types0, types1):
    compares = [single_type_compare(types0[0], types1[0]),
                single_type_compare(types0[1], types1[1])]
    if compares[0] != 0:
        return compares[0]
    if compares[1] != 0:
        return compares[1]
    if types0[0] is types1[0] and types0[1] is types1[1]:
        return 0
    return hash(types1) - hash(types0)


def single_type_compare(t0, t1):
    if t0 is t1:
        return 0
    if issubclass(t0, t1):
        return 1
    if issubclass(t1, t0):
        return -1
    return 0

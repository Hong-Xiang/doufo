from .function import PureFunction

class ConvertersDict(PureFunction):
    def __init__(self):
        self.converters = {}

    def sorted_converters_keys(self):
        pass


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

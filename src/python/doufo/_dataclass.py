import attr
import types

__all__ = ['DataClass', 'dataclass', 'replace', 'fields']


class DataClass:
    def replace(self, **kwargs):
        return attr.evolve(self, **kwargs)

    @classmethod
    def fields(cls):
        return attr.fields_dict(cls)

    def as_dict(self):
        return attr.asdict(self)

    def as_tuple(self):
        return attr.astuple(self)


def dataclass(cls):
    base = attr.s(frozen=True, auto_attribs=True, slots=True)(cls)
    return types.new_class(base.__name__, (base, DataClass))


def replace(o: DataClass, **kwargs):
    return o.replace(**kwargs)


def fields(o: DataClass):
    return o.fields()

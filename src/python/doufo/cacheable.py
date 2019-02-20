import typing as T
import abc

A = T.TypeVar("A")


class Cacheable(abc.ABC, T.Generic[A]):
    @abc.abstractmethod
    def fetch(self) -> A:
        ...

    @abc.abstractmethod
    @property
    def value(self) -> A:
        ...

    @abc.abstractmethod
    @property
    def is_fetched(self) -> bool:
        ...


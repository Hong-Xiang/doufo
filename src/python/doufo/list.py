"""`doufo.List`
    A more or less complete user-defined wrapper around list object
Example:  
Todo:  
Author:
"""

from typing import Sequence, TypeVar, Any, Union, Callable, Tuple
import typing
from collections import UserList
from .control import Functor

A = TypeVar('A')
B = TypeVar('B')
T = TypeVar('T')

__all__ = ['List']


class List(UserList, Sequence[T], Functor[T]):
    """`doufo.List`
        This `List` class behave similar with regular `list` but inherit Functor, making   
        it have `fmap` method. If we want a regular `list` object from it, we use `unbox`.  
    Attributes:  
    """
    def __init__(self, data=None):
        """doufo.List.__init__  
        Args:  
            `self`  
            `data` (`List` or any):  
        """
        if isinstance(data, List):
            super().__init__(data.unbox())
        else:
            super().__init__(data)

    @classmethod
    def empty(cls) -> 'List[Any]':
        """doufo.List.empty  
        Args:  
            `cls`
        Returns:  
            `List[]` (Empty `List`): return empty `List`
        Raises:
        """
        return List([])

    def __getitem__(self, x: Union[int, slice]) -> Union[T, 'List[T]']:  # type: ignore
        """doufo.List.__getitem__  
        Args:  
            `self`  
            `x` (`Union[int, slice]`): `int` or `slice`  
        Returns:   
            `selected item` ()  
        Raises: if wrong type variables inputted, raise `TyprError`   
        """
        if isinstance(x, int):
            return self.unbox()[x]
        if isinstance(x, slice):
            return type(self)(self.unbox()[x])
        raise TypeError(
            f"List indices must be integers or slices, not {type(x)}")

    def extend(self, xs: Union['List[T]', typing.List[T]]) -> 'List[T]':  # type: ignore
        """doufo.List.extend  
        Args:  
            `self`  
            `xs` (`Union['List[T]', typing.List[T]]`): Another List object or Typing.List  
        Returns:  
            extented `List` (`List[T]`)
        """
        return type(self)(self.unbox() + List(xs).unbox())

    def unbox(self) -> typing.List[T]:
        """doufo.List.unbox  
        Args:  
            `self`:  
        Returns:  
            return (`typing.list[t}`): unboxed object which is wrapped in `List`  
        Raises:
        """
        return self.data

    def fmap(self, f: Callable[[T], B]) -> 'List[B]':
        """doufo.List.fmap: map `List`  
        Args:  
            `self`:  
            `f` (`Callable[[T], B]`): any callable funtion  
        Returns:  
            return (`List[B]`): A `List` of objected from `f`.  
        Raises:
        """
        return List([f(x) for x in self.unbox()])

    def zip(self, xs: 'List[B]') -> 'List[Tuple[T, B]]':
        """doufo.List.zip: zip with another `List` object ot `tuple List` object
        Args:  
            `self`:  
            `xs` (`List[B]`): anther `List` object
        Returns:  
            return (`type`):description  
        Raises:  
            If the length of input and current object differs, warning!
        """
        if len(self) == len(xs):
            return List([(x, y) for x, y in zip(self, xs)])
        else:
            print(f"Warning: The two inputs have different lengths: {len(self)} and {len(xs)}")
            return List([(x, y) for x, y in zip(self, xs)])

    def filter(self, f: Callable[[A], B]) -> 'List[T]':
        """doufo.List.filter: filter this `List` obj with input `f` function  
        Args:  
            `self`:  
            f (`Callable[[A],B]`): function that tells `True` or `False`  
        Returns:  
            return (`List[T]`): Filtered List  
        Raises:
        """
        return List([x for x in self.unbox() if f(x) is True])


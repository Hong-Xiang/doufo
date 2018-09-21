"""TM_FILENAME  
    Defined a `Maybe` object in `doufo`    
Example:  `Maybe=Union(T, None)`
Todo:  
Author:  
"""
from .control import Monad
from functools import partial

from typing import TypeVar, Callable

T = TypeVar('T')
B = TypeVar('B')

__all__ = ['Maybe']

class Maybe(Monad[T]):
    """doufo.Maybe  define a `Type` or `None` class
    Attributes:  
    """
    def __init__(self, data: T):
        """doufo.Maybe.__init__: transfer any type of data to a `Maybe`
        Args:  
            `self`:  
            data (`T`): any type of data          
        """
        self.data = data

    def __eq__(self, m: T) -> bool:
        """doufo.Maybe.__eq__: check if a `Maybe` object is equal to another object  
        Args:  
            `self`:  
            m (`T`): any type object  
        Returns:  
            return (`bool`): `True` or `False`  
        Raises:
        """
        return isinstance(m, Maybe) and m.unbox() == self.unbox()

    def unbox(self) -> T:
        """doufo.Maybe.unbox: unbox a `Maybe` object to its `self.data`   
        Args:  
            `self`
        Returns:  
            return (`T`): self.data  
        Raises:
        """
        return self.data

    def fmap(self, f: Callable[[T], B]) -> 'Maybe[B]':
        """doufo.maybe.fmap: map a `Maybe` object with a function  
        Args:  
            `self`  
            f (`Callable[[T], B]`): a function    
        Returns:  
            return (`Maybe[B]`): returned `Maybe` objects from function `f`    
        Raises:
        """
        return Maybe(None) if self.unbox() is None else Maybe(f(self.unbox()))

    def apply(self, v) -> 'Callable[[T], Maybe[B]]':
        """doufo.Maybe.apply: apply a parameter on a funtion        
        Args:  
            `self`  
            v (`A`): parameter that want to be applied on functions
        Returns:  
            return (`Callable[[T], Maybe[B]]`): A function with a applied argument 
        Raises:
        """
        return self.fmap(lambda f: partial(f, v))

    def bind(self, f: Callable[[T], 'Maybe[B]']) -> 'Maybe[B]':
        """doufo.Maybe.bind  
        Args:  
            `self`:  
            f (`Callable[[T], Maybe[B]`): A function that returns `Maybe[B]`  
        Returns:  
            return (`Maybe[B]`): results of mapping in form of `Maybe[B]`  
        Raises:
        """
        return self.fmap(lambda x: f(x).unbox())

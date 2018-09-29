"""TM_FILENAME  
    define a `Monoid` class for objects those hold associative property for some operations      
    A Monoid is a Group without 'Inverse'   
    'group' \in 'monoid' \in 'semigroup'
Example:  
    e.g. the addition of lists. ([1,2] + [3,4]) + [5,6] = [1,2] + ([3,4] + [5,6])   
Todo:  Other operations?
Author:  
"""
from abc import abstractmethod
from typing import Generic, TypeVar

__all__ = ['Monoid']

T = TypeVar('T')


class Monoid(Generic[T]):
    """doufo.Monoid:   
    define a `Monoid` class for objects those hold associative property for some operations      
    A Monoid is a Group without 'Inverse'   
    'group' \in 'monoid' \in 'semigroup'
    """
    
    @classmethod
    @abstractmethod
    def empty(cls) -> 'Monoid[T]':
        """doufo.Monoid.empty: an empty class methods   
        Args:  
            `cls`  
            arg1 (`type`): description  
        Returns:  
            return (`type`):description  
        Raises:
        """
        pass

    @abstractmethod
    def extend(self, x: 'Monoid[T]') -> 'Monoid[T]':
        """doufo.Monoid.extend: extend current object  
        Args:  
            `self`  
            x (`Monoid[T]`):   
        Returns:  
            return (`Monoid[T]`):extended Monoid  
        Raises:
        """
        pass

    def __add__(self, x: 'Monoid[T]') -> 'Monoid[T]':
        """doufo.Monoid.__add__: plus another object.   
        For now, this `+` is defined as `extend`   
        Args:  
            `self`  
            x (`Monoid[T]`):   
        Returns:  
            return (`Monoid[T]`):extended Monoid  
        Raises:
        """
        return self.extend(x)

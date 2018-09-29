"""doufo.convert  
    abstract class of `dataType` converters. 
Example:  
Todo:  
Author:  
"""
from .function import func
from functools import wraps, cmp_to_key
from multipledispatch import Dispatcher
from typing import Callable, TypeVar

__all__ = ['converters', 'convert_to', 'convert']
T = TypeVar('T')
B = TypeVar('B')



class ConvertersDict:
    """doufo.ConverterDict: to define dictionary-like class to store converters.   
        Note, this class is hidden, and been used as `converters`
    Attributes:  
        `attr1` (type): Description
    """
    def __init__(self):
        """initial as a empty `dictionary`"""
        self.converters = {}

    def sorted_converters_keys(self):
        """doufo.ConvertDict().sorted_converters_key: sort converter keys  
        sort key according to their relationship (if parent- and child-class)   
            or their hash value.
        Args:  
            `self`  
        """
        keys = sorted(self.converters.keys(),
                      key=cmp_to_key(tuple_type_compare))
        return {k: self.converters[k] for k in keys}

    def register(self, src: type, tar: type) -> Callable[[T], B]:
        """doufo.ConverterDict().register(): A decorator factory to define typing converting decorator
            Attributes:  
                `self`
                `src` (`type`): source `type`,
                `tar` (`type`): target `type`,
            Returns:
                `f` (`Callable[[T], B]`): a decorater that defines a converter                
        """
        def deco(f):
            self.converters[(src, tar)] = f
            self.converters = self.sorted_converters_keys()
            return f
        return deco


    def convert(self, src: type, tar: type) -> Callable[[T], B]:
        """ doufo.ConvertDict().convert: define a converter from `type src` to `type tar`   
            Attibutes:   
                `self`
                `src` (`type`): source `type`,    
                `tar` (`type`): target `type`,    
            Returns:
                `converter` (`Callable[[T], B]`): converter from `type src` to `type tar` 
        """
        return self.converters[(src, tar)]


converters = ConvertersDict()


@func()
def convert_to(o, target_type):
    """doufo.convert_to: convert forward
    Args:  
        `o` (`A`): any object    
        `target_type` (`type`): destination type    
    Returns:  
        return (`target_type`):description: object `o` in type of `target_type`
    Raises:
    """
    return converters.convert(type(o), target_type)(o)


@func()
def convert(o, target_type):
    """doufo.convert: convert backwards
    Args:          
        `o` (`A`): any object    
        `target_type` (`type`): destination type    
    Returns:  
         return (`target_type`):description: object `o` in type of `target_type`
    Raises:
    """
    return converters.convert(type(o), target_type)(o)


def tuple_type_compare(types0, types1):
    """doufo.tuple_type_compare: compare two types  
        if `types0` is 'bigger' than `types1`, return negative (<0);   
        otherwise, return positive (>0). Here 'bigger' is defined by   
        whether they are 'parent and child', or ituitively bigger    
    Args:  
        types0 (`type`): types0  
        types1 (`type`): types1  
    Returns:  
        return (`int`): comparison results  
    Raises:
    """
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

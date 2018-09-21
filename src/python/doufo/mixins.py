from functools import partial

# from .control import Functor
__all__ = ['FunctorArithmeticMixin', 'GetItemSingleBatchMixin']


class FunctorArithmeticMixin():
    """doufo.FunctorArithmeticMixin(): provide multiple arithmetic   
        method for the classes which includes this. Note, these   
        arithmetic methods are used on `Functor` objects, which 
        is not explicitly inheritted here. 
    Attributes:  
    """
    def __eq__(self, t):
        """doufo.FunctorArithmeticMixin.__eq__: `self == t`  
        Args:  
            `self`  
            t (`Functor`): another `Functor` object  
        Returns:  
            return (`bool`)
        Raises:
        """
        return self.fmap(lambda d: d == t)

    def __ne__(self, t):
        """doufo.FunctorArithmeticMixin.__eq__: `self != t`  
        Args:  
            `self`  
            t (`Functor`): another `Functor` object  
        Returns:  
            return (`bool`)
        Raises:
        """
        return not self.fmap(lambda d: d == t)



    def __req__(self, t):
        """doufo.FunctorArithmeticMixin.__req__: `t == self`  
        Args:  
            `self`  
            t (`Functor`): another `Functor` object  
        Returns:  
            return (`bool`)
        Raises:
        """
        return self.fmap(lambda d: t == d)

    def __mul__(self, t):
        """doufo.FunctorArithmeticMixin.__mul__: `self * t`  
        Args:  
            `self`  
            t (`Functor`): another `Functor` object  
        Returns:  
            return (`Functor`): multiplicating product
        Raises:
        """
        return self.fmap(lambda d: d * t)


    def __rmul__(self, t):
        """doufo.FunctorArithmeticMixin.__rmul__: `t * self`  
        Args:  
            `self`  
            t (`Functor`): another `Functor` object  
        Returns:  
            return (`Functor`): multiplicating product
        Raises:
        """
        return self.fmap(lambda d: t * d)
    
    def __add__(self, t):
        """doufo.FunctorArithmeticMixin.__add__: `self + t`  
        Args:  
            `self`  
            t (`Functor`): another `Functor` object  
        Returns:  
            return (`Functor`): summation
        Raises:
        """
        return self.fmap(lambda d: d + t)

    def __radd__(self, t):
        """doufo.FunctorArithmeticMixin.__radd__: `t + self`  
        Args:  
            `self`  
            t (`Functor`): another `Functor` object  
        Returns:  
            return (`Functor`): summation
        Raises:
        """
        return self.fmap(lambda d: t + d)

    def __sub__(self, t):
        """doufo.FunctorArithmeticMixin.__sub__: `self - t`  
        Args:  
            `self`  
            t (`Functor`): another `Functor` object  
        Returns:  
            return (`Functor`): difference
        Raises:
        """
        return self.fmap(lambda d: d - t)

    def __rsub__(self, t):
        """doufo.FunctorArithmeticMixin.__rsub__: `t - self`  
        Args:  
            `self`  
            t (`Functor`): another `Functor` object  
        Returns:  
            return (`Functor`): difference
        Raises:
        """
        return self.fmap(lambda d: t - d)

    def __truediv__(self, t):
        """doufo.FunctorArithmeticMixin.__div__: `self / t`  
        Args:  
            `self`  
            t (`Functor`): another `Functor` object  
        Returns:  
            return (`Functor`): quotient 
        Raises:
        """
        return self.fmap(lambda d: d / t)

    def __rtruediv__(self, t):
        """doufo.FunctorArithmeticMixin.__rdiv__: `t / self`  
        Args:  
            `self`  
            t (`Functor`): another `Functor` object  
        Returns:  
            return (`Functor`): quotient 
        Raises:
        """
        return self.fmap(lambda d: t / d)

    def __floordiv__(self, t):
        """doufo.FunctorArithmeticMixin.__floordiv__: `self // t`  
        Args:  
            `self`  
            t (`Functor`): another `Functor` object  
        Returns:  
            return (`Functor`): integer quotient 
        Raises:
        """
        return self.fmap(lambda d: d // t)

    def __rfloordiv__(self, t):
        """doufo.FunctorArithmeticMixin.__rfloordiv__: `t // self`  
        Args:  
            `self`  
            t (`Functor`): another `Functor` object  
        Returns:  
            return (`Functor`): integer quotient 
        Raises:
        """
        return self.fmap(lambda d: t // d)

    def __mod__(self, t):
        """doufo.FunctorArithmeticMixin.__mod__: `self % t`  
        Args:  
            `self`  
            t (`Functor`): another `Functor` object  
        Returns:  
            return (`Functor`): remainer
        Raises:
        """
        return self.fmap(lambda d: d % t)

    def __rmod__(self, t):
        """doufo.FunctorArithmeticMixin.__rmod__: `t % self`  
        Args:  
            `self`  
            t (`Functor`): another `Functor` object  
        Returns:  
            return (`Functor`): remainer
        Raises:
        """
        return self.fmap(lambda d: t % d)

    def __neg__(self):
        """doufo.FunctorArithmeticMixin.__mod__: `-self`  
        Args:  
            `self`  
        Returns:  
            return (`Functor`): remainer
        Raises:
        """
        return self.fmap(lambda d: -d)

# TODO desigin: is this a mixin or abstract class? 
# TODO refactor: refactor List/Tensor/Table to use this class
class GetItemSingleBatchMixin:
    def __getitem__(self, s):
        if is_get_single_item(s):
            return self._getitem_single(s)
        else:
            return self._getitem_batch(s)

def is_get_single_item(s):
    if isinstance(s, int):
        return True
    if isinstance(s, tuple) and all(map(lambda x: isinstance(x, int), s)):
        return True
    return False
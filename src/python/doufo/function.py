"""
Function is a functor that can map function f on its function self
to generate a new function. Thus, a series of functions can be composited by 
generating new PureFunction instance and finally get a complex function.
"""

import inspect
from abc import abstractmethod
from functools import partial, wraps
from typing import Callable, Optional
from multipledispatch import Dispatcher
import functools
from .control import Monad
from typing import TypeVar
import re
import traceback
__all__ = ['Function', 'WrappedFunction', 'func', 'identity', 'flip', 'singledispatch', 'SingleDispatchFunction', 'multidispatch', 'MultiDispatchFunction', 'tagfunc']

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
T = TypeVar('T')


class Function(Callable, Monad[Callable]):
    '''
       Abstract class of a wrapped function. Note, it alse has Monad parent class to make it 
       has methods such as fmap and ubox.
       
       Basically, a Function object acts as a normal function, but some cool features. 
       : Function(Callable, Monad[Callable])
    '''
    def __call__(self, *args, **kwargs):
        '''
            call an Function object by firstly unboxing it.

            : __call__(self, *args, **kwargs)
        '''
        return self.unbox()(*args, **kwargs)

    def bind(self, f: 'Function') -> 'Function':
        """
        this method allows a Function-based instance obj to bind another Function-based instance obj
        for example: the composite function :'f2(f1)' is equivalent to 'f1.bind(f2)/f2.fmap(f1)'
        :param f: a Function-class-based function
        :return: a Function-class-based function(is a composite func)
        """
        return f.fmap(self)

    @abstractmethod
    def fmap(self, f: Callable):
        """
        an abstract method for function composition
        :param f: a callable instance obj
        :return: a callable instance obj
        """
        pass

    @abstractmethod
    def unbox(self) -> Callable:
        """
        an abstract method for raw func retrieval
        :return: raw func
        """
        pass

    @property
    @abstractmethod
    def nargs(self) -> Optional[int]:
        """
        an abstract method for retrieval of the amount of params
        :return: the amount of params / if params is None ,return None
        """
        pass

    @property
    @abstractmethod
    def nouts(self) -> Optional[int]:
        """
        an abstract method for retrieval of the amount of Function-based class's result after' __call__()'
        :return: the amount of '__call__ 'result of the Function-based obj / if result is None ,return None
        """
        pass

    @property
    @abstractmethod
    def ndefs(self) -> Optional[int]:
        """
        an abstract method for retrieval of the amount of params which have default values
        :return: the amount of default values / if there is no default value ,return None
        """
        pass


def _nargs(f) -> Optional[int]:
    """
    the concrete implementation of Function.nargs
    :param f: a Function-based instance obj
    :return: amount of params
    """
    if isinstance(f, Function):
        return f.nargs
    spec = inspect.getfullargspec(f)
    if spec.varargs is not None:
        return None
    return len(spec.args)


def _ndefs(f):
    """
    the concrete implementation of 'Function.ndefs'
    :param f: a Function-based instance obj
    :return: amount of default params
    """
    if isinstance(f, Function):
        return f.ndefs
    spec = inspect.getfullargspec(f)
    if spec.defaults is None:
        return 0
    return len(spec.defaults)


def _nouts(f):
    """
    the concrete implementation of 'Function.nouts'
    :param f: a Function-based instance obj
    :return: amount of f's' __call__' results
    """
    if isinstance(f, Function):
        return f.nouts
    return None


def get_nargs(f: Callable, hint: Optional[int]) -> Optional[int]:
    """
    method '_nargs()' with hint
    :param f: a Function-based instance obj
    :param hint: a prediction of amount of args
    :return: hint first,without hint invoke '_nargs()'
    """
    if hint is not None:
        return hint
    else:
        return _nargs(f)


def get_ndefs(f: Callable, hint: Optional[int]) -> Optional[int]:
    """
    method '_ndefs()' with hint
    :param f: a Function-based instance obj
    :param hint: a prediction of amount of default args
    :return: hint first,without hint invoke '_ndefs()'
    """
    if hint is not None:
        return hint
    else:
        return _ndefs(f)


p_few = re.compile(r"[\w()]+ missing (\d+) required positional arguments?: [\w,']+")
p_many = re.compile(r"[\w()]+ takes (\d+) positional arguments?: but (\d+) were given")


class WrappedFunction(Function):
    """
    a WrappedFunction is a Function-based class that provides basic method implementation of Function.
    it supports '*args' that has a tuple for example:'*args = [(arg1,arg2,arg3...),arg4,arg5)'
    """
    def __init__(self, f, *, nargs=None, nouts=None, ndefs=None):
        '''
            __init__(self, f, *, nargs=None, nouts=None, ndefs=None)
        '''
        self.f = f
        self._nargs = get_nargs(f, nargs)
        self._nouts = nouts
        self._ndefs = get_ndefs(f, ndefs) or 0

    def __matmul__(self, f: 'Function') -> 'Function':
        """
        support the operation: 'f1@f2'
        :param f:a Function-based instance obj
        :return:a composite Function-based obj (see 'Function.fmap()')
        """
        return self.fmap(f)

    def __call__(self, *args, **kwargs):
        try:
            return self.unbox()(*args, **kwargs)
        except TypeError as e:
            if p_few.match(str(e)):
                if self.is_expand_needed(args):
                    return self.unbox()(*args[0], **kwargs)
                return WrappedFunction(partial(self.unbox(), *args, **kwargs),
                                       nargs=self.left_args(args),
                                       nouts=self.nouts,
                                       ndefs=self.left_defs(args))
            elif p_many.match(str(e)):
                result = self.unbox()(*args[:self.nargs], **kwargs)
                if self.nouts is not None and self.nouts > 1:
                    return (*result, *args[self.nargs:])
                return (result, *args[self.nargs:])
            else:
                raise e
        except Exception as e:
                traceback.print_exc()


    def fmap(self, f: 'WrappedFunction') -> 'WrappedFunction':
        """
        a concrete implementation of 'Function.fmap()'
        :param f: a WrappedFunction obj or WrappedFunction-based instance obj
        :return: a WrappedFunction instance obj
        """
        if not isinstance(f, WrappedFunction):
            f = WrappedFunction(f)
        return WrappedFunction(lambda *args, **kwargs: self(f(*args, **kwargs)), nargs=f.nargs, nouts=self.nouts)

    def is_expand_needed(self, args):
        if len(args) == 1 and isinstance(args[0], tuple):
            if self.nargs is None:
                return False
            if len(args[0]) + self.ndefs >= self.nargs:
                return True
        return False

    def left_args(self, args):
        if self.nargs is None:
            return None
        return self.nargs - len(args)

    def left_defs(self, args):
        if self.nargs is None:
            return self.ndefs
        if len(args) > self.nargs - self.ndefs:
            return self.ndefs - len(args) + self.nargs
        else:
            return self.ndefs

    def unbox(self):
        return self.f

    @property
    def nargs(self):
        return self._nargs

    @property
    def nouts(self):
        return self._nouts

    @property
    def ndefs(self):
        return self._ndefs


def nargs_left(nargs, ndefs, args) -> Optional[int]:
    if nargs is None:
        return None
    if ndefs is None:
        ndefs = 0
    return nargs - len(args)


def func(nargs: Optional[int] = None, nouts: Optional[int] = None, ndefs: Optional[int] = None):
    """
    decorates normal function to Function with (optional) number of arguments and outputs.
    :param 'nargs, nouts, ndefs' are amount of args ,func '_call_' results and default values.
    :return a wraps-decorated WrappedFunction obj
    """
    return lambda f: wraps(f)(WrappedFunction(f, nargs=nargs, nouts=nouts, ndefs=ndefs))


@func(nargs=1, nouts=1, ndefs=0)
def nargs(f) -> Optional[int]:
    return _nargs(f)


@func(nargs=1, nouts=1, ndefs=0)
def ndefs(f):
    return _ndefs(f)


@func(nargs=1, nouts=1, ndefs=0)
def nouts(f) -> Optional[int]:
    return _nouts(f)


identity = WrappedFunction(lambda x: x, nargs=1, nouts=1, ndefs=0)


class SingleDispatchFunction(WrappedFunction):
    """
    provide a uniform interface for 'funtools.singledispatch'
    easier to extend and expand
    according to the type registered (only refer to the first param) dispatch the concrete implementation.
    """
    def __init__(self, f, nargs=None, nouts=None, ndefs=None):
        super().__init__(functools.singledispatch(f),
                         nargs=get_ndefs(f, nargs),
                         nouts=nouts,
                         ndefs=get_ndefs(f, ndefs))
        self.registered = {}

    def register(self, *args, **kwargs):
        """
        an extended method for 'funtools.register'
        :param args:params passing to singledispatch-decorated function for inference
        :param kwargs:params passing to singledispatch-decorated function for inference
        :return:a decorator of 'f.register(type)'
        """
        result = self.f.register(*args, **kwargs)
        if len(args) > 0:
            self.registered[args[0]] = result
        return result


def singledispatch(*, nargs=None, nouts=None, ndefs=None):
    """
        an extended decorator for getting nargs,ndefs,nouts params.
        decorate both functools.singledispatch and func
    """

    def wrapper(f):
        return wraps(f)(SingleDispatchFunction(f, nargs=nargs, nouts=nouts, ndefs=ndefs))

    return wrapper


class MultiDispatchFunction(WrappedFunction):
    """
    provide a uniform interface for 'multipledispatch'
    easier to extend and expand
    according to the types registered (maybe two or more types) dispatch the concrete implementation.
    """
    def __init__(self, f, *, nargs=None, nouts=None):
        super().__init__(Dispatcher(f.__name__),
                         nargs=get_nargs(f, nargs),
                         nouts=nouts,
                         ndefs=get_ndefs(f, ndefs))
        if self.nargs is None:
            raise TypeError("Explict nargs is required for multidispatch.")
        self.register(*([object] * self.nargs))(f)

    def register(self, *types):
        """
        an extended method for 'mutipledispatch.dispatcher.register'
        :param types:types of vars
        :return:a decorator of 'f.register(*types)'
        """

        def decorator(f):
            self.f.add(types, f)
            return f

        return decorator


def multidispatch(*, nargs=None, nouts=None):
    """
    an extended decorator for getting nargs,nouts params.
    """
    def wrapper(f):
        return wraps(f)(MultiDispatchFunction(f, nargs=nargs, nouts=nouts))

    return wrapper


@func()
def flip(f: Callable) -> Function:
    """
    flip order of first two arguments to function.
    :param:  a callable function
    :return: a  WrappedFunction obj
    """
    nargs_, nouts_, ndefs_ = nargs(f), nouts(f), ndefs(f)
    return WrappedFunction(lambda *args, **kwargs: f(args[1], args[0], *args[2:], **kwargs),
                           nargs=nargs_, nouts=nouts_, ndefs=ndefs_)


class FunctionWithTag(Function):
    """
    to decorate a function so that it supports 'func[key]()'
    """
    def __init__(self, default_func, *, nargs=None, nouts=None, ndefs=None):
        self.default_func = default_func
        self._nargs = get_nargs(default_func, nargs)
        self._nouts = nouts
        self._ndefs = get_nargs(default_func, nouts)
        self.methods = {}

    def __getitem__(self, item):
        if item is None and not item in self.methods:
            return self.default_func
        return self.methods[item]

    def register(self, tag):
        """
        store the decorated function according to tag.
        register itself is a decorator which takes in a function and a type value
        """

        def wrapper(f):
            self.methods[tag] = f
            return f

        return wrapper

    def __call__(self, *args, **kwargs):
        return self.default_func(*args, **kwargs)

    @property
    def nargs(self):
        return self._nargs

    @property
    def ndefs(self):
        return self._ndefs

    @property
    def nouts(self):
        return self._nouts

    def fmap(self, f: 'WrappedFunction') -> 'WrappedFunction':
        if not isinstance(f, WrappedFunction):
            f = WrappedFunction(f)
        return WrappedFunction(lambda *args, **kwargs: self(f(*args, **kwargs)), nargs=f.nargs, nouts=self.nouts)

    def unbox(self):
        return self.default_func


def tagfunc(nargs=None, ndefs=None, nouts=None):
    """
    extended decorator for FunctionWithTag for getting the nargs,ndefs,nouts params.
    """
    def wrapper(f):
        return wraps(f)(FunctionWithTag(f, nargs=nargs, nouts=nouts, ndefs=ndefs))

    return wrapper

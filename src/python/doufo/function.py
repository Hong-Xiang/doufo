"""
PureFunction represents a pure function.
PureFunction is also a functor that can map function f on its function self
to generate a new function. Thus, a series of functions can be composited by 
generating new PureFunction instance and finally get a complex function.
"""

from doufo.control import Monad
from functools import partial, wraps
import functools
import inspect
from typing import Callable, Union, Generic, cast, Any

__all__ = ['PureFunction', 'func', 'identity', 'flip', 'singledispatch']

from typing import TypeVar
from numba import jit


A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')


class PureFunction(Callable[[A], B], Monad[Callable[[A], B]]):
	def __init__(self, f, *, nargs=None):
		self.f = f
		self.nargs = nargs or guess_nargs(f)
		#self.is_guessed_nargs = nargs is None
		#self.star_args_flag = guess_starargs(f)
		#self.nargs_flag = get_nargs_flag(nargs, nargs_flag)

	def __call__(self, *args, **kwargs) -> Union['PureFunction', B]:
		if len(args) == 0 and len(kwargs) == 0:
			return self.f()
		# if self.nargs_flag == False and self.star_args_flag == True:
		# 	else:
		# 		return PureFunction(partial(self.f, *args, **kwargs),nargs_flag=self.nargs_flag)
		# else:
		if self.nargs is None or len(args) < self.nargs:
			nargs_post = self.nargs - len(args) if self.nargs is not None else None
			return PureFunction(partial(self.f, *args, **kwargs),nargs=nargs_post)
		return self.f(*args, **kwargs)



	def bind(self, f: 'PureFunction') -> 'PureFunction':
		return self.fmap(f)

	def fmap(self, f: 'PureFunction') -> 'PureFunction':
		if not isinstance(f, PureFunction):
			f = PureFunction(f)
		return PureFunction(lambda *args, **kwargs: f(self.__call__(*args, **kwargs)), nargs=f.nargs)

	def __matmul__(self, f: 'PureFunction') -> 'PureFunction':
		def foo(*args):
			mid = f(*args[:f.nargs])
			return self(mid, *args[f.nargs:])
		return PureFunction(foo, nargs=self.nargs - f.nargs + 1)

	def unbox(self) -> Callable[..., B]:
		return self.f


def guess_nargs(f):
	if isinstance(f, PureFunction) and f.nargs is not None:
		return f.nargs
	spec = inspect.getfullargspec(f)
	if spec.varargs is not None:
		return None
	if spec.defaults is None:
		nb_defaults = 0
	else:
		nb_defaults = len(spec.defaults)
	return len(spec.args) - nb_defaults



class SingleDispatchFunction(PureFunction):
	def __init__(self, f):
		super().__init__(functools.singledispatch(f), nargs=guess_nargs(f))
		self.registed = {}

	def register(self, *args, **kwargs):
		result = self.f.register(*args, **kwargs)
		if len(args) > 0:
			self.registed[args[0]] = result
		return result


def singledispatch(f):
	"""
	decorate of both functools.singledispatch and func
	"""
	return SingleDispatchFunction(f)


def func(f: Callable) -> PureFunction:
	"""
	decorate normal function to PureFunction, for currying, @composite, fmap, etc.
	"""
	return cast(PureFunction, wraps(f)(PureFunction(f)))


identity: PureFunction[A, A] = func(lambda x: x)

def func_nargs(nargs = None):
	"""
	decorate normal function to PureFunction with parameter number.

	"""
	def inner(f: Callable) -> PureFunction:
		return cast(PureFunction, wraps(f)(PureFunction(f, nargs=nargs)))
	return inner

@func
def flip(f: Callable[[A], B]) -> PureFunction[B, A]:
	"""
	flip order of first two arguments to function.
	"""
	@wraps(f)
	def inner(*args, **kwargs):
		return f(args[1], args[0], *args[2:], **kwargs)
	return inner

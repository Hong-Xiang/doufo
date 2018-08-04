from doufo import Function, List
from doufo.tensor import Tensor
from abc import ABCMeta, abstractmethod
from functools import singledispatch

class BatchableFunction(Function, ABCMeta):
    def batched(self):
        @singledispatch
        def func(x):
            raise TypeError(f"Can't apply batched function on {type(x)}.")

        @func.reigster(List)
        def _(x):
            return self.batched_list(x)
        return func
        
    
    @classmethod
    def batched_list(self):
        def func(xs):
            return List([x for x in xs]) 
    
    @classmethod
    def batched_tensor(self):
        pass
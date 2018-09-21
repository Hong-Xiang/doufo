"""
Define method not implementation message
example:
def fsdafsadfas(bdsfabfjkabd) -> Any:
    raise TypeError(method_not_support_msg(fsdafsadfas, bdsfabfjkabd))
"""
__all__ = ['method_not_support_msg']
def method_not_support_msg(func, obj) -> str:
    """
        Define method not implementation message
        method_not_support_msg(func, obj) -> 'List[Any]'
    """
    return f"{func} for {type(obj)} is not implemented yet."

from functools import wraps
from typing import Callable

__all__ = [
    'invoke_once',
    'set_precall_method'
]

def invoke_once(func):
    has_run = False
    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal has_run
        if not has_run:
            has_run = True
            return func(*args, **kwargs)
        return None
    return wrapper


def set_precall_method(method: Callable = lambda _ : None):
    def precall_method(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            method(self)
            return func(self, *args, **kwargs)
        return wrapper
    return precall_method
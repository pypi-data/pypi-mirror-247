from functools import wraps
import functools
from .dto import SPRequest
from typing import List


class sproute(object):
    def __init__(self, path, methods):
        self.path = path
        self.methods: List[str] = methods

    def __call__(self, original_func):
        decorator_self = self

        def wrappee(*args, **kwargs):
            if type(args[0]) == SPRequest:
                if args[0].requestType not in self.methods:
                    raise ValueError("Method not allowed")
            return original_func(*args, **kwargs)

        return wrappee

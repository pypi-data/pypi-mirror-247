from time import time
from functools import wraps
from flask import session


def timeit(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        start_time = session["start_time"]
        result = func(*args, **kwargs)
        duration = int(round(time() * 1000)) - start_time
        result["duration"] = f"{duration} ms"
        return result
    return _wrapper
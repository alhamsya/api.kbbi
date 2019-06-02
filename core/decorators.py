from functools import wraps

from core.hooks import resp_err, resp_success, check_connection

def is_connection(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not check_connection():
            return resp_err("No internet connection", 0, 444)

        return f(*args, **kwargs)
    return wrapper

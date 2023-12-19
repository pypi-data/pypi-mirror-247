import time
from functools import wraps


def debug_info(action_name: str, module_name: str = 'UNDEFINED'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            module_str = action_name[:24].ljust(24, ' ')
            action_str = module_name[:32].ljust(32, ' ')
            start_time = time.time()
            print(f"[{module_str}] {action_str}", end='')
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f" -> Elapsed time: {elapsed_time:.4f} seconds")
            return result
        return wrapper
    return decorator


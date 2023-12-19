import functools

from .datahub_engine import DataHubEngine

class DataHubValues(DataHubEngine):

    def __call__(self, fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            self._get_caller_settings()
            ret = self._retrieve_data()
            result = fn(ret, *args, **kwargs)
            return result
        return wrapper

import abc
import datetime


class Context(abc.ABC):

    def __init__(self, *args, **kwargs):
        self._product_path = None
        self._processing_start_time = datetime.datetime.utcnow()
        self._product = None
        self._error = None

    def register_exception(self, error):
        pass

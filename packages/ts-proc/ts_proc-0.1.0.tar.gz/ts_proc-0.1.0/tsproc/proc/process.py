import abc
import typing

from tsproc.proc.context import Context
from tsproc.proc.module import module, OutputModule


def make_registry():
    processes = {}

    def register_context(context: typing.Type[Context], product_type=None):
        def register_process(proc: typing.Type['Process']):
            processes[proc.__name__] = {'cls': proc, 'context': context, 'product_type': product_type}
            return proc

        return register_process

    register_context.processes = processes
    return register_context


register_process = make_registry()
process_registry = register_process


class Process(abc.ABC):
    def __init__(self, *args, **kwargs):
        pass

    @module(execution_order=999)
    def output_module(self):
        return OutputModule()


def get_modules_from_process(proc: Process):
    """Get all methods in the process decorated with the "module" decorator."""
    methods = [getattr(proc, name) for name in dir(proc)
               if hasattr(getattr(proc, name), "module") and getattr(proc, name).module
               ]
    return sorted(methods, key=lambda x: x.execution_order)

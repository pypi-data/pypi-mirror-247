from tsproc.proc.dummy.dummy_context import DummyContext
from tsproc.proc.dummy.dummy_module import DummyOutputModule
from tsproc.proc.module import module
from tsproc.proc.process import register_process


@register_process(context=DummyContext, product_type=None)
class DummyProcess:

    @module(execution_order=1, command=None)
    def do_something(self):
        return DummyOutputModule()

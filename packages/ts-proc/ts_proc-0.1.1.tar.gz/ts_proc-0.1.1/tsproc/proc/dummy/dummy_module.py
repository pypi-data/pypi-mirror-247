from tsproc.dto.io import OutputBuilder, Output
from tsproc.proc.context import Context
from tsproc.proc.module import OutputModule


class DummyOutputModule(OutputModule):

    def output(self, context: Context) -> Output:
        builder = OutputBuilder(**{key: getattr(context, key) for key in vars(context)})
        return builder.build()

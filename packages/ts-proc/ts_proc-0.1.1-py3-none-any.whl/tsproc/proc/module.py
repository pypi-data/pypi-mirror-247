import abc
import logging
import typing
from typing import final

from tsproc.dto.io import Output, OutputBuilder
from tsproc.proc.command import Command
from tsproc.proc.context import Context


def module(execution_order, command=None):
    def process_module(func):
        func.execution_order = execution_order
        func.command = command
        func.module = True
        return func

    return process_module


class Module(abc.ABC):

    @final
    def execute(self, context, command, *args, **kwargs) -> typing.Optional[Output]:
        logging.info(f"Executing module {type(self).__name__}")

        logging.info(f"Initialzing context")
        self._init_context(context, *args, **kwargs)
        logging.info(f"Context to command")
        self._context_to_command(context=context, command=command)
        logging.info(f"Updating command")
        self._update_command(command=command)
        logging.info(f"Command to context")
        self._command_to_context(context=context, command=command)
        logging.info(f"Generating output")
        output = self._output(context)

        logging.info(f"Execution of module {type(self).__name__} complete")
        return output

    @abc.abstractmethod
    def init_context(self, context: Context, *args, **kwargs):
        pass

    @final
    def _init_context(self, context: Context, *args, **kwargs):
        self.init_context(context=context, *args, **kwargs)

    @abc.abstractmethod
    def context_to_command(self, context: Context, command: Command):
        pass

    @final
    def _context_to_command(self, context: Context, command: Command):
        self.context_to_command(context=context, command=command)

    @abc.abstractmethod
    def update_command(self, command: Command):
        pass

    @final
    def _update_command(self, command: Command):
        self.update_command(command=command)

    @abc.abstractmethod
    def command_to_context(self, context: Context, command: Command):
        pass

    @final
    def _command_to_context(self, context: Context, command: Command):
        self.command_to_context(context=context, command=command)

    @abc.abstractmethod
    def output(self, context: Context) -> typing.Optional[Output]:
        return None

    @final
    def _output(self, context: Context) -> typing.Optional[Output]:
        return self.output(context=context)


class ProcModule(Module):

    @final
    def init_context(self, context: Context, *args, **kwargs):
        pass

    @abc.abstractmethod
    def context_to_command(self, context: Context, command: Command):
        pass

    @abc.abstractmethod
    def update_command(self, command: Command):
        pass

    @abc.abstractmethod
    def command_to_context(self, context: Context, command: Command):
        pass

    @final
    def output(self, context: Context) -> typing.Optional[Output]:
        pass


class InitModule(Module):

    @abc.abstractmethod
    def init_context(self, context: Context, *args, **kwargs):
        pass

    @final
    def command_to_context(self, context: Context, command: Command):
        pass

    @final
    def context_to_command(self, context: Context, command: Command):
        pass

    @final
    def update_command(self, command: Command):
        pass


class OutputModule(Module):
    @final
    def init_context(self, context: Context, *args, **kwargs):
        pass

    @final
    def command_to_context(self, context: Context, command: Command):
        pass

    @final
    def context_to_command(self, context: Context, command: Command):
        pass

    @final
    def update_command(self, command: Command):
        pass

    @abc.abstractmethod
    def output(self, context: Context) -> Output:
        pass


import logging

from tsproc.dto.io import Input, Output
from tsproc.dto.types import Product
from tsproc.proc.command import Command
from tsproc.proc.context import Context
from tsproc.proc.dummy.dummy_process import DummyProcess
from tsproc.proc.module import Module, OutputModule
from tsproc.proc.process import process_registry, get_modules_from_process


class ProcessEngine:
    def __init__(self):
        self._process = None

    def register_process(self, input: Input):
        """
        Process factory
        """
        try:
            product_type = Product(input.product_type)
            logging.info(f"Registrered product_type {product_type.name}")
            processes = [p['cls'] for k, p in process_registry.processes.items() if p['product_type'] == product_type]
            if len(processes) == 1:
                process = processes[0]
            else:
                process = processes[0]
                logging.warning(
                    f"Found {len(processes)} processes registred for product_type {product_type}: Selecting {process.__name__} for further use")
        except ValueError as e:
            logging.warning(f"Invalid input product_type {input.product_type}.")
            process = DummyProcess
        self.process = process

    def execute(self) -> Output:
        logging.info(f"Executing process {self.process.__name__}")
        proc = self.process()
        context = self._init_context()
        process_methods = get_modules_from_process(proc)
        for process_method in process_methods:
            module: Module = process_method()
            command = self._init_command(process_method)
            try:
                output = module.execute(context=context, command=command)
                if isinstance(module, OutputModule):
                    logging.info(f"Finished execution of process {self.process.__name__}")
                    return output
            except Exception as e:
                logging.exception(e)
                raise e
        raise RuntimeError(f"No output module found for process {self.process.__name__}")

    def _init_context(self) -> Context:
        context = process_registry.processes[self.process.__name__]['context']
        logging.info(f"Instantiating context {context.__name__}")
        return context()

    def _init_command(self, process_method) -> Command:
        command = process_method.command
        if command is not None:
            logging.info(f"Instantiating command {type(command).__name__}")
        else:
            logging.info(f"No registered command for process method '{process_method.__name__}'")
        return command

    @property
    def process(self):
        return self._process

    @process.setter
    def process(self, value):
        self._process = value

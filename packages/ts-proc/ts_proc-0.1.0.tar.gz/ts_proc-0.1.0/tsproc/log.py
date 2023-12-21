import logging
import sys


class InMemoryHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.log_messages = []

    def emit(self, record):
        log_message = self.format(record)
        self.log_messages.append(log_message)


def setup_logging():
    # Configure the logging settings
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Create an instance of MemoryHandler
    memory_handler = InMemoryHandler()
    memory_handler.setLevel(logging.INFO)
    memory_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Add the MemoryHandler to the root logger
    logging.getLogger().addHandler(memory_handler)


def custom_excepthook(exc_type, exc_value, exc_traceback): # TODO
    # Log unhandled exception
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


# Set custom excepthook
sys.excepthook = custom_excepthook

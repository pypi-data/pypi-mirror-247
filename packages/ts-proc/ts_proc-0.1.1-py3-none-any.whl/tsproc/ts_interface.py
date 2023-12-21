import json
import logging
import os

from tsproc import settings
from tsproc.dto.io import Input, Output
from tsproc.log import setup_logging, InMemoryHandler
from tsproc.proc.process_engine import ProcessEngine


class TsInterface:
    """This is the API that wraps the software"""

    @staticmethod
    def load() -> None:
        """Invoked once before any calls to predict"""
        # Set up logging
        setup_logging()
        logging.info('Loading API')

    @staticmethod
    def predict(input: Input) -> Output:
        engine = ProcessEngine()
        engine.register_process(input=input)
        output = engine.execute()
        return output

    @staticmethod
    def validate() -> bool:
        with open(os.path.join(settings.RESOURCE_DIR, 'test.json')) as json_file:
            data = json.load(json_file)
        return data['value'] == 1337

    @staticmethod
    def get_log():
        memory_handler = next(
            handler for handler in logging.getLogger().handlers if isinstance(handler, InMemoryHandler))
        log_messages = memory_handler.log_messages
        return log_messages


if __name__ == '__main__':
    ts = TsInterface()
    ts.load()
    ts.validate()
    input = Input(product_path='test', product_type=0, batch_size=24, image_size=256)
    output = ts.predict(input)
    print(output)

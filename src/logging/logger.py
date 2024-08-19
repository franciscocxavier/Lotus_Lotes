import logging

class LoggingConfig:
    def __init__(self):
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(self.formatter)

    def configure_logging(self):
        logging.getLogger().addHandler(self.console_handler)
        logging.getLogger().setLevel(logging.INFO)



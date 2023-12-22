import logging
import inspect

grey = "\x1b[38;20m"
yellow = "\x1b[33;20m"
red = "\x1b[31;20m"
bold_red = "\x1b[31;1m"
cyan = "\x1b[36;20m"
green = "\x1b[32;20m"
blue = "\x1b[34;20m"
orange = "\x1b[38;5;202m"
reset = "\x1b[0m"


class CustomFormatter(logging.Formatter):
    def __init__(self, filename, lineno):
        super().__init__()
        self.filename = filename
        self.lineno = lineno

    def format(self, record):
        first = f"❯ {self.filename} ({self.lineno}) | "
        date = "%(asctime)s.%(msecs)03d \n"
        msg = "%(message)s"

        FORMATS = {
            logging.INFO: cyan + first + green + date + reset + msg,
        }
        log_fmt = FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class LocalLogger:
    def reset(self, filename, lineno):
        self.logger = logging.getLogger("simple_example")
        self.logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        # Create a formatter and add it to the handler
        formatter = logging.Formatter(
            fmt=f"> {filename} ({lineno}) | %(asctime)s.%(msecs)03d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler.setFormatter(CustomFormatter(filename, lineno))

        # Add the handler to the logger
        self.logger.addHandler(console_handler)

    def print(self, msg):
        # for item in inspect.stack():
        #     pprint(item.filename)
        stack = inspect.stack()

        filename = stack[2].filename
        filename = filename.replace("\\", "/")
        filename = filename.split("/")[-1]
        lineno = stack[2].lineno
        self.reset(filename, lineno)

        self.logger.info(msg)
        self.logger.handlers.clear()


pprint = print


def print(msg=""):
    # if not type(msg) == str:
    #     msg = f"\n{msg}"
    msg = f"{msg}\n"
    LocalLogger().print(msg)

import logging
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)


class CustomFormatter(logging.Formatter):
    LEVEL_COLORS = {
        "DEBUG": Fore.BLUE,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.MAGENTA,
    }

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created)
        return dt.strftime("%Y/%m/%d %H:%M:%S:%f")[:-3]

    def format(self, record):
        record.class_method = f"{record.module}.{record.funcName}"
        log_color = self.LEVEL_COLORS.get(record.levelname, "")
        record.levelname = f"{log_color}{record.levelname}"
        return super().format(record)


formatter = CustomFormatter("[%(levelname)s] %(asctime)s - %(class_method)s - %(message)s")

handler = logging.StreamHandler()
handler.setFormatter(formatter)

log = logging.getLogger("custom_logger")
log.setLevel(logging.DEBUG)
log.addHandler(handler)

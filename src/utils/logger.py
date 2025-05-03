import logging
from datetime import datetime


class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created)
        return dt.strftime("%Y/%m/%d %H:%M:%S:%f")[:-3]

    def format(self, record):
        record.class_method = f"{record.module}.{record.funcName}"
        return super().format(record)


formatter = CustomFormatter("[%(levelname)s] %(asctime)s - %(class_method)s - %(message)s")

handler = logging.StreamHandler()
handler.setFormatter(formatter)

log = logging.getLogger("custom_logger")
log.setLevel(logging.DEBUG)
log.addHandler(handler)

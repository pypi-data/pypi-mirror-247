import os
from datetime import datetime

from loguru import logger


def get_pid():
    return os.getpid()


class LogService:
    def __init__(self, file_name=None, rotation=None):
        self.logger = logger
        if file_name is None:
            file_name = datetime.now().strftime("%Y%m%d") + '.log'
        if rotation is None:
            rotation = '1024MB'
        self.logger.add(file_name, rotation=rotation, encoding="GB2312", enqueue=True, backtrace=True, diagnose=True)


log_service = LogService()

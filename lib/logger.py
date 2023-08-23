# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : Zhang Zhanqi
# @FILE     : logger.py
# @Time     : 2021/8/5 14:39

import logging
from typing import Optional, IO

from loguru import logger


class InterceptFormatter(logging.Formatter):

    def formatTime(self, **kwargs):
        return ""


class InterceptHandler(logging.StreamHandler):

    def __init__(self, stream: Optional[IO[str]] = ...) -> None:
        super().__init__(stream)
        self.formatter = InterceptFormatter()

    def setFormatter(self, fmt: logging.Formatter) -> None:
        pass

    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

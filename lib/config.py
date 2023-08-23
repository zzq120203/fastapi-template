# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : zhangzhanqi
# @FILE     : config.py
# @Time     : 2021/11/4 17:38
from fastapi.logger import logger

from pydantic_settings import BaseSettings
from pydantic import RedisDsn, PostgresDsn, MySQLDsn


class Settings(BaseSettings):
    PROJECT_NAME: str = 'Grain Warehouse API'

    DATABASE_URL: PostgresDsn | MySQLDsn

    REDIS_URL: RedisDsn | None = None


settings = Settings()
logger.info(settings)

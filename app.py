# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : zhangzhanqi
# @FILE     : app.py
# @Time     : 2023/8/2 10:47

from fastapi_plugin.offline import FastAPI

from api import router as api
from lib.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
)

app.include_router(api)

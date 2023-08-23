# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : zhangzhanqi
# @FILE     : __init__.py.py
# @Time     : 2023/8/22 17:55
from fastapi import APIRouter

from api.person import router as person
from api.user import router as user
from db.database import create_db_and_tables

router = APIRouter(prefix='/api/v1')


@router.on_event("startup")
async def on_startup():
    await create_db_and_tables()


router.include_router(user)
router.include_router(person)

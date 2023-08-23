# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : zhangzhanqi
# @FILE     : __init__.py.py
# @Time     : 2023/8/15 9:44
from fastapi import Depends
from fastapi_plugin.db import UUIDIDMixin
from fastapi_plugin.users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend
from fastapi_plugin.users.db import BaseUserTable, BaseUserDatabase, BaseRoleTable
from fastapi_plugin.users.manager import BaseUserManager
from fastapi_plugin.users.router import BaseUserRouter, BaseRoleRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import Base, get_async_session


# 默认使用BaseRoleTable即可， 并绑定 Base
class RoleTable(BaseRoleTable, Base):
    pass


# 默认使用BaseUserTable即可， 并绑定 Base
class UserTable(BaseUserTable, Base):
    pass


secret = "ba2d990ca71bb6050380f7d866ae7ffdea85be0039d3f4c9aa730b24ee2426c7"


class UserManager(UUIDIDMixin, BaseUserManager):
    pass


# 获取用户表数据库管理实例
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield BaseUserDatabase(session, UserTable, RoleTable)


async def get_user_manager(
        user_db: BaseUserDatabase = Depends(get_user_db),
):
    yield UserManager(user_db)


# 创建 openapi 登录模块
bearer_transport = BearerTransport(tokenUrl=f"/api/v1/auth/jwt/login")


# 采用 jwt 存储 token, 也可选 RedisStrategy
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=secret, lifetime_minutes=60)


# 创建认证管理实例
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# 创建角色路由管理实例
role_router = BaseRoleRouter(
    get_user_manager=get_user_manager,
)

# 创建用户路由管理实例
router = BaseUserRouter(
    auth_backend=auth_backend,
    get_user_manager=get_user_manager,
)

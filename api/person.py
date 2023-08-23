# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : zhangzhanqi
# @FILE     : person.py
# @Time     : 2023/8/2 16:22
from fastapi import APIRouter, Security, Depends

from db.tables.person import router as person
from db.user import router as user
from db.user.permssions import operator, super_user

# 获取用户 depend
get_current_active_user = user.current_user()

router = APIRouter(tags=["person"])

# 绑定获取 person 的路由，所有权限可访问
router.include_router(person.get_object_router(), dependencies=[Depends(get_current_active_user)])
# 绑定创建 person 的路由，使用Security设置权限operator
router.include_router(person.create_object_router(),
                      dependencies=[Security(get_current_active_user, scopes=[operator])])
# 绑定更新 person 的路由，使用Security设置权限operator
router.include_router(person.update_object_router(),
                      dependencies=[Security(get_current_active_user, scopes=[operator])])
# 绑定删除 person 的路由，使用Security设置权限super_user
router.include_router(person.delete_object_router(),
                      dependencies=[Security(get_current_active_user, scopes=[super_user])])

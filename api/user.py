# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : zhangzhanqi
# @FILE     : user.py
# @Time     : 2023/8/2 17:09
from fastapi import APIRouter, Security, Depends

from db.user import router as user, role_router as role
from db.user.permssions import super_user

get_current_active_user = user.current_user()

router = APIRouter(tags=["user"])

# 绑定获取 user 的路由，所有权限可访问
router.include_router(user.get_current_user_router(), dependencies=[Depends(get_current_active_user)])
# 绑定获取 user 的路由，不设置用户权限，此处为登录接口
router.include_router(user.get_auth_router())
# 绑定获取 user 的路由，使用Security设置权限super_user，此处为注册接口
router.include_router(user.create_object_router(),
                      dependencies=[Security(get_current_active_user, scopes=[super_user])])
# 绑定获取 Permission 的路由，使用Security设置权限super_user
router.include_router(user.get_permission_router(),
                      dependencies=[Security(get_current_active_user, scopes=[super_user])])

# 绑定获取 role 的路由，使用Security设置权限super_user
router.include_router(role.get_object_router(), dependencies=[Security(get_current_active_user, scopes=[super_user])])
# 绑定删除 role 的路由，使用Security设置权限super_user
router.include_router(role.delete_object_router(),
                      dependencies=[Security(get_current_active_user, scopes=[super_user])])
# 绑定创建 role 的路由，使用Security设置权限super_user
router.include_router(role.create_object_router(),
                      dependencies=[Security(get_current_active_user, scopes=[super_user])])
# 绑定更新 role 的路由，使用Security设置权限super_user
router.include_router(role.update_object_router(),
                      dependencies=[Security(get_current_active_user, scopes=[super_user])])

# 用户路由
router.include_router(user.get_object_router(), dependencies=[Security(get_current_active_user, scopes=[super_user])])
router.include_router(user.update_object_router(),
                      dependencies=[Security(get_current_active_user, scopes=[super_user])])

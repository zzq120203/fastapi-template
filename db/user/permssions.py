# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : zhangzhanqi
# @FILE     : permssions.py
# @Time     : 2023/8/15 9:52
from fastapi_plugin.users.permission import Permission

# 定义两个权限，operator 和 super
operator = Permission("operator")
super_user = Permission("super")

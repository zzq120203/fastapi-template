# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : zhangzhanqi
# @FILE     : person.py
# @Time     : 2023/8/2 16:11
import uuid
from datetime import datetime
from typing import Optional

from fastapi import Depends, Query
from fastapi_plugin.db import (
    SQLAlchemyBaseObjectTableUUID, schemas,
    UUIDIDMixin, BaseObjectManager,
    SQLAlchemyObjectDatabase, BaseObjectRouter
)
from pydantic import Field, BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlalchemy import String, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base, get_async_session


# 电话号校验
class ChinesePhoneNumber(PhoneNumber):
    default_region_code = "CN"
    phone_format = 'NATIONAL'


# 创建 PersonTable ，并绑定 Base， 命名表为 person
# 继承来自 SQLAlchemyBaseObjectTableUUID 的字段 id(uuid)、name、create_time、insert_time
class PersonTable(SQLAlchemyBaseObjectTableUUID, Base):
    __tablename__ = 'person'
    phone: Mapped[str] = mapped_column(
        String(length=256), index=True, nullable=True, doc='电话'
    )
    company: Mapped[str] = mapped_column(
        String(length=256), index=True, nullable=True, doc='公司'
    )


# 创建 person 基础类，定义 phone、company 可空，并设置默认值
class BasePerson(BaseModel):
    phone: Optional[ChinesePhoneNumber] = Field(None, alias='phone')
    company: Optional[str] = Field(None, alias='company')


# 创建 peron 的数据返回类，继承 BasePerson 的 phone、company，并重写 create_time， 使其序列化时使用别名 insert_time
class Person(BasePerson, schemas.BaseObjectRead[uuid.UUID]):
    create_time: datetime = Field(..., serialization_alias='insert_time')


# 创建 peron 的数据创建类，继承 BasePerson 的 phone、company
class PersonCreate(BasePerson, schemas.BaseObjectCreate):
    pass


# 创建 peron 的数据更新类，继承 BasePerson 的 phone、company
class PersonUpdate(BasePerson, schemas.BaseObjectUpdate):
    pass


class PersonManager(UUIDIDMixin, BaseObjectManager[PersonTable, uuid.UUID]):
    pass


# 创建 person 管理类
async def get_person_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyObjectDatabase(session, PersonTable)


async def get_person_manager(user_db: SQLAlchemyObjectDatabase = Depends(get_person_db)):
    yield PersonManager(user_db)


# 创建用户路由类，集成 BaseObjectRouter
# 重写 get_objects_query 函数，增加查询的条件，此处会自动同步到 openapi
class PersonRouter(BaseObjectRouter):
    async def get_objects_query(
            self,
            name: Optional[str] = Query(None),
            phone: Optional[str] = Query(None),
            company: Optional[str] = Query(None),
    ):
        query = []

        if name:
            query.append(PersonTable.name.like(f"%{name}%"))
        if phone:
            query.append(PersonTable.phone == phone)
        if company:
            query.append(PersonTable.company.like(f"%{company}%"))
        return and_(*query) if query else None


# 创建 person 路由，完成 Person、 PersonCreate、 PersonUpdate 的绑定，以完善 openapi
router = PersonRouter(
    get_person_manager,
    name="person",
    schema_or=Person,
    schema_oc=PersonCreate,
    schema_ou=PersonUpdate
)

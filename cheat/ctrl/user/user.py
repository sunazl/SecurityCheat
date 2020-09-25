'''
用户增删改查
Created on 2020年9月24日

@author: xiandan
'''
import copy
import sys
import uuid
from datetime import datetime

from django.db import transaction
from django.db.models import OneToOneRel
from django.forms import CharField

from cheat import entry
from cheat.models import User, UserInfo


# 注册
@transaction.atomic()
def user_sign_in(req):
    user_number = "123"
    user_info_base = {}
    sign_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_id = str(uuid.uuid4()).replace('-', '')
    user_info_base["user_id"] = user_id
    user_info_base["user_name"] = req["user_name"]
    user_info_base["nick_name"] = req["nick_name"]
    user_info_base["user_number"] = user_number
    user_info_base["sign_time"] = sign_time

    # 用户全部信息
    user_info = copy.deepcopy(user_info_base)
    user_info["mail"] = req["mail"]
    user_info["password"] = req["password"]
    # 用户基础信息
    is_had = User.objects.filter(user_name=req["user_name"])
    if is_had:
        return {"result": "用户名已存在"}

    User(**user_info_base).save()
    # 用户完整信息
    UserInfo(**user_info).save()
    UserInfo.objects.get()
    entry.test()

    values = User.objects.filter(user_name=req["user_name"]).values()
    return values


# 注销账号
@transaction.atomic()
def user_delete(req):
    user_id = req["user_id"]
    User.objects.filter(user_id=user_id).delete()

    # UserInfo.objects.filter(user_id=user_id).delete()
    return "用户注销成功"


# 更新信息
def user_update(req):
    data = trans_req_model("User", req)
    u = User.objects.filter(req["user_id"])
    u.update(**data)


# 获取用户详细信息
def user_get_info(req):
    userid = req["user_id"]
    user_info_values = UserInfo.objects.filter(user_id=userid).values()
    return user_info_values


def general_token():
    num = 0

    return num


def login(req):
    user_name = req["user_name"]
    password = req["password"]

    count = UserInfo.objects.filter(user_name=user_name, password=password).count()
    # 登录成功返回一个token 和一个私钥
    # requests.

    if count:
        token = ""
        return token


# 匹配req和数据库中的字段,可直接进行update等使用
def trans_req_model(model_name, req):
    path = "cheat.models"
    __import__(path)
    # 实例化后 加载类
    obj = sys.modules[path]
    class_ = obj.__getattribute__(model_name)
    fields = class_._meta.get_fields()

    fields_list = []
    for field in fields:
        if isinstance(field,OneToOneRel):
            fields_list.append(str(field.field).split(".")[-1])
        else:
            fields_list.append(str(field).split(".")[-1])

    data = {}
    for field in fields_list:
        if req.__contains__(field):
            data[field] = req[field]

    return data

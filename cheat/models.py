# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.db import models


# 用户表
class User(models.Model):
    user_id = models.CharField("用户id,不对外展示", max_length=32, primary_key=True)
    user_name = models.CharField("用户名", max_length=128)
    nick_name = models.CharField("昵称", max_length=128)
    user_number = models.CharField("数字账号", max_length=128)
    sign_time = models.DateTimeField("注册日期", auto_now_add=True)


# # 用户详细信息
class UserInfo(User):
    mail = models.CharField("邮箱", max_length=128)
    password = models.CharField("密码", max_length=128)


# 登录记录
class Login(models.Model):
    user_id = models.CharField("用户id,不对外展示", max_length=32, primary_key=True)
    login_time = models.DateTimeField("最近一次登录时间", auto_now_add=True)
    login_time_last = models.DateTimeField("上次登录时间", auto_now_add=True)
    online_avg = models.CharField("平均在线时长", max_length=256)
    online_time = models.CharField("共计在线时长", max_length=256)



# 账号密码表
class Passwd(models.Model):
    user_id = models.CharField("用户id,不对外展示", max_length=32, primary_key=True)
    passwd = models.CharField("密码", max_length=128)
    update_time = models.DateTimeField("修改日期", auto_now_add=True)


# 无状态的  每次发送必须带token
class Token(models.Model):
    token_id = models.CharField("token_id", max_length=32, primary_key=True)
    user_id = models.CharField("用户id,不对外展示", max_length=32)


# 好友表
class friends(models.Model):
    user_id = models.CharField("用户id,不对外展示", max_length=32, primary_key=True)
    friend_id = models.CharField("好友id及昵称", max_length=4096)
    meet_date = models.DateTimeField("加好友日期", auto_now_add=True)
    black_list = models.CharField("黑名单的用户id", max_length=32)
    special_care = models.CharField("特别关心好友", max_length=32)

# 群组表
class group(models.Model):
    group_id = models.CharField("用户id,不对外展示", max_length=32, primary_key=True)
    group_name = models.CharField("群名称", max_length=32)
    create_time = models.DateTimeField("创建日期", auto_now_add=True)
    group_member = models.CharField("群成员", max_length=4096)
    join_method = models.CharField("进群方式", max_length=64)
    admin_id = models.CharField("群主id", max_length=32)
    is_everyone_invite = models.BooleanField("是否允许成员邀请")
    black_list = models.CharField("黑名单的用户id", max_length=32)

'''
Json工具类
Created on 2020年9月24日

@author: xiandan
'''

# -*- coding: utf-8 -*-
import json
from datetime import date, datetime
from secur.encry_util import encry_util


# 对datetime类型数据处理
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def encode_method(method_name, p_data):
    if method_name != "user_connect":
        p_data = encry_util.rsa_decrypt_by_req(p_data)
        return p_data

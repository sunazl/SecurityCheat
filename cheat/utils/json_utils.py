'''
Json工具类
Created on 2020年9月24日

@author: xiandan
'''

# -*- coding: utf-8 -*-
import json
from datetime import date, datetime

# 对datetime类型数据处理
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

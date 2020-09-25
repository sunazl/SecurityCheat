'''
项目启动时 扫描
Created on 2020年9月25日
'''
# -*- coding: utf-8 -*-
import os
from configparser import ConfigParser

# 扫描ctrl类
from SecurityCheat.settings import BASE_DIR


def scan_annotation():
    sdst = os.path.dirname(os.path.abspath(__file__))
    sdst = os.path.join(sdst, 'ctrl')
    dfile = os.path.join(BASE_DIR, 'ctrl.ini')
    deldir(dfile)
    write(sdst, dfile)
    return None


def deldir(path):
    if os.path.exists(path):
        os.remove(path)


# 写入文件
def write(sdst, dfile):
    config = ConfigParser()
    config.add_section("ctrl")
    config = scan_ctrl(sdst, config)
    config.write(open(dfile, "w"))


# 目录遍历器
def scan_ctrl(path, config):
    for root, dirs, files in os.walk(path):
        fpath = os.path.relpath(root, BASE_DIR)
        for i in files:
            config.set("ctrl", i, fpath)
    return config

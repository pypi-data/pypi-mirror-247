#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random, string
from test_script import *
from lcyframe.libs import cprint, utils


def get_imagecode(*args, **kwargs):
    """
    获取验证码:
    """
    headers = {}
    files = {}
    params = {
        "uuid": "",     # str,必填,随机串
        }
    return send(methed="get", url="/imagecode", params=params, headers=headers, files=files)

def post_imagecode(*args, **kwargs):
    """
    图形验证码:
    """
    headers = {}
    files = {}
    params = {
        "stype": 0,     # int,选填,类型
        "uuid": "",     # str,必填,随机串
        "code": "",     # str,必填,图形验证码
        }
    return send(methed="post", url="/imagecode", params=params, headers=headers, files=files)


def get_smscode(*args, **kwargs):
    """
    获取短信验证码:
    """
    headers = {}
    files = {}
    params = {
        "stype": 0,     # int,选填,类型，预留
        "uuid": "",     # str,必填,随机串，预留
        "mobile": "",     # str,必填,手机号
        }
    return send(methed="get", url="/smscode", params=params, headers=headers, files=files)

def post_smscode(*args, **kwargs):
    """
    短信验证码:
    """
    headers = {}
    files = {}
    params = {
        "stype": 0,     # int,选填,类型，预留
        "uuid": "",     # str,必填,随机串，预留
        "mobile": "",     # str,必填,随机串
        "code": "",     # str,必填,验证码
        }
    return send(methed="post", url="/smscode", params=params, headers=headers, files=files)


def get_download(*args, **kwargs):
    """
    下载:下载资源,返回文件是binary数据
    """
    headers = {}
    files = {}
    params = {
        "stype": 0,     # int,必填,类型，1下载授权文件
        "name": "",     # str,必填,文件名
        }
    return send(methed="get", url="/download", params=params, headers=headers, files=files)


def get_update_status(*args, **kwargs):
    """
    当前升级状态:engine_status值，1正常；2准备；3就绪；4升级中
    """
    headers = {}
    files = {}
    params = {
        }
    return send(methed="get", url="/update_status", params=params, headers=headers, files=files)

def post_update_status(*args, **kwargs):
    """
    确认升级:
    """
    headers = {}
    files = {}
    params = {
        }
    return send(methed="post", url="/update_status", params=params, headers=headers, files=files)


def get_update_status_list(*args, **kwargs):
    """
    升级记录:
    """
    headers = {}
    files = {}
    params = {
        "page": 0,     # int,选填,翻页码
        "count": 0,     # int,选填,每页显示条数
        }
    return send(methed="get", url="/update_status/list", params=params, headers=headers, files=files)


def batch_groups():
    """
    测试簇
    一键测试
    """
    get_imagecode()       # 获取验证码
    post_imagecode()       # 图形验证码
    get_smscode()       # 获取短信验证码
    post_smscode()       # 短信验证码
    get_download()       # 下载
    get_update_status()       # 当前升级状态
    post_update_status()       # 确认升级
    get_update_status_list()       # 升级记录
    

if __name__ == "__main__":
    # 获取验证码
    get_imagecode()
    # 图形验证码
    post_imagecode()
    # 获取短信验证码
    get_smscode()
    # 短信验证码
    post_smscode()
    # 下载
    get_download()
    # 当前升级状态
    get_update_status()
    # 确认升级
    post_update_status()
    # 升级记录
    get_update_status_list()
    
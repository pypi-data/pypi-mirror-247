#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random, string
from test_script import *
from lcyframe.libs import cprint, utils


def get_websocket(*args, **kwargs):
    """
    websocket链接测试:
    """
    headers = {}
    files = {}
    params = {
        "nickname": "",     # string,选填,用户昵称
        }
    return send(methed="get", url="/websocket", params=params, headers=headers, files=files)


def batch_groups():
    """
    测试簇
    一键测试
    """
    get_websocket()       # websocket链接测试
    

if __name__ == "__main__":
    # websocket链接测试
    get_websocket()
    
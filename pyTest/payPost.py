# -*- coding: utf-8 -*-
# !/usr/bin/env python


import time
import sys
import os
import threading
import tmjLog as lxLog
import json
import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0",
    "Content-Type": "application/json"
}


def admin_queryUser():
    try:
        registerDict = {}
        registerDict['acctName'] = ""
        registerDict['telephone'] = ''
        registerDict['toPageNum'] = 1
        registerDict['pageSize'] = 20
        registerStr = json.dumps(registerDict)
        r = requests.post('http://127.0.0.1:8080/admin/queryUser', headers=headers, data=registerStr, verify=False)
        # lxLog.getDebugLog()(r.text)
        loginRecvDict = json.loads(r.text)
        if '1' != loginRecvDict['result']:
            lxLog.getDebugLog()(unicode.format(u"注册失败，号码：{1}，错误代码{0}", loginRecvDict['result'], phone))
        else:
            lxLog.getDebugLog()(u'注册成功：%s', phone)
    except Exception as err:
        lxLog.getDebugLog()(u"异常:%s", str(err))


def opt_queryAccount():
    try:
        registerDict = {}
        registerDict['acctName'] = ""
        registerDict['telephone'] = ""
        registerDict['toPageNum'] = 1
        registerDict['pageSize'] = 20
        registerStr = json.dumps(registerDict)
        r = requests.post('http://127.0.0.1:21012/opt/queryAccount', headers=headers, data=registerStr, verify=False)
        lxLog.getDebugLog()(r.text)

    except Exception as err:
        lxLog.getDebugLog()(u"异常:%s", str(err))


def opt_queryBill():
    try:
        registerDict = {}
        registerDict['acctName'] = ""
        registerDict['type'] = ""
        registerDict['date'] = ""
        registerDict['telephone'] = ""
        registerDict['toPageNum'] = 1
        registerDict['pageSize'] = 20
        registerStr = json.dumps(registerDict)
        r = requests.post('http://127.0.0.1:21012/opt/queryBill', headers=headers, data=registerStr, verify=False)
        lxLog.getDebugLog()(r.text)

    except Exception as err:
        lxLog.getDebugLog()(u"异常:%s", str(err))


if __name__ == '__main__':
    opt_queryBill()

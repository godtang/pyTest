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
    "Content-Type": "application/json",
    "jwtToken": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIzIiwiZXhwIjoxNTk2MDA1NDExLCJvcGVyYXRvcklkIjoiMyIsImlhdCI6MTU5NTQwNTQxMCwianRpIjoiOGE2N2Q3ZjktOTAwYi00ZDQyLWFkNzktOTE4NTZkNDM5Njk4In0.x0lscg5KQw0-X5qcJrliZ1h6SUlk6lZHPCUfUt7JgYI"
}


def admin_queryUser():
    result = []
    retObj = {}
    retObj['acctName'] = ""
    retObj['telephone'] = ''
    retObj['pageNum'] = 1
    retObj['pageSize'] = 20
    result.append(retObj)
    result.append('http://127.0.0.1:21012/admin/queryUser')
    return result


def opt_queryAccount():
    result = []
    retObj = {}
    retObj['jwtToken'] = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIzIiwiZXhwIjoxNTk1Mzg1MTE0LCJvcGVyYXRvcklkIjoiMyIsImlhdCI6MTU5NTM4NTA1NCwianRpIjoiNzE3OTgzNzEtZDZiNS00YzhhLTg0MWItYjgyNzg4YzM3M2I3In0.4AQRnBUC0borqWGs-HwpF45BamT4gzh59r6nDdXYlF4"
    retObj['acctName'] = ""
    retObj['telephone'] = ""
    retObj['pageNum'] = 1
    retObj['pageSize'] = 20
    result.append(retObj)
    result.append('http://127.0.0.1:21000/opt/queryAccount')
    return result


def opt_queryBill():
    result = []
    retObj = {}
    retObj['acctName'] = ""
    retObj['type'] = ""
    retObj['date'] = ""
    retObj['telephone'] = ""
    retObj['pageNum'] = 1
    retObj['pageSize'] = 20
    result.append(retObj)
    result.append('http://127.0.0.1:21000/opt/queryBill')
    return result


def opt_queryFundRecord():
    result = []
    retObj = {}
    retObj['acctName'] = ""
    retObj['type'] = ""
    retObj['date'] = ""
    retObj['telephone'] = ""
    retObj['pageNum'] = 1
    retObj['pageSize'] = 20
    result.append(retObj)
    result.append('http://127.0.0.1:21012/opt/queryFundRecord')
    return result

def opt_vendorStatistics():
    result = []
    retObj = {}
    retObj['acctName'] = ""
    retObj['acctId'] = ""
    retObj['startDate'] = "2020-07-20"
    retObj['endDate'] = "2020-07-20"
    retObj['type'] = "2"
    retObj['pageNum'] = 1
    retObj['pageSize'] = 20
    result.append(retObj)
    result.append('http://192.168.3.80:21000/opt/vendorStatistics')
    return result

def acct_queryBalance():
    result = []
    retObj = {}
    retObj['baseUserId'] = "1"
    result.append(retObj)
    result.append('http://127.0.0.1:21010/queryBalance')
    return result

def acct_queryBillList():
    result = []
    retObj = {}
    retObj['baseUserId'] = "1"
    retObj['yearAndMonth'] = "2020-07"
    retObj['billTypeCode'] = ""
    retObj['pageNum'] = 1
    retObj['pageSize'] = 20
    result.append(retObj)
    result.append('http://127.0.0.1:21010/acct/queryBillList')
    return result

def acct_queryBillDetail():
    result = []
    retObj = {}
    retObj['baseUserId'] = "1"
    retObj['billId'] = "1"
    result.append(retObj)
    result.append('http://127.0.0.1:21010/acct/queryBillDetail')
    return result

def acct_queryMBillStatistics():
    result = []
    retObj = {}
    retObj['baseUserId'] = "1"
    retObj['yearAndMonth'] = "2020-07"
    retObj['direct'] = "0"
    retObj['pageNum'] = 1
    retObj['pageSize'] = 20
    result.append(retObj)
    result.append('http://127.0.0.1:21010/acct/queryMBillStatistics')
    return result

def acct_queryYBillStatistics():
    result = []
    retObj = {}
    retObj['baseUserId'] = "1"
    retObj['year'] = "2020"
    retObj['direct'] = "0"
    result.append(retObj)
    result.append('http://127.0.0.1:21010/acct/queryYBillStatistics')
    return result

def acct_modifyPayPassword():
    result = []
    retObj = {}
    retObj['acctId'] = "1"
    retObj['oldPayPwd'] = "11111asdfasd0"
    retObj['payPwd'] = "111111"
    result.append(retObj)
    result.append('http://127.0.0.1:21010/acct/modifyPayPassword')
    return result

def acct_queryBillType():
    result = []
    retObj = {}
    result.append(retObj)
    result.append('http://192.168.3.80:21000/acct/queryBillType')
    return result

def login():
    retObj = {}
    retObj['telephone'] = "12345000000"
    retObj['password'] = "f317424473928b0b840b0c9f4ee8f97e"
    postStr = json.dumps(retObj)
    r = requests.post("http://192.168.3.80:21012/userLogin", headers=headers, data=postStr, verify=False)
    lxLog.getDebugLog()(r.text)

def home_dataStatistics():
    result = []
    retObj = {}
    result.append(retObj)
    result.append('http://192.168.3.80:30000/home/dataStatistics')
    return result

def manufacturer():
    result = []
    retObj = {}
    retObj['title'] = 'asd'
    retObj['pageNum'] = 1
    retObj['pageSize'] = 20
    result.append(retObj)
    result.append('http://192.168.3.80:30000/product/productList')
    return result

if __name__ == '__main__':
    try:
        #login()
        result = manufacturer()
        postStr = json.dumps(result[0])
        r = requests.post(result[1], headers=headers, data=postStr, verify=False)
        lxLog.getDebugLog()(r.text)

    except Exception as err:
        lxLog.getDebugLog()(u"异常:%s", str(err))

# -*- coding: utf-8 -*-
# !/usr/bin/env python
import pprint
import time
import sys
import os
import threading
import tmjLog as lxLog
import json
import requests


def print_json(data):
    print(json.dumps(data, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))


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
    retObj[
        'jwtToken'] = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIzIiwiZXhwIjoxNTk1Mzg1MTE0LCJvcGVyYXRvcklkIjoiMyIsImlhdCI6MTU5NTM4NTA1NCwianRpIjoiNzE3OTgzNzEtZDZiNS00YzhhLTg0MWItYjgyNzg4YzM3M2I3In0.4AQRnBUC0borqWGs-HwpF45BamT4gzh59r6nDdXYlF4"
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
    retObj['pageNum'] = 10
    retObj['pageSize'] = 10
    result.append(retObj)
    result.append('http://127.0.0.1:21012/queryBill')
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
    retObj['acctId'] = "0110805041967"
    retObj['timestamp'] = "1"
    result.append(retObj)
    result.append('http://127.0.0.1:21010/queryBalance')
    return result


def acct_queryBillList():
    result = []
    retObj = {}
    retObj['baseUserId'] = "10815291"
    retObj['yearAndMonth'] = "2020-08"
    retObj['billTypeCode'] = ""
    retObj['pageNum'] = 2
    retObj['pageSize'] = 5
    result.append(retObj)
    result.append('http://127.0.0.1:21010/queryBillList')
    #result.append('http://192.168.3.128:21010/queryBillList')
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
    retObj['baseUserId'] = 10805042
    retObj['yearAndMonth'] = "2020-07"
    retObj['direct'] = 1
    result.append(retObj)
    result.append('http://127.0.0.1:21010/queryMBillStatistics')
    return result


def acct_queryYBillStatistics():
    result = []
    retObj = {}
    retObj['baseUserId'] = 10805042
    retObj['year'] = "2020"
    retObj['direct'] = 1
    result.append(retObj)
    result.append('http://127.0.0.1:21010/queryYBillStatistics')
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
    retObj['cmpId'] = 1
    result.append(retObj)
    result.append('http://192.168.3.80:30000/home/dataStatistics')
    return result

def addProduct():
    result = []
    retObj = {}
    retObj['title'] = "酒鬼槟郎"
    retObj['retailPrice'] = 123
    retObj['agtPrice'] = 321
    retObj['shopRebate'] = 3.3
    retObj['pdtPicUrl'] = "fff"
    retObj['pdtDesc'] = "酒不醉人人自醉"
    retObj['cmpId'] = 1
    retObj['operatorId'] = 1
    result.append(retObj)
    result.append('http://192.168.3.80:30000/product/addProduct')
    return result

def productList():
    result = []
    retObj = {}
    retObj['pageNum'] = 1
    retObj['pageSize'] = 20
    retObj['title'] = "槟榔"
    retObj['cmpId'] = 1
    result.append(retObj)
    result.append('http://192.168.3.80:30000/product/productList')
    return result


def manufacturer():
    result = []
    retObj = {}
    retObj['productId'] = 6
    retObj['title'] = "酒鬼槟郎"
    retObj['retailPrice'] = 123
    retObj['agtPrice'] = 321
    retObj['shopRebate'] = 2.2
    retObj['pdtPicUrl'] = "fff"
    retObj['pdtDesc'] = "酒不醉人人自醉"
    retObj['cmpId'] = 5
    result.append(retObj)
    result.append('http://192.168.3.80:30000/product/editProduct')
    return result


def agent():
    result = []
    retObj = {}
    retObj['agtId'] = 5
    retObj['cpmId'] = 8
    result.append(retObj)
    result.append('http://192.168.3.80:30000/agent/agentInfo')
    return result


def agent_addAgent():
    result = []
    retObj = {}
    retObj['companyName'] = "测试代理商ID"
    retObj['contacts'] = "1"
    retObj['telephone'] = "2221"
    retObj['telNumber'] = "1"
    retObj['province'] = "110000"
    retObj['city'] = "110100"
    retObj['area'] = "110107"
    retObj['addr'] = "1"
    retObj['sProvince'] = "1"
    retObj['sCity'] = "110000"
    retObj['sArea'] = "110100"
    retObj['orgId'] = "110107"
    retObj['businessLicense'] = "1"
    retObj['status'] = "1"
    retObj['cmpId'] = 1
    result.append(retObj)
    result.append('http://192.168.3.80:30000/agent/addAgent')
    return result


def agent_editAgent():
    result = []
    retObj = {}
    retObj['agtId'] = 9
    retObj['companyName'] = "1"
    retObj['contacts'] = "1"
    retObj['telephone'] = "2221"
    retObj['telNumber'] = "1"
    retObj['province'] = "1"
    retObj['city'] = "1"
    retObj['area'] = "1"
    retObj['addr'] = "1"
    retObj['sProvince'] = "1"
    retObj['sCity'] = "1"
    retObj['sArea'] = "1"
    retObj['orgId'] = "1"
    retObj['businessLicense'] = "1"
    retObj['status'] = "1"
    retObj['cmpId'] = 1
    result.append(retObj)
    result.append('http://192.168.3.80:30000/agent/editAgent')
    return result

def agent_enableAgent():
    result = []
    retObj = {}
    retObj['agtId'] = 5
    retObj['status'] = 8
    result.append(retObj)
    result.append('http://192.168.3.80:30000/agent/enableAgent')
    return result

def agent_enableCmpName():
    result = []
    retObj = {}
    retObj['cmpId'] = 1
    retObj['agtId'] = 5
    retObj['companyName'] = "asdfkkk"
    result.append(retObj)
    result.append('http://192.168.3.80:30000/agent/enableCmpName')
    return result

if __name__ == '__main__':
    try:
        # login()
        result = addProduct()
        postStr = json.dumps(result[0])
        # print(json.dumps(result[0], sort_keys=True, indent=4))
        r = requests.post(result[1], headers=headers, data=postStr, verify=False)
        lxLog.getDebugLog()(json.dumps(json.loads(r.text),
                                       sort_keys=True,
                                       indent=4,
                                       ensure_ascii=False))

    except Exception as err:
        lxLog.getDebugLog()(u"异常:%s", str(err))

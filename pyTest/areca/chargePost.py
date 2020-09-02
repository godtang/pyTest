# -*- coding: utf-8 -*-
# !/usr/bin/env python
import pprint
import time
import sys
import os
import threading
import sys

sys.path.append("..")
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


def chargeList():
    result = []
    retObj = {}
    retObj['pageNum'] = 1
    retObj['pageSize'] = 20
    retObj['chargeId'] = 1
    retObj['cmpId'] = 1
    retObj['paymentTime'] = '2020-07-07'
    result.append(retObj)
    result.append('http://192.168.3.80:30000/charge/chargeList')
    return result

def addRecord():
    result = []
    retObj = {}
    retObj['acctId'] = '和天下'
    retObj['rechargeAmt'] = 1
    retObj['amount'] = 2
    retObj['paymentTime'] = '2020-07-07'
    retObj['voucherNo'] = 'RA2020-7-25007'
    retObj['voucherPicUrl'] = '和天下'
    retObj['rmk'] = '和天下'
    retObj['createBy'] = 1
    retObj['cmpId'] = 1
    retObj['operatorId'] = 1

    result.append(retObj)
    result.append('http://192.168.3.80:30000/charge/addRecord')
    return result

def editRecord():
    result = []
    retObj = {}
    retObj['chargeId'] = 1
    retObj['acctId'] = '1234xcvasdf'
    retObj['rechargeAmt'] = 1
    retObj['amount'] = 2
    retObj['paymentTime'] = '2020-07-07'
    retObj['voucherNo'] = '2020-7-25 16:49:07'
    retObj['voucherPicUrl'] = 'fsdfasf'
    retObj['rmk'] = '和天下'
    result.append(retObj)
    result.append('http://192.168.3.80:30000/charge/editRecord')
    return result



if __name__ == '__main__':
    try:
        # login()
        result = chargeList()
        postStr = json.dumps(result[0])
        # print(json.dumps(result[0], sort_keys=True, indent=4))
        r = requests.post(result[1], headers=headers, data=postStr, verify=False)
        lxLog.getDebugLog()(json.dumps(json.loads(r.text),
                                       sort_keys=True,
                                       indent=4,
                                       ensure_ascii=False))
        # lxLog.getDebugLog()(r.text)

    except Exception as err:
        lxLog.getDebugLog()(u"异常:%s", str(err))

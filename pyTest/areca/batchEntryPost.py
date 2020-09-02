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


def batchList():
    result = []
    retObj = {}
    retObj['pageNum'] = 1
    retObj['pageSize'] = 0
    retObj['batchNum'] = ""
    retObj['batchName'] = ''
    result.append(retObj)
    result.append('http://192.168.3.80:30000/batch/batchList')
    return result

def addBatch():
    result = []
    retObj = {}
    retObj['operatorId'] = 3
    retObj['pdtName'] = '小龙王槟榔123'
    retObj['pdtId'] = 1
    retObj['pdtPrice'] = 35
    retObj['prodDate'] = '2010-07-22'
    retObj['totalAmount'] = 11111111
    retObj['usedAmount'] = 112
    retObj['validity'] = 123
    retObj['qrTotalCount'] = 1111
    retObj['ruleId'] = 2
    retObj['ruleType'] = 1
    retObj['maxScale'] = 80
    retObj['avgScale'] = 80
    retObj['minScale'] = 70
    retObj['createBy'] = 1
    retObj['cmpId'] = 1

    result.append(retObj)
    result.append('http://192.168.3.80:30000/batch/addBatch')
    return result

def editBatchInfo():
    result = []
    retObj = {}
    retObj['batchNum'] = '120200818634491'
    retObj['cmpId'] = 1
    retObj['pdtId'] = 1
    retObj['pdtName'] = '小龙王槟榔十多个地方是个好的方式更好的发'
    retObj['pdtPrice'] = 500
    retObj['prodDate'] = '2010-08-17'
    retObj['totalAmount'] = 11111
    retObj['usedAmount'] = 0
    retObj['validity'] = 60
    retObj['qrTotalCount'] = 10
    result.append(retObj)
    result.append('http://192.168.3.80:30000/batch/editBatchInfo')
    return result

def editBatchRule():
    result = []
    retObj = {}
    retObj['cmpId'] = 1
    retObj['operatorId'] = 2
    retObj['batchNum'] = '120200814408929'
    retObj['batchName'] = '和天下'
    retObj['ruleId'] = 1
    retObj['ruleType'] = 0
    retObj['maxScale'] = 2
    retObj['avgScale'] = 3
    retObj['minScale'] = 4
    result.append(retObj)
    result.append('http://192.168.3.80:30000/batch/editBatchRule')
    return result

def generateQRCode():
    result = []
    retObj = {}
    retObj['batchNum'] = '420200820747638'
    result.append(retObj)
    result.append('http://192.168.3.80:30000/batch/generateQRCode')
    return result

def downloadQRCode():
    result = []
    retObj = {}
    retObj['batchNum'] = '420200820747638'
    result.append(retObj)
    result.append('http://192.168.3.80:30000/batch/downloadQRCode')
    postStr = json.dumps(result[0])
    req = requests.post(result[1], headers=headers, data=postStr, verify=False)
    if True:
        with open('file.txt', 'wb') as file:
            file.write(req.content)

def batchInfo():
    result = []
    retObj = {}
    retObj['batchNum'] = '12020072512804'
    result.append(retObj)
    result.append('http://192.168.3.80:30000/batch/batchInfo')
    return result

def queryAmount():
    result = []
    retObj = {}
    retObj['cmpId'] = 1
    retObj['queryType'] = 0
    retObj['pdtId'] = 1
    retObj['qrTotalCount'] = 20
    retObj['ruleType'] = 0
    retObj['ruleId'] = 2
    retObj['avgScale'] = 3
    result.append(retObj)
    result.append('http://192.168.3.80:30000/batch/queryAmount')
    return result


if __name__ == '__main__':
    try:
        # login()
        result = downloadQRCode()
        postStr = json.dumps(result[0])
        # print(json.dumps(result[0], sort_keys=True, indent=4))
        r = requests.post(result[1], headers=headers, data=postStr, verify=False)
        lxLog.getDebugLog()(json.dumps(json.loads(r.text),
                                       sort_keys=True,
                                       indent=4,
                                       ensure_ascii=False))

    except Exception as err:
        lxLog.getDebugLog()(u"异常:%s", str(err))

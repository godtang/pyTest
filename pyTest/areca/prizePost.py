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


def prizeList():
    result = []
    retObj = {}
    retObj['pageNum'] = 1
    retObj['pageSize'] = 20
    retObj['cmpId'] = 1
    retObj['pName'] = '芙蓉'
    result.append(retObj)
    result.append('http://192.168.3.80:30000/prize/prizeList')
    return result
def enablePrize():
    result = []
    retObj = {}
    retObj['exchangeProductId'] = 2
    retObj['status'] = 1
    result.append(retObj)
    result.append('http://192.168.3.80:30000/prize/enablePrize')
    return result


if __name__ == '__main__':
    try:
        # login()
        result = enablePrize()
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

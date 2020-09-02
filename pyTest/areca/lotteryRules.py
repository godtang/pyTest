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


def ruleList():
    result = []
    retObj = {}
    retObj['pageNum'] = 1
    retObj['pageSize'] = 20
    retObj['cmpId'] = 1
    retObj['ruleName'] = '芙蓉'
    result.append(retObj)
    result.append('http://192.168.3.80:30000/lotterySetting/ruleList')
    return result

def addRule():
    result = []
    retObj = {}
    retObj['ruleName'] = '和天下'
    retObj['maxScale'] = 20
    retObj['avgScale'] = 1
    retObj['minScale'] = 1
    retObj['ruleExplain'] = '测试'
    retObj['operatorId'] = 1
    retObj['cmpId'] = 1
    result.append(retObj)
    result.append('http://192.168.3.80:30000/lotterySetting/addRule')
    return result

def editRule():
    result = []
    retObj = {}
    retObj['ruleId'] = 2
    retObj['ruleName'] = '抽奖规则01'
    retObj['maxScale'] = 66
    retObj['avgScale'] = 55
    retObj['minScale'] = 44
    retObj['ruleExplain'] = '收到公司的该多少个发给时大概多少公司根深蒂固十多个是个导师工读生公司德国大使馆时大概多少根深蒂固导师工读生根深蒂固导师工读生感受'
    retObj['operatorId'] = 1
    retObj['cmpId'] = 1
    result.append(retObj)
    result.append('http://192.168.3.80:30000/lotterySetting/editRule')
    return result

def enableRule():
    result = []
    retObj = {}
    retObj['ruleId'] = 2
    retObj['status'] = 123
    result.append(retObj)
    result.append('http://192.168.3.80:30000/lotterySetting/enableRule')
    return result

def enableRuleName():
    result = []
    retObj = {}
    retObj['ruleName'] = '测试'
    result.append(retObj)
    result.append('http://192.168.3.80:30000/lotterySetting/enableRuleName')
    return result

def relateRule():
    result = []
    retObj = {}
    retObj['ruleId'] = 2
    retObj['cmpId'] = 55
    result.append(retObj)
    result.append('http://192.168.3.80:30000/lotterySetting/relateRule')
    return result


if __name__ == '__main__':
    try:
        # login()
        result = editRule()
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

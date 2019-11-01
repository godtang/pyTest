# -*- coding: utf-8 -*-
#!/usr/bin/env python



import time
import sys
import os
import threading
import tmjLog as lxLog
import json
import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class lxRegister(threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    def run(self):        
        index = 0
        registerDict = {}
        while index < 1000:
            phone = '12399%03d%03d' % (self.threadID, index)
            registerDict['telephone'] = phone
            registerDict['verifyCode'] = '0000'
            registerDict['nickname'] = phone
            registerDict['password'] = 'f317424473928b0b840b0c9f4ee8f97e'
            registerDict['resisterCome'] = '1'
            registerStr = json.dumps(registerDict)
            r = requests.post('http://121.41.16.130:12000/sso/v1/register', data=registerStr, verify=False)
            #lxLog.getDebugLog()(r.text)
            loginRecvDict = json.loads(r.text)
            if '1' != loginRecvDict['result']:
                lxLog.getDebugLog()(unicode.format(u"注册失败，号码：{1}，错误代码{0}", loginRecvDict['result'], phone))
            else:
                lxLog.getDebugLog()(u'注册成功：%s', phone)
            index = index + 1

if __name__ == '__main__':
    threads = []
    index = 0
    while index < 200:
        # 创建新线程
        thread = lxRegister(index)
        # 开启新线程
        thread.start()
        threads.append(thread)
        index = index + 1
    # 等待所有线程完成
    for t in threads:
        t.join()
    print "Exiting Main Thread"
    

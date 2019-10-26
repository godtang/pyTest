# -*- coding: utf-8 -*-
import tmjLog as lxLog
import hashlib
import json
import requests
import time
import asyncore, socket
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys
sys.path.append('D:/CODE/IM_project/im-comm-proto/src/main/resources/python')
import LoginTokenAuth_pb2


loginAddr = 'https://192.168.3.149:12000/sso/v2/loginSimple'
getGateAddr = "http://47.99.117.9:5001/gate/addr/api/getGateAddr"
md5Salt = 'eccbc87e4b5ce2fe28308fd9f2a7baf312tt390t9874'
loginName = '13980557094'
loginPassword = 'Bo3mKqgSr0hYIc7r'

class HTTPClient(asyncore.dispatcher):
 
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( (host, port) )   
        self.buffer = 'bbbbbbbbb'
    def handle_connect(self):
        print 'handle_connect'
        pass
 
    def handle_close(self):
        print 'handle_close'
        self.close()
 
    def handle_read(self):
        print 'handle_read'
        print self.recv(8192)
        self.buffer = 'aaaaaaaaaaaa'
 
    def writable(self):
        print 'writable'
        return (len(self.buffer) > 0)
 
    def handle_write(self):
        print 'handle_write'
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]


def login():
    #登陆
    loginDict = {}
    loginDict['telephone'] = loginName
    loginDict['devType'] = 1
    loginDict['password'] = hashlib.md5(md5Salt+loginPassword).hexdigest()
    loginDict['devBrand'] = 'vivo'
    loginStr = json.dumps(loginDict)
    lxLog.getDebugLog()(unicode.format(u'登陆发送数据：{0}', loginStr))
    r = requests.post(loginAddr, data=loginStr, verify=False)
    lxLog.getDebugLog()(r.text)
    loginRecvDict = json.loads(r.text)
    if '1' != loginRecvDict['result']:
        lxLog.getDebugLog()(unicode.format(u"登陆失败，错误代码{0}", loginRecvDict['result']))
        return

    #寻址
    '''getGateDict = {}
    getGateDict['useId'] = loginRecvDict['userId']
    getGateDict['devType'] = '1'
    getGateDict['authToken'] = loginRecvDict['authToken']
    getGateDict['version'] = '0.1'
    getGateStr = json.dumps(getGateDict)
    lxLog.getDebugLog()(unicode.format(u'寻址发送数据：{0}', getGateStr))
    r = requests.post(loginAddr, data=loginStr, verify=False)
    lxLog.getDebugLog()(r.text)'''



    client = HTTPClient('192.168.3.149', 9091)
    asyncore.loop()

    lxLog.getDebugLog()('异常退出了')

if __name__ == '__main__':
    while True:
        try:
            login()
        except Exception as err:
            lxLog.getDebugLog()(u"main异常退出:%s", str(err))
        finally:
            time.sleep(10000)



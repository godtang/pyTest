# -*- coding: utf-8 -*-
import tmjLog as lxLog
import hashlib
import json
import requests
import time
import struct
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

class APPClient(asyncore.dispatcher):

    def __init__(self, host, port, userInfo):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.userInfo = userInfo
        self.buffer = ''
        self.login()

    def handle_connect(self):
        print 'handle_connect'

    def handle_close(self):
        print 'handle_close'
        self.close()

    def handle_read(self):
        print 'handle_read'
        data = self.recv(8192)
        interfaceCode, recvBody = self.appUnpack(data)
        if 1002 == interfaceCode:
            self.loginRecv(recvBody)

    def writable(self):
        print 'writable'
        return (len(self.buffer) > 0)

    def handle_write(self):
        print 'handle_write'
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

    def appPack(self, data, routeCode, interfaceCode):
        # 自定义包头

        #
        # MARS包头
        marsBodyLen = 8 + len(data)

        # 打包
        result = struct.pack('!iiiiiii', 20, 8, interfaceCode, 0, marsBodyLen, routeCode, interfaceCode)
        result += data
        return result

    def appUnpack(self, data):
        marsHeadLen, clientVersion, marsCommand, marsSN, marsBodyLen, routeCode, interfaceCode, responceSN = -1, -1, -1, -1, -1, -1, -1, -1

        # 自定义包头

        # MARS包头

        # 打包
        length = len(data)
        if length >= 32:
            marsHeadLen, clientVersion, marsCommand, marsSN, marsBodyLen, routeCode, interfaceCode, responceSN = struct.unpack('!iiiiiiii', data[0:32])
            recvBody = data[32:]
        else:
            lxLog.getDebugLog()(u"appUnpack 接收数据较短，无法解析")
            return None
        return interfaceCode, recvBody

    def login(self):
        loginTokenAuthRequest = LoginTokenAuth_pb2.LoginTokenAuthRequest()
        loginTokenAuthRequest.devId = 'aaaaaaa'
        loginTokenAuthRequest.userId = self.userInfo['userId']
        loginTokenAuthRequest.authToken = self.userInfo['authToken']
        loginTokenAuthRequest.devType = 1
        loginTokenAuthRequest.devBrand = 'vivo'
        try:
            data = loginTokenAuthRequest.SerializeToString()
            sendData = self.appPack(data,99902,1002)
            self.buffer = sendData
        except Exception as err:
            lxLog.getDebugLog()(u"main异常退出:%s", str(err))

    def loginRecv(self, data):
        loginTokenAuthResponse = LoginTokenAuth_pb2.LoginTokenAuthResponse()
        loginTokenAuthResponse.ParseFromString(data)
        pass


def login():
    # 登陆
    loginDict = {}
    loginDict['telephone'] = loginName
    loginDict['devType'] = 1
    loginDict['password'] = hashlib.md5(md5Salt + loginPassword).hexdigest()
    loginDict['devBrand'] = 'vivo'
    loginStr = json.dumps(loginDict)
    lxLog.getDebugLog()(unicode.format(u'登陆发送数据：{0}', loginStr))
    r = requests.post(loginAddr, data=loginStr, verify=False)
    lxLog.getDebugLog()(u'登陆接收数据:%s', r.text)
    loginRecvDict = json.loads(r.text)
    if '1' != loginRecvDict['result']:
        lxLog.getDebugLog()(unicode.format(u"登陆失败，错误代码{0}", loginRecvDict['result']))
        return

    # 寻址
    '''
    getGateDict = {}
    getGateDict['useId'] = loginRecvDict['userId']
    getGateDict['devType'] = '1'
    getGateDict['authToken'] = loginRecvDict['authToken']
    getGateDict['version'] = '0.1'
    getGateStr = json.dumps(getGateDict)
    lxLog.getDebugLog()(unicode.format(u'寻址发送数据：{0}', getGateStr))
    r = requests.post(loginAddr, data=loginStr, verify=False)
    lxLog.getDebugLog()(r.text)
    '''

    userInfo = {}
    userInfo['userId'] = loginRecvDict['userId']
    userInfo['authToken'] = loginRecvDict['authToken']

    client = APPClient('192.168.3.149', 9091, userInfo)
    asyncore.loop()

    lxLog.getDebugLog()(u'异常退出了')


if __name__ == '__main__':
    '''
    #注册
    index = 0
    registerDict = {}
    while index < 1:
        phone = '1239999%04d' % index
        registerDict['telephone'] = phone
        registerDict['verifyCode'] = '0000'
        registerDict['nickname'] = phone
        registerDict['password'] = 'f317424473928b0b840b0c9f4ee8f97e'
        registerDict['resisterCome'] = '1'
        registerStr = json.dumps(registerDict)
        r = requests.post('https://192.168.3.149:12000/sso/v1/register', data=registerStr, verify=False)
        #lxLog.getDebugLog()(r.text)
        loginRecvDict = json.loads(r.text)
        if '1' != loginRecvDict['result']:
            lxLog.getDebugLog()(unicode.format(u"注册失败，号码：{1}，错误代码{0}", loginRecvDict['result'], phone))
        else:
            lxLog.getDebugLog()(u'注册成功：%s', phone)
        index = index + 1
    '''

    while True:
        try:
            login()
        except Exception as err:
            lxLog.getDebugLog()(u"main异常退出:%s", str(err))
        finally:
            time.sleep(10000)



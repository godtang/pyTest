# -*- coding: utf-8 -*-
import tmjLog as lxLog
import struct
import socket
import time
import sys
from time import sleep
from kazoo.client import KazooClient
from kazoo.client import KazooState

avHost = "120.79.16.27"
avPort = 20000
nodePath = "/im_base/Video/"
zkHost = "47.96.77.187"
zkPort = "2181"
#publicIP = '192.168.3.24' #以上报的服务器为准
maxBandwidth = 4096


def reportToZK():
    zk = KazooClient(zkHost+":"+zkPort)
    zk.start()
    node = nodePath + avHost
    while True:
        try:
            lxLog.getDebugLog()(u"往%s:%d取数据", avHost, avPort)
            audioSize, videoSize = getConnections(avHost, avPort)
            currentTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            value = avHost + ':' + str(avPort) + '|' + str(audioSize) + '|' + str(videoSize) + '|' + str(maxBandwidth) + '|' + currentTime
            lxLog.getDebugLog()(u"往%s:%s上报数据:%s", zkHost, zkPort, value)
            if zk.exists(node):
                zk.set(node, value.encode('ascii'))
            else:
                zk.create(node, value.encode('ascii'), None, True, False)
        except Exception as err:
            lxLog.getDebugLog()(u"reportToZK异常退出:%s", str(err))
            zk.close()
            break
        finally:
            time.sleep(60)

def getConnections(host, port):
    TotalLen = 8
    CmdId = 6
    SeqId = 0
    CmdStatus = 0
    str = struct.pack('!HHHH',TotalLen, CmdId, SeqId, CmdStatus)
    #print(str)

    #不需要建立连接
    #创建socket对象
    #SOCK_DGRAM    udp模式
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.settimeout(10)
    #发送数据 字节
    s.sendto(str,(host, port))
    #接收返回的数据
    data=s.recv(1024)
    #print(data)

    TotalLen, CmdId, SeqId, CmdStatus, audioSize, videoSize = struct.unpack('=HHHHii', data)

    #print(TotalLen, CmdId, SeqId, CmdStatus, audioSize, videoSize)

    return audioSize, videoSize

if __name__ == '__main__':
    while True:
        try:
            reportToZK()
        except Exception as err:
            lxLog.getDebugLog()(u"main异常退出:%s", str(err))
        finally:
            time.sleep(5)



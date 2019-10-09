# -*- coding: utf-8 -*-
import tmjLog as lxLog
import struct
import socket
import time
import sys
#from kazoo.client import KazooClient
import zookeeper

host = "47.110.127.165"
loginPort = 20000
nodePath = "/zktest"
zkHost = "192.168.3.22"
zkPort = "2181"

import logging
from time import sleep
from kazoo.client import KazooClient
from kazoo.client import KazooState

zk = KazooClient("192.168.3.22:2181")
zk.start()

#判断zk客户端是否与server连接
def my_listener():

    if zk.state == "LOST":
        print("1111")# Register somewhere that the session was lost
    elif zk.state == "SUSPENDED":
        print("222222")
        # Handle being disconnected from Zookeeper
    else:
        # Handle being connected/reconnected to Zookeeper
        print("6666")

# print log to console
#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

#zk = KazooClient('127.0.0.1:2181')
#zk.start()

def children_callback(children):
    print('****',children)

children = zk.get_children('/im_base/gate', children_callback)
my_listener()
zk.create('/im_base/Video/sandfiadsnfias')
#zk.delete('/zookeeper/555555')
while True: sleep(1)    

def reportByZK():
    zk=zookeeper.init("192.168.3.22:2181")
    aaa = zookeeper.create(zk,"/zk_for_py","mydata1",[{"perms":4,"scheme":"world","id":"anyone"}],0)
    bbb = zookeeper.get(zk,"/zk_for_py1")
    return

def reportToZK():
    try:
        zkTimeout = 100
        zkc = KazooClient(hosts=zkHost + ':' + zkPort, timeout=zkTimeout)
        zkc.start()

        # 判断节点是否存在
        if zkc.exists(nodePath+"/test111"):
            print(nodePath + "/test111", "存在")
        else:
            aaaa = zkc.ensure_path(nodePath)
            # 建立节点，成功后返回新节点路径
            childrenPath = zkc.create(nodePath+"/test111", b"test111")
            print("创建节点：", childrenPath, "成功。")
            # 创建临时节点，连接断开则节点自动删除
            cccc = zkc.create(nodePath+"/test999", "test999", ephemeral=True)

        # 获取节点数据和节点数据，返回2个值，一个是节点数据，一个是节点stat，这是个ZnodeStat对象，它其实是节点属性，一共有12个属性
        dataAndStat = zkc.get(nodePath)
        data = dataAndStat[0]
        print ("数据为：", data)
        stat = dataAndStat[1]
        print ("数据版本号为：", stat.version)
        print ("数据长度为：", stat.data_length)
        print ("子节点数量：", stat.numChildren)

        # 更新节点数据,数据最大为1MB超过则报错，成功后返回 ZnodeStat 对象
        stat = zkc.set(nodePath, value="test222")
        print ("数据版本号为：", stat.version)

        # 删除节点，后面的参数用于控制是否递归删除，默认是False,但是这样就会有一个问题，如果该节点下有子节点则本次删除失败，你需要先删除
        # 它下面的所有子节点才行
        if zkc.exists(nodePath+"/test111"):
            result = zkc.delete(nodePath+"/test111", recursive=False)
            if result:
                print ("删除节点成功。")

        print (nodePath + " 的子节点为：", zkc.get_children(nodePath))

        zkc.close()
        zkc.stop()
    except Exception as err:
        print(str(err))

def getConnections(host, port):
    TotalLen = 8
    CmdId = 6
    SeqId = 0
    CmdStatus = 0
    str = struct.pack('!HHHH',TotalLen, CmdId, SeqId, CmdStatus)
    print(str)

    #不需要建立连接
    #创建socket对象
    #SOCK_DGRAM    udp模式
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    #发送数据 字节
    s.sendto(str,(host, port))
    #接收返回的数据
    data=s.recv(1024)
    print(data)

    TotalLen, CmdId, SeqId, CmdStatus, audioSize, videoSize = struct.unpack('=HHHHii', data)

    print(TotalLen, CmdId, SeqId, CmdStatus, audioSize, videoSize)

if __name__ == '__main__':
    while True:
        reportByZK()
        continue
        try:
            getConnections(host, loginPort)
        except Exception as e:
            print(str(e))
        finally:
            time.sleep(5)



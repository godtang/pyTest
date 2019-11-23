# -*- coding: utf-8 -*-

import os

timeFile = 'time.txt'
funcFile = 'func.txt'
recvFile = 'recv.txt'
srcFile = 'src.txt'


def generateFunc(timeObj, funcObj, recvObj, funcPrefix, routeCode, interFaceCode):
    timeObj.write(funcPrefix + 'Time int64\n')
    funcString = 'func ' + funcPrefix + 'Request_' + str(interFaceCode) + '''(v *longConnectionStruct) {
	if time.Now().UnixNano()-v.lastSendTime.''' + funcPrefix + '''Time < int64(heartSleepTime*1e9) {
		return
	}
	sendPB := &go_protobuf.''' + funcPrefix + '''Request{}
    data, err := proto.Marshal(sendPB)
	if err != nil {
		Error.Println("proto.Marshal err:", err)
	}

	sendBytes := appPack(data, ''' + str(routeCode) + ', ' + str(interFaceCode) + ''')
    v.conn.Write(sendBytes)
	v.lastSendTime.''' + funcPrefix + '''Time = time.Now().UnixNano()
	    return
}

func ''' + funcPrefix + 'Responce_' + str(interFaceCode) + '''(byte_body []byte, v *longConnectionStruct, iLoop int) {
	logCostTimeEx(v.phone, v.userId, v.lastSendTime.''' + funcPrefix + '''Time, runFuncName())
	recvPB := &go_protobuf.''' + funcPrefix + '''Response{}
	err := proto.Unmarshal(byte_body, recvPB)
	if err != nil {
		Error.Printf("proto decode error[%s]\\n", err.Error())
		return
	}
	//if 1 == *recvPB.Result {
	//	v.currentVersion.RoomModifyVersion = *recvPB.ServerVersion
	//	//不保存本地群记录
	//}
	return
}\n\n'''
    funcObj.write(funcString)
    recvString = 'recvFuncs[' + str(interFaceCode) + '] = ' + funcPrefix + 'Responce_' + str(interFaceCode) + '\n'
    recvObj.write(recvString)


def readSrc():
    srcObj = open(srcFile, 'r+')
    timeObj = open(timeFile, 'w+')
    funcObj = open(funcFile, 'w+')
    recvObj = open(recvFile, 'w+')
    for line in srcObj.readlines():
        curLine = line.strip().split(",")
        generateFunc(timeObj, funcObj, recvObj, curLine[0], curLine[1], curLine[2])
    timeObj.close()
    funcObj.close()
    recvObj.close()


if __name__ == '__main__':
    readSrc()

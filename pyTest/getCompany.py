# -*- coding: utf-8 -*-
import json
import os
import requests

allConstructionOrganization = 'allConstructionOrganization.txt'
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


def getCompany():
    allConstructionOrganizationObj = open(allConstructionOrganization, 'w+', encoding='utf-8')
    urlIndex = 357
    verifyid = 'da609ebcf245423fb8eaa8fea0c01a56'
    moveX = '114'
    while urlIndex >= 1:
        print('i\'m processing ' + str(urlIndex))
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0",
            "X-Requested-With": "XMLHttpRequest",
            "DNT": "1",
            "Referer": "http://gcxm.hunanjs.gov.cn/dataservice.html",
            "Cookie": "ASP.NET_SessionId=2jgoosgdhbvkgagtnbtlll0f"
        }
        getUrl = 'http://gcxm.hunanjs.gov.cn/AjaxHandler/PersonHandler.ashx?method=GetListPage&type=1&corptype_1=7&corpname_1=&licensenum_1=&Province_1=430000&City_1=&county_1=&persontype=&persontype_2=&personname_2=&idcard_2=&certnum_2=&corpname_2=&prjname_3=&corpname_3=&prjtype_3=&cityname_3=&year_4=2019&jidu_4=4&corpname_4=&corpname_5=&corpcode_5=&legalman_5=&cityname_5=&SafeNum_6=&corpname_6=&corpname_7=&piciname_7=&corptype_7=&pageSize=30&pageIndex=' + \
                 str(urlIndex) + '&xypjcorptype=3&moveX=' + moveX + '&verifyid='+verifyid
        response = requests.get(getUrl, headers = headers)
        j = json.loads(response.text)
        if 0 == j['code']:
            queryList = j['data']['list']
            for tempObj in queryList:
                allConstructionOrganizationObj.write(str(tempObj['corpid'])+'\t'+tempObj['corpname']+'\r\n')
        else:
            print('error, i\'m quit')
            os._exit(0)
        urlIndex = urlIndex - 1
    allConstructionOrganizationObj.close()

def getSuitableCompany():
    allConstructionOrganizationObj = open(allConstructionOrganization, 'r+', encoding='utf-8')
    pass

if __name__ == '__main__':
    #getCompany()

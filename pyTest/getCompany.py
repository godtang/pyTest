# -*- coding: utf-8 -*-
import datetime
import json
import os
import time
import pymysql
import requests
import queue
import threading
import tmjLog as lxLog

q = queue.Queue()
allConstructionOrganization = 'allConstructionOrganization.txt'
suitableCompany = 'suitableCompany.txt'
greaterThan500 = 'greaterThan500.txt'


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
                 str(urlIndex) + '&xypjcorptype=3&moveX=' + moveX + '&verifyid=' + verifyid
        response = requests.get(getUrl, headers=headers)
        j = json.loads(response.text)
        if 0 == j['code']:
            queryList = j['data']['list']
            for tempObj in queryList:
                allConstructionOrganizationObj.write(str(tempObj['corpid']) + '\t' + tempObj['corpname'] + '\r\n')
        else:
            print('error, i\'m quit')
            os._exit(0)
        urlIndex = urlIndex - 1
    allConstructionOrganizationObj.close()


def getSuitableCompany():
    suitableCompanyObj = open(suitableCompany, 'w+', encoding='utf-8')
    allConstructionOrganizationObj = open(allConstructionOrganization, 'r+', encoding='utf-8')
    lines = allConstructionOrganizationObj.readlines()
    for line in lines:
        line = line.strip()
        if len(line) > 0:
            result = line.split('\t')
            print(result[0])
            corpid = str(result[0])
            detailUrl = 'http://gcxm.hunanjs.gov.cn/AjaxHandler/PersonHandler.ashx?method=getCorpDetail&corpid=' + corpid + '&isout='
            response = requests.get(detailUrl)
            result = response.text
            if result.find(u'市政公用工程施工') > 0 and result.find(u'地基基础工程') > 0:
                suitableCompanyObj.write(line + '\n')
    suitableCompanyObj.close()
    allConstructionOrganizationObj.close()


def getGreaterThan500():
    suitableCompanyObj = open(suitableCompany, 'r+', encoding='utf-8')
    greaterThan500Obj = open(greaterThan500, 'w+', encoding='utf-8')
    lines = suitableCompanyObj.readlines()
    for line in lines:
        try:
            line = line.strip()
            if len(line) > 0:
                result = line.split('\t')
                print(line)
                corpid = str(result[0])
                pageIndex = 1
                fitCompany = False
                projectInfo = ''
                while True:
                    getProjectListUrl = 'http://gcxm.hunanjs.gov.cn/AjaxHandler/PersonHandler.ashx?method=getProjectList&corpid=' \
                                        + corpid + '&corptype=0&pageSize=10&pageIndex=' + str(pageIndex)
                    projectResponse = requests.get(getProjectListUrl)
                    projectResult = projectResponse.text
                    j = json.loads(projectResult)
                    if 0 == j['code']:
                        if j['data']['total'] > 0:
                            queryList = j['data']['list']
                            for tempObj in queryList:
                                if tempObj['prjname'].find(u'景观') > 0 or \
                                        tempObj['prjname'].find(u'绿化') > 0:
                                    print('\t' + tempObj['prjname'])
                                    getDetailUrl = 'http://gcxm.hunanjs.gov.cn/AjaxHandler/PersonHandler.ashx?method=getProjectDetail&prjid=' \
                                                   + str(tempObj['prjid'])
                                    projectDetailResponse = requests.get(getDetailUrl)
                                    detailResult = projectDetailResponse.text
                                    jDetail = json.loads(detailResult)
                                    if 0 == jDetail['code']:
                                        for tempDetailObj in jDetail['data']['ds1']:
                                            if str(tempDetailObj['tendercorpid']) == str(result[0]) \
                                                    and float(tempDetailObj['tendermoney2']) >= 500.0:
                                                fitCompany = True
                                                projectInfo = tempObj['prjname'] + '\t' + str(
                                                    tempDetailObj['tendermoney2'])
                                                break
                                        if fitCompany:
                                            break
                        else:
                            break
                    else:
                        print('error, i\'m quit')
                        os._exit(0)
                    pageIndex = pageIndex + 1
                    if fitCompany or j['data']['pageIndex'] >= j['data']['pages']:
                        break
                if fitCompany:
                    greaterThan500Obj.write(line + '\t' + projectInfo + '\n')
        except Exception as err:
            lxLog.getDebugLog(str(err))

    suitableCompanyObj.close()
    greaterThan500Obj.close()


R = threading.Lock()


class GetGreaterThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = str(threadID)

    def run(self):
        mysqlConfig = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '111111',
            'port': 3306,
            'database': 'tmj',
            'charset': 'utf8'
        }
        mysqlConn = pymysql.connect(**mysqlConfig)
        mysqlCursor = mysqlConn.cursor()
        startDate = time.mktime(time.strptime('2017-2-1', '%Y-%m-%d'))
        while True:
            try:
                if q.empty():
                    break
                R.acquire()
                result = q.get()
                R.release()
                print(result)
                threadFileObj = open('thread' + str(self.threadID) + '.txt', 'a+', encoding='utf-8')
                try:
                    corpid = str(result[0])
                    pageIndex = 1
                    fitCompany = False
                    projectInfo = ''
                    while True:
                        getProjectListUrl = 'http://gcxm.hunanjs.gov.cn/AjaxHandler/PersonHandler.ashx?method=getProjectList&corpid=' \
                                            + corpid + '&corptype=0&pageSize=10&pageIndex=' + str(pageIndex)
                        projectResponse = requests.get(getProjectListUrl)
                        projectResult = projectResponse.text
                        j = json.loads(projectResult)
                        if 0 == j['code']:
                            if j['data']['total'] > 0:
                                queryList = j['data']['list']
                                for tempObj in queryList:
                                    saveProject(tempObj, mysqlCursor)
                                    if True:
                                        print('\t' + tempObj['prjname'])
                                        getDetailUrl = 'http://gcxm.hunanjs.gov.cn/AjaxHandler/PersonHandler.ashx?method=getProjectDetail&prjid=' \
                                                       + str(tempObj['prjid'])
                                        projectDetailResponse = requests.get(getDetailUrl)
                                        detailResult = projectDetailResponse.text
                                        jDetail = json.loads(detailResult)
                                        if 0 == jDetail['code']:
                                            for tempDetailObj in jDetail['data']['ds1']:
                                                saveTender(tempDetailObj, mysqlCursor)
                                                continue
                                                tenderStartDateStr = tempDetailObj['tenderresultdate'].split('T')[0]
                                                tenderStartDate = time.mktime(
                                                    time.strptime(tenderStartDateStr, '%Y-%m-%d'))
                                                if str(tempDetailObj['tendercorpid']) == str(result[0]) \
                                                        and float(tempDetailObj['tendermoney2']) >= 500.0 \
                                                        and tenderStartDate >= startDate:
                                                    fitCompany = True
                                                    projectInfo = tempObj['prjname'] + '\t' + str(
                                                        tempDetailObj['tendermoney2'])
                                                    break
                                            if fitCompany:
                                                break
                            else:
                                break
                        else:
                            print(str(result) + 'error, i\'m quit|' + projectResult)
                            os._exit(0)
                        pageIndex = pageIndex + 1
                        if fitCompany or j['data']['pageIndex'] >= j['data']['pages']:
                            break
                    if fitCompany:
                        threadFileObj.write(result[1] + '\t' + projectInfo + '\n')
                except Exception as err:
                    lxLog.getDebugLog(str(err))

                threadFileObj.close()
            except Exception as e:
                lxLog.getDebugLog(str(e))
            finally:
                pass


def getGreaterByThread():
    suitableCompanyObj = open(suitableCompany, 'r+', encoding='utf-8')
    lines = suitableCompanyObj.readlines()
    for line in lines:
        line = line.strip()
        if len(line) > 0:
            result = line.split('\t')
            q.put(result)
    threads = []
    for index in range(1, 11):
        # 创建新线程
        thread = GetGreaterThread(index)
        # 开启新线程
        thread.start()
        threads.append(thread)
    # 等待所有线程完成
    for t in threads:
        t.join()
    print("Exiting getGreaterByThread")


def rabotThread():
    suitableCompanyObj = open(suitableCompany, 'r+', encoding='utf-8')
    lines = suitableCompanyObj.readlines()
    for line in lines:
        line = line.strip()
        if len(line) > 0:
            result = line.split('\t')
            q.put(result)
    threads = []
    for index in range(1, 21):
        # 创建新线程
        thread = GetGreaterThread(index)
        # 开启新线程
        thread.start()
        threads.append(thread)
    # 等待所有线程完成
    for t in threads:
        t.join()
    print("Exiting getGreaterByThread")


def saveProject(projectInfo, mysqlCursor):
    try:
        querySql = "select * from project where prjid = {}".format(projectInfo['prjid'])
        mysqlCursor.execute(querySql)
        temp = None
        for tempResult in mysqlCursor:
            temp = tempResult[0]
        if not temp is None:
            return
        else:
            for key in projectInfo.keys():
                if projectInfo[key] is None:
                    projectInfo[key] = 0
            insertSql = "insert into project set prjid = {}, prjnum = '{}'" \
                        ", prjname = '{}', buildcorpname = '{}', prjtypenum = '{}'" \
                        ", county = '{}', prjtypename = '{}'".format(
                projectInfo['prjid'], projectInfo['prjnum'], projectInfo['prjname'] \
                , projectInfo['buildcorpname'], projectInfo['prjtypenum'], projectInfo['county'] \
                , projectInfo['prjtypename'])
            mysqlCursor.execute(insertSql)
            mysqlCursor.execute('commit')
    except Exception as e:
        lxLog.getDebugLog(str(e))
        lxLog.getDebugLog()(u"数据库执行异常:%s", str(projectInfo))


def saveTender(tenderInfo, mysqlCursor):
    try:
        querySql = "select * from tender where tenderid = {}".format(tenderInfo['tenderid'])
        mysqlCursor.execute(querySql)
        temp = None
        for tempResult in mysqlCursor:
            temp = tempResult[0]
        if not temp is None:
            return
        else:
            for key in tenderInfo.keys():
                if tenderInfo[key] is None:
                    tenderInfo[key] = 0
            tenderInfo['tenderresultdate'] = str.replace(tenderInfo['tenderresultdate'], 'T', ' ')
            tenderInfo['createdate'] = str.replace(tenderInfo['createdate'], 'T', ' ')
            tenderInfo['CheckTime'] = str.replace(tenderInfo['CheckTime'], 'T', ' ')
            insertSql = "insert into tender set tenderid = {}, tenderclassname = '{}'" \
                        ", tendertypename = '{}', tendernum = '{}', prjid = '{}'" \
                        ", tendertypenum = '{}', tenderclassnum = '{}'" \
                        ", tenderresultdate = '{}', tendermoney = '{}'" \
                        ", tendermoney2 = '{}', prjsize = '{}'" \
                        ", area = '{}', agencycorpid = '{}'" \
                        ", agencycorpname = '{}', tendercorpid = '{}'" \
                        ", tendercorpname = '{}', tenderprojectname = '{}'" \
                        ", tenderprojectidcard = '{}', createdate = '{}'" \
                        ", statusnum = '{}', oldid = '{}'" \
                        ", isxzjg = '{}', CheckDepartName = '{}'" \
                        ", CheckPersonName = '{}', CheckTime = '{}'".format(
                tenderInfo['tenderid'], tenderInfo['tenderclassname'], tenderInfo['tendertypename'] \
                , tenderInfo['tendernum'], tenderInfo['prjid'], tenderInfo['tendertypenum'] \
                , tenderInfo['tenderclassnum'], tenderInfo['tenderresultdate'] \
                , tenderInfo['tendermoney'], tenderInfo['tendermoney2'] \
                , tenderInfo['prjsize'], tenderInfo['area'] \
                , tenderInfo['agencycorpid'], tenderInfo['agencycorpname'] \
                , tenderInfo['tendercorpid'], tenderInfo['tendercorpname'] \
                , tenderInfo['tenderprojectname'], tenderInfo['tenderprojectidcard'] \
                , tenderInfo['createdate'], tenderInfo['statusnum'] \
                , tenderInfo['oldid'], tenderInfo['isxzjg'] \
                , tenderInfo['CheckDepartName'], tenderInfo['CheckPersonName'] \
                , tenderInfo['CheckTime'])
            mysqlCursor.execute(insertSql)
            mysqlCursor.execute('commit')
    except Exception as e:
        lxLog.getDebugLog(str(e))
        lxLog.getDebugLog()(u"数据库执行异常:%s", str(tenderInfo))



def getCompanyByThread():
    allConstructionOrganizationObj = open(allConstructionOrganization, 'r+', encoding='utf-8')
    lines = allConstructionOrganizationObj.readlines()
    for line in lines:
        line = line.strip()
        if len(line) > 0:
            result = line.split('\t')
            q.put(result)
    threads = []
    for index in range(1, 2):
        # 创建新线程
        thread = GetCompanyThread(index)
        # 开启新线程
        thread.start()
        threads.append(thread)
    # 等待所有线程完成
    for t in threads:
        t.join()
    print("Exiting getCompanyByThread")


class GetCompanyThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = str(threadID)

    def run(self):
        mysqlConfig = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '111111',
            'port': 3306,
            'database': 'tmj',
            'charset': 'utf8'
        }
        mysqlConn = pymysql.connect(**mysqlConfig)
        mysqlCursor = mysqlConn.cursor()
        while True:
            try:
                if q.empty():
                    break
                R.acquire()
                result = q.get()
                R.release()
                print(result)
                corpid = str(result[0])
                detailUrl = 'http://gcxm.hunanjs.gov.cn/AjaxHandler/PersonHandler.ashx?method=getCorpDetail&corpid=' + corpid + '&isout='
                response = requests.get(detailUrl)
                j = json.loads(response.text)
                if 0 == j['code']:
                    saveCompany(corpid, j, mysqlCursor)

            except Exception as e:
                lxLog.getDebugLog(str(e))
                lxLog.getDebugLog()(u"corpid:%s", corpid)
            finally:
                pass

def saveCompany(corpid, companyInfo, mysqlCursor):
    querySql = "select * from company where corpid = {}".format(corpid)
    mysqlCursor.execute(querySql)
    temp = None
    for tempResult in mysqlCursor:
        temp = tempResult[0]
    if not temp is None:
        return
    else:
        companyObj = companyInfo['data']['ds'][0]
        for key in companyObj.keys():
            if companyObj[key] is None:
                companyObj[key] = ""
        insertSql = "insert into company set " + \
                    "corpid = " + str(corpid) + \
                    ", corpname = '" + companyObj['corpname'] + "'" + \
                    ", legalman = '" + companyObj['legalman'] + "'" + \
                    ", county = '" + companyObj['county'] + "'" + \
                    ", corpcode = '" + companyObj['corpcode'] + "'" + \
                    ", address = '" + companyObj['address'] + "'" + \
                    ", econtypename = '" + companyObj['econtypename']+ "'"
        mysqlCursor.execute(insertSql)
        qualificationList = companyInfo['data']['ds1']
        for qualificationObj in qualificationList:
            querySql = "select * from companyqualification where corpid = {} and mark = ''".format(corpid, qualificationObj['mark'])
            mysqlCursor.execute(querySql)
            temp = None
            for tempResult in mysqlCursor:
                temp = tempResult[0]
            if not temp is None:
                continue
            else:
                for key in qualificationObj.keys():
                    if qualificationObj[key] is None:
                        qualificationObj[key] = ""
                tenderInfo['organdate'] = str.replace(tenderInfo['organdate'], 'T', ' ')
                tenderInfo['enddate'] = str.replace(tenderInfo['enddate'], 'T', ' ')
                insertSql = "insert into companyqualification set " + \
                            "corpid = " + str(corpid) + \
                            ", certtypenum = " + str(qualificationObj['certtypenum'])  + \
                            ", certnum = " + str(qualificationObj['certnum']) + \
                            ", aptitudekindname = '" + qualificationObj['aptitudekindname'] + "'" + \
                            ", certid = '" + qualificationObj['certid'] + "'" + \
                            ", organdate = '" + qualificationObj['organdate'] + "'" + \
                            ", organname = '" + qualificationObj['organname'] + "'" + \
                            ", enddate = '" + qualificationObj['enddate'] + "'" + \
                            ", mark = '" + qualificationObj['mark']+ "'"
                mysqlCursor.execute(insertSql)
        mysqlCursor.execute('commit')

if __name__ == '__main__':
    # getCompany()
    # getSuitableCompany()
    # getGreaterThan500()
    # getGreaterByThread()
    getCompanyByThread()

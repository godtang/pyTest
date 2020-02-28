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
            lxLog.getDebugLog()(str(err))

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
                #threadFileObj = open('thread' + str(self.threadID) + '.txt', 'a+', encoding='utf-8')
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
                    #if fitCompany:
                        #threadFileObj.write(result[1] + '\t' + projectInfo + '\n')
                except Exception as err:
                    lxLog.getDebugLog()(str(err))

                #threadFileObj.close()
            except Exception as e:
                lxLog.getDebugLog()(str(e))
            finally:
                pass


def getGreaterByThread():
    suitableCompanyObj = open(allConstructionOrganization, 'r+', encoding='utf-8')
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
        lxLog.getDebugLog()(str(e))
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
            if 0 == tenderInfo['tenderresultdate']:
                tenderInfo['tenderresultdate'] = '2099-1-1 0:0:0'
            if 0 == tenderInfo['createdate']:
                tenderInfo['createdate'] = '2099-1-1 0:0:0'
            if 0 == tenderInfo['CheckTime']:
                tenderInfo['CheckTime'] = '2099-1-1 0:0:0'
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
        lxLog.getDebugLog()(str(e))
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
    for index in range(1, 11):
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
            logInfo = ""
            try:
                if q.empty():
                    break
                R.acquire()
                result = q.get()
                R.release()
                print(result)
                corpid = str(result[0])
                logInfo = corpid
                detailUrl = 'http://gcxm.hunanjs.gov.cn/AjaxHandler/PersonHandler.ashx?method=getCorpDetail&corpid=' + corpid + '&isout='
                response = requests.get(detailUrl)
                j = json.loads(response.text)
                if 0 == j['code']:
                    saveCompany(corpid, j, mysqlCursor)

            except Exception as e:
                lxLog.getDebugLog()(str(e))
                lxLog.getDebugLog()(logInfo)
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
                    ", econtypename = '" + companyObj['econtypename'] + "'"
        mysqlCursor.execute(insertSql)
        qualificationList = companyInfo['data']['ds1']
        for qualificationObj in qualificationList:
            querySql = "select * from companyqualification where corpid = {} and mark = ''".format(corpid,
                                                                                                   qualificationObj[
                                                                                                       'mark'])
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
                        if "organdate" == key or "enddate" == key:
                            qualificationObj[key] = "2099-11-11 00:00:00"
                qualificationObj['organdate'] = str.replace(qualificationObj['organdate'], 'T', ' ')
                qualificationObj['enddate'] = str.replace(qualificationObj['enddate'], 'T', ' ')
                insertSql = "insert into companyqualification set " + \
                            "corpid = " + str(corpid) + \
                            ", certtypenum = " + str(qualificationObj['certtypenum']) + \
                            ", certnum = " + str(qualificationObj['certnum']) + \
                            ", aptitudekindname = '" + qualificationObj['aptitudekindname'] + "'" + \
                            ", certid = '" + qualificationObj['certid'] + "'" + \
                            ", organdate = '" + qualificationObj['organdate'] + "'" + \
                            ", organname = '" + qualificationObj['organname'] + "'" + \
                            ", enddate = '" + qualificationObj['enddate'] + "'" + \
                            ", mark = '" + qualificationObj['mark'] + "'"
                mysqlCursor.execute(insertSql)
        mysqlCursor.execute('commit')


if __name__ == '__main__':
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
    tenderInfo = {'MarginAmount': 0, 'planbdate': 0, 'OutputTax': 0, 'tenderprojectname': 0, 'tendertypename': 0, 'uniontendercorpid1': 0, 'JianAnFee': 0, 'issgdw': '003', 'planedate': 0, 'managedepmark': '同意', 'constructionuseridcard': 0, 'isxzjg': 0, 'projectdate': 0, 'uniontendercorpcode4': 0, 'tendermoney2': 0, 'prjname': 0, 'managedepdate': '2019-12-10T10:00:25.673', 'TBBIDWINNINGNOTICEID': 94, 'tradetypenum': 0, 'tenderprojectcertnum3': 0, 'isnotsgxk': 0, 'area': 0, 'DirectCost': 0, 'DataLevel': 'B', 'bdate': 0, 'SocialInsuranceFee': 0, 'CheckPersonName': '株洲市中标通知书', 'constructionusernum': 0, 'tenderprojectname4': 0, 'prjid': 75345, 'invest': 0, 'prefix': 0, 'Form': 0, 'uniontendercorpid4': 0, 'percent': 0, 'SJZL_serverfilename': 0, 'tenderid': 72839, 'EngineeringEvaluation': 0, 'CheckDepartName': '株洲市住房城乡建设局', 'tenderresultdate': 0, 'AdditionalTax': 0, 'uniontendercorpname4': 0, 'Deadline': 0, 'tendermoney': 0, 'uploaddate': '2019-12-10T09:30:06.423', 'prjnum': '4302912019112791102', 'ProvisionalSum': 0, 'uniontendercorpcode3': 0, 'HWCLAddress': 0, 'supervisoridcard': 0, 'WinningAmount': 0, 'createdate': '2019-12-10T09:30:01.853', 'tenderprojectcertnum4': 0, 'tenderclassname': 0, 'BiaoDuanid': 6329, 'BIMSpecialCost': 0, 'iszl': 0, 'managedepnum': 430291, 'designusername': 0, 'projectusername': 0, 'tendercorpcode': 0, 'issqbg': 0, 'tendercorpname': 0, 'techusercertnum': 0, 'WinningBidRange': 0, 'tenderurl': 0, 'agencycorpcode': 0, 'COSTS_AND_PROFITS': 0, 'tenderprojectidcard2': 0, 'percent3': 0, 'managedepstatusnum': 301, 'supervisornum': 0, 'BuildLinkPhone': 0, 'tenderprojectcertnum': 0, 'tenderprojectidcard3': 0, 'supervisorname': 0, 'BXPLANID': 0, 'percent1': 0, 'isimport': 0, 'kbaddress': 0, 'countynum': 430291, 'SafetyCivilizationFee': 0, 'KBCORPNAME': 0, 'datelimit': 0, 'RowGuid': 0, 'prjsize': 0, 'tendercorpid': 0, 'sortnum': 0, 'designusercertnum': 0, 'mark': 0, 'uniontendercorpid3': 0, 'fwzq': 0, 'designuseridcard': 0, 'tenderprojectname2': 0, 'tenderprojectname3': 0, 'bubaocorpid': 0, 'tendernum': '招2019-011号', 'TENDERGSID': 0, 'zbggurl': 0, 'period': 0, 'BuildLinkMan': 0, 'tenderclassnum': 0, 'tenderprojectidcard': 0, 'isbubao': 0, 'SJZL_filename': 0, 'constructionusername': 0, 'BuildCorpName': 0, 'qualityIndicator': 0, 'BID_SECTION_CODE': 0, 'tendertypenum': 0, 'techuseridcard': 0, 'outkey': 0, 'termination': 0, 'importdate': 0, 'isupload': 1, 'managedepnumusername': '云龙示范区中标通知书', 'techusername': 0, 'supervisionusernum': 0, 'uniontendercorpname2': 0, 'TENDER_PROJECT_CODE': 0, 'uniontendercorpcode1': 0, 'printprjsize': 0, 'citynum': 430200, 'bxid': 0, 'Rate': 0, 'edate': 0, 'TENDERRESULTID': 0, 'Basecost': 0, 'agencycorpid': 0, 'uniontendercorpid2': 0, 'uniontendercorpname1': 0, 'uniontendercorpname3': 0, 'OTHER_PROJECT_COSTS': 0, 'Fees': 0, 'tenderprojectidcard4': 0, 'uniontendercorpcode2': 0, 'supervisionuseridcard': 0, 'statusnum': 304, 'HWCLProcurementMethods': 0, 'percent2': 0, 'overview': 0, 'tradeboundnum': 0, 'oldid': 0, 'agencycorpname': 0, 'CheckTime': '2019-12-12T16:11:27.727', 'DataSource': 0, 'ISXYPJ': 0, 'IsUnion': 0, 'tenderprojectcertnum2': 0, 'HWCLPhone': 0, 'supervisionusername': 0, 'projectmark': 0}
    saveTender(tenderInfo, mysqlCursor)
    # getCompany()
    # getSuitableCompany()
    # getGreaterThan500()
    getGreaterByThread()
    #getCompanyByThread()

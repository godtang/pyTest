# -*- coding: utf-8 -*-
import json
import os
import requests
import queue
import threading

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
    lastPosition = False
    for line in lines:
        try:
            line = line.strip()
            if len(line) > 0:
                result = line.split('\t')
                print(line)
                corpid = str(result[0])
                # if '5130' == corpid:
                #     lastPosition = True
                # if not lastPosition:
                #     continue
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
            print(err)

    suitableCompanyObj.close()
    greaterThan500Obj.close()

R=threading.Lock()


class GetGreaterThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = str(threadID)

    def run(self):
        while True:
            try:
                if q.empty():
                    break
                R.acquire()
                line = q.get()
                R.release()
                print(line)
                threadFileObj = open('thread' + str(self.threadID) + '.txt', 'w+', encoding='utf-8')
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
                            threadFileObj.write(line + '\t' + projectInfo + '\n')
                except Exception as err:
                    print(err)

                threadFileObj.close()
            except Exception as e:
                print(e)
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
    for index in range(1, 10):
        # 创建新线程
        thread = GetGreaterThread(index)
        # 开启新线程
        thread.start()
        threads.append(thread)
    # 等待所有线程完成
    for t in threads:
        t.join()
    print("Exiting getGreaterByThread")


if __name__ == '__main__':
    # getCompany()
    # getSuitableCompany()
    # getGreaterThan500()
    getGreaterByThread()

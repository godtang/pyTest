# -*- coding: utf-8 -*-
import json
import os
import requests

allConstructionOrganization = 'allConstructionOrganization.txt'
suitableCompany = 'suitableCompany.txt'


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
            detailUrl = 'http://gcxm.hunanjs.gov.cn/AjaxHandler/PersonHandler.ashx?method=getCorpDetail&corpid='+corpid+'&isout='
            response = requests.get(detailUrl)
            result = response.text
            if result.find(u'市政公用工程施工') > 0 and result.find(u'地基基础工程') > 0:
                suitableCompanyObj.write(line + '\n')
    suitableCompanyObj.close()
    allConstructionOrganizationObj.close()

if __name__ == '__main__':
    # getCompany()
    getSuitableCompany()

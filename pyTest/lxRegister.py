# -*- coding: utf-8 -*-
# !/usr/bin/env python


import time
import sys
import os
import threading
import tmjLog as lxLog
import json
import requests
import mysql.connector

from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

_PhonePrefix = 12345
_PHoneStart = 0
_PHoneEnd = 10


class lxRegisterMysql(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        config = {
            'host': 'drdshbgav95e0z5apublic.drds.aliyuncs.com',
            'user': 'root',
            'password': '@lxkjim20191011',
            'port': 3306,
            'database': 'test_base_user',
            'charset': 'utf8'
        }
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        index = 0
        phonePrefix = '%d%03d' % (_PhonePrefix, self.threadID)
        queryCountSql = "select count(*) from base_user where telephone like '{}%'".format(phonePrefix)
        cursor.execute(queryCountSql)
        data = cursor.fetchone()
        countZero = False
        if 1000 == data[0]:
            lxLog.LOG_DEBUG(u"%s已经有1000条记录", phonePrefix)
            return
        elif 0 == data[0]:
            countZero = True
        cursor.execute("begin")
        while index < 1000:
            phone = '%d%03d%03d' % (_PhonePrefix, self.threadID, index)
            if index % 100 == 0:
                lxLog.getDebugLog()(u"处理手机号码：%s", phone)
            try:
                if countZero :
                    sql_query = "INSERT INTO `base_user` SET password = 'f317424473928b0b840b0c9f4ee8f97e'" \
                                ", telephone = '" + phone + "'" \
                                                            ", resister_come = 1, login_fail_cnt = 0, user_status = 0, reg_time = NOW()"
                    cursor.execute(sql_query)
                else:
                    sql_query = "select user_id from base_user where telephone = '" + phone + "' "
                    cursor.execute(sql_query)
                    exist = False
                    for user_id in cursor:
                        exist = True
                        break
                    if False == exist:
                        sql_query = "INSERT INTO `base_user`.`base_user` SET password = 'f317424473928b0b840b0c9f4ee8f97e'" \
                                    ", telephone = '" + phone + "'" \
                                                                ", resister_come = 1, login_fail_cnt = 0, user_status = 0, reg_time = NOW()"
                        cursor.execute(sql_query)
            except Exception as err:
                lxLog.getDebugLog()(u"异常:%s", str(err))
            finally:
                index = index + 1
        cursor.execute("commit")

        #必须在事务后执行
        QueueSql = " insert into base_sync_quee (user_id,telephone,nickname,type,cnt,next_syns_time) "\
                   " select user_id,telephone,telephone,1,0,now() from base_user where telephone like '{}%'"\
            .format(phonePrefix)
        cursor.execute(QueueSql)


class lxRegister(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        index = 0
        registerDict = {}
        while index < 1000:
            phone = '%d%03d%03d' % (_PhonePrefix, self.threadID, index)
            registerDict['telephone'] = phone
            registerDict['verifyCode'] = '0000'
            registerDict['nickname'] = phone
            registerDict['password'] = 'f317424473928b0b840b0c9f4ee8f97e'
            registerDict['resisterCome'] = '1'
            registerStr = json.dumps(registerDict)
            try:
                r = requests.post('https://sso.im.test.bolod.xin:19000/sso/v1/register', data=registerStr, verify=False)
                # lxLog.getDebugLog()(r.text)
                loginRecvDict = json.loads(r.text)
                if '1' != loginRecvDict['result']:
                    lxLog.getDebugLog()(unicode.format(u"注册失败，号码：{1}，错误代码{0}", loginRecvDict['result'], phone))
                else:
                    lxLog.getDebugLog()(u'注册成功：%s', phone)
            except Exception as err:
                lxLog.getDebugLog()(u"异常:%s", str(err))
            finally:
                index = index + 1


if __name__ == '__main__':
    lxLog.LOG_DEBUG(u"本次注册账号为 %d 到 %d", _PhonePrefix*1000000+_PHoneStart*1000, _PhonePrefix*1000000+_PHoneEnd*1000 -1)
    threads = []
    index = _PHoneStart
    while index < _PHoneEnd:
        # 创建新线程
        thread = lxRegister(index)
        # 开启新线程
        thread.start()
        threads.append(thread)
        index = index + 1
        time.sleep(1)
    # 等待所有线程完成
    for t in threads:
        t.join()
    print("Exiting Main Thread")

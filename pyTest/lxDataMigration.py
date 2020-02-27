# -*- coding: utf-8 -*-

import time
import mysql.connector
import pymongo
import redis
import hashlib
import datetime
import urllib
import uuid
import pytz
import random
import requests
from pathlib import Path

'''
本脚本不考虑老版龙信在新版龙信注册的情况
默认老版龙信的账号在新版龙信为未注册！！！！！！！！！
'''

unixtimestart_str = '1970-01-01 08:00:00'
unixtimestart_time = datetime.datetime.strptime(unixtimestart_str, '%Y-%m-%d %H:%M:%S')

md5Salt = 'eccbc87e4b5ce2fe28308fd9f2a7baf312tt390t9874'

# mongoDst = pymongo.MongoClient(
#     "mongodb://root:%40lxkjim20191011@s-bp14f967f9546e94-pub.mongodb.rds.aliyuncs.com:3717,s-bp175f73fb274424-pub.mongodb.rds.aliyuncs.com:3717/admin")
mongoDst = pymongo.MongoClient("mongodb://root:111111@192.168.8.24:27017/")
mongoSrc = pymongo.MongoClient("mongodb://root:iiy485K$Om4$@dds-wz9a8aa83f8d37c41174-pub.mongodb.rds.aliyuncs.com:3717")

redisPool = redis.ConnectionPool(host='r-bp1mm21uqa61wkfvclpd.redis.rds.aliyuncs.com', password='@lxkjim20191011')
redisDB = redis.Redis(connection_pool=redisPool)

# mysqlConfig = {
#     'host': 'drdshbgav95e0z5apublic.drds.aliyuncs.com',
#     'user': 'root',
#     'password': '@lxkjim20191011',
#     'port': 3306,
#     'database': 'base_user',
#     'charset': 'utf8'
# }

mysqlConfig = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '111111',
    'port': 3306,
    'database': 'lx',
    'charset': 'utf8'
}
mysqlConn = mysql.connector.connect(**mysqlConfig)
mysqlCursor = mysqlConn.cursor()


def getRandomString(type, length):
    result = ''
    availableLetter = ''
    if 2 == type:
        availableLetter = u'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        b = len(availableLetter)
    while length != 0:
        length = length - 1
        if 1 == type:
            # type为1时为纯数字
            result = result + str(random.randint(0, 9))
        elif 2 == type:
            # 低概率出现纯数字或纯字母，暂不考虑
            result = result + availableLetter[random.randint(0, len(availableLetter) - 1)]
    return result


def getMySqlValueInDict(key, dictSrc):
    if key in dictSrc:
        try:
            if 'birthday' == key \
                    or 'idcardBirthday' == key \
                    or 'idcardValidityStart' == key:
                delta = datetime.timedelta(seconds=dictSrc[key])
                dst_day = unixtimestart_time + delta
                return "\'" + dst_day.strftime('%Y-%m-%d') + "\'"
            elif 'idcardValidityEnd' == key:
                if -1 == dictSrc[key]:
                    return "\'2222-02-02\'"
                else:
                    delta = datetime.timedelta(seconds=dictSrc[key])
                    dst_day = unixtimestart_time + delta
                    return "\'" + dst_day.strftime('%Y-%m-%d') + "\'"
            elif 'createTime' == key:
                delta = datetime.timedelta(seconds=dictSrc[key])
                dst_day = unixtimestart_time + delta
                return "\'" + dst_day.strftime("%Y-%m-%d %H:%M:%S") + "\'"
            elif 'nickname' == key:
                return "\'" + urllib.quote_plus(str(dictSrc[key].encode('utf8'))) + "\'"
            elif 'idcardName' == key \
                    or 'idcardNation' == key \
                    or 'idcardAddres' == key \
                    or 'idcardSignOrg' == key:
                return "\'" + str(dictSrc[key].encode('utf8')) + "\'"
            else:
                return "\'" + str(dictSrc[key]) + "\'"
        except Exception as e:
            print e
            return "NULL"
    else:
        return "NULL"


def getMongoValueInDict(key, dictSrc):
    if key in dictSrc:
        try:
            if 'birthday' == key \
                    or 'idcardBirthday' == key \
                    or 'idcardValidityStart' == key \
                    or 'createTime' == key \
                    or 'idcardValidityEnd' == key:
                if -1 == dictSrc[key]:
                    pacific = pytz.timezone('Asia/Shanghai')
                    aware_datetime = pacific.localize(datetime.datetime(
                        2222,
                        2,
                        2,
                        2,
                        2,
                        2
                    ))
                    return aware_datetime
                else:
                    delta = datetime.timedelta(seconds=dictSrc[key])
                    dst_day = unixtimestart_time + delta
                    # return "\'" + dst_day.strftime('%Y-%m-%d %H:%M:%S') + "\'"
                    # return ISODate(dst_day.strftime('%Y-%m-%d %H:%M:%S'))
                    pacific = pytz.timezone('Asia/Shanghai')
                    aware_datetime = pacific.localize(datetime.datetime(
                        int(dst_day.strftime('%Y')),
                        int(dst_day.strftime('%m')),
                        int(dst_day.strftime('%d')),
                        int(dst_day.strftime('%H')),
                        int(dst_day.strftime('%M')),
                        int(dst_day.strftime('%S'))
                    ))
                    return aware_datetime
            elif 'nickname' == key \
                    or 'idcardName' == key \
                    or 'idcardNation' == key \
                    or 'idcardAddres' == key \
                    or 'idcardSignOrg' == key:
                return str(dictSrc[key].encode('utf8'))
            else:
                return dictSrc[key]
        except Exception as e:
            print key + ", " + str(e)
            return None
    else:
        # print key + " not in dict"
        return None


def getMongoValueCurrentTime():
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.datetime.now(tz)


def getNewUserId(oldUserId):
    dbSrc = mongoSrc.imapi
    src_user_set = dbSrc.user
    dbDst = mongoDst.lxim
    user_set = dbDst.im_user
    oldObj = src_user_set.find_one({'_id': oldUserId}, {'phone': 1})
    if oldObj is None:
        return None
    newObj = user_set.find_one({'telephone': oldObj['phone']}, {'baseUserId': 1})
    if newObj is None:
        return None
    return newObj['baseUserId']


def user():
    dbSrc = mongoSrc.imapi
    src_user_set = dbSrc.user
    dbDst = mongoDst.lxim
    user_set = dbDst.im_user
    i = 0
    for content in src_user_set.find():
        i = i + 1
        if content['_id'] <= 10000:
            continue
        else:
            print "im_user" + str(i) + "_" + str(content['_id']) + "_" + str(content['phone'])
        if content['_id'] != 11003205:
            continue
        mysqlCursor.execute(
            "select user_id from base_user where telephone = " + getMySqlValueInDict('phone', content))
        userId = None
        for user_id in mysqlCursor:
            userId = user_id[0]
        if not userId is None:
            print "im_user" + str(i) + "_" + str(content['_id']) + ' phone exist, continue'
            continue

        if 'idcard' in content and None != content['idcard']:
            insertSql = "INSERT INTO `base_user`" \
                        "(`password`, `nickname`, `telephone`, " \
                        "`provinceId`, `cityId`, `areaId`, `idcard`, " \
                        "`idcardName`, `idcardSex`, `idcardNation`, `idcardBirthday`, " \
                        "`idcardAddres`, `idcardSignOrg`, `idcardValidityStart`, `idcardValidityEnd`, " \
                        "`lxphone`, `resister_come`, `login_fail_cnt`, `user_status`, `last_login_time`, " \
                        "`reg_time`) " \
                        " VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},  " \
                        " {}, {}, {}, {}, {}, {}, {}, {}, {}) ;".format(
                "\'" + hashlib.md5(md5Salt + content['phone'][-8:]).hexdigest() + "\'",
                getMySqlValueInDict('nickname', content),
                getMySqlValueInDict('phone', content),
                getMySqlValueInDict('provinceId', content),
                getMySqlValueInDict('cityId', content),
                getMySqlValueInDict('areaId', content),
                getMySqlValueInDict('idcard', content),
                getMySqlValueInDict('idcardName', content),
                getMySqlValueInDict('idcardSex', content),
                getMySqlValueInDict('idcardNation', content),
                getMySqlValueInDict('idcardBirthday', content),
                getMySqlValueInDict('idcardAddres', content),
                getMySqlValueInDict('idcardSignOrg', content),
                getMySqlValueInDict('idcardValidityStart', content),
                getMySqlValueInDict('idcardValidityEnd', content),
                getMySqlValueInDict('lxPhone', content),
                1,
                0,
                0,
                getMySqlValueInDict('last_login_time', content),
                getMySqlValueInDict('createTime', content)
            )
            mysqlCursor.execute(insertSql)

            mysqlCursor.execute(
                "select user_id from base_user where telephone = " + getMySqlValueInDict('phone', content))
            userId = None
            for user_id in mysqlCursor:
                userId = user_id[0]
            #     updateSql = "update base_user set idcardUrl = '{}' " \
            #                 " , idcardBackUrl = '{}' " \
            #                 " , idcardPhotoUrl = '{}' " \
            #                 " where user_id = {} ".format(
            #         hashlib.md5(str(userId)).hexdigest() + "idcardUrl.jpg",
            #         hashlib.md5(str(userId)).hexdigest() + "idcardBackUrl.jpg",
            #         hashlib.md5(str(userId)).hexdigest() + "idcardPhotoUrl.jpg",
            #         userId
            #     )
            #     mysqlCursor.execute(updateSql)
            if userId is None:
                print getMySqlValueInDict('phone', content) + "can't found userId 1"
                continue
            mysqlCursor.execute("commit")

            _id = userId
            baseUserId = _id
            nickname = getMongoValueInDict('nickname', content)
            description = getMongoValueInDict('description', content)
            telephone = getMongoValueInDict('phone', content)
            allPhone = getMongoValueInDict('allPhone', content)
            lxphone = getMongoValueInDict('lxPhone', content)
            # avatarUrl = hashlib.md5(str(_id)).hexdigest() + "stranger0.png"  # getValueInDict('avatarUrl', content)
            # avatarSmallUrl = hashlib.md5(
            #     str(_id)).hexdigest() + "strangersmall.png"  # getValueInDict('avatarSmallUrl', content)
            # idcardavatarUrl = None  # getValueInDict('idcardavatarUrl', content)
            # idcardavatarSmallUrl = None  # getValueInDict('idcardavatarSmallUrl', content)
            birthday = getMongoValueInDict('birthday', content)
            sex = getMongoValueInDict('sex', content)
            idcardName = getMongoValueInDict('idcardName', content)
            idcard = getMongoValueInDict('idcard', content)
            # idcardPhotoUrl = hashlib.md5(
            #     str(_id)).hexdigest() + "idcardPhotoUrl.jpg"  # getValueInDict('idcardPhotoUrl', content)
            idcardNation = getMongoValueInDict('idcardNation', content)
            idcardAddres = getMongoValueInDict('idcardAddres', content)
            idcardSignOrg = getMongoValueInDict('idcardSignOrg', content)
            idcardValidityStart = getMongoValueInDict('idcardValidityStart', content)
            idcardValidityEnd = getMongoValueInDict('idcardValidityEnd', content)
            # idcardUrl = hashlib.md5(str(_id)).hexdigest() + "idcardUrl.jpg"  # getValueInDict('idcardUrl', content)
            # idcardBackUrl = hashlib.md5(
            #     str(_id)).hexdigest() + "idcardBackUrl.jpg"  # getValueInDict('idcardBackUrl', content)
            isRealName = 1
            provinceId = getMongoValueInDict('provinceId', content)
            cityId = getMongoValueInDict('cityId', content)
            qdCode = 'U' + str(baseUserId) + '_0'
            qdCodeValidTime = 0
            qdCodeUpdateTime = getMongoValueCurrentTime()
            isInvisible = 1
            isEncrypt = 1  # getValueInDict('isEncrypt', content)
            blacklistMap = getMongoValueInDict('blacklistMap', content)
            msgDisturb = {'msgDisturb': 0, 'msgDisturbTimeStart': '23:00',
                          'msgDisturbTimeEnd': '7:00'}  # getValueInDict('msgDisturb', content)
            loc = getMongoValueInDict('loc', content)
            # loc["lng"] = getValueInDict('loc["lng"]', content)
            # loc["lat"] = getValueInDict('loc["lat"]', content)
            newMsgRemindObj = {'msgPush': 1, 'msgVoice': 1, 'msgVibration': 1, 'voiceAndvVideoRemind': 1,
                               'voiceAndvVideoRemindVoice': 1, 'voiceAndvVideoRemindVibration': 1}
            urlUserPath = ''.join(str(uuid.uuid4()).split('-'))
            privateFileSecret = ''.join(str(uuid.uuid4()).split('-'))
            worthObj = {'level': 0, 'relationshipValue': 0, 'creditValue': 0, 'totalValue': 0, 'bLv0': 0, 'bLv1': 0,
                        'bLv2': 0, 'bLv3': 0, 'mLv0': 0, 'mLv1': 0, 'mLv2': 0, 'mLv3': 0}
            friendDelVersion = 0
            followDelVersion = 0
            roomDelVersion = 0
            devType = getMongoValueInDict('devType', content)  # 老版无
            devBrand = getMongoValueInDict('devBrand', content)  # 老版无
            devTokenMap = getMongoValueInDict('devTokenMap', content)  # 老版无

            data = {}
            data["_id"] = _id
            data["baseUserId"] = baseUserId
            data["nickname"] = nickname
            data["description"] = description
            data["telephone"] = telephone
            data["allPhone"] = allPhone
            data["lxphone"] = lxphone
            # data["avatarUrl"] = avatarUrl
            # data["avatarSmallUrl"] = avatarSmallUrl
            # data["idcardavatarUrl"] = idcardavatarUrl
            # data["idcardavatarSmallUrl"] = idcardavatarSmallUrl
            data["birthday"] = birthday
            data["sex"] = sex
            data["idcardName"] = idcardName
            data["idcard"] = idcard
            # data["idcardPhotoUrl"] = idcardPhotoUrl
            data["idcardNation"] = idcardNation
            data["idcardAddres"] = idcardAddres
            data["idcardSignOrg"] = idcardSignOrg
            data["idcardValidityStart"] = idcardValidityStart
            data["idcardValidityEnd"] = idcardValidityEnd
            # data["idcardUrl"] = idcardUrl
            # data["idcardBackUrl"] = idcardBackUrl
            data["isRealName"] = isRealName
            data["provinceId"] = provinceId
            data["cityId"] = cityId
            data["qdCode"] = qdCode
            data["qdCodeValidTime"] = qdCodeValidTime
            data["qdCodeUpdateTime"] = qdCodeUpdateTime
            data["isInvisible"] = isInvisible
            data["isEncrypt"] = isEncrypt
            data["blacklistMap"] = blacklistMap
            data["msgDisturb"] = msgDisturb
            data["loc"] = loc
            data["newMsgRemindObj"] = newMsgRemindObj
            data["urlUserPath"] = urlUserPath
            data["privateFileSecret"] = privateFileSecret
            data["worthObj"] = worthObj
            data["friendDelVersion"] = friendDelVersion
            data["followDelVersion"] = followDelVersion
            data["roomDelVersion"] = roomDelVersion
            data["devType"] = devType
            data["devBrand"] = devBrand
            data["devTokenMap"] = devTokenMap

            user_set.update({"_id": data["_id"]}, data, upsert=True)
        else:
            insertSql = "INSERT INTO `base_user`" \
                        "(`password`, `nickname`, `telephone`, " \
                        "`provinceId`, `cityId`, `areaId`, " \
                        "`lxphone`, `resister_come`, `login_fail_cnt`, `user_status`, `last_login_time`, " \
                        "`reg_time`) " \
                        " VALUES ({}, {}, {}, {}, {}, {}, {}, " \
                        " {}, {}, {}, {}, {}) ;".format(
                "\'" + hashlib.md5(md5Salt + content['phone'][-8:]).hexdigest() + "\'",
                getMySqlValueInDict('nickname', content),
                getMySqlValueInDict('phone', content),
                getMySqlValueInDict('provinceId', content),
                getMySqlValueInDict('cityId', content),
                getMySqlValueInDict('areaId', content),
                getMySqlValueInDict('lxPhone', content),
                1,
                0,
                0,
                getMySqlValueInDict('last_login_time', content),
                getMySqlValueInDict('createTime', content)
            )
            mysqlCursor.execute(insertSql)

            mysqlCursor.execute(
                "select user_id from base_user where telephone = " + getMySqlValueInDict('phone', content))
            userId = None
            for user_id in mysqlCursor:
                userId = user_id[0]
            if userId is None:
                print getMySqlValueInDict('phone', content) + "can't found userId 2"
                continue
            mysqlCursor.execute("commit")

            _id = userId
            baseUserId = _id
            nickname = getMongoValueInDict('nickname', content)
            description = getMongoValueInDict('description', content)
            telephone = getMongoValueInDict('phone', content)
            allPhone = getMongoValueInDict('allPhone', content)
            lxphone = getMongoValueInDict('lxPhone', content)
            # avatarUrl = hashlib.md5(str(_id)).hexdigest() + "stranger0.png"  # getValueInDict('avatarUrl', content)
            # avatarSmallUrl = hashlib.md5(
            #     str(_id)).hexdigest() + "strangersmall.png"  # getValueInDict('avatarSmallUrl', content)
            # idcardavatarUrl = None  # getValueInDict('idcardavatarUrl', content)
            # idcardavatarSmallUrl = None  # getValueInDict('idcardavatarSmallUrl', content)
            birthday = getMongoValueInDict('birthday', content)
            sex = getMongoValueInDict('sex', content)
            # idcardName = getMongoValueInDict('idcardName', content)
            # idcard = getMongoValueInDict('idcard', content)
            # idcardPhotoUrl = hashlib.md5(
            #     str(_id)).hexdigest() + "idcardPhotoUrl.jpg"  # getValueInDict('idcardPhotoUrl', content)
            # idcardNation = getMongoValueInDict('idcardNation', content)
            # idcardAddres = getMongoValueInDict('idcardAddres', content)
            # idcardSignOrg = getMongoValueInDict('idcardSignOrg', content)
            # idcardValidityStart = getMongoValueInDict('idcardValidityStart', content)
            # idcardValidityEnd = getMongoValueInDict('idcardValidityEnd', content)
            # idcardUrl = hashlib.md5(str(_id)).hexdigest() + "idcardUrl.jpg"  # getValueInDict('idcardUrl', content)
            # idcardBackUrl = hashlib.md5(
            #     str(_id)).hexdigest() + "idcardBackUrl.jpg"  # getValueInDict('idcardBackUrl', content)
            isRealName = 0
            provinceId = getMongoValueInDict('provinceId', content)
            cityId = getMongoValueInDict('cityId', content)
            qdCode = 'U' + str(baseUserId) + '_0'
            qdCodeValidTime = 0
            qdCodeUpdateTime = getMongoValueCurrentTime()
            isInvisible = 1
            isEncrypt = 1  # getValueInDict('isEncrypt', content)
            blacklistMap = getMongoValueInDict('blacklistMap', content)
            msgDisturb = {'msgDisturb': 0, 'msgDisturbTimeStart': '23:00',
                          'msgDisturbTimeEnd': '7:00'}
            loc = getMongoValueInDict('loc', content)
            # loc["lng"] = getValueInDict('loc["lng"]', content)
            # loc["lat"] = getValueInDict('loc["lat"]', content)
            newMsgRemindObj = {'msgPush': 1, 'msgVoice': 1, 'msgVibration': 1, 'voiceAndvVideoRemind': 1,
                               'voiceAndvVideoRemindVoice': 1, 'voiceAndvVideoRemindVibration': 1}
            urlUserPath = ''.join(str(uuid.uuid4()).split('-'))
            privateFileSecret = ''.join(str(uuid.uuid4()).split('-'))
            worthObj = {'level': 0, 'relationshipValue': 0, 'creditValue': 0, 'totalValue': 0, 'bLv0': 0, 'bLv1': 0,
                        'bLv2': 0, 'bLv3': 0, 'mLv0': 0, 'mLv1': 0, 'mLv2': 0, 'mLv3': 0}
            friendDelVersion = 0
            followDelVersion = 0
            roomDelVersion = 0
            devType = getMongoValueInDict('devType', content)
            devBrand = getMongoValueInDict('devBrand', content)
            devTokenMap = getMongoValueInDict('devTokenMap', content)

            data = {}
            data["_id"] = _id
            data["baseUserId"] = baseUserId
            data["nickname"] = nickname
            data["description"] = description
            data["telephone"] = telephone
            data["allPhone"] = allPhone
            data["lxphone"] = lxphone
            # data["avatarUrl"] = avatarUrl
            # data["avatarSmallUrl"] = avatarSmallUrl
            # data["idcardavatarUrl"] = idcardavatarUrl
            # data["idcardavatarSmallUrl"] = idcardavatarSmallUrl
            data["birthday"] = birthday
            data["sex"] = sex
            # data["idcardName"] = idcardName
            # data["idcard"] = idcard
            # data["idcardPhotoUrl"] = idcardPhotoUrl
            # data["idcardNation"] = idcardNation
            # data["idcardAddres"] = idcardAddres
            # data["idcardSignOrg"] = idcardSignOrg
            # data["idcardValidityStart"] = idcardValidityStart
            # data["idcardValidityEnd"] = idcardValidityEnd
            # data["idcardUrl"] = idcardUrl
            # data["idcardBackUrl"] = idcardBackUrl
            data["isRealName"] = isRealName
            data["provinceId"] = provinceId
            data["cityId"] = cityId
            data["qdCode"] = qdCode
            data["qdCodeValidTime"] = qdCodeValidTime
            data["qdCodeUpdateTime"] = qdCodeUpdateTime
            data["isInvisible"] = isInvisible
            data["isEncrypt"] = isEncrypt
            data["blacklistMap"] = blacklistMap
            data["msgDisturb"] = msgDisturb
            data["loc"] = loc
            data["newMsgRemindObj"] = newMsgRemindObj
            data["urlUserPath"] = urlUserPath
            data["privateFileSecret"] = privateFileSecret
            data["worthObj"] = worthObj
            data["friendDelVersion"] = friendDelVersion
            data["followDelVersion"] = followDelVersion
            data["roomDelVersion"] = roomDelVersion
            data["devType"] = devType
            data["devBrand"] = devBrand
            data["devTokenMap"] = devTokenMap

            user_set.update({"_id": data["_id"]}, data, upsert=True)


def u_friends():
    dbSrc = mongoSrc.imapi
    src_friends_set = dbSrc.u_friends
    src_friends_temp = dbSrc.u_friends
    dbDst = mongoDst.lxim
    friends_set = dbDst.im_friends
    follows_set = dbDst.im_follows
    i = 0
    for content in src_friends_set.find():
        i = i + 1
        print str(i) + ":" + str(content['userId']) + ' had ' + str(content['toUserId']) + " " + str(content['status'])
        if content['userId'] <= 10000 \
                or content['toUserId'] <= 10000:
            print "some userId <= 10000, continue"
            continue
        newUserId = getNewUserId(content['userId'])
        newToUserId = getNewUserId(content['toUserId'])
        if newUserId is None \
                or newToUserId is None:
            print "user not found, continue"
            continue
        print str(i) + ":" + str(newUserId) + ' had ' + str(newToUserId) + " " + str(content['status'])
        if 10000 == content['userId'] \
                or 10000 == content['toUserId']:
            # 10000号不处理
            continue
        if 0 == content['status']:
            # 陌生人不处理
            continue
        elif 1 == content['status']:
            # 关注
            # 1 关注对方
            userId = newUserId
            toUserId = newToUserId
            direct = 1
            createTime = getMongoValueInDict("createTime", content)
            logicalDelFlag = 1
            logicalDelTime = None
            isblack = 0
            isBeenBlack = 0
            msgTop = 0
            offlineNoPushMsg = getMongoValueInDict("offlineNoPushMsg", content)
            modifyVersion = redisDB.incr("version_" + str(userId))

            data = {}
            data["userId"] = userId
            data["toUserId"] = toUserId
            data["direct"] = direct
            data["createTime"] = createTime
            data["logicalDelFlag"] = logicalDelFlag
            data["logicalDelTime"] = logicalDelTime
            data["isblack"] = isblack
            data["isBeenBlack"] = isBeenBlack
            data["msgTop"] = msgTop
            data["offlineNoPushMsg"] = offlineNoPushMsg
            data["modifyVersion"] = modifyVersion

            follows_set.update({"userId": data["userId"], "toUserId": data["toUserId"], "direct": data["direct"]}, data,
                               upsert=True)
            # 2 关注对方
            userId = newToUserId
            toUserId = newUserId
            direct = 2
            createTime = getMongoValueInDict("createTime", content)
            logicalDelFlag = 1
            logicalDelTime = None
            isblack = 0
            isBeenBlack = 0
            msgTop = 0
            offlineNoPushMsg = getMongoValueInDict("offlineNoPushMsg", content)
            modifyVersion = redisDB.incr("version_" + str(userId))

            # data = {}
            data["userId"] = userId
            data["toUserId"] = toUserId
            data["direct"] = direct
            data["createTime"] = createTime
            data["logicalDelFlag"] = logicalDelFlag
            data["logicalDelTime"] = logicalDelTime
            data["isblack"] = isblack
            data["isBeenBlack"] = isBeenBlack
            data["msgTop"] = msgTop
            data["offlineNoPushMsg"] = offlineNoPushMsg
            data["modifyVersion"] = modifyVersion

            follows_set.update({"userId": data["userId"], "toUserId": data["toUserId"], "direct": data["direct"]}, data,
                               upsert=True)
        elif 2 == content['status']:
            # 好友
            userId = newUserId
            toUserId = newToUserId
            toNickname = getMongoValueInDict("toNikname", content)
            createTime = getMongoValueInDict("createTime", content)
            logicalDelFlag = 1
            isblack = 0
            isBeenBlack = 0
            msgTop = 0
            offlineNoPushMsg = getMongoValueInDict("offlineNoPushMsg", content)
            flevel = getMongoValueInDict("flevel", content)
            flevelModifyTime = getMongoValueCurrentTime()
            beenFlevel = src_friends_temp.find_one(
                {'status': 2, 'userId': content['userId'], 'toUserId': content['toUserId']},
                {'flevel': 1}).get('flevel')
            beenFlevelModifyTime = getMongoValueCurrentTime()
            remarkName = getMongoValueInDict("remarkName", content)
            remarkPhone = getMongoValueInDict("remarkPhone", content)
            modifyVersion = redisDB.incr("version_" + str(userId))

            data = {}
            data["userId"] = userId
            data["toUserId"] = toUserId
            data["toNickname"] = toNickname
            data["createTime"] = createTime
            data["logicalDelFlag"] = logicalDelFlag
            data["isblack"] = isblack
            data["isBeenBlack"] = isBeenBlack
            data["msgTop"] = msgTop
            data["offlineNoPushMsg"] = offlineNoPushMsg
            data["flevel"] = flevel
            data["flevelModifyTime"] = flevelModifyTime
            data["beenFlevel"] = beenFlevel
            data["beenFlevelModifyTime"] = beenFlevelModifyTime
            data["remarkName"] = remarkName
            data["remarkPhone"] = remarkPhone
            data["modifyVersion"] = modifyVersion

            friends_set.update({"userId": data["userId"], "toUserId": data["toUserId"]}, data, upsert=True)
        else:
            print "error status"


def shiku_room():
    dbSrc = mongoSrc.imRoom
    room_set = dbSrc.shiku_room
    room_member_set = dbSrc.shiku_room_member

    dbDst = mongoDst.lxim
    dst_room = dbDst.im_room
    dst_room_copy = dbDst.im_room_copy
    dst_room_member = dbDst.im_room_member
    dst_room_member_copy = dbDst.im_room_member_copy

    mongoDestSession = mongoDst.start_session()

    i = 0
    startTime = time.time()
    for content in room_set.find({'userSize': {'$gt': 0}}, no_cursor_timeout=True, batch_size=1):
        i = i + 1
        endTime = time.time()
        print str(i) + ":" + content['name'].encode('utf8') + '|prev cost ' + str(endTime - startTime)
        startTime = time.time()
        _id = redisDB.incr("seq_room")
        name = getMongoValueInDict("name", content)
        desc = getMongoValueInDict("desc", content)
        notice = ""
        userSize = content['userSize']
        createUserId = getNewUserId(content['userId'])
        if createUserId is None:
            continue
        createTime = getMongoValueInDict("createTime", content)
        isNeedVerify = content['isNeedVerify']
        delMemberNotify = 1
        allowInviteFriend = 1
        allowPrivateChat = 1
        isForbidTalk = 0
        qdCode = "R" + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + getRandomString(2, 6)
        isLogicalDel = 1

        data = {}
        data["_id"] = _id
        data["name"] = name
        data["desc"] = desc
        data["notice"] = notice
        data["userSize"] = userSize
        data["createUserId"] = createUserId
        data["createTime"] = createTime
        data["isNeedVerify"] = isNeedVerify
        data["delMemberNotify"] = delMemberNotify
        data["allowInviteFriend"] = allowInviteFriend
        data["allowPrivateChat"] = allowPrivateChat
        data["isForbidTalk"] = isForbidTalk
        data["qdCode"] = qdCode
        data["isLogicalDel"] = isLogicalDel

        dst_room.update({"_id": data["_id"]}, data, upsert=True)
        mongoDestSession.start_transaction()
        for memberSet in room_member_set.find({'roomId': content['_id']}, no_cursor_timeout=True, batch_size=1):
            print '\t' + memberSet['nickname'].encode('utf8')
            memberSet['userId'] = getNewUserId(memberSet['userId'])
            if memberSet['userId'] is None:
                continue
            roomCopyData = {}
            roomCopyData["_id"] = str(_id) + '_' + str(memberSet['userId'])
            roomCopyData["ownerUserId"] = memberSet['userId']
            roomCopyData["roomId"] = _id
            roomCopyData["role"] = memberSet['role']
            roomCopyData["offlineNoPushMsg"] = memberSet['offlineNoPushMsg']
            roomCopyData["isTopChat"] = 0
            roomCopyData["isShowNickName"] = 0
            roomCopyData["isLogicalDel"] = 1
            # roomCopyData["logicalDelTime"] = logicalDelTime
            # roomCopyData["delReason"] = delReason
            roomCopyData["modifyVersion"] = redisDB.incr("version_" + str(memberSet['userId']))
            roomCopyData["name"] = name
            roomCopyData["desc"] = desc
            roomCopyData["isForbidTalk"] = isForbidTalk
            roomCopyData["qdCode"] = qdCode
            roomCopyData["createUserId"] = createUserId
            roomCopyData["createTime"] = createTime
            roomCopyData["isNeedVerify"] = isNeedVerify
            roomCopyData["delMemberNotify"] = delMemberNotify
            roomCopyData["allowInviteFriend"] = allowInviteFriend
            roomCopyData["allowPrivateChat"] = allowPrivateChat
            roomCopyData["notice"] = notice

            # dst_room_copy.update({"_id": roomCopyData["_id"]}, roomCopyData, upsert=True)
            dst_room_copy.insert_one(roomCopyData)

            roomMemberData = {}
            roomMemberData["memberId"] = str(_id) + '_' + str(memberSet['userId'])
            roomMemberData["roomId"] = _id
            roomMemberData["memberUserId"] = memberSet['userId']
            roomMemberData["role"] = memberSet['role']
            roomMemberData["isInVisibleMan"] = 0
            roomMemberData["inTime"] = createTime

            # dst_room_member.update({"memberId": roomMemberData["memberId"]}, roomMemberData, upsert=True)
            dst_room_member.insert_one(roomMemberData)
            roomMemberCopyDataList = []
            for memberSetTemp in room_member_set.find({'roomId': content['_id']}, no_cursor_timeout=True, batch_size=1):
                memberSetTemp['userId'] = getNewUserId(memberSetTemp['userId'])
                if memberSetTemp['userId'] is None:
                    continue
                roomMemberCopyData = {}

                roomMemberCopyData["_id"] = str(_id) + '_' + str(memberSet['userId']) + '_' + str(
                    memberSetTemp['userId'])
                roomMemberCopyData["memberId"] = roomMemberData["memberId"]
                roomMemberCopyData["memberUserId"] = roomCopyData["ownerUserId"]
                roomMemberCopyData["ownerUserId"] = memberSetTemp['userId']
                roomMemberCopyData["roomId"] = _id
                roomMemberCopyData["isLogicalDel"] = 1
                # roomMemberCopyData["logicalDelTime"] = logicalDelTime
                roomMemberCopyData["modifyVersion"] = redisDB.incr("version_" + str(memberSetTemp['userId']))
                roomMemberCopyData["role"] = memberSetTemp['role']
                roomMemberCopyData["isInVisibleMan"] = 0
                roomMemberCopyData["inTime"] = createTime
                roomMemberCopyData["isForbidTalk"] = 0
                # roomMemberCopyData["remarkName "] = remarkName

                # dst_room_member_copy.update({"_id": roomMemberCopyData["_id"]}, roomMemberCopyData, upsert=True)
                # dst_room_member_copy.insert_one(roomMemberCopyData)
                roomMemberCopyDataList.append(roomMemberCopyData)
            dst_room_member_copy.insert_many(roomMemberCopyDataList, ordered=False)
        mongoDestSession.commit_transaction()

    mongoDestSession.end_session()


def segment_init():
    baseList = [136, 137, 138, 139, 147, 188]
    for basePrefix in baseList:
        print 'insert base_segment:' + str(basePrefix)
        mysqlCursor.execute('begin')
        i = 0
        while i < 10000:
            insertSql = "insert into base_segment set segment = '{}', status = 0".format(basePrefix * 10000 + i)
            mysqlCursor.execute(insertSql)
            i = i + 1
        mysqlCursor.execute('commit')
    segmentList = [1368010,
                   1370730,
                   1370731,
                   1371730,
                   1377300,
                   1377307,
                   1377308,
                   1377309,
                   1377730,
                   1378730,
                   1379730,
                   1380533,
                   1380730,
                   1380731,
                   1380738,
                   1380739,
                   1380745,
                   1380888,
                   1381738,
                   1381739,
                   1381745,
                   1382731,
                   1383730,
                   1383738,
                   1386730,
                   1386731,
                   1386738,
                   1387300,
                   1387301,
                   1387303,
                   1387305,
                   1387307,
                   1387308,
                   1387309,
                   1387310,
                   1387311,
                   1387315,
                   1387316,
                   1387317,
                   1387318,
                   1387319,
                   1387382,
                   1387383,
                   1387385,
                   1387386,
                   1387388,
                   1387389,
                   1387398,
                   1387399,
                   1387450,
                   1387451,
                   1387455,
                   1387456,
                   1387458,
                   1387459,
                   1387730,
                   1387731,
                   1387738,
                   1388730,
                   1388731,
                   1388738,
                   1389730,
                   1389731,
                   1389738,
                   1390000,
                   1390099,
                   1390100,
                   1390101,
                   1390123,
                   1390248,
                   1390298,
                   1390371,
                   1390451,
                   1390730,
                   1390731,
                   1390732,
                   1390734,
                   1390735,
                   1390736,
                   1390737,
                   1390738,
                   1390739,
                   1390745,
                   1390746,
                   1390755,
                   1390756,
                   1390769,
                   1390851,
                   1390855,
                   1390898,
                   1390958,
                   1391008,
                   1391532,
                   1391730,
                   1391731,
                   1391736,
                   1391738,
                   1391739,
                   1391755,
                   1391855,
                   1392733,
                   1392739,
                   1392755,
                   1393730,
                   1393731,
                   1393738,
                   1393739,
                   1394731,
                   1395599,
                   1395731,
                   1395738,
                   1395739,
                   1395999,
                   1396739,
                   1396855,
                   1396898,
                   1397139,
                   1397300,
                   1397301,
                   1397302,
                   1397303,
                   1397305,
                   1397306,
                   1397308,
                   1397309,
                   1397310,
                   1397311,
                   1397312,
                   1397315,
                   1397316,
                   1397317,
                   1397318,
                   1397319,
                   1397320,
                   1397321,
                   1397322,
                   1397328,
                   1397360,
                   1397366,
                   1397368,
                   1397378,
                   1397380,
                   1397381,
                   1397382,
                   1397383,
                   1397385,
                   1397386,
                   1397387,
                   1397388,
                   1397389,
                   1397390,
                   1397391,
                   1397392,
                   1397394,
                   1397395,
                   1397396,
                   1397397,
                   1397398,
                   1397399,
                   1397450,
                   1397451,
                   1397452,
                   1397456,
                   1397457,
                   1397458,
                   1397459,
                   1397468,
                   1397566,
                   1397595,
                   1397597,
                   1397598,
                   1397599,
                   1397606,
                   1397711,
                   1397730,
                   1397731,
                   1397738,
                   1397739,
                   1397755,
                   1398511,
                   1398516,
                   1398518,
                   1398550,
                   1398555,
                   1398558,
                   1398560,
                   1398730,
                   1398731,
                   1398736,
                   1398738,
                   1398739,
                   1398745,
                   1398811,
                   1398851,
                   1398855,
                   1398898,
                   1398988,
                   1398989,
                   1399599,
                   1399730,
                   1399731,
                   1399738,
                   1399739,
                   1399855,
                   1399888,
                   1399999,
                   1470731,
                   1880010,
                   1880020,
                   1880021,
                   1880022,
                   1880023,
                   1880024,
                   1880025,
                   1880027,
                   1880028,
                   1880029,
                   1880100,
                   1880311,
                   1880351,
                   1880371,
                   1880431,
                   1880451,
                   1880471,
                   1880531,
                   1880551,
                   1880571,
                   1880591,
                   1880731,
                   1880771,
                   1880791,
                   1880851,
                   1880871,
                   1880891,
                   1880898,
                   1880931,
                   1880951,
                   1880971,
                   1880991,
                   1887388]
    for segment in segmentList:
        mysqlCursor.execute('begin')
        insertSql = "update base_segment set status = 1 where segment = '" + str(segment) + "' "
        mysqlCursor.execute(insertSql)
        i = 0
        print 'insert base_number:' + str(segment)
        while i < 10000:
            insertSql = "insert into base_number set segment = '{}', number = '{}' " \
                .format(segment, segment * 10000 + i)
            mysqlCursor.execute(insertSql)
            i = i + 1
        mysqlCursor.execute('commit')


def lxh():
    dbSrc = mongoSrc.imapi
    i = 0
    for collectionName in dbSrc.list_collection_names():
        if collectionName[0:4] == 'lxh_':
            print str(i) + '|update base_number:' + collectionName.encode('utf8')
            continue
            src_lxh = dbSrc[collectionName]
            mysqlCursor.execute('begin')
            for content in src_lxh.find({'$or': [{"status": 1}, {"isspecial": 1}]}):
                i = i + 1
                updateSql = 'update base_number set status = {}, isspecial = {} where number = "{}"'.format(
                    content['status'], content['isspecial'], content['lxphone'])
                mysqlCursor.execute(updateSql)
            mysqlCursor.execute('commit')


def sellers():
    dbSrc = mongoSrc.imapi
    sellers_set = dbSrc.sellers
    i = 0
    for content in sellers_set.find({}):
        print 'insert base_lxphoneselect:' + content['haodan'].encode('utf8')
        mysqlCursor.execute('begin')
        insertSql = "insert into base_lxphoneselect set userId = '{}', businessCode = '{}', agtCode = '{}', " \
                    "agtName = '{}', agtProvince = '{}', agtCity = '{}', lxphoneSection = '{}' ".format(
            content['id'], 10000, content['id'], content['realname'].encode('utf8'), content['province'],
            content['city'],
            content['haodan']
        )
        mysqlCursor.execute(insertSql)
        i = 0
        while i < 10000:
            insertSql = "insert into base_lxphone set businessCode = '10000', agtCode = '{}', " \
                        " lxphoneSection = '{}', lxphone = '{}' " \
                .format(content['id'], content['haodan'], int(content['haodan']) * 10000 + i)
            mysqlCursor.execute(insertSql)
            i = i + 1
        mysqlCursor.execute('commit')


def modify_user():
    dbSrc = mongoSrc.imapi
    src_user_set = dbSrc.user
    dbDst = mongoDst.lxim
    user_set = dbDst.im_user
    i = 0
    for content in src_user_set.find():
        i = i + 1
        if content['_id'] <= 10000:
            continue
        else:
            print "modify_user" + str(i) + "_" + str(content['_id']) + "_" + str(content['phone'])
        updateSql = " update base_user set idcardUrl = NULL, idcardBackUrl = NULL, idcardPhotoUrl = NULL " \
                    " where telephone = '{}' ".format(str(content['phone']))
        mysqlCursor.execute(updateSql)
        mysqlCursor.execute('commit')
        queryDict = {"telephone": str(content['phone'])}
        newValueDict = {
            "$set": {
                'sex': getMongoValueInDict('idcardSex', content),
                'birthday': getMongoValueInDict('idcardBirthday', content),
                'avatarUrl': None,
                'avatarSmallUrl': None,
                'idcardavatarUrl': None,
                'idcardavatarSmallUrl': None,
                'idcardUrl': None,
                'idcardBackUrl': None
            }}
        user_set.update_many(queryDict, newValueDict)


def download_img(img_url, userId, phone, picType):
    r = requests.get(img_url, stream=True)
    if r.status_code == 200:
        open('./id/'+str(userId)+'_'+phone+'_'+str(picType)+'.jpg', 'wb').write(r.content) # 将内容写入图片
    del r


def migrateAvatar():
    dbSrc = mongoSrc.imapi
    src_user_set = dbSrc.user
    dbDst = mongoDst.lxim
    user_set = dbDst.im_user
    i = 0
    for content in src_user_set.find().batch_size(100):
        i = i + 1
        if content['_id'] <= 10000:
            continue
        else:
            downloadFlag = False
            newUserId = getNewUserId(content['_id'])
            print "migrateAvatar" + str(i) + "_" + str(content['phone']) + "_" + str(newUserId)
            if 'idcardUrl' in content and not content['idcardUrl'] is None:
                print "\t" + content['idcardUrl']
                my_file = Path('./id/'+str(newUserId)+'_'+content['phone']+'_0.jpg')
                if not my_file.exists():
                    download_img(content['idcardUrl'], newUserId, content['phone'], 0)
                    downloadFlag = True
            if 'idcardBackUrl' in content and not content['idcardBackUrl'] is None:
                print "\t" + content['idcardBackUrl']
                my_file = Path('./id/'+str(newUserId)+'_'+content['phone']+'_1.jpg')
                if not my_file.exists():
                    download_img(content['idcardBackUrl'], newUserId, content['phone'], 1)
                    downloadFlag = True
            if 'idcardPhotoUrl' in content and not content['idcardPhotoUrl'] is None:
                print "\t" + content['idcardPhotoUrl']
                my_file = Path('./id/'+str(newUserId)+'_'+content['phone']+'_2.jpg')
                if not my_file.exists():
                    download_img(content['idcardPhotoUrl'], newUserId, content['phone'], 2)
                    downloadFlag = True
            if downloadFlag:
                time.sleep(1)


if __name__ == '__main__':
    try:
        # # 用户迁移
        user()
        # # 好友、关注迁移
        # u_friends()
        # # 号码初始化
        # segment_init()
        # # 更新已售龙信号和特殊号码
        # lxh()
        # # 更新代理商
        # sellers()
        # 群迁移 数据最多，最后迁移
        shiku_room()
        # 修改生日和性别错误的问题，正常不需要调用
        # modify_user()
        #迁移图片（仅身份证正、反面和头像）
        #migrateAvatar()
    except Exception as e:
        print e

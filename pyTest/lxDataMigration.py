# -*- coding: utf-8 -*-
import random
import time
import mysql.connector
import pymongo
import redis
import hashlib

mongoDst = pymongo.MongoClient("mongodb://root:111111@192.168.8.24:27017/")
mongoSrc = pymongo.MongoClient("mongodb://root:iiy485K$Om4$@dds-wz9a8aa83f8d37c41174-pub.mongodb.rds.aliyuncs.com:3717")

redisPool = redis.ConnectionPool(host='r-bp1mm21uqa61wkfvclpd.redis.rds.aliyuncs.com', password='@lxkjim20191011')
redisDB = redis.Redis(connection_pool=redisPool)

mysqlConfig = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '111111',
    'port': 3306,
    'database': 'tmj',
    'charset': 'utf8'
}
conn = mysql.connector.connect(**mysqlConfig)
mysqlDB = conn.cursor()

def getValueInDict(key, dictSrc):
    if key in dictSrc:
        return dictSrc[key]
    else:
        return None

def im_user():
    dbSrc = mongoSrc.imapi
    src_user_set = dbSrc.user
    dbDst = mongoDst.lxim
    user_set = dbDst.im_user
    i = 0
    for content in src_user_set.find():
        i = i + 1
        if content['_id'] < 10000:
            continue
        else:
            print "im_user" + str(i) + "_" + str(content['_id'])

        _id = content['_id']
        baseUserId = _id
        nickname = getValueInDict('nickname', content)
        description = getValueInDict('description', content)
        telephone = getValueInDict('description', content)
        allPhone = getValueInDict('allPhone', content)
        lxphone = getValueInDict('lxphone', content)
        avatarUrl = hashlib.md5(str(_id)).hexdigest() + "stranger0.png" #getValueInDict('avatarUrl', content)
        avatarSmallUrl = hashlib.md5(str(_id)).hexdigest() + "strangersmall.png" #getValueInDict('avatarSmallUrl', content)
        idcardavatarUrl = None #getValueInDict('idcardavatarUrl', content)
        idcardavatarSmallUrl = None #getValueInDict('idcardavatarSmallUrl', content)
        birthday = getValueInDict('birthday', content)
        sex = getValueInDict('sex', content)
        idcardName = getValueInDict('idcardName', content)
        idcard = getValueInDict('idcard', content)
        idcardPhotoUrl = hashlib.md5(str(_id)).hexdigest() + "idcardPhotoUrl.jpg" #getValueInDict('idcardPhotoUrl', content)
        idcardNation = getValueInDict('idcardNation', content)
        idcardAddres = getValueInDict('idcardAddres', content)
        idcardSignOrg = getValueInDict('idcardSignOrg', content)
        idcardValidityStart = getValueInDict('idcardValidityStart', content)
        idcardValidityEnd = getValueInDict('idcardValidityEnd', content)
        idcardUrl = hashlib.md5(str(_id)).hexdigest() + "idcardUrl.jpg" #getValueInDict('idcardUrl', content)
        idcardBackUrl = hashlib.md5(str(_id)).hexdigest() + "idcardBackUrl.jpg" #getValueInDict('idcardBackUrl', content)
        isRealName = getValueInDict('isAuth', content)
        provinceId = getValueInDict('provinceId', content)
        cityId = getValueInDict('cityId', content)
        qdCode = getValueInDict('qdCode', content)
        qdCodeValidTime = getValueInDict('qdCodeValidTime', content)
        qdCodeUpdateTime = getValueInDict('qdCodeUpdateTime', content)
        isInvisible = getValueInDict('isInvisible', content)
        isEncrypt = 1 #getValueInDict('isEncrypt', content)
        blacklistMap = getValueInDict('blacklistMap', content)
        msgDisturb = {msgDisturb: 0, msgDisturbTimeStart:'23:00', msgDisturbTimeEnd:'7:00'} #getValueInDict('msgDisturb', content)
        loc = getValueInDict('loc', content)
        #loc["lng"] = getValueInDict('loc["lng"]', content)
        #loc["lat"] = getValueInDict('loc["lat"]', content)
        newMsgRemindObj = getValueInDict('newMsgRemindObj', content)
        urlUserPath = getValueInDict('urlUserPath', content)
        privateFileSecret = getValueInDict('privateFileSecret', content)
        worthObj = getValueInDict('worthObj', content)
        friendDelVersion = getValueInDict('friendDelVersion', content)
        followDelVersion = getValueInDict('followDelVersion', content)
        roomDelVersion = getValueInDict('roomDelVersion', content)
        devType = getValueInDict('devType', content)
        devBrand = getValueInDict('devBrand', content)
        devTokenMap = getValueInDict('devTokenMap', content)

        data = {}
        data["_id"] = _id
        data["baseUserId"] = baseUserId
        data["nickname"] = nickname
        data["description"] = description
        data["telephone"] = telephone
        data["allPhone"] = allPhone
        data["lxphone"] = lxphone
        data["avatarUrl"] = avatarUrl
        data["avatarSmallUrl"] = avatarSmallUrl
        data["idcardavatarUrl"] = idcardavatarUrl
        data["idcardavatarSmallUrl"] = idcardavatarSmallUrl
        data["birthday"] = birthday
        data["sex"] = sex
        data["idcardName"] = idcardName
        data["idcard"] = idcard
        data["idcardPhotoUrl"] = idcardPhotoUrl
        data["idcardNation"] = idcardNation
        data["idcardAddres"] = idcardAddres
        data["idcardSignOrg"] = idcardSignOrg
        data["idcardValidityStart"] = idcardValidityStart
        data["idcardValidityEnd"] = idcardValidityEnd
        data["idcardUrl"] = idcardUrl
        data["idcardBackUrl"] = idcardBackUrl
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


def im_friends():
    dbDst = mongoDst.lxim
    friends_set = dbDst.im_friends

    userId = 2
    toUserId = 1
    toNickname = "toNikname"
    createTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    logicalDelFlag = "logicalDelFlag"
    isblack = 0
    isBeenBlack = 0
    msgTop = 0
    offlineNoPushMsg = 0
    flevel = 1
    flevelModifyTime = "flevelModifyTime"
    beenFlevel = 0
    beenFlevelModifyTime = "beenFlevelModifyTime"
    remarkName = "remarkName"
    remarkPhone = "remarkPhone"
    modifyVersion = 0

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
    data["modifyVersion"] = redisDB.incr("user_version_record_" + str(userId))

    friends_set.update({"userId": data["userId"], "toUserId": data["toUserId"]}, data, upsert=True)


def im_follows():
    dbDst = mongoDst.lxim
    follows_set = dbDst.im_follows

    userId = 1
    toUserId = 2
    direct = random.randint(1, 2)
    createTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    logicalDelFlag = 0
    logicalDelTime = "2020-01-04 17:20:54"
    isblack = 0
    isBeenBlack = 0
    msgTop = 0
    offlineNoPushMsg = 0
    modifyVersion = 0

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
    data["modifyVersion"] = redisDB.incr("user_version_record_" + str(userId))

    follows_set.update({"userId": data["userId"], "toUserId": data["toUserId"], "direct": data["direct"]}, data,
                       upsert=True)


def im_friend_tag():
    dbDst = mongoDst.lxim
    tag_set = dbDst.im_friend_tag

    tagId = 0
    tagName = "tagName"
    userId = 1
    createTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    userIdMap = {}

    data = {}
    data["tagId"] = tagId
    data["tagName"] = tagName
    data["userId"] = userId
    data["createTime"] = createTime
    data["userIdMap"] = userIdMap

    tag_set.update({"tagId": data["tagId"]}, data, upsert=True)


def im_room():
    dbDst = mongoDst.lxim
    room_set = dbDst.im_room

    roomId = redisDB.incr("seq_room")
    name = "name"
    desc = "desc"
    notice = "notice"
    userSize = 10
    createUserId = 1
    createTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    isNeedVerify = 1
    delMemberNotify = 0
    allowInviteFriend = 0
    allowPrivateChat = 0
    isForbidTalk = 0
    qdCode = "qdCode"
    isLogicalDel = 0

    data = {}
    data["roomId"] = roomId
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

    room_set.update({"roomId": data["roomId"]}, data, upsert=True)


def im_room_copy():
    dbDst = mongoDst.lxim
    room_copy_set = dbDst.im_room_copy

    ownerUserId = 1
    roomId = 1
    _id = str(roomId) + "_" + str(ownerUserId)
    role = 3
    offlineNoPushMsg = 0
    isTopChat = 0
    isShowNickName = 0
    isLogicalDel = 0
    logicalDelTime = ""
    delReason = 3
    modifyVersion = 0
    name = "name"
    desc = "desc"
    isForbidTalk = 0
    qdCode = "qdCode"
    createUserId = 1
    createTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    isNeedVerify = 0
    delMemberNotify = 0
    allowInviteFriend = 0
    allowPrivateChat = 0
    notice = "notice"

    data = {}
    data["_id"] = _id
    data["ownerUserId"] = ownerUserId
    data["roomId"] = roomId
    data["role"] = role
    data["offlineNoPushMsg"] = offlineNoPushMsg
    data["isTopChat"] = isTopChat
    data["isShowNickName"] = isShowNickName
    data["isLogicalDel"] = isLogicalDel
    data["logicalDelTime"] = logicalDelTime
    data["delReason"] = delReason
    data["modifyVersion"] = modifyVersion
    data["name"] = name
    data["desc"] = desc
    data["isForbidTalk"] = isForbidTalk
    data["qdCode"] = qdCode
    data["createUserId"] = createUserId
    data["createTime"] = createTime
    data["isNeedVerify"] = isNeedVerify
    data["delMemberNotify"] = delMemberNotify
    data["allowInviteFriend"] = allowInviteFriend
    data["allowPrivateChat"] = allowPrivateChat
    data["notice"] = notice

    room_copy_set.update({"_id": data["_id"]}, data, upsert=True)


def im_room_member():
    dbDst = mongoDst.lxim
    room_member_set = dbDst.im_room_member

    roomId = 1
    memberUserId = 1
    memberId = str(roomId) + '_' + str(memberUserId)
    role = 3
    isInVisibleMan = 0
    inTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    data = {}
    data["memberId"] = memberId
    data["roomId"] = roomId
    data["memberUserId"] = memberUserId
    data["role"] = role
    data["isInVisibleMan"] = isInVisibleMan
    data["inTime"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    room_member_set.update({"memberId": data["memberId"]}, data, upsert=True)


def im_room_member_copy():
    dbDst = mongoDst.lxim
    room_member_copy_set = dbDst.im_room_member_copy

    memberId = "memberId"
    memberUserId = 1
    ownerUserId = 1
    roomId = 1
    _id = str(roomId) + '_' + str(ownerUserId) + '_' + str(memberUserId)
    isLogicalDel = 0
    logicalDelTime = ""
    modifyVersion = 0
    role = 3
    isInVisibleMan = 0
    inTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    isForbidTalk = 0
    remarkName = "remarkName"

    data = {}

    data["_id"] = _id
    data["memberId"] = memberId
    data["memberUserId"] = memberUserId
    data["ownerUserId"] = ownerUserId
    data["roomId"] = roomId
    data["isLogicalDel"] = isLogicalDel
    data["logicalDelTime"] = logicalDelTime
    data["modifyVersion"] = modifyVersion
    data["role"] = role
    data["isInVisibleMan"] = isInVisibleMan
    data["inTime"] = inTime
    data["isForbidTalk"] = isForbidTalk
    data["remarkName "] = remarkName

    room_member_copy_set.update({"_id": data["_id"]}, data, upsert=True)


if __name__ == '__main__':
    im_user()
    # im_friends()
    # im_follows()
    # # im_friend_tag()
    # im_room()
    # im_room_copy()
    # im_room_member()
    # im_room_member_copy()

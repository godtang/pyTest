# -*- coding: utf-8 -*-
import random
import time

import pymongo

def im_user(clientDst, clientSrc):
    dbDst = clientDst.lxim
    user_set = dbDst.im_user

    _id = 100000
    baseUserId = _id
    nickname = "1111111111111111111111111"
    description = "description"
    telephone = "telephone"
    allPhone = "allPhone"
    lxphone = "lxphone"
    avatarUrl = "avatarUrl"
    avatarSmallUrl = "avatarSmallUrl"
    idcardavatarUrl = "idcardavatarUrl"
    idcardavatarSmallUrl = "idcardavatarSmallUrl"
    birthday = "birthday"
    sex = random.randint(0,1)
    idcardName = "idcardName "
    idcard = "idcard "
    idcardPhotoUrl = "idcardPhotoUrl"
    idcardNation = "idcardNation "
    idcardAddres = "idcardAddres "
    idcardSignOrg = "idcardSignOrg"
    idcardValidityStart = "2009-01-01"
    idcardValidityEnd = "2029-01-01"
    idcardUrl = "idcardUrl"
    idcardBackUrl = "idcardBackUrl"
    isRealName = "0"
    provinceId = 0
    cityId = 0
    qdCode = "qdCode"
    qdCodeValidTime = 300
    qdCodeUpdateTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    isInvisible = 0
    isEncrypt = 1
    blacklistMap = {}
    msgDisturb = "{msgDisturb:1,msgDisturbTimeStart:'7:30',msgDisturbTimeEnd:'06:00'}"
    loc = {}
    loc["lng"] = 45.0
    loc["lat"] = 45.0
    newMsgRemindObj = {}
    urlUserPath = "urlUserPath"
    privateFileSecret = "privateFileSecret"
    worthObj = {}
    friendDelVersion = 0
    followDelVersion = 0
    roomDelVersion = 0
    devType = 1
    devBrand = "devBrand"
    devTokenMap = {}

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
    data["idcardName "] = idcardName
    data["idcard "] = idcard
    data["idcardPhotoUrl"] = idcardPhotoUrl
    data["idcardNation "] = idcardNation
    data["idcardAddres "] = idcardAddres
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
    data["isEncrypt "] = isEncrypt
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

def im_friends(clientDst, clientSrc):
    dbDst = clientDst.lxim
    friends_set = dbDst.im_friends

    _id = 1
    userId = 1
    toUserId = 1
    toNickname = "toNickname"
    createTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
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
    data["_id"] = _id
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

    friends_set.update({"_id": data["_id"]}, data, upsert=True)

def im_follows(clientDst, clientSrc):
    dbDst = clientDst.lxim
    follows_set = dbDst.im_follows

    _id = 1
    userId = 1
    toUserId = 2
    direct = random.randint(1,2)
    createTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    logicalDelFlag = 0
    logicalDelTime = "2020-01-04 17:20:54"
    isblack = 0
    isBeenBlack = 0
    msgTop = 0
    offlineNoPushMsg = 0
    modifyVersion = 0

    data = {}
    data["_id"] = _id
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

    follows_set.update({"_id": data["_id"]}, data, upsert=True)

if __name__ == '__main__':
    myclientDst = pymongo.MongoClient("mongodb://root:111111@192.168.8.24:27017/")
    myclientSrc = pymongo.MongoClient("mongodb://root:111111@192.168.8.24:27017/")
    im_user(myclientDst, myclientSrc)
    im_friends(myclientDst, myclientSrc)
    im_follows(myclientDst, myclientSrc)

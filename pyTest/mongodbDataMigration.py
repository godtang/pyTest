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

    userId = 2
    toUserId = 1
    toNickname = "toNikname"
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

def im_follows(clientDst, clientSrc):
    dbDst = clientDst.lxim
    follows_set = dbDst.im_follows

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

    follows_set.update({"userId": data["userId"], "toUserId": data["toUserId"], "direct": data["direct"]}, data, upsert=True)

def im_friend_tag(clientDst, clientSrc):
    dbDst = clientDst.lxim
    tag_set = dbDst.im_friend_tag

    tagId = 0
    tagName = "tagName"
    userId = 1
    createTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    userIdMap = {}

    data = {}
    data["tagId"] = tagId
    data["tagName"] = tagName
    data["userId"] = userId
    data["createTime"] = createTime
    data["userIdMap"] = userIdMap

    tag_set.update({"tagId": data["tagId"]}, data, upsert=True)

def im_room(clientDst, clientSrc):
    dbDst = clientDst.lxim
    room_set = dbDst.im_room

    roomId = 11111
    name = "name"
    desc = "desc"
    notice = "notice"
    userSize = 10
    createUserId = 1
    createTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
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

def im_room_copy(clientDst, clientSrc):
    dbDst = clientDst.lxim
    room_copy_set = dbDst.im_room_copy

    _id = "_id"
    ownerUserId = 1
    roomId = 1
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
    createTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
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

def im_room_member(clientDst, clientSrc):
    dbDst = clientDst.lxim
    room_member_set = dbDst.im_room_member

    roomId = "roomId"
    memberUserId = 1
    memberId = roomId + '_' + str(memberUserId)
    role = 3
    isInVisibleMan = 0
    inTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    data = {}
    data["memberId"] = memberId
    data["roomId"] = roomId
    data["memberUserId"] = memberUserId
    data["role"] = role
    data["isInVisibleMan"] = isInVisibleMan
    data["inTime"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    room_member_set.update({"memberId": data["memberId"]}, data, upsert=True)

def im_room_member_copy(clientDst, clientSrc):
    dbDst = clientDst.lxim
    room_member_copy_set = dbDst.im_room_member_copy

    _id = "_id"
    memberId = "memberId"
    memberUserId = 1
    ownerUserId = 1
    roomId = 1
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

    room_member_copy_set.update({"memberId": data["memberId"]}, data, upsert=True)

if __name__ == '__main__':
    myclientDst = pymongo.MongoClient("mongodb://root:111111@192.168.8.24:27017/")
    myclientSrc = pymongo.MongoClient("mongodb://root:111111@192.168.8.24:27017/")
    im_user(myclientDst, myclientSrc)
    im_friends(myclientDst, myclientSrc)
    im_follows(myclientDst, myclientSrc)
    #im_friend_tag(myclientDst, myclientSrc)
    im_room(myclientDst, myclientSrc)
    im_room_copy(myclientDst, myclientSrc)
    im_room_member(myclientDst, myclientSrc)
    im_room_member_copy(myclientDst, myclientSrc)

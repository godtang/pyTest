# -*- coding: utf-8 -*-
# !/usr/bin/env python


import time
import sys
import os
import threading
import tmjLog as lxLog
import json
import requests


def fieldToStr():
    f = open('D:/work/0723/field.txt', 'r')
    dstSqlStr = ""
    for lines in f.readlines():
        lines = lines.strip()
        dstSqlStr = dstSqlStr + '"' + lines + '",'
    print(dstSqlStr)


def renameType():
    typeDic = {"int": "Integer",
               "varchar": "String",
               "tinyint": "Integer",
               "datetime": "String",
               "decimal": "Double",
               "date": "String",
               "smallint": "Integer"}
    f = open('D:/work/0723/type.txt', 'r')
    dstSqlStr = ""
    dstRequiredStr = ""
    for lines in f.readlines():
        line = lines.split("\t")
        dstStr = "private "
        oldType = line[2].split('(')[0].strip()
        newType = typeDic[oldType]
        oldField = line[1].strip()
        newField = ""
        index = 0
        while index < len(oldField):
            if '_' != oldField[index]:
                newField = newField + oldField[index]
                index = index + 1
            else:
                newField = newField + oldField[index + 1].upper()
                index = index + 2
        comment = line[0].strip()
        dstSqlStr = dstSqlStr + oldField + "=#{" + newField + "},"
        dstRequiredStr = dstRequiredStr + '"' + newField + '",'
        print(dstStr + newType + ' ' + newField + ';//' + comment)
    print(dstSqlStr)
    print(dstRequiredStr)


if __name__ == '__main__':
    try:
        renameType()

    except Exception as err:
        lxLog.getDebugLog()(u"异常:%s", str(err))

# -*- coding: utf-8 -*-
#!/usr/bin/env python

import random


def getRandomString(type, length):
    result = ''
    availableLetter = ''
    if 2 == type:
        availableLetter = u'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        b = len(availableLetter)
    while length != 0:
        length = length - 1
        if 1 == type:
            #type为1时为纯数字
            result = result + str(random.randint(0,9))
        elif 2 == type:
            #低概率出现纯数字或纯字母，暂不考虑
            result = result + availableLetter[random.randint(0, len(availableLetter)-1)]
    return result

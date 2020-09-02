# -*- coding: utf-8 -*-
# !/usr/bin/env python


# 柱形图
import random
import time

import pandas
import numpy
import matplotlib
from matplotlib import pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def getDrawList(drawerCount, totalAmount):
    residueCount = drawerCount
    residueAmount = totalAmount
    if totalAmount < drawerCount:
        raise Exception("金额小于抽奖次数")
    drawList = []
    for i in range(1, 1 + drawerCount):
        if 0 == residueCount:
            drawAmount = residueAmount
            drawList.append(drawAmount)
            break
        avgAmount = totalAmount / drawerCount
        drawAmount = random.randint(1, 2 * avgAmount)
        residueCount = residueCount - 1
        residueAmount = totalAmount - residueAmount
        drawList.append(drawAmount)
    return drawList


# 生成一个间隔为1的序列
drawerCount = 10
totalAmount = 100
index = numpy.arange(drawerCount)
# 绘制纵向柱形图

xList = []
amountList = []

for i in range(1, 1 + drawerCount):
    xList.append("draw" + str(i))
plt.xticks(index, xList)

while True:
    plt.xticks(index, xList)
    amountList = getDrawList(drawerCount, totalAmount)
    plt.bar(index, amountList)
    # 配置X轴标签
    plt.show()
    time.sleep(1)

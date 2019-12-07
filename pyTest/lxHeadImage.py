# -*- coding: utf-8 -*-
# !/usr/bin/env python


import time
import sys
import os
import threading
import tmjLog as lxLog
import json
import requests
from PIL import Image, ImageDraw, ImageFont
import random


def draw_image(new_img, text, show_image=False):
    text = str(text)
    text1 = text[:5]
    text2 = text[6:]
    textColor = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    lineColor = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    draw = ImageDraw.Draw(new_img)
    img_size = new_img.size
    draw.line((0, 0) + img_size, fill=lineColor)
    draw.line((0, img_size[1], img_size[0], 0), fill=lineColor)

    font_size = 80
    fnt = ImageFont.truetype('arial.ttf', font_size)
    fnt_size = fnt.getsize(text1)
    while fnt_size[0] > img_size[0] or fnt_size[0] > img_size[0]:
        font_size -= 5
        fnt = ImageFont.truetype('arial.ttf', font_size)
        fnt_size = fnt.getsize(text1)

    x = (img_size[0] - fnt_size[0]) / 2
    y = (img_size[1] - fnt_size[1]) / 2 - 40
    draw.text((x, y), text1, font=fnt, fill=textColor)

    font_size = 80
    fnt = ImageFont.truetype('arial.ttf', font_size)
    fnt_size = fnt.getsize(text2)
    while fnt_size[0] > img_size[0] or fnt_size[0] > img_size[0]:
        font_size -= 5
        fnt = ImageFont.truetype('arial.ttf', font_size)
        fnt_size = fnt.getsize(text2)

    x = (img_size[0] - fnt_size[0]) / 2
    y = (img_size[1] - fnt_size[1]) / 2 + 40
    draw.text((x, y), text2, font=fnt, fill=textColor)

    if show_image:
        new_img.show()
    del draw


def new_image(width, height, text='default', color=(100, 100, 100, 255), show_image=False):
    new_img = Image.new('RGBA', (int(width), int(height)), color)
    draw_image(new_img, text, show_image)
    new_img.save(r'headImage/%s_%s_%s.png' % (width, height, text))
    del new_img


def new_image_with_file(fn):
    with open(fn, encoding='utf-8') as f:
        for l in f:
            l = l.strip()
            if l:
                ls = l.split(',')
                if '#' == l[0] or len(ls) < 2:
                    continue

                new_image(*ls)


class lxHeadImage(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        index = 0
        while index < 10:
            phone = '1238000%03d%01d' % (self.threadID, index)
            if index % 1 == 0:
                lxLog.getDebugLog()(u"处理手机号码：%s", phone)
            try:
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                new_image(300, 300, phone, color=color, show_image=False)
            except Exception as err:
                lxLog.getDebugLog()(u"异常:%s", str(err))
            finally:
                index = index + 1


if __name__ == '__main__':
    threads = []
    index = 0
    while index < 30:
        # 创建新线程
        thread = lxHeadImage(index)
        # 开启新线程
        thread.start()
        threads.append(thread)
        index = index + 1
    # 等待所有线程完成
    for t in threads:
        t.join()
    print "Exiting Main Thread"

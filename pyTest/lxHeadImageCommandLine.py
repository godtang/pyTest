# -*- coding: utf-8 -*-
# !/usr/bin/env python



import sys
from PIL import Image, ImageDraw, ImageFont
import random
import tmjLog as lxLog

_PhonePrefix = 1888801
_PHoneStart = 0
_PHoneEnd = 30

def draw_image(new_img, text, show_image=False):
    text = str(text)
    text1 = text[:5]
    text2 = text[5:]
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
    new_img.save(r'D:/CODE/pyTest/pyTest/headImage/%s.png' % (text))
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


def createHeadImage(phone):
    try:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        new_image(300, 300, phone, color=color, show_image=False)
    except Exception as err:
        lxLog.getDebugLog()(u"异常:%s", str(err))



if __name__ == '__main__':
    if 2 == len(sys.argv):
        createHeadImage(sys.argv[1])
    else:
        pass

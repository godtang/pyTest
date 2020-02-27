# -*- coding: utf-8 -*-
#!/usr/bin/env python
import shutil
import time
import sys
import os
import threading
import tmjLog as lxLog

rootDir = 'D:/CODE/python/lxDataMigration/id/'

def saveScreen(self, driver, e):
    baseImagePath = 'D:/CODE/pyTest/pyTest/exception/'
    phone = self.deviceInfo[0]['normalName']
    currentTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
    saveFile = baseImagePath + phone
    mkdirlambda = lambda x: os.makedirs(x) if not os.path.exists(x)  else True
    mkdirlambda(saveFile)
    saveFile = saveFile + '/' + currentTime + '.png'
    exc_type, exc_obj, exc_tb = sys.exc_info()
    msg = unicode.format(u"saveScreen\n截图：{}\n错误文件:{}:{}\n错误原因:{}", \
        saveFile, exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno, str(e))
    self.myLog(msg)
    driver.get_screenshot_as_file(saveFile)


if __name__ == '__main__':
    for root, dirs, files in os.walk(rootDir):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            print f[:8]
            saveFile = f[:8]
            mkdirlambda = lambda x: os.makedirs(x) if not os.path.exists(x) else True
            mkdirlambda(rootDir + saveFile)
            shutil.move(rootDir + f, rootDir + saveFile + '/')

        # 遍历所有的文件夹
        for d in dirs:
            pass

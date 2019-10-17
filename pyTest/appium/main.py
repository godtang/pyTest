# -*- coding: utf-8 -*-
#!/usr/bin/env python
from appium import webdriver
import desired_capabilities
from unittest import TestCase
import unittest
import time
import sys
import os
import threading
from androidExample import androidExample
sys.path.append("..")
import tmjLog as lxLog

class testThread(threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, deviceInfo):
        threading.Thread.__init__(self)
        self.threadID = str(threadID)
        self.deviceInfo = deviceInfo
    def run(self):
        example = androidExample(self.deviceInfo)
        while True:
            try:
                example.runTest()                
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                msg = unicode.format(u"saveScreen\n截图：{}\n错误文件:{}:{}\n错误原因:{}", \
                    saveFile, exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno, str(e))
                lxLog.getDebugLog()(msg)

if __name__ == '__main__':
    deviceInfos = desired_capabilities.get_deviceInfos()
    threads = []
    index = 0
    for deviceInfo in deviceInfos:
        index = index + 1
        # 创建新线程
        thread = testThread(index, deviceInfo)
        # 开启新线程
        thread.start()
        threads.append(thread)
    # 等待所有线程完成
    for t in threads:
        t.join()
    print "Exiting Main Thread"
    

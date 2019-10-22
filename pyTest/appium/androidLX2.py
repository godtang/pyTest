# -*- coding: utf-8 -*-
#!/usr/bin/env python
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import desired_capabilities
from unittest import TestCase
import unittest
import time
import sys
import os
import threading
sys.path.append("..")
import tmjLog as lxLog

class androidLX2(object):
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

    def initDevice(self, deviceInfo):
        # 创建会话，得到driver对象，driver对象封装了所有的设备操作。下面会具体讲。
        driver = webdriver.Remote(deviceInfo[1], deviceInfo[0])
        if None == driver:
            return None
        else:
            self.myLog(u'initDevice ok')
            return driver

    def test_WelcomePage(self, driver):
        self.myLog(u'test_WelcomePage begin')
        try:
            TouchAction(driver).press(x=661, y=867).move_to(x=70, y=895).release().perform()
            time.sleep(3)
            TouchAction(driver).press(x=685, y=733).move_to(x=15, y=746).release().perform()
            time.sleep(3)
            TouchAction(driver).press(x=678, y=770).move_to(x=28, y=779).release().perform()
            time.sleep(3)
    

            isFind = False
            permits = driver.find_elements_by_class_name('android.widget.TextView')
            for permit in permits:
                if -1 != permit.text.find(u'立即体验'):
                    permit.click()
                    isFind = True
                    break
            if False == isFind:
                self.myLog(u'test_WelcomePage not find')
            else:
                self.myLog(u'test_WelcomePage over')
        except Exception as e:
            print e
            self.saveScreen(driver, e)

    def tearDown(self, driver): 
        self.myLog(u'tearDown')
        # 测试结束，退出会话。
        driver.quit()
        
    def __init__(self, deviceInfo):
        self.deviceInfo = deviceInfo

    def myLog(self, msg):
        lxLog.getDebugLog()("%s:%s", self.deviceInfo[0]['normalName'], msg)

    def runTest(self):
        self.myLog("Starting " + self.deviceInfo[0]['normalName'])
        driver = self.initDevice(self.deviceInfo)
        if None == driver:
            self.myLog("程序初始化失败，请检查程序安装和首次调用")
        else:
            pass
            #self.test_WelcomePage(driver)
            #self.tearDown(driver)
        self.myLog("Exiting " + self.deviceInfo[0]['normalName'])
        time.sleep(60)

    

# -*- coding: utf-8 -*-
#!/usr/bin/env python
from appium.webdriver.common.touch_action import TouchAction
from appium import webdriver
import desired_capabilities
import time
import sys
import os
import util
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

    def saveScreenNormal(self, driver, info):
        baseImagePath = 'D:/CODE/pyTest/pyTest/exception/'
        phone = self.deviceInfo[0]['normalName']
        currentTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        saveFile = baseImagePath + phone
        mkdirlambda = lambda x: os.makedirs(x) if not os.path.exists(x)  else True
        mkdirlambda(saveFile)
        saveFile = saveFile + '/' + currentTime + info + '.png'
        msg = unicode.format(u"saveScreenNormal\n截图：{}\n截图原因:{}", \
            saveFile, info)
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
            time.sleep(3)
            TouchAction(driver).press(x=661, y=867).move_to(x=70, y=895).release().perform()
            self.myLog(u'test_WelcomePage 右滑1')
            time.sleep(3)
            TouchAction(driver).press(x=685, y=733).move_to(x=15, y=746).release().perform()
            self.myLog(u'test_WelcomePage 右滑2')
            time.sleep(3)
            TouchAction(driver).press(x=678, y=770).move_to(x=28, y=779).release().perform()
            self.myLog(u'test_WelcomePage 右滑3')
            time.sleep(3)    

            driver.find_element_by_id('com.lx.chat:id/tv_into').click()
            self.myLog(u'test_WelcomePage over')
        except Exception as e:
            print e
            self.saveScreen(driver, e)

    def test_InstallApk(self, deviceInfo):
        self.myLog(u'test_InstallApk begin')
        try:
            pass
        except Exception as e:
            print e
            self.saveScreen(driver, e)

    def test_Register(self, driver):
        self.myLog(u'test_Register begin')
        try:
            self.myLog(u'test_Register 点击注册按钮')
            driver.find_element_by_id('com.lx.chat:id/sign_tv_register_2').click()
            time.sleep(3)
            phone = '13' + util.getRandomString(1, 9)
            driver.find_element_by_id('com.lx.chat:id/sign_et_register_num').send_keys(phone)
            driver.hide_keyboard()
            time.sleep(3)
            driver.find_element_by_id('com.lx.chat:id/sign_btn_login').click()
            time.sleep(3)
            driver.find_element_by_id('com.lx.chat:id/sign_verify_code').send_keys(util.getRandomString(1, 4))
            driver.hide_keyboard()
            time.sleep(3)
            driver.find_element_by_id('com.lx.chat:id/sign_et_nick').send_keys(phone)
            driver.hide_keyboard()
            time.sleep(3)

            #进行密码输入错误的验证
            #1.输入纯数字密码
            driver.find_element_by_id('com.lx.chat:id/sign_et_num').send_keys(phone)
            driver.hide_keyboard()
            time.sleep(3)
            driver.find_element_by_id('com.lx.chat:id/sign_btn_login').click()
            self.saveScreenNormal(driver, u"输入纯数字密码")
            time.sleep(3)
            #2.输入随机密码
            driver.find_element_by_id('com.lx.chat:id/sign_et_num').clear()
            password = util.getRandomString(2, 16)
            driver.find_element_by_id('com.lx.chat:id/sign_et_num').send_keys(password)
            driver.hide_keyboard()
            time.sleep(3)
            driver.find_element_by_id('com.lx.chat:id/sign_btn_login').click()
            time.sleep(3)
            if True:
                lxLog.getDebugLog()(u'注册成功，号码：' + phone + u',密码：' + password)
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
            self.test_WelcomePage(driver)
            self.test_Register(driver)
            time.sleep(60)
            self.tearDown(driver)
        self.myLog("Exiting " + self.deviceInfo[0]['normalName'])

    

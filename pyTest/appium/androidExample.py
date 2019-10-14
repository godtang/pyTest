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
sys.path.append("..")
import tmjLog as lxLog

class androidExample(object):
    def saveScreen(self, driver, e):
        baseImagePath = 'D:/CODE/pyTest/pyTest/exception/'
        desired_caps = desired_capabilities.get_desired_capabilities()
        phone = desired_caps['normalName']
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

    def setUp():
        # 获取我们设定的capabilities，通知Appium Server创建相应的会话。
        desired_caps = desired_capabilities.get_desired_capabilities()
        # 获取server的地址。
        uri = desired_capabilities.get_uri()
        # 创建会话，得到driver对象，driver对象封装了所有的设备操作。下面会具体讲。
        driver = webdriver.Remote(uri, desired_caps)
        if None == driver:
            return None
        else:
            self.myLog(u'setUp ok')
            return driver

    def initDevice(self, deviceInfo):
        # 创建会话，得到driver对象，driver对象封装了所有的设备操作。下面会具体讲。
        driver = webdriver.Remote(deviceInfo[1], deviceInfo[0])
        if None == driver:
            return None
        else:
            self.myLog(u'initDevice ok')
            return driver

    def test_getPermit(self, driver):
        self.myLog(u'test_getPermit begin')
        while True:
            time.sleep(1)
            try:
                isFind = False
                permits = driver.find_elements_by_class_name('android.widget.Button')
                for permit in permits:
                    if -1 != permit.text.find(u'允许'):
                        permit.click()
                        isFind = True
                        break
                if False == isFind:
                    break
            except Exception as e:
                print e
                self.saveScreen(driver, e)
                break
        self.myLog(u'test_getPermit over')
   
    def test_audioDial(self, driver):  
        self.myLog(u'test_audioDial begin')
        try:
            btnAudioDial = driver.find_element_by_id('com.lx.netphone:id/btn_dial')
            self.myLog(u'test_audioDial 语音拨号')
            btnAudioDial.click()
            time.sleep(3)
            btnAudioMute = driver.find_element_by_id('com.lx.netphone:id/button_audio_mute')
            btnAudioMute.click()
            self.myLog(u'test_audioDial 禁用麦克风')
            time.sleep(3)
            btnAudioSpeaker = driver.find_element_by_id('com.lx.netphone:id/button_audio_speaker')
            btnAudioSpeaker.click()
            self.myLog(u'test_audioDial 使用外放')
            time.sleep(3)
            btnAudioHangup = driver.find_element_by_id('com.lx.netphone:id/button_audio_hang_up')
            btnAudioHangup.click()
            self.myLog(u'test_audioDial 语音挂断')
            time.sleep(3)
        except Exception as e:
            print e
            self.saveScreen(driver, e)
   
    def test_audioAccept(self, driver): 
        self.myLog(u'test_audioAccept begin')
        try:
            btnAudioDial = driver.find_element_by_id('com.lx.netphone:id/btn_answer')
            btnAudioDial.click()
            self.myLog(u'test_audioAccept 语音接听')
            time.sleep(3)
            btnAudioMute = driver.find_element_by_id('com.lx.netphone:id/button_audio_mute')
            btnAudioMute.click()
            self.myLog(u'test_audioAccept 禁用麦克风')
            time.sleep(3)
            btnAudioSpeaker = driver.find_element_by_id('com.lx.netphone:id/button_audio_speaker')
            btnAudioSpeaker.click()
            self.myLog(u'test_audioAccept 使用外放')
            time.sleep(3)
            btnAudioHangup = driver.find_element_by_id('com.lx.netphone:id/button_audio_hang_up')
            btnAudioHangup.click()
            self.myLog(u'test_audioAccept 语音挂断')
            time.sleep(3)
        except Exception as e:
            print e
            self.saveScreen(driver, e)
   
    def test_videoDial1(self, driver):  
        self.myLog(u'test_videoDial1 begin')
        try:
            btnVideoDial = driver.find_element_by_id('com.lx.netphone:id/btn_videoDial')
            btnVideoDial.click()
            self.myLog(u'test_videoDial1 视频拨号')
            time.sleep(3)
            btnVideoSwitchCamera = driver.find_element_by_id('com.lx.netphone:id/video_image_change_camera')
            btnVideoSwitchCamera.click()
            self.myLog(u'test_videoDial1 切换摄像头')
            time.sleep(3)
            btnVideoSwitchToAudio = driver.find_element_by_id('com.lx.netphone:id/video_image_change_voice_call')
            btnVideoSwitchToAudio.click()
            self.myLog(u'test_videoDial1 视频转语音')
            time.sleep(3)
            btnAudioHangup = driver.find_element_by_id('com.lx.netphone:id/button_audio_hang_up')
            btnAudioHangup.click()
            self.myLog(u'test_videoDial1 语音挂断')
            time.sleep(3)
        except Exception as e:
            print e
            self.saveScreen(driver, e)
   
    def test_videoDial2(self, driver):  
        self.myLog(u'test_videoDial2 begin')
        try:
            btnVideoDial = driver.find_element_by_id('com.lx.netphone:id/btn_videoDial')
            btnVideoDial.click()
            self.myLog(u'test_videoDial2 视频接听')
            time.sleep(3)
            btnVideoSwitchCamera = driver.find_element_by_id('com.lx.netphone:id/video_image_change_camera')
            btnVideoSwitchCamera.click()
            self.myLog(u'test_videoDial2 切换摄像头1')
            time.sleep(3)
            btnVideoSwitchCamera.click()
            self.myLog(u'test_videoDial2 切换摄像头2')
            time.sleep(3)
            btnVideoHangup = driver.find_element_by_id('com.lx.netphone:id/video_image_hang_up')
            btnVideoHangup.click()
            self.myLog(u'test_videoDial2 视频挂断')
            time.sleep(3)
        except Exception as e:
            print e
            self.saveScreen(driver, e)
   
    def test_videoAccept1(self, driver):  
        self.myLog(u'test_videoAccept1 begin')
        try:
            btnVideoDial = driver.find_element_by_id('com.lx.netphone:id/btn_videoAnswer')
            btnVideoDial.click()
            self.myLog(u'test_videoAccept1 视频接听')
            time.sleep(3)
            btnVideoSwitchCamera = driver.find_element_by_id('com.lx.netphone:id/video_image_change_camera')
            btnVideoSwitchCamera.click()
            self.myLog(u'test_videoAccept1 切换摄像头')
            time.sleep(3)
            btnVideoSwitchToAudio = driver.find_element_by_id('com.lx.netphone:id/video_image_change_voice_call')
            btnVideoSwitchToAudio.click()
            self.myLog(u'test_videoAccept1 视频转语音')
            time.sleep(3)
            btnAudioHangup = driver.find_element_by_id('com.lx.netphone:id/button_audio_hang_up')
            btnAudioHangup.click()
            self.myLog(u'test_videoAccept1 视频挂断')
            time.sleep(3)
        except Exception as e:
            print e
            self.saveScreen(driver, e)
   
    def test_videoAccept2(self, driver):  
        self.myLog(u'test_videoAccept2 begin')
        try:
            btnVideoDial = driver.find_element_by_id('com.lx.netphone:id/btn_videoAnswer')
            btnVideoDial.click()
            self.myLog(u'test_videoAccept2 视频接听')
            time.sleep(3)
            btnVideoSwitchCamera = driver.find_element_by_id('com.lx.netphone:id/video_image_change_camera')
            btnVideoSwitchCamera.click()
            self.myLog(u'test_videoAccept2 切换摄像头1')
            time.sleep(3)
            btnVideoSwitchCamera.click()
            self.myLog(u'test_videoAccept2 切换摄像头2')
            time.sleep(3)
            btnVideoHangup = driver.find_element_by_id('com.lx.netphone:id/video_image_hang_up')
            btnVideoHangup.click()
            self.myLog(u'test_videoAccept2 视频挂断')
            time.sleep(3)
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
            self.test_getPermit(driver)
            self.test_audioDial(driver)
            self.test_audioAccept(driver)
            self.test_videoDial1(driver)
            self.test_videoAccept1(driver)
            self.test_videoDial2(driver)
            self.test_videoAccept2(driver)
            self.tearDown(driver)
        self.myLog("Exiting " + self.deviceInfo[0]['normalName'])

    

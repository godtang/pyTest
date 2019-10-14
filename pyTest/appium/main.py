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

def saveScreen(driver, e):
    baseImagePath = 'D:/CODE/pyTest/pyTest/exception/'
    desired_caps = desired_capabilities.get_desired_capabilities()
    phone = desired_caps['normalName']
    currentTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
    saveFile = baseImagePath + phone
    mkdirlambda = lambda x: os.makedirs(x) if not os.path.exists(x)  else True
    mkdirlambda(saveFile)
    saveFile = saveFile + '/' + currentTime + '.png'
    exc_type, exc_obj, exc_tb = sys.exc_info()
    lxLog.getDebugLog()(u"saveScreen\n截图：%s\n错误文件:%s:%d\n错误原因:%s", \
        saveFile, exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno, str(e))
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
        lxLog.getDebugLog()(u'setUp ok')
        return driver

def initDevice(deviceInfo):
    # 创建会话，得到driver对象，driver对象封装了所有的设备操作。下面会具体讲。
    driver = webdriver.Remote(deviceInfo[1], deviceInfo[0])
    if None == driver:
        return None
    else:
        lxLog.getDebugLog()(u'setUp ok')
        return driver

def test_getPermit(driver):
    lxLog.getDebugLog()(u'test_getPermit begin')
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
            saveScreen(driver, e)
            break
    lxLog.getDebugLog()(u'test_getPermit over')
   
def test_audioDial(driver):  
    lxLog.getDebugLog()(u'test_audioDial begin')
    try:
        btnAudioDial = driver.find_element_by_id('com.lx.netphone:id/btn_dial')
        lxLog.getDebugLog()(u'test_audioDial 语音拨号')
        btnAudioDial.click()
        time.sleep(3)
        btnAudioMute = driver.find_element_by_id('com.lx.netphone:id/button_audio_mute')
        btnAudioMute.click()
        lxLog.getDebugLog()(u'test_audioDial 禁用麦克风')
        time.sleep(3)
        btnAudioSpeaker = driver.find_element_by_id('com.lx.netphone:id/button_audio_speaker')
        btnAudioSpeaker.click()
        lxLog.getDebugLog()(u'test_audioDial 使用外放')
        time.sleep(3)
        btnAudioHangup = driver.find_element_by_id('com.lx.netphone:id/button_audio_hang_up')
        btnAudioHangup.click()
        lxLog.getDebugLog()(u'test_audioDial 语音挂断')
        time.sleep(3)
    except Exception as e:
        print e
        saveScreen(driver, e)
   
def test_audioAccept(driver): 
    lxLog.getDebugLog()(u'test_audioAccept begin')
    try:
        btnAudioDial = driver.find_element_by_id('com.lx.netphone:id/btn_answer')
        btnAudioDial.click()
        lxLog.getDebugLog()(u'test_audioAccept 语音接听')
        time.sleep(3)
        btnAudioMute = driver.find_element_by_id('com.lx.netphone:id/button_audio_mute')
        btnAudioMute.click()
        lxLog.getDebugLog()(u'test_audioAccept 禁用麦克风')
        time.sleep(3)
        btnAudioSpeaker = driver.find_element_by_id('com.lx.netphone:id/button_audio_speaker')
        btnAudioSpeaker.click()
        lxLog.getDebugLog()(u'test_audioAccept 使用外放')
        time.sleep(3)
        btnAudioHangup = driver.find_element_by_id('com.lx.netphone:id/button_audio_hang_up')
        btnAudioHangup.click()
        lxLog.getDebugLog()(u'test_audioAccept 语音挂断')
        time.sleep(3)
    except Exception as e:
        print e
        saveScreen(driver, e)
   
def test_videoDial1(driver):  
    lxLog.getDebugLog()(u'test_videoDial1 begin')
    try:
        btnVideoDial = driver.find_element_by_id('com.lx.netphone:id/btn_videoDial')
        btnVideoDial.click()
        lxLog.getDebugLog()(u'test_videoDial1 视频拨号')
        time.sleep(3)
        btnVideoSwitchCamera = driver.find_element_by_id('com.lx.netphone:id/video_image_change_camera')
        btnVideoSwitchCamera.click()
        lxLog.getDebugLog()(u'test_videoDial1 切换摄像头')
        time.sleep(3)
        btnVideoSwitchToAudio = driver.find_element_by_id('com.lx.netphone:id/video_image_change_voice_call')
        btnVideoSwitchToAudio.click()
        lxLog.getDebugLog()(u'test_videoDial1 视频转语音')
        time.sleep(3)
        btnAudioHangup = driver.find_element_by_id('com.lx.netphone:id/button_audio_hang_up')
        btnAudioHangup.click()
        lxLog.getDebugLog()(u'test_videoDial1 语音挂断')
        time.sleep(3)
    except Exception as e:
        print e
        saveScreen(driver, e)
   
def test_videoDial2(driver):  
    lxLog.getDebugLog()(u'test_videoDial2 begin')
    try:
        btnVideoDial = driver.find_element_by_id('com.lx.netphone:id/btn_videoDial')
        btnVideoDial.click()
        lxLog.getDebugLog()(u'test_videoDial2 视频接听')
        time.sleep(3)
        btnVideoSwitchCamera = driver.find_element_by_id('com.lx.netphone:id/video_image_change_camera')
        btnVideoSwitchCamera.click()
        lxLog.getDebugLog()(u'test_videoDial2 切换摄像头1')
        time.sleep(3)
        btnVideoSwitchCamera.click()
        lxLog.getDebugLog()(u'test_videoDial2 切换摄像头2')
        time.sleep(3)
        btnVideoHangup = driver.find_element_by_id('com.lx.netphone:id/video_image_hang_up')
        btnVideoHangup.click()
        lxLog.getDebugLog()(u'test_videoDial2 视频挂断')
        time.sleep(3)
    except Exception as e:
        print e
        saveScreen(driver, e)
   
def test_videoAccept1(driver):  
    lxLog.getDebugLog()(u'test_videoAccept1 begin')
    try:
        btnVideoDial = driver.find_element_by_id('com.lx.netphone:id/btn_videoAnswer')
        btnVideoDial.click()
        lxLog.getDebugLog()(u'test_videoAccept1 视频接听')
        time.sleep(3)
        btnVideoSwitchCamera = driver.find_element_by_id('com.lx.netphone:id/video_image_change_camera')
        btnVideoSwitchCamera.click()
        lxLog.getDebugLog()(u'test_videoAccept1 切换摄像头')
        time.sleep(3)
        btnVideoSwitchToAudio = driver.find_element_by_id('com.lx.netphone:id/video_image_change_voice_call')
        btnVideoSwitchToAudio.click()
        lxLog.getDebugLog()(u'test_videoAccept1 视频转语音')
        time.sleep(3)
        btnAudioHangup = driver.find_element_by_id('com.lx.netphone:id/button_audio_hang_up')
        btnAudioHangup.click()
        lxLog.getDebugLog()(u'test_videoAccept1 视频挂断')
        time.sleep(3)
    except Exception as e:
        print e
        saveScreen(driver, e)
   
def test_videoAccept2(driver):  
    lxLog.getDebugLog()(u'test_videoAccept2 begin')
    try:
        btnVideoDial = driver.find_element_by_id('com.lx.netphone:id/btn_videoAnswer')
        btnVideoDial.click()
        lxLog.getDebugLog()(u'test_videoAccept2 视频接听')
        time.sleep(3)
        btnVideoSwitchCamera = driver.find_element_by_id('com.lx.netphone:id/video_image_change_camera')
        btnVideoSwitchCamera.click()
        lxLog.getDebugLog()(u'test_videoAccept2 切换摄像头1')
        time.sleep(3)
        btnVideoSwitchCamera.click()
        lxLog.getDebugLog()(u'test_videoAccept2 切换摄像头2')
        time.sleep(3)
        btnVideoHangup = driver.find_element_by_id('com.lx.netphone:id/video_image_hang_up')
        btnVideoHangup.click()
        lxLog.getDebugLog()(u'test_videoAccept2 视频挂断')
        time.sleep(3)
    except Exception as e:
        print e
        saveScreen(driver, e)

def tearDown(driver): 
    lxLog.getDebugLog()(u'tearDown')
    # 测试结束，退出会话。 
    driver.quit()

class testThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, deviceInfo):
        threading.Thread.__init__(self)
        self.threadID = str(threadID)
        self.deviceInfo = deviceInfo
    def run(self):
        while True:
            lxLog.getDebugLog()("Starting " + self.threadID)
            driver = initDevice(self.deviceInfo)
            if None == driver:
                lxLog.getDebugLog()("程序初始化失败，请检查程序安装和首次调用")
            else:
                test_getPermit(driver)
                test_audioDial(driver)
                test_audioAccept(driver)
                test_videoDial1(driver)
                test_videoAccept1(driver)
                test_videoDial2(driver)
                test_videoAccept2(driver)
                tearDown(driver)
            lxLog.getDebugLog()("Exiting " + self.threadID)

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
    

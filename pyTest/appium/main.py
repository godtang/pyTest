# -*- coding: utf-8 -*-
#!/usr/bin/env python
from appium import webdriver
import desired_capabilities
from unittest import TestCase
import unittest
import time
import sys
import os
sys.path.append("..")
import tmjLog as lxLog
driver = None

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
    global driver
    driver = webdriver.Remote(uri, desired_caps)
    if None == driver:
        return
    else:
        lxLog.getDebugLog()('setUp ok')

def test_getPermit():
    lxLog.getDebugLog()('test_getPermit begin')
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
    lxLog.getDebugLog()('test_getPermit over')
   
def test_audioDial():  
    lxLog.getDebugLog()('test_audioDial begin')
    try:
        btnAudioDial = driver.find_element_by_id('com.lx.netphone:id/btn_dial')
        btnAudioDial.click()
        time.sleep(3)
        btnAudioMute = driver.find_element_by_id('com.lx.netphone:id/button_audio_mute')
        btnAudioMute.click()
        time.sleep(3)
        btnAudioSpeaker = driver.find_element_by_id('com.lx.netphone:id/button_audio_speaker')
        btnAudioSpeaker.click()
        time.sleep(3)
        btnAudioHangup = driver.find_element_by_id('com.lx.netphone:id/button_audio_hang_up')
        btnAudioHangup.click()
        time.sleep(3)
    except Exception as e:
        print e
        saveScreen(driver, e)
   
def test_audioAccept(): 
    lxLog.getDebugLog()('test_audioAccept begin')
    try:
        btnAudioDial = driver.find_element_by_id('com.lx.netphone:id/btn_answer')
        btnAudioDial.click()
        time.sleep(3)
        btnAudioMute = driver.find_element_by_id('com.lx.netphone:id/button_audio_mute')
        btnAudioMute.click()
        time.sleep(3)
        btnAudioSpeaker = driver.find_element_by_id('com.lx.netphone:id/button_audio_speaker')
        btnAudioSpeaker.click()
        time.sleep(3)
        btnAudioHangup = driver.find_element_by_id('com.lx.netphone:id/button_audio_hang_up')
        btnAudioHangup.click()
        time.sleep(3)
    except Exception as e:
        print e
        saveScreen(driver, e)
   
def test_videoDial1():  
    lxLog.getDebugLog()('test_videoDial1 begin')
    try:
        btnVideoDial = driver.find_element_by_id('com.lx.netphone:id/btn_videoDial')
        btnVideoDial.click()
        time.sleep(3)
        btnVideoSwitchCamera = driver.find_element_by_id('com.lx.netphone:id/video_image_change_camera')
        btnVideoSwitchCamera.click()
        time.sleep(3)
        btnVideoSwitchToAudio = driver.find_element_by_id('com.lx.netphone:id/video_image_change_voice_call')
        btnVideoSwitchToAudio.click()
        time.sleep(3)
        btnAudioHangup = driver.find_element_by_id('com.lx.netphone:id/button_audio_hang_up')
        btnAudioHangup.click()
        time.sleep(3)
    except Exception as e:
        print e
        saveScreen(driver, e)
   
def test_videoDial2():  
    lxLog.getDebugLog()('test_videoDial2 begin')
    try:
        btnVideoDial = driver.find_element_by_id('com.lx.netphone:id/btn_videoDial')
        btnVideoDial.click()
        time.sleep(3)
        btnVideoSwitchCamera = driver.find_element_by_id('com.lx.netphone:id/video_image_change_camera')
        btnVideoSwitchCamera.click()
        time.sleep(3)
        btnVideoSwitchCamera.click()
        time.sleep(3)
        btnVideoHangup = driver.find_element_by_id('com.lx.netphone:id/video_image_hang_up')
        btnVideoHangup.click()
        time.sleep(3)
    except Exception as e:
        print e
        saveScreen(driver, e)
   
def test_videoAccept1():  
    lxLog.getDebugLog()('test_videoAccept1 begin')
    try:
        btnVideoDial = driver.find_element_by_id('com.lx.netphone:id/btn_videoAnswer')
        btnVideoDial.click()
        time.sleep(3)
        btnVideoSwitchCamera = driver.find_element_by_id('com.lx.netphone:id/video_image_change_camera')
        btnVideoSwitchCamera.click()
        time.sleep(3)
        btnVideoSwitchToAudio = driver.find_element_by_id('com.lx.netphone:id/video_image_change_voice_call')
        btnVideoSwitchToAudio.click()
        time.sleep(3)
        btnAudioHangup = driver.find_element_by_id('com.lx.netphone:id/button_audio_hang_up')
        btnAudioHangup.click()
        time.sleep(3)
    except Exception as e:
        print e
        saveScreen(driver, e)
   
def test_videoAccept2():  
    lxLog.getDebugLog()('test_videoAccept2 begin')
    try:
        btnVideoDial = driver.find_element_by_id('com.lx.netphone:id/btn_videoAnswer')
        btnVideoDial.click()
        time.sleep(3)
        btnVideoSwitchCamera = driver.find_element_by_id('com.lx.netphone:id/video_image_change_camera')
        btnVideoSwitchCamera.click()
        time.sleep(3)
        btnVideoSwitchCamera.click()
        time.sleep(3)
        btnVideoHangup = driver.find_element_by_id('com.lx.netphone:id/video_image_hang_up')
        btnVideoHangup.click()
        time.sleep(3)
    except Exception as e:
        print e
        saveScreen(driver, e)

def tearDown(): 
    lxLog.getDebugLog()('tearDown')
    # 测试结束，退出会话。 
    driver.quit()

if __name__ == '__main__':
    setUp()
    test_getPermit()
    test_audioDial()
    test_audioAccept()
    test_videoDial1()
    test_videoAccept1()
    test_videoDial2()
    test_videoAccept2()
    tearDown()


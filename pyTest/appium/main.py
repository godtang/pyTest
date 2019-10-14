# -*- coding: utf-8 -*-
#!/usr/bin/env python
from appium import webdriver
import desired_capabilities
from unittest import TestCase
import unittest
import time

driver = None

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
        print 'setUp ok'

def test_getPermit():
    print 'test_getPermit begin'
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
            break
    print 'test_getPermit over'
   
def test_audioDial():  
    print 'test_audioDial begin'      
    time.sleep(3)
   
def test_audioAccept(): 
    print 'test_audioAccept begin'           
    time.sleep(3)
   
def test_videoDial():  
    print 'test_videoDial begin'          
    time.sleep(3)
   
def test_videoAccept():  
    print 'test_videoAccept begin'          
    time.sleep(3)

def tearDown(): 
    print 'tearDown'    
    # 测试结束，退出会话。 
    driver.quit()

if __name__ == '__main__':
    setUp()
    test_getPermit()
    test_audioDial()
    test_audioAccept()
    test_videoDial()
    test_videoAccept()
    tearDown()


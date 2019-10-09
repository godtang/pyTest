# -*- coding: utf-8 -*-
import tmjLog as lxLog
from appium import webdriver

# 我们使用python的unittest作为单元测试工具
from unittest import TestCase
# 我们使用python的unittest作为单元测试工具
import unittest
import time

def get_desired_capabilities():
    desired_caps = {
        'platformName': 'Android',
        'platformVersion': '7.0',
        'deviceName': 'V889F',
        'appPackage': 'com.lx.netphone',
        'appWaitPackage': 'com.lx.netphone',
        'app': 'D:/CODE/IM_project_net_phone/android/app/build/outputs/apk/debug/app-debug.apk',
        'newCommandTimeout': 30,
        'automationName': 'Appium'
    }
    return desired_caps
def get_uri():
    return "http://localhost:4723/"

class MqcTest(TestCase):
   global automationName
   def setUp(self):
       # 获取我们设定的capabilities，通知Appium Server创建相应的会话。
       desired_caps = get_desired_capabilities()
       # 获取server的地址。 
       uri = get_uri()
       # 获取使用的测试框架
       self.automationName = desired_caps.get('automationName')
       # 创建会话，得到driver对象，driver对象封装了所有的设备操作。下面会具体讲。
       self.driver = webdriver.Remote(uri, desired_caps)
   def test_searchbox(self):
        # 找到包含”Tab4”字符串的控件。
        if self.automationName == 'Appium':
            tab4 = self.driver.find_element_by_name("Tab4")
        else:
            tab4 = self.driver.find_element_by_link_text("Tab4")
        # 点击.
        tab4.click()
        # 等待2秒钟
        time.sleep(2)
        # 通过控件类名找到用户名和密码输入框。
        editTexts = self.driver.find_elements_by_class_name("android.widget.EditText")
        # 第一个框为用户名输入框，输入用户名；第二个框为密码框，输入密码
        editTexts[0].send_keys("admin")
        editTexts[1].send_keys("admin")
        # 隐藏出现的软键盘
        self.driver.hide_keyboard()
        # 找到包含“登录”的按钮并点击
        if self.automationName == 'Appium':
            self.driver.find_element_by_name("登陆").click()
        else:
            self.driver.find_element_by_link_text("登陆").click()
        # 等待3秒钟，登录需要与服务器通讯。 
        time.sleep(3)
   def tearDown(self): 
        # 测试结束，退出会话。 
        self.driver.quit()
if __name__ == '__main__':
    unittest.main()

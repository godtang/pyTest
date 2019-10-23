# -*- coding: utf-8 -*-
#!/usr/bin/env python
def get_desired_capabilities():
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    
    #华为荣耀6P
    desired_caps['platformVersion'] = '4.4.2'
    desired_caps['deviceName'] = 'F8UDU15818002253'
    desired_caps['normalName'] = u'荣耀6P'
    '''
    #华为荣耀X1
    desired_caps['platformVersion']='4.4'
    desired_caps['deviceName'] = 'T7K6R14B01000626'
    desired_caps['normalName'] = u'荣耀X1'
    #红米NOTE6A
    desired_caps['platformVersion']='9'
    desired_caps['deviceName'] = '0d68e2427d32'
    desired_caps['normalName'] = u'红米NOTE6A'
    #华为荣耀畅玩7
    desired_caps['platformVersion']='8.1.0'
    desired_caps['deviceName']='HFK9K19330910557'
    desired_caps['normalName'] = u'荣耀畅玩7'
    '''

    desired_caps['noReset'] = True

    #测试apk包的路径
    #desired_caps['app']="D:/CODE/IM_project_net_phone/android/app/build/outputs/apk/debug/app-debug.apk"

    #如果设置了apk包的路径，则不需要配appPackage和appActivity
    desired_caps['appPackage'] = 'com.lx.netphone'
    desired_caps['appWaitPackage'] = 'com.lx.netphone'
    desired_caps['appActivity'] = 'MainActivity'
    
    desired_caps['newCommandTimeout'] = 30
    if int(desired_caps['platformVersion'][0]) >= 5:
        desired_caps['automationName'] = 'Appium'
    else:
        desired_caps['automationName'] = 'UiAutomator1'
    desired_caps['autoGrantPermissions'] = True

    return desired_caps

def get_uri():
    return 'http://localhost:4723/wd/hub'

def get_deviceInfos():
    deviceInfoList = []
    deviceInfoRedmi6A = []
    deviceInfoRedmi6A.append({
  "platformName": "Android",
  "platformVersion": "9",
  "deviceName": "0d68e2427d32",
  "noReset": True,
  "appPackage": "com.lx.netphone",
  "appWaitPackage": "com.lx.netphone",
  "appActivity": "MainActivity",
  "newCommandTimeout": 30,
  "automationName": "Appium",
  "autoGrantPermissions": True,
  "normalName": "redmi6a"
})
    deviceInfoRedmi6A.append('http://localhost:4723/wd/hub')

    deviceInfoHonor6P = []
    deviceInfoHonor6P.append({
  "platformName": "Android",
  "platformVersion": "4.4.2",
  "deviceName": "F8UDU15818002253",
  "noReset": True,
  "appPackage": "com.lx.netphone",
  "appWaitPackage": "com.lx.netphone",
  "appActivity": "MainActivity",
  "newCommandTimeout": 30,
  "autoGrantPermissions": True,
  "automationName": "UiAutomator1",
  "normalName": "honor6p"
})
    deviceInfoHonor6P.append('http://localhost:4723/wd/hub')

    deviceInfoHonorX1 = []
    deviceInfoHonorX1.append({
  "platformName": "Android",
  "platformVersion": "4.4.2",
  "deviceName": "T7K6R14B01000626",
  "noReset": True,
  "appPackage": "com.lx.netphone",
  "appWaitPackage": "com.lx.netphone",
  "appActivity": "MainActivity",
  "newCommandTimeout": 30,
  "autoGrantPermissions": True,
  "automationName": "UiAutomator1",
  "normalName": "honorx1"
})
    deviceInfoHonorX1.append('http://192.168.3.76:4723/wd/hub')

    deviceInfoHonor7 = []
    deviceInfoHonor7.append({
  "platformName": "Android",
  "platformVersion": "8.1.0",
  "deviceName": "HFK9K19330910557",
  "noReset": True,
  "appPackage": "com.lx.netphone",
  "appWaitPackage": "com.lx.netphone",
  "appActivity": "MainActivity",
  "newCommandTimeout": 30,
  "autoGrantPermissions": True,
  "automationName": "Appium",
  "normalName": "honor7"
})
    deviceInfoHonor7.append('http://localhost:4723/wd/hub')

    deviceInfoIPhone6P = []
    deviceInfoIPhone6P.append({
  "automationName": "XCUITest",
  "platformName": "iOS",
  "platformVersion": "12.4.1",
  "deviceName": "iPhone 6 Plus",
  "bundleId": "com.lx.NtePhone",
  "udid": "5946f3c3d63f7a1455f18f4612c8ff26c9b5f033",
  "normalName": "iPhone6Plus"
})
    deviceInfoIPhone6P.append('http://192.168.3.81:4723/wd/hub')

    deviceInfoRedmi6A_chat = []
    deviceInfoRedmi6A_chat.append({
  "platformName": "Android",
  "platformVersion": "9",
  "deviceName": "0d68e2427d32",
  "noReset": True,
  "appPackage": "com.lx.chat",
  "appActivity": "com.lx.longxin2.main.main.ui.SplashActivity",
  "newCommandTimeout": 30,
  "automationName": "Appium",
  "autoGrantPermissions": True,
  "normalName": "redmi6a"
})
    deviceInfoRedmi6A_chat.append('http://localhost:4723/wd/hub')

    deviceInfoRedmi6A_chatInstall = []
    deviceInfoRedmi6A_chatInstall.append({
  "platformName": "Android",
  "platformVersion": "9",
  "deviceName": "0d68e2427d32",
  "noReset": True,
  "app": "D:/CODE/IM_project_net_phone/android/app/build/outputs/apk/debug/app-debug.apk",
  "appPackage": "com.lx.netphone",
  "appWaitPackage": "com.lx.netphone",
  "appActivity": "MainActivity",
  "newCommandTimeout": 30,
  "automationName": "Appium",
  "autoGrantPermissions": True,
  "normalName": "redmi6a"
})
    deviceInfoRedmi6A_chatInstall.append('http://localhost:4723/wd/hub')

    deviceInfoHonor6P_lx = []
    deviceInfoHonor6P_lx.append({
  "platformName": "Android",
  "platformVersion": "4.4.2",
  "deviceName": "F8UDU15818002253",
  "noReset": True,
  "appPackage": "com.lx.chat",
  "appWaitPackage": "com.lx.chat",
  "appActivity": "com.lx.longxin2.main.main.ui.SplashActivity",
  "newCommandTimeout": 30,
  "autoGrantPermissions": True,
  "automationName": "UiAutomator1",
  "normalName": "honor6p"
})
    deviceInfoHonor6P_lx.append('http://localhost:4723/wd/hub')

    deviceInfoIPhone6P_lx = []
    deviceInfoIPhone6P_lx.append({
  "automationName": "XCUITest",
  "platformName": "iOS",
  "platformVersion": "12.4.1",
  "deviceName": "iPhone 6 Plus",
  "bundleId": "com.laixun.longxins",
  "udid": "5946f3c3d63f7a1455f18f4612c8ff26c9b5f033",
  "normalName": "iPhone6Plus"
})
    deviceInfoIPhone6P_lx.append('http://192.168.3.81:4723/wd/hub')


    #deviceInfoList.append(deviceInfoRedmi6A)
    #deviceInfoList.append(deviceInfoHonor6P)
    #deviceInfoList.append(deviceInfoHonorX1)
    #deviceInfoList.append(deviceInfoHonor7)
    #deviceInfoList.append(deviceInfoIPhone6P)
    #deviceInfoList.append(deviceInfoRedmi6A_chat)
    deviceInfoList.append(deviceInfoIPhone6P_lx)

    return deviceInfoList

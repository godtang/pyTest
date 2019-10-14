# -*- coding: utf-8 -*-
#!/usr/bin/env python

def get_desired_capabilities():
    desired_caps={}
    desired_caps['platformName']='Android'
    
    #华为荣耀6P
    desired_caps['platformVersion']='4.4.2'
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

    desired_caps['noReset']=True

    #测试apk包的路径
    #desired_caps['app']="D:/CODE/IM_project_net_phone/android/app/build/outputs/apk/debug/app-debug.apk" 

    #如果设置了apk包的路径，则不需要配appPackage和appActivity
    desired_caps['appPackage']='com.lx.netphone'
    desired_caps['appWaitPackage']='com.lx.netphone'
    desired_caps['appActivity']='MainActivity'
    
    desired_caps['newCommandTimeout']=30
    if int(desired_caps['platformVersion'][0]) >= 5:
        desired_caps['automationName']='Appium'
    else:
        desired_caps['automationName']='UiAutomator1'
    desired_caps['autoGrantPermissions']=True

    return desired_caps

def get_uri():
    return 'http://localhost:4723/wd/hub'

def get_deviceInfos():
    deviceInfos = []
    deviceInfo = []
    deviceInfo.append({
  "platformName": "Android",
  "platformVersion": "9",
  "deviceName": "0d68e2427d32",
  "noReset": True,
  "appPackage": "com.lx.netphone",
  "appWaitPackage": "com.lx.netphone",
  "appActivity": "MainActivity",
  "newCommandTimeout": 30,
  "automationName": "Appium",
  "autoGrantPermissions": True
})
    deviceInfo.append('http://localhost:4723/wd/hub')
    deviceInfos.append(deviceInfo)
    deviceInfo = []
    deviceInfo.append({
  "platformName": "Android",
  "platformVersion": "4.4.2",
  "deviceName": "F8UDU15818002253",
  "noReset": True,
  "appPackage": "com.lx.netphone",
  "appWaitPackage": "com.lx.netphone",
  "appActivity": "MainActivity",
  "newCommandTimeout": 30,
  "autoGrantPermissions": True,
  "automationName": "UiAutomator1"
})
    deviceInfo.append('http://localhost:4723/wd/hub')
    deviceInfos.append(deviceInfo)

    return deviceInfos

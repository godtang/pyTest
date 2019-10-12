import os
from appium import webdriver
import time
 
#apk_path=os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) #获取当前项目的根路径
 
desired_caps={}
desired_caps['platformName']='Android'

'''
desired_caps['platformVersion']='8.1.0'
desired_caps['deviceName']='HFK9K19330910557'#adb devices命令输入的设置名称
'''
desired_caps['platformVersion']='9'
desired_caps['deviceName'] = '0d68e2427d32'

desired_caps['noReset']=True
#测试apk包的路径
#desired_caps['app']="D:/CODE/IM_project_net_phone/android/app/build/outputs/apk/debug/app-debug.apk" 

#如果设置了apk包的路径，则不需要配appPackage和appActivity
desired_caps['appPackage']='com.lx.netphone'
desired_caps['appActivity']='MainActivity'
 
driver=webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)#启动app


btn_dial = driver.find_element_by_id('com.lx.netphone:id/btn_dial')
if None != btn_dial:
    btn_dial.click()


time.sleep(20)
driver.quit()
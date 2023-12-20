from airtest.core.api import *
import pytest
from Config.config import Mobile,Web
import allure
class MobileBasePage:
    #poco = None
    imagePath = Mobile().DaBao['imagePath']
    def locator(self, loc, type):
        if type == 'text':
            self.poco(text=loc).wait_for_appearance(timeout=10)
            with allure.step("元素定位-成功(text)：" + str(loc)):
                print("元素定位-成功(text)：" + str(loc))
            return True
        if type == 'name':
            self.poco(name=loc).wait_for_appearance(timeout=10)
            with allure.step("元素定位-成功(name)：" + str(loc)):
                print("元素定位-成功(name)：" + str(loc))
            return True
        if type == 'image':
            if exists(loc):
                with allure.step("元素定位-成功(image)：" + str(loc)):
                    print("元素定位-成功(image)：" + str(loc))
                return True
        else:
            with allure.step("不存在元素类型：类型为：" +type+"，属性为："+str(loc)):
                print("不存在元素类型：类型为：" +type+"，属性为："+str(loc))
            pytest.assume(False)
            return False
    def click(self, loc, type):
        if self.locator(loc, type):
            if type == 'text':
                self.poco(text=loc).click()
                with allure.step("点击元素(text)：" + str(loc)):
                    print("点击元素(text)：" + str(loc))
                return True

            if type == 'name':
                self.poco(name=loc).click()
                with allure.step("点击元素(name)：" + str(loc)):
                    print("点击元素(name)：" + str(loc))
                return True

            if type == 'image':
                touch(loc)
                with allure.step("点击元素(image)：" + str(loc)):
                    print("点击元素(image)：" + str(loc))
                return True

        else:
            with allure.step("点击元素-失败：" + str(loc) + type):
                print("点击元素-失败：" + str(loc) + type)
            pytest.assume(False)
            return False

    def setValue(self,loc,value,type):
        if self.locator(loc, type):
            if type == 'name':
                input_box = self.poco(name=loc)
                input_box.setattr("text", value)
                with allure.step("元素赋值-成功(name)：" + str(loc)):
                    print("元素赋值-成功(name)：" + str(loc))
            if type == 'text':
                input_box = self.poco(text=loc)
                input_box.setattr("text", value)
                with allure.step("元素赋值-成功(text)：" + str(loc)):
                    print("元素赋值-成功(text)：" + str(loc))
        else:
            with allure.step("元素赋值-失败：" + str(loc) + type):
                print("元素赋值-失败：" + str(loc) + type)
            pytest.assume(False)

    def inputValueAirtest(self,loc,value,type):
        if self.click(loc, type):
            if type == 'name':
                text(value)
                with allure.step("元素赋值-成功(name)：" + str(loc)):
                    print("元素赋值-成功(name)：" + str(loc))
            if type == 'text':
                text(value)
                with allure.step("元素赋值-成功(text)：" + str(loc)):
                    print("元素赋值-成功(text)：" + str(loc))
            if type == 'image':
                text(value)
                with allure.step("元素赋值-成功(image)：" + str(loc)):
                    print("元素赋值-成功(image)：" + str(loc))
        else:
            with allure.step("元素赋值-失败：" + str(loc) + type):
                print("元素赋值-失败：" + str(loc) + type)
            pytest.assume(False)

    def inputValuePoco(self,loc,value,type):
        if self.click(loc, type):
            if type == 'name':
                self.poco(name=loc).set_text(value)
                with allure.step("元素赋值-成功(name)：" + str(loc)):
                    print("元素赋值-成功(name)：" + str(loc))
            if type == 'text':
                self.poco(text=loc).set_text(value)
                with allure.step("元素赋值-成功(text)：" + str(loc)):
                    print("元素赋值-成功(text)：" + str(loc))
        else:
            with allure.step("元素赋值-失败：" + str(loc) + type):
                print("元素赋值-失败：" + str(loc) + type)
            pytest.assume(False)

class WebBasePage:
    imagePath = Web().xdz['imagePath']
    def openUrl(self,url):
        with allure.step("打开地址：" +url):
            print("打开地址：" +url)
            self.driver.get(self.url)
    #判断元素是否存在


    # 查找并返回元素
    def findElement(self,loc,type):
        try:
            if type == 'xpath' :
                with allure.step("发现元素:%s" % loc+',类型：xpath'):
                    print("发现元素:%s" % loc+',类型：xpath')
                element = self.driver.find_element_by_xpath(loc)
                return element
            # if type == 'xpath' :
            #     with allure.step("发现元素:%s" % loc+'xpath'):
            #         print("发现元素:%s" % loc+'xpath')
            #     element = self.driver.find_element_by_xpath(loc)
            #     return element
        except:
            with allure.step("发现元素失败:%s"  %(loc)):
                print("发现元素失败:%s"  %(loc))
            pytest.assume(False)
            return False




    def sendKeys(self,loc,type,value):
        self.findElement(loc,type).send_keys(value)
        with allure.step("输入:%s" % value):
            print("输入:%s" % value)

    def jsExcute(self,value):
        with allure.step("JS点击:%s" % value):
            print("点击:%s" % value )
            self.driver.execute_script(value)

    def click(self,loc,type):
        self.findElement(loc,type).click()
        with allure.step("点击:%s" % loc):
            print("点击:%s" % loc )

    def assertText(self,loc,type,text):
        if text in self.findElement(loc, type).text:
            with allure.step("文字断言:%s-成功" % text):
                print("文字断言:%s-成功" % text)
            pytest.assume(True)
        else:
            with allure.step("文字断言-失败:%s，实际为:%s" % (text,self.findElement(loc, type).text)):
                print("文字断言:%s-失败，实际为:%s" % (text,self.findElement(loc, type).text))
            pytest.assume(False)
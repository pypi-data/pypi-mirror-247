import time
from random import random
import datetime
import random
import subprocess
import pytest
import allure
from PIL import Image
import ddddocr
from Config.config import CommonConfig,Interface,Web
import pymysql
import os
import hashlib
import requests
import json
from redis.client import StrictRedis
class fun:
    # def get_time(self):
    #     time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     return time

    def check_assert(self,expected, result, type):
        with allure.step('断言期望内容：' + json.dumps(expected, indent=4, ensure_ascii=False)+'；断言模式：'+type):
            print('断言期望内容：' + json.dumps(expected, indent=4, ensure_ascii=False)+'；断言模式：'+type)
        if result != None:
            if expected == None:
                with allure.step('断言结果：无须断言'):
                    print('断言结果：无须断言')
                    pytest.assume(True)
                    return True
            else:
                if type == 'and':
                    for expected_key, expected_value in expected.items():
                        # 取出的键值拼装新的单个字典
                        dic = dict.fromkeys([expected_key], expected_value)
                        # 字典转为字符串，并截取dic的花括号
                        dic = str(dic)
                        # 截取去除花括号
                        dic = dic[1:len(dic) - 1]
                        result = str(result)
                        # print(str(dic),str(result))
                        if dic in result :
                            continue
                        if dic not in result:
                            with allure.step('断言结果：断言失败'):
                                print('断言结果：断言失败')
                                pytest.assume(False)
                                return False
                    with allure.step('断言结果：断言成功'):
                        print('断言结果：断言成功')
                        pytest.assume(True)
                        return True
                if type == 'or':
                    for expected_key, expected_value in expected.items():
                        # 取出的键值拼装新的单个字典
                        dic = dict.fromkeys([expected_key], expected_value)
                        # 字典转为字符串，并截取dic的花括号
                        dic = str(dic)
                        # 截取去除花括号
                        dic = dic[1:len(dic) - 1]
                        result = str(result)
                        if dic in result:
                            with allure.step('断言结果：断言成功'):
                                print('断言结果：断言成功')
                                pytest.assume(True)
                                return True
                        if dic not in result:
                            continue
                    with allure.step('断言结果：断言失败'):
                        print('断言结果：断言失败')
                        pytest.assume(False)
                        return False
                if type == 'not_and':
                    for expected_key, expected_value in expected.items():
                        # 取出的键值拼装新的单个字典
                        dic = dict.fromkeys([expected_key], expected_value)
                        # 字典转为字符串，并截取dic的花括号
                        dic = str(dic)
                        # 截取去除花括号
                        dic = dic[1:len(dic) - 1]
                        result = str(result)
                        # print(str(dic),str(result))
                        if dic not in result:
                            continue
                        if dic  in result:
                            with allure.step('断言结果：断言失败'):
                                print('断言结果：断言失败')
                                pytest.assume(False)
                                return False
                    with allure.step('断言结果：断言成功'):
                        print('断言结果：断言成功')
                        pytest.assume(True)
                        return True
                if type == 'not_or':
                    for expected_key, expected_value in expected.items():
                        # 取出的键值拼装新的单个字典
                        dic = dict.fromkeys([expected_key], expected_value)
                        # 字典转为字符串，并截取dic的花括号
                        dic = str(dic)
                        # 截取去除花括号
                        dic = dic[1:len(dic) - 1]
                        result = str(result)
                        if dic not in result:
                            with allure.step('断言结果：断言成功'):
                                print('断言结果：断言成功')
                                pytest.assume(True)
                                return True
                        if dic in result:
                            continue
                    with allure.step('断言结果：断言失败'):
                        print('断言结果：断言失败')
                        pytest.assume(False)
                        return False
        else:
            pytest.assume(False)
            return False
            print('接口返回为空')

    #随机生成身份证
    def generate_id(self):
        # 地区码，可根据实际情况修改
        region_code = '110101'
        birth_year = str(random.randint(1950, 2015))
        birth_month = str(random.randint(1, 12)).rjust(2, '0')
        birth_day = str(random.randint(1, 28)).rjust(2, '0')
        sequence_code = str(random.randint(1, 999)).rjust(3, '0')
        id_17 = region_code + birth_year + birth_month + birth_day + sequence_code
        # 加权因子
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        # 校验码对应值
        check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
        # 对前17位数字依次乘以对应的加权因子并求和
        total = sum(int(id_17[i]) * weights[i] for i in range(17))
        check_digit = check_codes[total % 11]
        return id_17 + check_digit

    #随机生成车牌号
    def generate_license_plate(self):
        # 车牌号码由省份+字母+数字组成
        provinces = ["京", "津", "沪", "渝", "冀", "豫", "云", "辽", "黑", "湘", "皖", "鲁", "新", "苏", "浙", "赣",
                     "鄂", "桂", "甘", "晋", "蒙", "陕", "吉", "闽", "贵", "粤", "青", "藏", "川", "宁", "琼"]
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numbers = "0123456789"

        province = random.choice(provinces)
        letter = random.choice(letters)
        number = "".join(random.choice(numbers) for _ in range(5))

        license_plate = province + letter + number
        return license_plate

    #向手机传输电脑图片
    def import_image(self,image_path, dest_path):
        command = f"adb push {image_path} {dest_path}"
        command1 =f"adb shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{dest_path}"
        subprocess.run(command.split(), stdout=subprocess.PIPE)
        subprocess.run(command1.split(), stdout=subprocess.PIPE)


    #
    # #UI自动化判断元素是否存在
    # def is_element_exist(self, driver,text):
    #
    #     max_retry = 5
    #     #driver.implicitly_wait(60)
    #     wait = WebDriverWait(driver, 10)
    #     wait.until(lambda driver: driver.page_source)
    #     source = driver.page_source
    #     # 循环重试
    #     for i in range(1,max_retry+1):
    #         time.sleep(1)
    #         #print(source)
    #         if text in source:
    #             print('找到元素：'+text)
    #             return True
    #         else:
    #             print('未找到元素：'+text+';进行第'+str(i)+'次重试')
    #             if i == max_retry:
    #                 print('未找到元素：'+text)
    #                 return False
    #新大宗验证码校验
    def verificationCode(self,driver,element):

        while True:
            driver.screenshot(Web().xdz['imagePath']+'printscreen.png')
            imgelement = driver.find_element_by_xpath(element)
            location = imgelement.location
            # 获取验证码的长宽
            size = imgelement.size
            # 写成我们需要截取的位置坐标
            rangle = (int(location['x']),
                      int(location['y']),
                      int(location['x'] + size['width']),
                      int(location['y'] + size['height']))
            i = Image.open(Web().xdz['imagePath']+'printscreen.png')
            fimg = i.crop(rangle)
            fimg = fimg.convert('RGB')
            # 保存我们截下来的验证码图片，并读取验证码内容
            fimg.save(Web().xdz['imagePath']+'code.png', quality=95, subsampling=0, compress_level=0)
            ocr = ddddocr.DdddOcr()
            with open(Web().xdz['imagePath']+'code.png', 'rb') as f:
                img_bytes = f.read()
                res = ocr.classification(img_bytes)
            print('原始验证码' + res)
            if len(res) == 4 and res.isdigit():
                print('识别正确'+res)
                break
            else:
                driver.execute_script(
                    "document.getElementsByClassName('code_image')[0].click()")
                time.sleep(1)
        print('返回正确验证码' + res)
        return res


    def excuteSql(sefl,host,user,password,db,filePath):
        conn = pymysql.connect(host=host, user=user, password=password, db=db)
        cursor = conn.cursor()

        # 读取 SQL 文件
        with open(CommonConfig.rootPath+filePath, 'r',encoding='utf-8') as f:
            sqlList = f.readlines()
            for sql in sqlList:
                print('执行sql：'+sql)
                cursor.execute(sql)
        conn.close()
    def video_result(self):
        trans_id = '6FEB23ACB0374985A2A52D282EDD5361u6643'
        app_security_key = 'ca61c3b7b9d50ae0406070c8758190b1'
        reward_name = '自动化测试'
        check_sign_raw = "%s:%s" % (app_security_key, trans_id)
        sign = hashlib.sha256(check_sign_raw.encode('utf-8')).hexdigest()

        # print(sign)
        url = "https://api.test.qy566.com/rest/receiveAdCallback?user_id=" + Interface().JiFen['user_id'] + "&trans_id=" + trans_id + "&reward_name=" + reward_name + "&reward_amount=10&extra={'source':'ios'}&sign=" + sign
        # url2 = "https://api.test.qy566.com/rest/receiveAdCallback?user_id=123&trans_id=5646282&reward_name=积分&reward_amount=1&extra={\"source\": \"android\"}&sign=18db1451c7b80f56d6c3d809ebb2ba983a1fbad90d3836687298257d54131b5b"
        res = requests.get(url=url)
        print(url)
        print(res.text)
        return json.loads(res.text)



import json
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)

import requests
from Common.fun_util import fun_util,DateEncoder
import allure
import json


class requsts_util:
    session = requests.session()
    def send_request(self,method,url,data,headers,**kwargs):
        method = str(method).lower()
        #rep = None
        try:
            if method == 'get':
                rep = requsts_util.session.request(method=method, url=url, params=data,headers = headers,**kwargs)
            else:
                if 'form' in str(headers):
                    rep = requsts_util.session.request(method=method, url=url, data=data,headers= headers, **kwargs)
                else:
                    rep = requsts_util.session.request(method=method, url=url, json=data,headers= headers, **kwargs)
        except:
            print('无法连接')
        else:
            if rep.status_code==200:
                resp = json.loads(rep.text)
                return resp
            else:
                print('请求状态异常：'+str(rep.status_code))





    def excute_interface(self,caseinfo1,domain):
        #循环读取yml中配置的接口参数
        for caseinfo in caseinfo1:
            #caseinfo是个dic，通过caseinfo.keys()获取key，使用list()转为list类型，取下标0即可，yml测试数据的动态管理
            caseinfo_key = list(caseinfo.keys())[0]
            #从config文件中读取domain与接口地址拼接,login接口可能用别的域名，判断一下

            url = domain + caseinfo[caseinfo_key]['path']
            #读取请求类型
            method = caseinfo[caseinfo_key]['method']
            #读取请求数据
            data = caseinfo[caseinfo_key]['data']
            #读取请求头
            headers = caseinfo[caseinfo_key]['headers']
            #读取断言类型
            assert_type = caseinfo[caseinfo_key]['assert_type']
            #读取断言信息
            is_assert = caseinfo[caseinfo_key]['is_assert']
            #读取描述
            description = caseinfo[caseinfo_key]['description']
            #发送请求
            resp = self.send_request(method=method,url=url,data=data,headers=headers)
            print('\n')
            print('描述：')
            print(description )
            with allure.step('请求url：'+url):
                print('\n'+'请求url：')
                print(url+'\n')
            with allure.step('请求header：'+json.dumps(headers,indent = 4,ensure_ascii=False)):
                print('请求header：')
                print(json.dumps(headers,indent = 4,ensure_ascii=False)+'\n')
            with allure.step('请求body：'+json.dumps(data,indent = 4,ensure_ascii=False,cls=DateEncoder)):
                print('请求body：')
                print(json.dumps(data,indent = 4,ensure_ascii=False,cls=DateEncoder)+'\n')
            with allure.step('返回：'+json.dumps(resp,indent = 4,ensure_ascii=False)):
                print('返回：')
                print(json.dumps(resp,indent = 4,ensure_ascii=False)+'\n')
            fun_util().check_assert(is_assert,resp,assert_type)

        print('----------------------------------------------------------------------------------------------------------')
        return resp

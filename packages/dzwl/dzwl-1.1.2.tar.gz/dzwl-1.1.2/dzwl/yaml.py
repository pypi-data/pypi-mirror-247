import os
import yaml
from string import Template
import json
from Config.config import CommonConfig
class yaml_util:
    #读取extract.yml文件
    rootPath = CommonConfig.rootPath
    def read_extract_yaml(self,key):
        with open(self.rootPath+"/Common/common_var.yml",mode='r',encoding='utf-8') as f:
            value = yaml.load(stream=f,Loader=yaml.FullLoader)
            return value[key];


    def write_extract_yaml(self,data):
        file_path = os.path.join(self.rootPath, "Common", "common_var.yml")

        # 读取文件中的所有数据
        with open(file_path, mode='r', encoding='utf-8') as f:
            all_data = yaml.safe_load(f) or {}

        # 将传入的数据转换为字典格式，并更新到all_data中
        for d in data:
            for key_data in d.keys():
                if key_data in all_data:
                    all_data[key_data]=d[key_data]
                else:
                    all_data.update(d)


        # 将所有数据写入文件中
        with open(file_path, mode='w', encoding='utf-8') as f:
            yaml.dump(data=all_data, stream=f, allow_unicode=True)


    #清除extract.ym1文件
    def clean_extract_yaml(self) :
        with open(self.rootPath+"/Common/common_var.yml",mode='w',encoding='utf-8') as f:
            f.truncate()

    #读取测试用例的yml文件
    def read_testcase_yaml(self,yaml_name):
        with open(self.rootPath+yaml_name,mode='r',encoding='utf-8') as f:
            value = yaml.load(stream=f,Loader=yaml.FullLoader)
            return value;

    #写入测试用例的yml文件
    def write_testcase_yaml(self,caseinfo,content) :
        caseinfo_str = json.dumps(caseinfo)
        for cont in content:
            c = Template(caseinfo_str).safe_substitute(cont)
            caseinfo_str = c
        caseinfo_str = caseinfo_str.replace('"None"', 'null')
        caseinfo_list =json.loads(caseinfo_str)
        return caseinfo_list



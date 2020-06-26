#-*-coding:utf-8-*-
"""
@author zhj1121
@date 2020.6.24
@desc 一个文件操作的类，包含多个文件操作方法
"""
import json
import os
import shutil
# from db_conf import db_data_file as workFile
from conf.db_conf import db_data_file as workFile

class db_File():
    '''easyredis的文件操作'''
    def __init__(self,workfile=workFile):
        """
            args:workFile(db_data_file)easyredis数据持久化文件
        """
        self.file = workfile
    def write(self,content):
        '''
            描述：写入文件，以覆盖的方式
            功能：用户
            参数：content(记录的内容)
            返回值：boole类型
        '''
        with open(self.file, "w", encoding='utf-8') as f:
            json.dump(content, f,indent=2,sort_keys=True, ensure_ascii=False)
        return True
    def additional(self,content):
        """
            描述：写文件，以追加的方式
            功能：用于日志的记录(此时的workfile非easyredis数据持久化文件)
            返回值：boole类型
        """
        with open(self.file, "a", encoding='utf-8') as f:
            f.write(content+'\n')
        return True
    def read(self):
        '''
            描述：读取文件
            返回值：根据json格式返回
        '''
        with open(self.file, encoding="utf-8") as f:
            data = json.load(f)
        return data
    def delete(self):
        '''
            描述：删除文件
            返回值：boole类型
        '''
        os.remove(self.file)
        return True
    def copy(self,backfile):
        '''
            描述：复制备份文件，将工作文件进行备份，预防数据丢失
            返回值：boole类型
        '''
        shutil.copyfile(self.file, backfile)
        return True
    def recopy(self,backfile):
        '''
            描述：复制备份文件，将备份文件的内容复制到工作文件中
            返回值：boole类型
        '''
        shutil.copyfile(backfile,self.file)
        return True
# if __name__ == "__main__":
#     mydict = {'zhj':{'type':'hash','json':'11111'}}
    # file = db_File('data/da.json')
    # file.write(mydict)#success
    #print(file.read())#success
    #file.copy('data/back.json')#success
    #file.recopy('data/back.json')
    # file = db_File('log/data.log')
    # file.additional("a123")
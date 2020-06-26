#-*-coding:utf-8-*-
"""
@author zhj1121
@date 2020.6.24
@desc 一个用于处理关于easyredis的命令文件的类
"""
import json
import os
import shutil
import random
from conf.db_conf import command_path
from conf.db_conf import command_file

class db_command(object):
    def __init__(self,command_file=command_file,command_path = command_path):
        self.command_file = command_file
        self.command_path = command_path
    def randomTouchFile(self):
        """ 随机生成一个不存在的文件，并返回路径 """
        file_list = os.listdir(self.command_path)
        str = 'abcdefghijklmnopqrstuvwxyz123456789'
        touchFileName = ""
        while touchFileName in file_list or touchFileName == "":
            touchFileName = ""
            for i in range(8):
                touchFileName += random.choice(str)
            touchFileName += ".txt"
        shutil.copyfile(self.command_file, self.command_path+touchFileName)
        return self.command_path+touchFileName
    def delete(self,filePath):
        """ 根据路径，删除一个文件 """
        os.remove(filePath)
        return True
#-*-coding:utf-8-*-
"""
@author zhj1121
@date 2020.6.24
@desc easyredis的hash数据类型
"""
class struct_hash(object):
    """
        easyredis的hash类型对象,使用python的hash实现
    """
    def __init__(self,name):
        self.name = name
        self.dict = {}
    def setDict(self,dict):
        self.dict = dict
    def getDict(self):
        return self.dict
    def hset(self,field,value):
        '''
            描述：在hash中存入键值
            返回值：
                1).如果当前field存在，则重写，但返回0
                2).如果当前field不存在，则写入，返回1
        '''
        boolvalue = 0
        if field not in self.dict:
            boolvalue +=1
        self.dict[field] = value
        return boolvalue
    def hget(self,field):
        '''
            描述：在hash中获取对应键的值
            返回值：
                1).如果当前field不存在时，返回 (nil)
                2).如果当前field存在时，则返回当前对应的值即可
        '''
        if field  not in self.dict:
            return '(nil)'
        else:
            return self.dict[field]
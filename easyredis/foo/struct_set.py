#-*-coding:utf-8-*-
"""
@author zhj1121
@date 2020.6.24
@desc easyredis的set数据类型
"""
class struct_set(object):
    def __init__(self,name):
        self.name = name
        self.set = []
    def setSet(self,dataSet):
        self.set = dataSet
    def sadd(self,member):
        '''
            描述：向集合中加入元素
            返回值：
                1).如果加入的元素已存在于对象中，则返回0
                2).如果加入的元素不存在于对象中，则将该元素加入对象中
                并返回1
        '''
        boolValue = 0
        if member not in self.set:
            boolValue += 1
            self.set.append(member)
        return boolValue
    def smembers(self):
        '''
            描述：遍历集合的所有元素
            返回值：
                1).如果当前对象不存在，则返回 (empty list or set)
                2).如果当前对象存在，则返回当前对象的所有元素
        '''
        if len(self.set) == 0:
            return "(empty list or set)"
        else:
            printStr = ""
            for i in range(len(self.set)-1):
                printStr += "{}) {}\n".format(i+1,self.set[i])
            printStr += "{}) {}".format(len(self.set),self.set[-1])
            return printStr
#-*-coding:utf-8-*-
"""
@author zhj1121
@date 2020.6.24
@desc easyredis的string数据类型
"""
class struct_string(object):
    '''
        使用Python3的字符串实现
    '''
    def __init__(self,name):
        self.name = name
        self.value = None
    def setValue(self,value):
        '''
            描述：设置值
            返回值：OK
        '''
        self.value = value
        return "OK"
    def getValue(self):
        '''
            描述：获取值
            返回值：
                1).如果当前字符串存在值，返回对应的值
                2).如果当前字符串不存在，返回 '(nil)'
        '''
        if self.value:
            return str(self.value)
        return "(nil)"
    def exist(self,key):
        '''
            在 db_key 中处理
        '''
    def incr(self):
        '''
            描述：数值 + 1
            返回值：(integer) {}
            注意：
                1)如果该对象的值不是数值，即字符串，则返回
                (error) ERR value is not an integer or out of range
        '''
        try:
            self.value = int(self.value)+1
            return "(integer) {} ".format(self.value)
        except:
            return "(error) ERR value is not an integer or out of range"
if __name__ == "__main__":
    obj_string = struct_string('zhj')
    obj_string.setValue('89')
    print(obj_string.getValue())
    print(obj_string.incr())
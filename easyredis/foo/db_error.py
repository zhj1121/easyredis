#-*-coding:utf-8-*-
"""
@author zhj1121
@date 2020.6.24
@desc explain the command,and return to the result
"""
class db_error(object):
    """ 定义了数据库中各种异常 """
    def __init__(self,name):
        self.name = name
    def wrongKind(self):
        """ 类型异常 """
        return '(error) WRONGTYPE Operation against a key holding the wrong kind of value'
    def emptyValue(self):
        """ 空值异常 """
        return '(empty list or set)'
    def unknowCommand(self,commandhead):
        """ 未知命令异常 """
        return "(error) ERR unknown command '{}'".format(commandhead)
    def argError(self,commandhead):
        """ 命令输入参数异常 """
        return "(error) ERR wrong number of arguments for '{}' command".format(commandhead)
    def otherError(self):
        """ 其它异常 """
        return 'Error...'
#-*-coding:utf-8-*-
"""
@author zhj1121
@date 2020.6.24
@desc 日志装饰器集合
"""
import os
import sys
import functools

# from db_File import db_File
# from db_conf import localTime,path_log,path_log_back
from foo.db_File import db_File
from conf.db_conf import localTime,path_log,path_log_back

def conn_log(func):
    """
        描述：收集每一个线程(即连接)的连接断开的日志
        主函数：db_use_user.tcplink(sock,address)
        参数对应：
            sock = arg1,address = arg2  #address:({host},{port}),author = arg3
    """
    @functools.wraps(func)
    def wrapper(arg1,arg2,arg3):#添加不定参数
        file = db_File(path_log)
        connect_start= '{TIME} * Accept new connection from {HOST}:{PORT}...'.format(
            TIME = localTime(),HOST=arg2[0],PORT=arg2[1])
        file.additional(connect_start)
        print(connect_start)
        func(arg1,arg2,arg3)#添加不定参数
        connect_end = '{TIME} * connection {HOST}:{PORT} is close...'.format(
            TIME = localTime(),HOST=arg2[0],PORT=arg2[1])
        print(connect_end)
        file.additional(connect_end)
        file.copy(path_log_back)
    return wrapper
def command_log(address,recvData,resultData):
    """
        描述：收集每一个线程(即连接)的命令请求与返回结果
        主函数：db_use_user.manageRecvData(recvdata)
        参数对应：
            recvdata = arg1
    """
    file = db_File(path_log)
    PR_Str = '{TIME} * {HOST}:{PORT} * command:\n'.format(
        TIME=localTime(),HOST=address[0],PORT=address[1])
    RS_Str = '{TIME} * {HOST}:{PORT} * command result:\n'.format(
    TIME=localTime(),HOST=address[0],PORT=address[1])
    file.additional(PR_Str+str(recvData))
    file.additional(RS_Str+str(resultData))
    file.copy(path_log_back)
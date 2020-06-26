#-*-coding:utf-8-*-
"""
@author zhj1121
@date 2020.6.24
@desc easyredis的配置参数
"""
import requests
import json
""" socket配置"""
import socket
def getPublicIP():
    """ 获取服务的公网IP """
    try:
        url = 'http://jsonip.com'
        r = requests.get(url, timeout=30)
        r.raise_for_status() #如果状态不是200，引发异常
        r.encoding = 'utf-8' #无论原来用什么编码，都改成utf-8
        return r.text#正常的获取的结果
    except:
        return None
"""
    监听哪些网络
    127.0.0.1是监听本机
    0.0.0.0是监听整个网络
"""
db_host_listen = "127.0.0.1"
"""
    服务端的IP
"""
#db_server_host = getPublicIP() if getPublicIP() else '127.0.0.1'
db_server_host = '127.0.0.1'
"""
    监听自己的哪个端口
"""
db_port = 2111
"""
    接收从客户端发来的数据的缓存区大小 
"""
db_buffSize = 1024

"""
    最大的连接数
"""
max_connect = 5

"""持久化配置"""
"""
    数据持久化文件
"""
db_data_file = 'data/data.json'
"""
    数据持久化备份文件
"""
db_data_back_file = 'data/back.json'

""" 命令行提示配置 """
"""
    命令类文件
"""
"""
    命令行提示历史文件
    注意：history_path 和command_path 的区别在于：
    每当客户端与服务端初次连接时，将把command的内容复制到history_command
"""
# command_path = 'command/command.txt'
# command_file = ''
history_path = 'lib/command.txt'
command_path = 'lib/'
command_file = 'lib/command.txt'

""" 时间 """
import time
def localTime():
    return time.strftime("%d %b %a %H:%M:%S %Y", time.localtime())

""" 启动输出设置 """

""" 安全权限设置 """
"""
    0:false 
    1:true 
"""
security_switch = 1
security = {'zhj':"zhj"}
security_Str = ''

def login_failed():
    """ 打印登录错误信息 """
    print('')
    print('Sorry,db authority failed,so unable to connect...')

def login_success(username):
    """ 打印登录成功信息 """
    print('welcom {}'.format(username))

""" 日志 """
path_log = 'log/db.log'
path_log_back = 'log/back_db.log'

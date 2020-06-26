"""
@author zhj1121
@date 2020.6.25
@desc easyredis客户端(独立)
"""
import getpass
import random
import shutil
import os
#socket
from socket import *
# clik
from clik import app,args,parser
# prompt_toolkit
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

db_server_host = '127.0.0.1'
db_port = 2111
db_buffSize = 1024
command_file = 'command.txt'
command_path = os.getcwd()+'/'

security_switch = 1
# gobal 
user = None
password = None

def login_failed():
    """ 打印登录错误信息 """
    print('')
    print('Sorry,db authority failed,so unable to connect...')

def login_success(username):
    """ 打印登录成功信息 """
    print('welcom {}'.format(username))

def authority(socket_client,username,password):
    # 这里的信号代表着服务端与客户端已经断开，
    # 以下逻辑仅为了客户端能够跳出 while True
    """ 
        注意：有两个说明
        1).参数security_switch
        必须是配置文件中的值
        当然，在独立的客户端中，这个参数默认是1
        另外，即使在这个开源且不独立的客户端中进行修改，
        也不会影响到服务端的安全逻辑正常进行
        2).函数的逻辑
        如果在客户端中，注释掉或者删掉这个函数，
        将无法与服务端进行正常通信，
        因为客户端与服务端连接成功后，且如果服务端启用安全验证，
        那么必须在客户端中进行安全验证后，才能够与服务端正常通信，
    """
    if security_switch:
        print('Since security authentication is enabled, you should log in first...')
        if not username and not password:
            username = input("Please input the username:")
            password = getpass.getpass("Please input the password:")
        senddata = 'author {} {}'.format(username,password)
        socket_client.send(senddata.encode())
        recvdata = socket_client.recv(db_buffSize).decode('utf-8')
        if recvdata == 'connectionclose':
            login_failed()
            return False
        login_success(username)
        return True
    else:
        print('Since security authentication is disenabled, so you use easyredis freely...')
        return True
def randomTouchFile(command_path,command_file):
    """ 随机生成一个不存在的文件，并返回路径 """
    file_list = os.listdir(command_path)
    str = 'abcdefghijklmnopqrstuvwxyz123456789'
    touchFileName = ""
    while touchFileName in file_list or touchFileName == "":
        touchFileName = ""
        for i in range(8):
            touchFileName += random.choice(str)
        touchFileName += ".txt"
    shutil.copyfile(command_file, command_path+touchFileName)
    return command_path+touchFileName
def delFile(file_path):
    """ 删除一个路径下的文件 """
    os.remove(file_path)
def socketClient(db_server_host,db_port,username,password):
    socket_client = socket(AF_INET, SOCK_STREAM)
    socket_client.connect((db_server_host,db_port))
    # 如果没有以下逻辑，客户端与服务端也不能进行通信
    # 所以以下逻辑与安全验证是否有效无关
    if not authority(socket_client, username, password):
        socket_client.close()
        return
    user_commandfile = randomTouchFile(command_path,command_file)
    while True:
        senddata = prompt(">",history=FileHistory(user_commandfile),auto_suggest=AutoSuggestFromHistory())
        if senddata == "":
            senddata = "Null"
            socket_client.send(senddata.encode())
        # senddata = input('send:')
        # 如果发送exit，则会先保存，在进行跳出
        elif senddata == 'exit':
            senddata = "save_exit"
            socket_client.send(senddata.encode())
            print("Goodbye and look forward to seeing you next time")
            break
        else:
            socket_client.send(senddata.encode())
        recvdata = socket_client.recv(db_buffSize).decode('utf-8')
        if recvdata == 'connectionclose':
            login_failed()
            break
        print(recvdata)
    socket_client.close()
    delFile(user_commandfile)
@app(name = 'easyredis_client')
def run():
    #snippets = description+epilog
    """
    The database's name is easyredis, a simple memory-based database based on redis.

    You can view it in detail by content optional arguments,
    and learn about it from the documentation.
    """
    #文件
    parser.add_argument(
        '-host',
        '--host',
        default=db_server_host,
        help='the server host (default: %(default)s)',
    )
    parser.add_argument(
        '-port',
        '--port',
        default=db_port,
        help='the server port (default: %(default)s)',
    )
    parser.add_argument(
        '-u',
        '--user',
        default=user,
        help='the server username (default: %(default)s)',
    )
    parser.add_argument(
        '-p',
        '--password',
        default=password,
        help='the client password (default: %(default)s)',
    )
    yield
    socketClient(args.host,int(args.port),args.user,args.password)
if __name__ == "__main__":
    run.main()
"""
@author zhj1121
@date 2020.6.25
@desc easyredis服务端
"""
import threading
import msvcrt
from socket import *
from clik import app,args,parser

# from db_conf import db_host_listen,db_port,db_buffSize,max_connect
# from db_conf import history_path
# from db_conf import path_log,path_log_back
# from db_decorate import prefixStr
# from db_log import conn_log,command_log
# from db_Key import db_Key
# from db_manager import db_manager

from conf.db_conf import db_host_listen,db_port,db_buffSize,max_connect
from conf.db_conf import path_log,path_log_back
from conf.db_conf import security,security_switch

from foo.db_decorate import prefixStr
from foo.db_log import conn_log,command_log
from foo.db_Key import db_Key
from foo.db_manager import db_manager

global db
db = db_Key()
db.load()

def manageRecvData(recvdata):
    """
        处理客户端发送的命令,并返回值
        接收数据，返回结果
    """
    #print(recvdata)
    if recvdata=='exit':
        return None
    elif recvdata=="Null":
        return recvdata
    elif recvdata=="save":
        db.save()
        db.load()
        resultData = "successfully to saved data "
        return resultData
    elif recvdata == "save_exit":
        db.save()
        db.load()
        return None
    else:
        db_manager_obj = db_manager(recvdata)
        # print(recvdata)
        result = db_manager_obj.command_operation(db.keyDict)
        # print(result)
        resultData = result
        return resultData

@conn_log
def tcplink(clientsock,address,author):
    """ 创建多个线程，满足多个客户端可以链接 """
    authorlabel = 0
    while True:  
        recvdata=clientsock.recv(db_buffSize).decode('utf-8')
        resultdata = manageRecvData(recvdata)#命令处理
        if resultdata == 'authorissuccess':
            authorlabel = 1
        if not authorlabel and author:
            clientsock.send('connectionclose'.encode())
            break
        command_log(address,recvdata,resultdata)#日志收集
        if not resultdata:
            break
        # print(resultdata)
        clientsock.send(resultdata.encode())
    clientsock.close()

def socketServer(db_host_listen,db_port,max_connect,author):
    """ 配置socket """
    socket_server = socket(AF_INET, SOCK_STREAM)
    socket_server.bind((db_host_listen,db_port))
    socket_server.listen(max_connect)
    try:
        while True:
            # if ord(msvcrt.getch())==27:
            #     break
            clientsock,clientaddress=socket_server.accept()
            print('connect from:{},pid:{}'.format(clientaddress[0],clientaddress[1]))
            t=threading.Thread(
                target=tcplink,args=(clientsock,clientaddress,author))  #t为新创建的线程
            t.start()
        print("server is shutdown...")
        socket_server.shutdown(2)
        socket_server.close()
        db.save()
    except:
        print("good bye")
@app(name = 'easyredis_server')
def run():
    #snippets = description+epilog
    """
    The database's name is easyredis, a simple memory-based database based on redis.

    You can view it in detail by content optional arguments,
    and learn about it from the documentation.
    """
    #文件
    parser.add_argument(
        '-log',
        '--logpath',
        default=path_log,
        help='log file (default: %(default)s)',
    )
    parser.add_argument(
        '-listen',
        '--listen',
        default=db_host_listen,
        help='listen host (default: %(default)s)',
    )
    parser.add_argument(
        '-port',
        '--port',
        default=db_port,
        help='listen port (default: %(default)s)',
    )
    parser.add_argument(
        '-m',
        '--max_connect',
        default=max_connect,
        help='the database max connect (default: %(default)s)',
    )
    parser.add_argument(
        '-a',
        '--author',
        default=security_switch,
        help='the database max connect (default: %(default)s)',
    )
    yield
    prefixStr(args.listen,args.port)#打印启动动画
#    print('log file path is:',args.logpath)
    socketServer(args.listen,int(args.port),args.max_connect,args.author)
if __name__ == "__main__":
    run.main()


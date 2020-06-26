#-*-coding:utf-8-*-
"""
@author zhj1121
@date 2020.6.24
@desc easyredis的修饰文件,例如easyredis服务启动动画
"""
import time
from conf.db_conf import localTime

def prefixStr(host,port):
    """ 修饰启动动画 """
    prefixStr = """Welcome to use easyredis
            _._
        _.-``__ ''-._
    _.-``    `.  `_.  ''-._           easyredis 1.0 (00000000/0) 64 bit
.-`` .-```.  ```\/    _.,_ ''-._
(    '      ,       .-`  | `,    )    Running in standalone mode
|`-._`-...-` __...-.``-._|'` _.-'|    LISTEN HOST: {HOST}
|    `-._   `._    /     _.-'    |    LISTEN PORT: {PORT}
|-._    `-._  `-./  _.-'    _.-' |
|`-._`-._    `-.__.-'    _.-'_.-'|
|    `-._`-._        _.-'_.-'    |    https://www.zhj1121.xyz/
`-._    `-._`-.__.-'_.-'    _.-'
|`-._`-._    `-.__.-'    _.-'_.-'|
|    `-._`-._        _.-'_.-'    |
`-._    `-._`-.__.-'_.-'    _.-'
    `-._    `-.__.-'    _.-'
        `-._        _.-'
            `-.__.-'
{TIME} * Server started, Easyredis 1.0
{TIME} * The server is now ready to accept connections on host {HOST} and port {PORT}
""".format(TIME = localTime(),HOST=host,PORT = port)
    print(prefixStr)
# easyredis

The database is name is easyredis, a simple memory-based database based on redis.

easyredis is a server side with the client side of the program,and easyredis_privateclient is a separate client.
## Directory

- [Language](#install)
- [Install](#install)
- [Use](#install)
- [Security](#install)
- [Config](#install)
- [Command](#install)

## Language
Python3.x

## Install
```python
pip install clik
pip install prompt_toolkit
```
## Use
```python
#server
py db_server.py -h
py db_server.py
#client##separate client
py db_client.py -h
py db_client.py
```
## Security
>You can configure at easyredis/conf/db.conf.py.

```python
security_switch = 1
security = {'zhj':"zhj"}
security_Str = ''
```
>Of course,you also configuer at at startup.

```python
py db_server.py -a 1
#or
py db_server.py -a 0
```

>client

```python
py db_client.py -u zhj -p zhj
```
## Config
>You can configure at easyredis/conf/db.conf.py and learn more.

## Command
>You can learn at easyredis/command/db.conf.py.

```txt
# This file contains all the statements that can be executed in the application
# And complete the client prompt function at the same time

# string
+set [key] [value]

+get [value]

...

```

#-*-coding:utf-8-*-
"""
@author zhj1121
@date 2020.6.24
@desc explain the command,and return to the result
"""

# from struct_string import struct_string
# from struct_list import struct_list
# from struct_hash import struct_hash
# from struct_set import struct_set
# from db_Key import db_Key
from foo.struct_string import struct_string
from foo.struct_list import struct_list
from foo.struct_hash import struct_hash
from foo.struct_set import struct_set
from foo.struct_zset import struct_zset
from foo.db_Key import db_Key
from foo.db_error import db_error

from conf.db_conf import security

class db_manager(object):
    def __init__(self,command):
        """Fetches args from a command , and save to the list

        Split the command line and get the args
        if the frist arg is not in the dict mapping ,
        we should return None
        That's all

        Args:
            recvdata: A command.
        Returns:
            A list or None
            if list:
            the first arg is important,
            beacuse the first arg is used to determine 
            whether it exists in the command_head
            and other is the key or filed
            if None:
            return None and no doing other anyting
        Raises:
            No Error happen
        """
        self.command = command
        self.argList = command.split(" ")
        self.argLen = len(self.argList)
        self.error = db_error('myerror')
        self.head = self.argList.pop(0)
        self.key = self.argList.pop(0) if len(self.argList) >= 1 else None
    def command_head(self):
        """we should implement the key command

        strings : set，get，exist，incr 
        list ：lpush, rpop, lrange
        set ：sadd，smembers
        hash ：hset，hget
        rdb ：save(save object to the disk)

        and save the  key to list

        args:
            the head in head_dict : return easyredis object
            other : return error.unknowCommand()
        """
        command_head_dict = {
            'set':'string','get':'string','exists':'string','incr':'string',
            'lpush':'list','rpop':'list','lrange':'list',
            'sadd':'set','smembers':'set',
            'hset':'hash','hget':'hash',
            'zadd':'zset','zrange':'zset',
            'keys':'key',
            'author':'author'
        }
        if self.head not in command_head_dict:
            return self.error.unknowCommand(self.head)
        return command_head_dict[self.head]
    def command_operation_str(self,keyDict):
        """ type of string """
        """ set,get,exists,incr """
        if self.head == 'set':
            try:
                key_type = 'string'
                obj_str = struct_string(self.key)
                obj_str.setValue(self.argList.pop(0))
                # if self.key is exists,
                # and type is't string,
                # it was repalce
                keyDict[self.key] = {'type':key_type,'value':obj_str}
                return 'OK'
            except:
                return Exception('Error...')
        elif self.head == 'get':
            try:
                if self.key in keyDict:
                    if keyDict[self.key]['type'] == 'string':
                        obj_str = keyDict[self.key]['value']
                        return obj_str.getValue()
                    else:
                        return self.error.wrongKind()
                else:
                    return '(nil)'
            except:
                return Exception('Error...')
        elif self.head == 'exists':
            try:
                boolValue = 0
                if self.key in keyDict:
                    boolValue += 1
                return '(integer) {}'.format(boolValue)
            except:
                return Exception('Error...')
        elif self.head == 'incr':
            try:
                if self.key in keyDict:
                    if keyDict[self.key]['type'] == 'string':
                        obj_str = keyDict[self.key]['value']
                        return obj_str.incr()
                    else:
                        return self.error.wrongKind()
                else:
                    obj_str = struct_string(self.key)
                    obj_str.setValue(1)
                    keyDict[self.key] = {'type':'string','value':obj_str}
            except:
                return Exception('Error...')
    def command_operation_list(self,keyDict):
        """ type of list """
        """ lpush,rpop,lrange """
        if self.head == 'lpush':
            if self.key in keyDict:
                if keyDict[self.key]['type'] == 'list':
                    for i in self.argList:
                        keyDict[self.key]['value'].lpush(i)
                    return "(integer) {}".format(keyDict[self.key]['value'].getLenght())
                else:
                    return self.error.wrongKind()
            else:
                obj_list = struct_list(self.key)
                for i in self.argList:
                    obj_list.lpush(i)
                keyDict[self.key] = {'type':'list','value':obj_list}
                return str(obj_list.getLenght())
        elif self.head == 'rpop':
            if self.key in keyDict and keyDict[self.key]['type']=='list':
                obj_list = keyDict[self.key]['value']
                return obj_list.rpop()
            if self.key in keyDict:
                if keyDict[self.key]['type']=='list':
                    obj_list = keyDict[self.key]['value']
                    return obj_list.rpop()
                else:
                    return self.error.wrongKind()
            else:
                return '(nil)'
        elif self.head == 'lrange':
            if self.key in keyDict:
                if keyDict[self.key]['type'] == 'list':
                    obj_list = keyDict[self.key]['value']
                    return obj_list.lrange(self.argList[0],self.argList[1])
                else:
                    return self.error.wrongKind()
            else:
                return self.error.emptyValue()
    def command_operation_hash(self,keyDict):
        """ type fo hash """
        """ hset,hget """
        if self.head == 'hset':
            if self.key in keyDict:
                if keyDict[self.key]['type'] == 'hash':
                    obj_hash = keyDict[self.key]['value']
                    count = 0
                    while len(self.argList) >= 2:
                        if obj_hash.hset(self.argList.pop(0),self.argList.pop(0)):
                            count +=1
                    return '(integer) {}'.format(count)
                else:
                    return self.error.wrongKind()
            else:
                obj_hash = struct_hash(self.key)
                count = 0
                while len(self.argList) >= 2:
                    if obj_hash.hset(self.argList.pop(0),self.argList.pop(0)):
                        count +=1
                keyDict[self.key] = {'type':'hash','value':obj_hash}
                return '(integer) {}'.format(count)
        elif self.head == 'hget':
            if self.key in keyDict:
                if keyDict[self.key]['type'] == 'hash':
                    obj_hash = keyDict[self.key]['value']
                    return obj_hash.hget(self.argList[0])
                else:
                    return self.error.wrongKind()
            else:
                return '(nil)'
    def command_operation_set(self,keyDict):
        """ type of set """
        """
            'sadd':'set','smembers':'set'
        """
        if self.head == 'sadd':
            if self.key in keyDict:
                if keyDict[self.key]['type'] == 'set':
                    obj_set = keyDict[self.key]['value']
                    count = 0#记录有效的插入操作
                    for i in self.argList:
                        if obj_set.sadd(i):
                            count += 1
                    keyDict[self.key] = {'type':'set','value':obj_set}
                    return '(integer) {}'.format(count)
                else:
                    return self.error.wrongKind()
            else:
                obj_set = struct_set(self.key)
                count = 0
                for i in self.argList:
                    if obj_set.sadd(i):
                        count +=1
                keyDict[self.key] = {'type':'set','value':obj_set}
                return '(integer) {}'.format(count)
        elif self.head == 'smembers':
            if self.key in keyDict:
                if keyDict[self.key]['type'] == 'set':
                    return keyDict[self.key]['value'].smembers()
                else:
                    return self.error.wrongKind()
            else:
                return self.error.emptyValue()
    def command_operation_zset(self,keyDict):
        """ type of sort set """
        """
            'zadd':'zset','zrange':'zset'
        """
        if self.head == 'zadd':
            if self.key in keyDict:
                if keyDict[self.key]['type'] == 'zset':
                    obj_zset = keyDict[self.key]['value']
                    count = 0
                    while len(self.argList) >= 2:
                        scorevalue = self.argList.pop(0)
                        keyvalue = self.argList.pop(0)
                        if keyDict[self.key]['value'].zadd(keyvalue,scorevalue):
                            count += 1
                    keyDict[self.key]['value'] = obj_zset
                    return '(integer) {}'.format(count)
                else:
                    return self.error.wrongKind()
            else:
                obj_zset = struct_zset(self.key)
                count = 0
                while len(self.argList) >= 2:
                    scorevalue = self.argList.pop(0)
                    keyvalue = self.argList.pop(0)
                    if obj_zset.zadd(keyvalue,scorevalue):
                        count += 1
                keyDict[self.key] = {'type':'zset','value':obj_zset}
                return '(integer) {}'.format(count)
        elif self.head == 'zrange':
            if self.key in keyDict:
                if keyDict[self.key]['type'] == 'zset':
                    obj_zset = keyDict[self.key]['value']
                    if self.argList[-1] == 'withscore':
                        return obj_zset.zrangewithScore(self.argList[0],self.argList[1])
                    else:
                        return obj_zset.zrange(self.argList[0],self.argList[1])
                else:
                    return self.error.wrongKind()
            else:
                return self.error.emptyValue()
    def command_operation_key(self,keyDict):
        """ key of easyredis """
        """ keys * """
        if self.head == 'keys' and self.key == '*':
            printStr = ''
            count = 0
            for i in keyDict:
                count+=1
                if count == len(keyDict):
                    printStr += '{}) {}'.format(count,i)
                else:
                    printStr += '{}) {}\n'.format(count,i)
            return printStr
    def command_operation_author(self):
        """ author of easyredis """
        ''' author username password'''
        if self.head == 'author':
            if self.key in security and self.argList[-1]==security[self.key]:
                return 'authorissuccess'
            return 'authorisfailed'
    def command_operation(self,keyDict):
        """ string,hash,list,set,zset,key """
        if self.key:
            if self.command_head() == 'string':
                return self.command_operation_str(keyDict)
            elif self.command_head() == 'hash':
                return self.command_operation_hash(keyDict)
            elif self.command_head() == 'list':
                return self.command_operation_list(keyDict)
            elif self.command_head() == 'set':
                return self.command_operation_set(keyDict)
            elif self.command_head() == 'zset':
                return self.command_operation_zset(keyDict)
            elif self.command_head() == 'key':
                return self.command_operation_key(keyDict)
            elif self.command_head() == 'author':
                return self.command_operation_author()
            else:
                return self.error.unknowCommand(self.head)
        return self.error.argError(self.head)
if __name__ == "__main__":
    db = db_Key()
    db.load()
    print(db.keyDict)
    #Test
    """ 
            'set':'string','get':'string','incr':'string',
            'lpush':'list','rpop':'list','lrange':'list',
            'sadd':'set','smembers':'set',
            'hset':'hash','hget':'hash',
            'exist':'key'
    """
    # string
    # sendStr = 'set name tom'
    # sendStr = 'get name'
    # sendStr = 'incr score'
    #list
    # sendStr = 'lpush list1 1 2 3'
    # sendStr = 'rpop list1'
    # sendStr = 'lrange list1 0 -1'
    #set
    # sendStr = 'sadd myset 1 2 3'
    # sendStr = 'smembers myset'
    #hash
    # sendStr = 'hset myhash name tom'
    # sendStr = 'hget myhash name'
    #key
    # sendStr = 'exists myhash1'
    # sendStr = 'keys *'
    # db_manager = db_manager(sendStr)
    # result = db_manager.command_operation(db.keyDict)
    # print(result)
    # print(db.keyDict)
    # db.save()
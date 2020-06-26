#-*-coding:utf-8-*-
"""
@author zhj1121
@date 2020.6.24
@desc 一个处理easyredis键的重要类
"""
import json

from foo.db_File import db_File
from foo.struct_string import struct_string
from foo.struct_hash import struct_hash
from foo.struct_list import struct_list
from foo.struct_set import struct_set
from foo.struct_zset import struct_zset

class db_Key(object):
    """ 管理easyredis的所有键 """
    def __init__(self):
        self.keyDict = {}
    def add(self,key,type,value):
        """ 
            描述：使用python字典进行存储
            细节描述：
                每一次easyredis创建新键时，
                同时将这个新键加入到Python3的字典中，即内存中
                如果键发生变化时，因为绑定了对应的对象，所以不需要进行更改
            返回值：None
            注意：
                1).如果一个键存在，将再次覆盖设值
                2).与方法self.load(self)的格式一致
            因为方法self.add(self)的目标对象即是self.keyDict = {}
        """
        self.keyDict[key] = {'type':type,'value':value}
    def exists(self,key):
        """
            描述：判断easyredis中是否存在对象key
            返回值：存在则返回(integer) 1 不存在则返回 (integer) 0
        """
        boolValue = 0
        if key in self.keyDict:
            boolValue += 1
        return '(integer) {}'.format(boolValue)
    def hasKey(self,key):
        '''
            描述：判断easyredis中是否存在对象key
            使用场景：用于给已存在的对象重新设值
            返回值：
                存在则返回该对象
                不存在则返回None
            format:
                    {
                        'type':xxx,
                        'value':Object(easyredis中的所有对象)
                    }
        '''
        if key in self.keyDict:
            return self.keyDict[key]
        else:
            return None
    def save(self):
        """  
            描述：将keyDict的对象以json格式存储到文件data.json中
            如果想要更换数据文件，可以去db_conf进行重新设置
            返回值：boole
            注意：
                format：
                    {
                        key:{'type':type,'value':value}
                    }
                self.save(self)format的value类型为josn的str，
            这区别于方法self.load(self)
        """
        data_File = db_File()
        keyDict_Json = {}
        for i in self.keyDict:
            # print(i)
            # print(self.keyDict[i])
            # print(self.keyDict[i]['value'].scoreList)
            obj_dict = self.keyDict[i]['value'].__dict__
            obj_json = json.dumps(obj_dict)
            # print(obj_json)
            self.keyDict[i]['value'] = obj_json
            keyDict_Json[i]={'type':self.keyDict[i]['type'],'value':obj_json}
        #将所有数据写入easyredis的数据文件中
        data_File.write(keyDict_Json)
        return True
    def load(self):
        """
            描述：将数据文件的数据全部加入内存中
            返回值：boole
            注意：
                format:
                    {
                        key:{
                            'type':xxx,
                            'value':Object(easyredis中的所有对象)
                        }
                    }
        """
        data_File = db_File()
        keyDict = data_File.read()
        for key in keyDict:
            #json 转 object
            obj_json = keyDict[key]['value']
            obj_dict = json.loads(obj_json)
            #获取每个键值对的内容
            obj_type = keyDict[key]['type']
            obj_key = key
            if obj_type == 'string':
                new_obj = struct_string(obj_key)
                new_obj.setValue(obj_dict['value'])
            elif obj_type == 'hash':
                new_obj = struct_hash(obj_key)
                new_obj.setDict(obj_dict['dict'])
            elif obj_type == 'set':
                new_obj = struct_set(obj_key)
                new_obj.setSet(obj_dict['set'])
            elif obj_type == 'list':
                new_obj = struct_list(obj_key)
                new_obj.setList(obj_dict['list'])
            elif obj_type == 'zset':
                new_obj = struct_zset(obj_key)
                new_obj.setList(obj_dict['keyList'],obj_dict['scoreList'])
            self.keyDict[obj_key] = {'type':obj_type,'value':new_obj}
        return True
if __name__ == "__main__":
    key = db_Key()
    key.load()
    print(key.keyDict)
    #######################
    # string test
    #######
    # save
    # obj_string = struct_string('zhj')
    # obj_string.setValue('90')
    # key.add(obj_string.name,'string',obj_string)
    # key.save()
    #######
    # load
    # key.load()
    # print(key.keyDict['zhj'].getValue())
    #######################
    # hash test
    #######
    # save
    # obj_hash = struct_hash('game')
    # obj_hash.hset('dnf','good game')
    # obj_hash.hset('lol','low game')
    # key.add(obj_hash.name,'hash',obj_hash)
    # key.save()
    #######
    # load
    # key.load()
    # print(key.keyDict['game']['value'].hget('dnf'))
    #######################
    # set test
    #######
    # save
    # obj_set = struct_set('mySet')
    # obj_set.sadd('lol')
    # obj_set.sadd('dnf')
    # obj_set.sadd('dnf')
    # key.add(obj_set.name,'set',obj_set)
    # key.save()
    #######
    # load
    # key.load()
    # print(key.keyDict)
    # print(key.keyDict['mySet']['value'].smembers())
    #######################
    # list test
    #######
    # save
    # obj_list = struct_list('myList')
    # obj_list.lpush('zhj')
    # obj_list.lpush('Tome')
    # key.add(obj_list.name,'list',obj_list)
    # key.save()
    #######
    # load
    # key.load()
    # print(key.keyDict['myList']['value'].getList())
    #######################
    # zset test
    #######
    # save
    # obj_zset = struct_zset('myzset')
    # obj_zset.zadd('key',1)
    # obj_zset.zrange(0,-1)
    # obj_zset.zrangewithScore(0,-1)
    # key.save()
    #######
    # load
    # key.load()
    # print(key.keyDict)


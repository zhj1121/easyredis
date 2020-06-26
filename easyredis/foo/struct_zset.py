#-*-coding:utf-8-*-
"""
@author zhj1121
@date 2020.6.24
@desc easyredis的sorted set数据类型
"""
import json
class struct_zset(object):
    """
        使用python的list实现有序集合
        使用两个list分别存储score和filed
    """
    def __init__(self,name):
        self.name = name
        self.keyList = []
        self.scoreList = []
    def setList(self,keylist,scorelist):
        self.keyList = keylist
        self.scoreList = scorelist
    def existsKey(self,key):
        if key in self.keyList:
            return True
        return False
    def getlen(self):
        return len(self.keyList)
    def zadd(self,key,score):
        """
            使用直接插入排序实现集合的有序
            注意：zadd方法只能实现一次的加入，多次加入在db_manager中进行处理
            依据：
                当元素分布有序，直接插入排序将大大减少比较次数和移动记录的次数
            最终结果：
                self.keyList中无重复元素
                self.scoreList中根据分数从小到大排序
                同分数的key根据字典升序排序
        """
        #加入元素
        ##保证score的类型为 int 或者 float
        score = eval(score)
        if type(score) != type(1) :
            if type(score) != type(1.0) :
                return "(error) ERR value is not a valid float"
        ##保证元素的分数有序
        existsStatus = 1#做个标记，保存是否存在该元素的判断状态
        if self.existsKey(key):
            existsStatus = 0#如果存在的话，则existsStatus = 0
            index = self.keyList.index(key)
            self.scoreList.pop(index)
            self.keyList.pop(index)
        self.keyList.append(key)
        self.scoreList.append(score)
        if self.getlen()!=1:
            current = self.getlen()-2
            while current >=0 and self.scoreList[current] > score:
                self.scoreList[current+1] = self.scoreList[current]
                self.keyList[current+1] = self.keyList[current]
                current -= 1
            self.keyList[current+1] = key
            self.scoreList[current+1] = score
        #保证同分数的元素按照key字典顺序排序
        current = 0
        while self.getlen()-1 >= current:
            sameEle_count = self.scoreList.count(self.scoreList[current])
            if sameEle_count > 1:
                dict_keyList = self.keyList[current:current+sameEle_count]
                sort_dict_keyList = dict_keyList.copy()
                sort_dict_keyList.sort()
                for i in range(sameEle_count):
                    self.keyList[current+i] = sort_dict_keyList[i]
            current += sameEle_count
        return existsStatus
    def zrange(self,start,end):
        """
            描述：遍历zset中的元素，可以参考struct_list.lrange()
            注意：换行符的使用
        """
        if int(end) == -1:
            printResult = self.keyList[int(start):]
        else:
            printResult = self.keyList[int(start):int(end)+1]
        printStr = ""
        for i in range(len(printResult)-1):
            printStr += "{}) {}\n".format(i+1,printResult[i])
        printStr += "{}) {}".format(len(printResult),printResult[-1])
        return printStr
    def zrangewithScore(self,start,end):
        """
            区别：与self.zrange()的区别在于
            返回结果是否包含分数
        """
        if int(end) == -1:
            keyResult = self.keyList[int(start):]
            scoreResult = self.scoreList[int(start):]
        else:
            keyResult = self.keyList[int(start):int(end)+1]
            scoreResult = self.scoreList[int(start):int(end)+1]
        printStr = ""
        count = 1
        for i in range(len(keyResult)):
            printStr += "{}) {}\n".format(count,keyResult[i])
            count +=1
            if i == len(keyResult)-1:
                printStr += "{}) {}".format(count,scoreResult[i])
            else:
                printStr += "{}) {}\n".format(count,scoreResult[i])
            count +=1
        return printStr
# if __name__ == "__main__":
#     zset = struct_zset()
#     zset.zadd('a',1)
#     zset.zadd('c',2)
#     zset.zadd('b',3)
#     zset.zadd('d',3)
#     print(zset.zrange(0,-1))
    # print(zset.zrangewithScore(0,-1))
    # print('1111')
    # #save
    # dict_zset = zset.__dict__
    # print(json.dumps(dict_zset))
    # json_zset = json.dumps(dict_zset)
    # # #load
    # print(json.loads(json_zset))


#-*-coding:utf-8-*-
"""
@author zhj1121
@date 2020.6.24
@desc easyredis的list数据类型
"""
class struct_list(object):
    '''
        使用Python3的list实现
    '''
    def __init__(self,name):
        self.name = name
        self.list = []
    def setList(self,list):
        self.list = list
    def getList(self):
        return self.list
    def getLenght(self):
        return len(self.list)
    def lpush(self,data):
        '''
            描述：在列表的左边加入元素
            返回值：返回当前list的长度
        '''
        newList = []
        newList.append(data)
        for i in self.list:
            newList.append(i)
        self.list = newList
        return True
    def rpush(self,data):
        '''
            描述：在列表的右边加入元素，即在链表尾插入元素
            返回值：返回当前list的长度
        '''
        self.list.append(data)
    def rpop(self):
        '''
            描述：删除列表的最后一个元素，即删除链表尾元素
            时间复杂度：O(1)
            返回值：
                当key不存在时，返回null
                当key存在时，返回被删除的元素
        '''
        if len(self.list) == 0:
            return "null"
        return self.list.pop()
    def lrange(self,start:int,end:int):
        '''
            描述：根据起始下标和终止下标返回元素
            返回值：起始下标和终止下标之间的元素
            注意：1).如果起始下标为负数，即代表从链表尾计数开始计算
                例如： -1 代表链表的最后一个元素
                2).终止下标可以超出链表的长度，当终止下标大于链表的长度时，
                默认终止下标为最后一个元素，即-1
                3).返回的元素包含终止下标位置的元素，例如： lange xxx 0 3 
                表示返回4个元素  位置0 1 2 3上的元素
                4).如果起始下标大于链表的长度时，返回 "(empty list or set)"
                5).如果对象不存在时，则返回 "(empty list or set)" 
        '''
        if int(end) == -1:
            printResult = self.list[int(start):]
        else:
            printResult = self.list[int(start):int(end)+1]
        printStr = ""
        for i in range(len(printResult)):
            if i == len(printResult)-1:
                printStr += "{}) {}".format(i+1,printResult[i])
            else:
                printStr += "{}) {}\n".format(i+1,printResult[i])
        return printStr
if __name__ == "__main__":
    ls = struct_list('mylist')
    ls.lpush(1)
    ls.lpush(2)
    ls.lpush(3)
    ls.lpush(4)
    print(ls.lrange(0,-5))
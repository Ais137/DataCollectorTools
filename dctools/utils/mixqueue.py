# Name: 元素混合队列
# Date: 2022-09-13
# Author: Ais
# Desc: 对队列中的元素进行混合

# 场景描述
""" 
在进行多域名网站数据采集时，遇到这样一个场景。对于每一个网站各有一个迭代器，持续的产出该网站的URL请求。
这些URL请求具有相同的域名。当这些请求推送到下载器中进行下载时，可能会导致“同一域名”下的请求并发数
过大，这可能会触发目标网站的风控。因此需要通过一种算法来“混合”不同域名下的URL请求。以在保持请求数
低于目标网站的风控线下提高请求并发上限。
"""
# 模型抽象
"""  
假设有 a, b, c, ... 类元素，现在有一个生成器集群。该集群持续的生成同一类元素，且这些元素构成一个
连续片段，如 a a a a, b b b, c c, ....，于是对于队列的输入有这样的场景
in -> a a b b b a a a c c a c c c ...
现在需要构建一个队列对这个序列中的元素进行“混合”，输出以下序列
out -> a b c a b c a b c ...
"""


# 元素混合队列
class MixQueue(object):
    """  
    算法实现:
    构建一个“环形队列”来进行分类存储。其中队列的每个子项表示一个类别并用于存储元素。
    通过一个索引指针来进行出队操作，每次元素出队时，索引指针在这个环形队列上进行轮转。
    """

    def __init__(self, classifier):
        # 分类器(lambda data: key): 对元素进行分类
        self.classifier = classifier
        # 环形队列(用于分类索引)
        self.__data = {}
        # 索引
        self.__index = []
        # 出队索引指针
        self.__index_pointer = -1
        # 队列长度计数变量
        self.__n = 0

    def __len__(self):
        return self.__n

    # 入队
    def __push(self, data):
        # 分类
        _class = self.classifier(data)
        if _class in self.__data:
            self.__data[_class].append(data)
        else:
            self.__index.append(_class)
            self.__data[_class] = [data]
        self.__n += 1

    def push(self, datas):
        [self.__push(data) for data in datas] if isinstance(datas, (list, tuple)) else self.__push(datas)

    # 出队
    def __pop(self):
        # 移动索引指针
        self.__index_pointer = (self.__index_pointer + 1) % len(self.__index)
        _class = self.__index[self.__index_pointer]
        dq = self.__data[_class]
        # 弹出元素
        if len(self.__data[_class]) == 1:
            self.__index.pop(self.__index_pointer)
            self.__data.pop(_class)
            self.__index_pointer -= 1
        self.__n -= 1
        return dq.pop(0)

    def pop(self, k=1):
        return [self.__pop() for i in range(min(k, self.__n))]
         

# Test
if __name__ ==  "__main__":

    # 构建队列
    mq = MixQueue(lambda data: data.split("/", 1)[0].upper())
    # 元素入队
    mq.push(["a.com/1", "a.com/2", "a.com/a3", "a.com/4"])
    mq.push(["b.com/1", "b.com/2", "b.com/3"])
    mq.push(["c.com/1", "c.com/2"])
    mq.push(["b.com/4", "c.com/3"])
    # 元素出队
    [print(i, mq.pop()) for i in range(len(mq))]



# Name: 分片队列
# Date: 2022-09-13
# Author: Ais
# Desc: None

# 场景描述
"""  
在数据采集流程中，原始数据解析后需要推送到数据库做持久化存储。对于scrapy框架，这个
IO读写过程发生在 pipline(数据管道) 中，每当框架产生item后，就需要向数据库推送。
为了减少这个频繁读写数据库的过程，需要构建一种“缓存读写”机制来进行优化。
"""
# 模型抽象
"""  
设 in 为入队操作，q 为队列元素状态， out 为出队操作。
设“分片大小” n=3
则有以下队列状态
[1]: in(1) | q(1) | out([])
[2]: in(2) | q(1, 2) | out([])
[3]: in(3) | q(1, 2, 3) | out(1, 2, 3) 
[4]: in(4) | q(4) | out([])
[5]: in(5) | q(4, 5) | out([])
[6]: in(6) | q(4, 5, 6) | out(4, 5, 6) 
...
"""
# 注意事项
"""  
在实际的项目中，对于分片大小的选取要根据场景而定，分片过大会导致内存占用过多，
同时如果服务器宕机会导致缓存的分片队列中的数据丢失(未推送到数据库)。
"""


# 分片队列
class SliceQueue(object):
    """  
    队列实现
    队列内部的 slice_size 属性用于控制分片大小。当队列数据长度小于该分片大小时，
    pop()操作弹出空数据([]), 当队列数据大于该值时，pop()弹出一个分片长度的数据序列(list)
    """

    def __init__(self, slice_size):
        if slice_size <= 0:
            raise ValueError("slice_size must be greater than 0")
        # 分片大小
        self.__slice_size = int(slice_size)
        # 数据容器
        self.__data = []

    def __len__(self):
        return len(self.__data)

    # 入队
    def push(self, datas):
        [self.__data.append(data) for data in datas] if isinstance(datas, (list, tuple)) else self.__data.append(datas)

    # 出队
    def pop(self, all=False):
        if not all and len(self) < self.__slice_size:
            return []
        else:
            return [self.__data.pop(0) for i in range(len(self) if all else self.__slice_size)]
        

# Test
if __name__ ==  "__main__":
    
    # 构建分片队列
    sq = SliceQueue(3)
    [sq.push(i) or print(f"[{i}]: in({i}) | out({sq.pop()})") for i in range(1, 11)]
    print(f"[11]: out_all({sq.pop(True)})")

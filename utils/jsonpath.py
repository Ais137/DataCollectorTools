# Name: JsonPathExtractor
# Date: 2022-09-13
# Author: Ais
# Desc: 通过类xpath的"路径表达式"来提取json格式的数据
# Version: 2.0

import re


# Json数据提取器
class JsonPathExtractor(object):
    """  
    # 概述:
        通过类xpath的"jpath路径表达式"来提取json格式的数据
    # jpath路径表达式
        1. jpath路径表达式以 "NODEPATH_SEP(节点路径分隔符)+STARTPATH(起始路径名)" 起始
            exp -> jpath("/data/...")
        2. jpath在描述json数据中的数组时，通过 "索引" 作为路径的键
            exp -> data = {
                "a": "aaa",
                "b": [
                    "b111",
                    "b222"
                ]
            }
            提取 b222 -> jpath(/data/b/1)
        3. 在使用 "find" 实例方法进行查找时，jpath 支持以"正则表达式"的形式进行查找
            jpath(/data/A|/data/C/d/\d+/\w+)
    """

    # 节点路径分隔符
    NODEPATH_SEP = "/"
    # 起始路径名
    STARTPATH = "data"
    

    # ------------------------------------------------------------ #
    # 数据节点容器
    class Node(object):
        
        def __init__(self, key, val="", p_node=None):
            # 节点名(键名)
            self.key = key
            # 节点值
            self.val = val
            # 父节点
            self.p_node = p_node
            # 绑定父节点
            p_node and self.p_node.nodes.append(self)
            # 子节点
            self.nodes = []
            # 节点路径
            self.path = JsonPathExtractor.NODEPATH_SEP.join([self.p_node.path if self.p_node else "", key])


    # ------------------------------------------------------------ #
    # (静态方法)提取值
    @staticmethod
    def extract(data, jpath, default=None):
        """
        @func: 根据路径表达式提取数据
        @params: 
            * data(json): 待提取的json数据
            * jpath: 路径表达式 
        @return(any): val
        @warning: 该jpath以"/"起始，而非JsonPathExtractor.STARTPATH("data")开头
        @exp:
            JsonPathExtractor.extract(data, "/k1/k2/1/k4")
        """
        # 拆分路径
        jpath = jpath.split(JsonPathExtractor.NODEPATH_SEP)[1:]
        # 根据jpath遍历data
        __data = data
        while jpath:
            try:
                key = int(jpath.pop(0)) if isinstance(__data, (list, tuple)) else jpath.pop(0)
                __data = __data[key]
            except: 
                return default
        return __data      

    # jpath路径映射
    @staticmethod
    def jpathmap(data, jmap):
        """
        @func: 根据 map(key->jpath) 映射表批量提取数据
        @params: 
            * data(json): 待提取的json数据
            * jmap(dict|map): key->jpath 映射表  
        @return(dict): 提取的数据
        @exp: 
            JsonPathExtractor.jpathmap(data, {
                "datakey": "op:jpath"
                "key1": "get:jpath",
                "key2": "find:jpath",
                ...
            })
        """
        # 构建jpath提取器
        extractor = JsonPathExtractor(data)
        __data = {}
        # 提取数据
        for key, op_exp in jmap.items():
            op, jpath = op_exp.split(":", 1)
            if op == "get":
                __data[key] = extractor.get(jpath)
            elif op == "find":
                __data[key] = extractor.find(jpath)
            else:
                raise ValueError(f"unknown op({op}) in jmap[{key}]")
        return __data


    # ------------------------------------------------------------ #
    # 构造器
    def __init__(self, data, BUILD_NODE=True):
        """
        @class: json数据提取器
        @desc: 通过路径表达式(jpath)提取数据
        @property: 
            * data(json): 原始json数据
            * root(Node): 根节点
            * index(dict): 索引(jpath->val)
            * BUILD_NODE(bool): 是否构建节点
                * True -> 将原始数据构建成树状结构
                * False -> 仅构建索引
        @method: 
            * get: 通过路径表达式获取值
            * find: 通过路径表达式查找值
            * DFS: 深度优先遍历器
            * BFS: 广度优先遍历器
        """
        # 原始json数据
        self.data = data
        # 根节点
        self.root = None
        # 索引(jpath->val)
        self.index = {}
        # 是否构建节点
        self.BUILD_NODE = BUILD_NODE
        # 构建
        self.__build(JsonPathExtractor.STARTPATH, self.data, "", self.root)

    # 构建树
    def __build(self, key, val, path, p_node):
        """
        @func: 通过遍历json数据结构构建树和索引
        """
        # 构建索引
        node_path = self.NODEPATH_SEP.join([path, key])
        self.index[node_path] = val
        # 构建节点
        node = JsonPathExtractor.Node(key, val, p_node) if self.BUILD_NODE else None
        # 连接根节点
        if self.root is None:
            self.root = node
        # 迭代
        if isinstance(val, dict):
            [self.__build(k, v, node_path, node) for k, v in val.items()]
        elif isinstance(val, (list, tuple)):
            [self.__build(str(i), val[i], node_path, node) for i in range(len(val))]
        else:
            pass

    # 取值
    def get(self, jpath, default=None):
        """
        @func: 通过路径表达式获取值
        @params: 
            * jpath: 路径表达式 
        @return(any): val
        """
        return self.index.get(jpath, default)

    # 查找
    def find(self, jpath):
        """
        @func: 通过路径表达式查找值
        @params: 
            * jpath: 路径表达式(支持正则表达式匹配)
        @return(list): [val ...]
        @exp:
            jpath.find("/data/A|/data/C/d/\d+/\w+")
        """
        return [val for path, val in self.index.items() if re.match(jpath, path)]

    # DFS(深度优先)遍历器
    def DFS(self, func, node=None):
        node = node or self.root
        node and ([self.DFS(func, n) for n in node.nodes] if node.nodes else func(node))

    # BFS(广度优先)遍历器
    def BFS(self, func):
        iter_queue = [self.root] if self.root else []
        while iter_queue:
            next_iter_queue = []
            [next_iter_queue.extend(node.nodes) if node.nodes else func(node) for node in iter_queue]
            iter_queue = next_iter_queue


# Test
if __name__ == "__main__":

    data = {
        "A": 111,
        "B": 222,
        "C": {
            "a": "aaa",
            "b": "bbb",
            "c": "ccc",
            "d": [
                "111",
                {
                    "a": "111_aaa",
                    "b": "222_bbb",
                },
                "222",
                "333",
                {
                    "c": "333_ccc",
                    "d": "444_ddd",
                    "e": "555_eee",
                }
            ]
        },
        "D": "444"
    }

    # 构建jpath提取器
    extractor = JsonPathExtractor(data)

    # [extract]: 通过路径表达式获取值
    print("-----------" * 5)
    print("[extract]: 通过路径表达式获取值")
    print("jpath(/C/d/4) -> ", JsonPathExtractor.extract(data, "/C/d/4"))

    # [jpathmap]: jpath路径映射
    print("-----------" * 5)
    print("[jpathmap]: jpath路径映射")
    jmap = {
        "data1": "get:/data/C/a",
        "data2": "get:/data/C/d/1",
        "data3": "find:/data/C/d/\d+/\w+",
        "data4": "get:/data/11111",
        "data5": "find:/data/3333"
    }
    print(f"{jmap} -> \n{JsonPathExtractor.jpathmap(data, jmap)}")

    # [get]: 通过路径表达式获取值
    print("-----------" * 5)
    print("[get]: 通过路径表达式获取值")
    print("jpath(/data/C/d/4/d) -> ", extractor.get("/data/C/d/4/d"))

    # [find]: 通过路径表达式查找值
    print("-----------" * 5)
    print("[find]: 通过路径表达式查找值")
    print("jpath(/data/A|/data/C/d/\d+/\w+): ", extractor.find("/data/A|/data/C/d/\d+/\w+"))

    # DFS(深度优先)遍历器
    print("-----------" * 5)
    print("[DFS]: ")
    extractor.DFS(lambda node: print(f'[{node.path}] -> ({node.val})'))

    # BFS(广度优先)遍历器
    print("-----------" * 5)
    print("[BFS]: ")
    extractor.BFS(lambda node: print(f'[{node.path}] -> ({node.val})'))
    
    
    

# Name: data process pipeline
# Date: 2023-03-03
# Author: Ais
# Desc: 一种组件化的数据处理模块
"""
# 一种组件化的数据处理模块

-------------------------------------------------------
## Question · 场景描述
在数据采集项目中，从采集模块的源数据到具体业务模块需要的数据之间，通常需要通过一个数据处理流程
对源数据进行格式转换等一系列操作。这个数据处理流程对于不同的业务需求有不同的实现，当业务变更时，
需要根据新的业务需求修改处理模块，因此，考虑设计一种组件化的数据处理模块来提高扩展性和代码复用率，
同时规范化数据处理流程。

-------------------------------------------------------
## FrameWork · 架构设计
模块的主要设计思想来源于 scrapy 框架中 pipeline 数据处理管道的架构和一种类似责任链的设计模式。

模块主要包含两个核心类：***DataProcessNode(数据处理节点)*** 和 ***DataProcessPipeline(数据处理管道)***

***DataProcessNode(数据处理节点)*** 
用于将完整的数据流程拆解到单个组件，每个组件封装不同的处理逻辑，比如对字段类型进行转换，缺失值检测，数据过滤等。对于不同的业务
可能包含一段相同的处理逻辑片段，因此可以通过这种组件化的架构来提高代码的复用率。同时在具体的实现时，每个节点应该具有单一的处理逻辑。

***DataProcessPipeline(数据处理管道)*** 
则用于将 *DataProcessNode(数据处理节点)* 封装成一个完整的数据处理流程，通过组装不同的数据处理节点来覆盖不同的数据处理需求。
同时当需求变更时，通过增删组件来实现可扩展性。在进行数据处理时，会让数据流过每个数据处理节点，以实现完整的数据处理流程，
同时当某个节点处理异常时，会记录异常的节点和异常信息，用于后续分析。

-------------------------------------------------------
## Features · 特性设计
1. 组件化构建: 通过组件化的方式完成数据处理流程的构建。
2. 处理状态监控: 对数据的处理状态进行监控，记录异常的处理节点和异常信息。
3. 兼容性检测: 通过对函数类型注解的自省，来校验两个数据处理节点之间输入输出数据类型的兼容性
4. 数据测试: 对单条数据进行测试，测试完整数据处理流程，并记录每个节点处理的数据副本，用于后续分析。
5. 文档生成: 自动集成数据处理节点的文档并构建一个总体描述文档

"""


import json
import inspect
import traceback
from copy import deepcopy


# 数据处理节点
class DataProcessNode(object):
    """
    @class: DataProcessNode | 数据处理节点
    @desc: 
        数据处理节点基类，数据处理组件需要继承并重写 process 方法，
        用于将完整的数据流程拆解到单个组件，每个组件封装不同的单一处理逻辑。
    @property: 
        * pid(str): 数据节点ID
    @method: 
        * build(staticmethod): 基于函数快速构建 DataProcessNode 类
        * init: 数据处理节点初始化
        * process: 核心处理逻辑
        * exit: 数据处理节点销毁
    @standard:
        process 方法的开发规范如下:
        1. 方法参数必须包含类型注解，以便后续框架中进行节点之间的数据兼容性校验。
        2. 文档字符串规范如下:
            @func: 数据处理逻辑简述(必要)
            @desc: 数据处理逻辑的详细描述(可选)
            @input: 数据输入数据样例(必要)
            @output: 数据输出数据样例(必要)
    """

    # 快速封装装饰器
    @staticmethod
    def build(process_func):
        """
        @func: 
            基于函数 process_func 快速封装和动态构建 DataProcessNode 子类
        @params: 
            * process_func: 数据处理逻辑
        @return(DataProcessNode): DataProcessNode
        @exp:
            @DataProcessNode.build
            def DataFieldConverter(self, data: dict) -> dict:
                \"\"\"
                @func: 对源数据的数据字段类型进行转换
                @desc: 将 count 字段转换成 int 类型
                @input: {"count": "137", ...}
                @output: {"count": 137, ...}
                \"\"\"
                data["count"] = int(data["count"])
                return data
        """
        return type(
            # 函数名作为类名
            process_func.__name__, 
            # 继承基类
            (DataProcessNode, ), 
            # 构建属性
            dict(process = process_func, )
        )

    def __init__(self, pid=None):
        # 处理节点ID: 类名作为默认值
        self._pid = pid or self.__class__.__name__

    @property
    def pid(self):
        return self._pid

    # 初始化
    def init(self):
        """
        @func: 数据处理节点初始化
        @desc: 在 process 方法调用之前进行初始化操作，比如数据库连接，数据输出目录构建等操作
        """
        pass

    # 核心处理逻辑
    def process(self, data: dict) -> dict:
        """
        @func: 数据处理逻辑简述(必要)
        @desc: 数据处理逻辑的详细描述(可选)
        @input: 数据输入数据样例(必要)
        @output: 数据输出数据样例(必要)
        """
        raise NotImplementedError("method(process) must be implemented")
    
    # 销毁
    def exit(self):
        """
        @func: 数据处理节点销毁
        @desc: 在数据节点销毁之前执行，可以用于关闭数据库或者文件描述符等操作
        """
        pass


# 数据处理管道
class DataProcessPipeline(object):
    """
    @class: DataProcessPipeline | 数据处理管道
    @desc: 
        对 **数据处理节点(DataProcessNode)** 进行集成和封装，
        以构建一个完整的数据处理流程，通过组装不同的数据处理节点来
        覆盖不同的数据处理需求。
    @property
    @method: 
        * init: 初始化数据处理管道
        * process: 数据处理接口
        * exit: 销毁数据处理管道
        * check: 检测数据处理节点规范，数据类型兼容性校验
        * test: 测试完整数据处理流程，并输出完整的数据流
        * doc: 提取和构建数据处理节点文档
    @exp: 

    """

    def __init__(self, data_process_nodes=[]):
        """
        @func: 构建器
        @params: 
            * data_process_nodes(list: DataProcessNode): 数据处理节点流 
        """
        # 数据处理节点流
        self.__data_process_nodes = data_process_nodes
        # 初始化状态标记
        self.__isInit = False

    # 初始化数据处理管道
    def init(self):
        if self.__isInit:
            raise Exception("DataProcessPipeline is initialized")
        # 校验数据处理节点规范
        self.check()
        # 初始化所有数据处理节点
        [node.init() for node in self.__data_process_nodes]
        # 更新初始化状态标记
        self.__isInit = True
        return self

    # 数据处理(调用接口)
    def process(self, datas: list) -> dict:
        """
        @func: 数据处理(调用接口)
        @desc: 通过数据处理节点流处理数据，并将结果集按照处理状态分类
        @params: 
            * datas(list): 待处理的数据
        @return(dict): 
            数据处理结果，其结构如下:
            {
                "SUCCES": [data1, data2, ...],
                "FILTER": [data1, data2, ...],
                "ERROR":  [data1, data2, ...],
            }
            其中单条处理结果的字段定义如下:
            {
                "data": "处理后的数据",
                "source": "原始数据",
                "node": "数据处理节点ID，("FILTER", "ERROR")状态下具有该字段",
                "error": "异常信息，("ERROR")状态下具有该字段"
            }
        """
        (not self.__isInit) and self.init()
        # 处理数据(结果按照处理状态分类)
        processed_result = {}
        for data in datas:
            result = self.__process(data)
            state = result.pop("state")
            processed_result.setdefault(state, []).append(result)
        return processed_result
    
    # 数据处理(核心逻辑)
    def __process(self, data, SAVE_DATA_FLOW=False):
        """
        @func: 对单条数据进行处理
        @params: 
            * data(any): 待处理的数据
            * SAVE_DATA_FLOW(bool): 用于记录节点的数据副本
        @return(type): 
        {
            "state": 处理结果状态("SUCCES", "FILTER", "ERROR"),
            "source": 原始数据,
            "data": 处理后的数据,
            "node": ("FILTER", "ERROR")状态下记录的节点id,
            "error": ("ERROR")状态下的异常信息
            "flow": 节点处理的数据副本(可选字段), -> [{"node": "节点ID", "data": "数据副本"}]
        }
        """
        # 处理结果容器
        processed_result = {"state": "SUCCES", "source": deepcopy(data)}
        # 保留数据流
        SAVE_DATA_FLOW and processed_result.update({"flow": []})
        # 调用数据处理节点
        for node in self.__data_process_nodes:
            try:
                _data = node.process(data)
                # FILTER: 节点过滤数据
                if _data is None:
                    processed_result.update({"state": "FILTER", "node": node.pid})
                    break
                # 记录节点处理数据副本
                SAVE_DATA_FLOW and processed_result["flow"].append({"node": node.pid, "data": deepcopy(_data)})
                data = _data
            except:
                # ERROR: 节点处理异常
                processed_result.update({"state": "ERROR", "node": node.pid, "error": traceback.format_exc()})
                break
        processed_result["data"] = data
        return processed_result
    
    # 销毁数据处理管道
    def exit(self):
        if not self.__isInit:
            raise Exception("DataProcessPipeline is not init")
        # 销毁所有数据处理节点
        [node.exit() for node in self.__data_process_nodes]

    # 校验数据处理节点规范
    def check(self):
        """
        @func: 校验数据处理节点规范
        @desc: 
            一种“伪静态”的数据类型校验，
            通过提取 DataProcessNode.process 的函数签名来校验两个节点之间输入输出数据类型的兼容性
            一个处理节点输出的数据类型应该与下一个处理节点输入的数据类型保持一致
            True:  node(A) -> list:list -> node(B)
            False: node(A) -> list:dict -> node(B)
            当 process 方法未包含类型注解时，视作任意数据类型。
            需要注意的是，该方法只能校验数据的“外层”数据类型，无法检测内部字段的数据类型。
        @algo: 
            对于两个类型 A，B 数据类型是兼容性定义如下:
                1. A，B 中包含一个任意类型(inspect._empty) 
                2. A，B 的继承链上具有一个共同父类，即存在一个父类 Base，A，B 是 Base 的子类
                3. A 是 B 的子类，或者 B 是 A 的子类。 
        """
        # 数据类型兼容性测试(inspect._empty作为任意类型标识)
        def compatibility(dataTypeA, dataTypeB):
            if (dataTypeA is inspect._empty) or (dataTypeB is inspect._empty):
                return True
            return bool(set(dataTypeA.__mro__[:-1]) & set(dataTypeB.__mro__[:-1]))
        # 验证整个数据处理链路输入输出的数据类型兼容性
        for i in range(len(self.__data_process_nodes)-1):
            # 当前处理节点输出数据类型
            node = self.__data_process_nodes[i]
            if not isinstance(node, DataProcessNode):
                raise TypeError(f'{node} is not DataProcessNode object')
            node_output_datatype = inspect.signature(node.process).return_annotation
            # 下一个处理节点输入数据类型
            next_node = self.__data_process_nodes[i+1]
            if not isinstance(next_node, DataProcessNode):
                raise TypeError(f'{next_node} is not DataProcessNode object')
            next_node_input_datatype = inspect.signature(next_node.process).parameters["data"].annotation
            # 比较两个节点之间的数据兼容性
            if not compatibility(node_output_datatype, next_node_input_datatype):
                raise TypeError(f"node({node.pid}) -> {node_output_datatype}|{next_node_input_datatype} -> node({next_node.pid})")
        return True
    
    # 数据测试
    def test(self, data, export_filepath=None):
        """
        @func: 测试完整数据处理流程，并输出完整的数据流
        @desc: 
            对单条数据进行测试，测试完整数据处理流程，并记录每个节点处理的数据副本，用于在开发阶段进行快速测试和修正。
        @params:
            * data(any): 测试数据
            * export_filepath(str): 测试结果导出文件
        @return(dict): 
        {
            "state": 处理结果状态("SUCCES", "FILTER", "ERROR"),
            "source": 原始数据,
            "flow": 节点处理的数据副本 -> [{"node": "节点ID", "data": "数据副本"}],
            "data": 处理后的数据
        }
        """
        test_data = self.__process(data, SAVE_DATA_FLOW=True)
        if export_filepath:
            with open(export_filepath, "w", encoding="utf-8") as f:
                f.write(json.dumps(test_data, ensure_ascii=False))
        return test_data

    # 构建文档
    def doc(self, export_filepath="./DataProcessPipeline_doc.md", extract_doc_from_node=None):
        """
        @func: 提取和构建数据处理节点文档
        @desc:  
            基于数据处理节点 *process* 方法的文档字符串构建简单的文档，
            用于快速了解整个数据处理管道的数据处理流程。
        @params: 
            * export_filepath(str): 文档导出路径
            * extract_doc_from_node(callable): 一个可调用对象，用于从 DataProcessNode 对象中提取文档字符串
        @return(file): 文档文件 
        """
        # 分隔符
        separator = "\n" + ("----------" * 6) + "\n"
        # (默认)节点文档提取器
        def __extract_doc_from_node(node):
            _doc = f'\n@annotation: process{inspect.signature(node.process)}'
            _doc += "\n".join([line.strip() for line in node.process.__doc__.split("\n")])
            return f'## {node.pid}\n```{_doc}```'
        extract_doc_from_node = extract_doc_from_node or __extract_doc_from_node
        # 提取所以节点文档
        all_doc = separator.join([extract_doc_from_node(node) for node in self.__data_process_nodes])
        # 导出文档
        with open(export_filepath, "w", encoding="utf-8") as f:
            f.write("# DataProcessPipeline\n")
            f.write(separator)
            f.write(all_doc)

    # 上下文协议
    def __enter__(self):
        self.init()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit()



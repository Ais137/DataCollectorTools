# Name: 示例
# Date: 2023-03-03
# Author: Ais
# Desc: None


import os
import json
import time
# 导入组件
from .data_process_pipeline import DataProcessNode, DataProcessPipeline


# 数据id过滤器
class DataIdFilter(DataProcessNode):

    def process(self, data: dict) -> dict:
        """
        @func: 过滤缺失id的数据，并输出日志
        @input: {"id": "", "content": "aaa"} | {"content": "aaa"}
        @output: None | None
        """
        return data if data.get("id") else None

# 字段类型转换器
class DataFieldConverter(DataProcessNode):

    def process(self, data: dict) -> dict:
        """
        @func: 对源数据的数据字段类型进行转换
        @desc: 将 count 字段转换成 int 类型
        @input: {"count": "137", ...}
        @output: {"count": 137, ...}
        """
        data["count"] = int(data["count"])
        return data
    
# 时间字段转换器
@DataProcessNode.build
def DateTimeConverter(self, data: dict) -> dict:
    """
    @func: 将 time 字段的时间戳转换成字符串
    @input: {"time": 1677661655, ...}
    @output: {"time": "2023-03-01 17:07:35", ...}
    """
    data["time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data["time"]))
    return data


if __name__ == "__main__":

    # 构建数据处理管道
    with DataProcessPipeline([
        DataIdFilter(),
        DataFieldConverter(),
        DateTimeConverter(),
    ]) as dp:
        
        # 构建测试目录
        not os.path.exists("./test") and os.makedirs("./test")

        # 数据测试
        test_data = {"id": 1, "content": "aaa", "count": "3", "time": 1677661655}
        dp.test(test_data, "./test/test.json")

        # 文档构建
        dp.doc("./test/doc.md")

        # 数据处理
        datas = [
            {"id": 1, "content": "aaa", "count": "3", "time": 1677661655},
            {"id": 2, "content": "bbbb", "count": "4", "time": 1677661677},
            {"id": 3, "content": "ccccc", "count": "5", "time": 1677662677},
            {"id": "", "content": "ddd", "count": "4", "time": 1677361677},
            {"id": 5, "content": "eeee", "count": "4"},
        ]
        processed_datas = dp.process(datas)
        # 导出数据结果
        with open("./test/data.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(processed_datas))

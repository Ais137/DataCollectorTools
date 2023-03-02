# DataCollectorTools

## Overview · 概述
***DataCollectorTools*** 项目用于封装和记录在 *数据采集(爬虫)* 开发过程中的一些工具和常用代码块。

--------------------------------------------------
## Index · 项目结构索引
### *framework* :
* [data_pipeline](./dctools/framework/data_pipeline/data_process_pipeline.py) : 一种组件化的轻量级数据处理模块设计 [开发与设计文档](./dctools/framework/data_pipeline/%E4%B8%80%E7%A7%8D%E7%BB%84%E4%BB%B6%E5%8C%96%E7%9A%84%E6%95%B0%E6%8D%AE%E5%A4%84%E7%90%86%E6%A8%A1%E5%9D%97%E8%AE%BE%E8%AE%A1.md)  
    *Features*
    1. 组件化构建: 通过组件化的方式完成数据处理流程的构建。
    2. 处理状态监控: 对数据的处理状态进行监控，记录异常的处理节点和异常信息。
    3. 兼容性检测: 通过对函数类型注解的自省，来校验两个数据处理节点之间输入输出数据类型的兼容性
    4. 数据测试: 对单条数据进行测试，验证完整的数据处理流程，记录每个节点处理的数据副本，用于后续分析。
    5. 文档生成: 自动集成数据处理节点的文档并构建一个总体描述文档


### *ats* :
* [ArtificialTrailSamples](./dctools/ats/artificial_trail_samples.py) : 人工滑动轨迹样本库，用于滑动缺口验证码的轨迹模式识别绕过。

### *utils* :
* [RequestsExtender](./dctools/utils/requests_extender.py) : requests扩展器，通过hook的方式扩展requests的功能，用于辅助分析目标网站的API请求。
* [JsonPathExtractor](./dctools/utils/jsonpath.py) : 通过类xpath的"路径表达式"来提取json格式的数据
* [MixQueue](./dctools/utils/mixqueue.py) : 元素混合队列，针对多域名网站进行数据采集时，对下载队列元素进行“混合”来减少“单一域名”下的并发请求数。
* [SliceQueue](./dctools/utils/slicequeue.py) : 分片队列，用于进行数据持久化时减少IO读写次数。

### *tools* :
* [CTR](./dctools/tools/curl_to_requests/CTR.py) : CURL命令转换器，用于分析/测试API请求，将chrome中复制的curl命令文本(str)转换成req对象(dict)，exp-> *python CTR.py curl.txt(curl文本文件)* 
* [modify_chromedriver_cdc](./dctools/tools/modify_chromedriver_cdc/modify_chromedriver_cdc.py) : 修改 *chromedriver($cdc)* 特征值


--------------------------------------------------
## Build · 构建
### install(安装): 
```cmd
python setup.py install
```
### cmdline(命令行工具)
```cmd
python -m dctools
```
### import(导入)
```python
import dctools
```

--------------------------------------------------
## DevPlan · 开发计划
* URL参数化迭代器: 通过配置参数构建URL迭代器，实现翻页迭代采集逻辑。
* 基于时间失效的URL去重器设计，用于解决增量采集框架的去重器资源占用随时间递增的问题
* 最小有效cookies检测器
* 网站拓扑结构探针

--------------------------------------------------
## Docs · 文档记录
* [一种组件化的轻量级数据处理模块设计](./docs/%E4%B8%80%E7%A7%8D%E7%BB%84%E4%BB%B6%E5%8C%96%E7%9A%84%E6%95%B0%E6%8D%AE%E5%A4%84%E7%90%86%E6%A8%A1%E5%9D%97%E8%AE%BE%E8%AE%A1.md)
* [requests模块二次编码导致的请求异常分析](./docs/requests模块二次编码导致的请求异常分析/requests模块二次编码导致的请求异常分析.md)
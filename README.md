# DataCollectorTools

## Overview · 概述
*DataCollectorTools* 项目用于封装和记录在 *数据采集(爬虫)* 开发过程中的一些工具和常用代码块。

--------------------------------------------------
## Index · 项目结构索引
### *utils*:
* **JsonPathExtractor** (*/utils/jsonpath.py*): 通过类xpath的"路径表达式"来提取json格式的数据
* **MixQueue** (*/utils/mixqueue.py*): 元素混合队列，针对多域名网站进行数据采集时，对下载队列元素进行“混合”来减少“单一域名”下的并发请求数。
* **SliceQueue** (*/utils/slicequeue.py*): 分片队列，用于进行数据持久化时减少IO读写次数。
### *tools*:
* **CTR** (*/tools/curl_to_requests/CTR.py*): CURL命令转换器，用于分析/测试API请求，将chrome中复制的curl命令文本(str)转换成req对象(dict)，exp-> *python CTR.py curl.txt(curl文本文件)* 

--------------------------------------------------
## DevPlan · 开发计划
* 人工轨迹样本 
* requests extension: requests库扩展

--------------------------------------------------
## Note · 文档记录
* requests模块二次编码导致的请求异常分析
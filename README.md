# DataCollectorTools

## Overview · 概述
*DataCollectorTools* 项目用于封装和记录在 *数据采集(爬虫)* 开发过程中的一些工具和常用代码块。

## Index · 项目结构索引
* JsonPathExtractor (*/utils/jsonpath.py*): 通过类xpath的"路径表达式"来提取json格式的数据
* MixQueue (*/utils/mixqueue.py*): 元素混合队列，针对多域名网站进行数据采集时，对下载队列元素进行“混合”来减少“单一域名”下的并发请求数。
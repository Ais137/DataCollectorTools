# Name: requests_extender | requests库扩展器
# Date: 2022-09-20
# Author: Ais
# Desc: 通过hook的方式扩展requests的功能
"""  
# 场景描述
数据采集的早期阶段，在对目标网站的API进行分析时，通常需要用requests来测试
API的回传数据格式和请求的关键参数。即通过调整请求参数来观察API回传数据变化来
验证关键参数，这个过程通常涉及到response数据的导出和请求参数的打印。因此
为了提高代码的复用率，考虑通过封装这些常用逻辑代码来“扩展”requests的功能。

# 设计思想
核心思想是通过“Hook”的方式来替换“关键方法”来实现功能的扩展。
在早期设计阶段，是通过 hook get(),post() 方法并结合闭包的方式来实现的。
```
@staticmethod
def requests_extender_templates():
    # 固定hook前的原方法
    requests_method = RequestsExtender.requests_method_fixed()
    # 扩展器代码
    def extender(**req_args):
        # ...
        # 调用原方法
        res = requests_method(**req_args)
        # ...
        return res
    # hook
    RequestsExtender.requests_hook(extender)
```
但是这种设计导致了一个问题，上述代码中的 *requests_method* 是用来存储
原始函数容器。当 get(), post() 函数调用时，requests_method 函数无法
获取到请求方法是 get 还是 post, 一个临时解决方案是判断 data 参数是否为空。
同时这种设计会导致随着扩展函数越多，函数嵌套也越深。
通过对requests源码的观察发现，对于get(), post(), ...方法来说，其内部都是
对 *requests.api.request* 的调用，因此可以通过hook这个关键函数来实现对
get(), post(), ... 等API的功能扩展。
"""


import os
import time
import json
import requests


# requests扩展器
class RequestsExtender(object):

    # hook目标函数(requests.api.request)
    request_method = None
    # 扩展器hook节点
    __HOOK_NODES = ["req", "res", "err"]
    # 扩展器
    extender = {node:[] for node in __HOOK_NODES}

    # -------------------------------------------------- #
    @staticmethod
    def load(extender, add=False):
        """
        @func: 加载扩展并hook目标函数
        @params: 
            * extender(dict): 扩展器 -> {"req": [], "res": [], "err": []}
                * (req): 在请求之前执行 -> extender_func(req: dict) 
                * (res): 在请求之后执行 -> extender_func(res: Response, req: dict)
                * (err): 请求异常时执行 -> extender_func(err: Exception, req: dict)
                其中 extender_func 为扩展器函数(callable)
            * add(bool): 新增模式，默认(False)会覆盖extender。
        @exp:
            > RequestsExtender.load({"req": [A, B], "res": [C]})
        """
        # 设置扩展器
        (not add) and RequestsExtender.extender.update({node:[] for node in RequestsExtender.__HOOK_NODES})
        [RequestsExtender.extender[node].extend(extender.get(node, [])) for node in RequestsExtender.__HOOK_NODES]
        # 固定目标函数
        if RequestsExtender.request_method is None:
            RequestsExtender.request_method = requests.api.request
        # request扩展函数
        def request_extension(method, url, **kwargs):
            # 构建req对象
            req = {"method": method, "url": url, **kwargs}
            # (req) hook node
            [extender(req) for extender in RequestsExtender.extender["req"]]
            try:
                # 调用目标函数
                res = RequestsExtender.request_method(req.pop("method"), req.pop("url"), **req)
                # (res) hook node
                [extender(res, {"method": method, "url": url, **kwargs}) for extender in RequestsExtender.extender["res"]]
                return res
            except Exception as err:
                # (err) hook node
                if RequestsExtender.extender["err"]:
                    [extender(err, {"method": method, "url": url, **kwargs}) for extender in RequestsExtender.extender["err"]]
                else:
                    raise err
        # hook目标函数
        requests.api.request = request_extension


    # -------------------------------------------------- #
    # 数据流记录器
    @staticmethod
    def dataflow(export_dir="./dataflow", req_field_filter=[], res_field_filter=[], export_filename_builder=None):
        """
        @func: 记录 request 和 response，用于分析请求数据流
        @params: 
            * export_dir(str:path): 数据导出目录
            * req_field_filter(list): 请求字段导出过滤器，用于过滤导出字段 
                默认导出字段 -> ["url", "method", "params", "data", "headers", "cookies"]
            * res_field_filter(list): 返回字段导出过滤器 
                默认导出字段 -> ["url", "status_code", "headers", "cookies", "history", "text"]
            * export_filename_builder(callabe): 用于生成导出文件名
                参数形式: builder(url: str) -> str
        @return(func): 扩展器函数
        @warning: 该扩展器绑定到(res)hook节点
        @exp:
            > RequestsExtender.load({"res": [RequestsExtender.dataflow()]})
        """
        from urllib.parse import urlparse
        # request对象导出字段
        req_export_field = ["url", "method", "params", "data", "headers", "cookies"]
        # response对象导出字段
        res_export_field = ["url", "status_code", "headers", "cookies", "history", "text"]
        # 导出文件名构建器
        export_filename_builder = export_filename_builder or (lambda url: f"{urlparse(url).netloc}_{int(time.time()*1000)}")
        # 扩展器函数
        def extender(res, req):
            # 构建导出目录
            (not os.path.exists(export_dir)) and os.makedirs(export_dir)
            # 构建数据
            dataflow = {
                "request": {f:req.get(f) for f in req_export_field if f not in req_field_filter},
                "response": {f:getattr(res, f, None) for f in res_export_field if f not in res_field_filter}
            }
            # 解析(params)
            try:
                if "params" not in req_field_filter and dataflow["request"]["params"] is None:
                    dataflow["request"]["params"] = {p.split("=", 1)[0]:p.split("=", 1)[1] for p in urlparse(dataflow["request"]["url"]).query.split("&")}
            except: 
                pass
            # 解析(headers)(CaseInsensitiveDict)
            if "headers" not in res_field_filter:
                dataflow["response"]["headers"] = dict(dataflow["response"].get("headers", {}))
            # 解析(cookies)(RequestsCookieJar)
            if "cookies" not in res_field_filter:
                dataflow["response"]["cookies"] = requests.utils.dict_from_cookiejar(res.cookies)
            # 解析(history)(Response)
            if "history" not in res_field_filter:
                dataflow["response"]["history"] = [h.url for h in dataflow["response"]["history"]]
            # 导出数据
            with open(os.path.join(export_dir, f"{export_filename_builder(req['url'])}.json"), "w", encoding="utf-8") as f:
                f.write(json.dumps(dataflow, ensure_ascii=False))
        return extender
        

    # -------------------------------------------------- #
    # 数据导出器
    @staticmethod
    def exporter(export_dir="./req", export_filename_builder=None):
        """
        @func: 导出response数据
        @params: 
            * export_dir(str:path): 数据导出目录
            * export_filename_builder(callabe): 用于生成导出文件名
                参数形式: builder(url: str) -> str
        @return(func): 扩展器函数
        @warning: 该扩展器绑定到(res)hook节点
        @exp:
            > RequestsExtender.load({"res": [RequestsExtender.exporter()]})
        """
        from urllib.parse import urlparse
        # 扩展器函数
        def extender(res, req):
            # 构建导出目录
            (not os.path.exists(export_dir)) and os.makedirs(export_dir)
            # 解析文件名/后缀
            filename, filetype = os.path.splitext(urlparse(res.url).path.split("/")[-1])
            if export_filename_builder:
                filename = export_filename_builder(res.url)
            filename = filename or urlparse(res.url).netloc
            # 导出数据
            if filetype == "":
                try:
                    json.loads(res.text)
                    with open(os.path.join(export_dir, f"{filename}.json"), "w", encoding="utf-8") as f:
                        f.write(res.text)
                except: 
                    with open(os.path.join(export_dir, f"{filename}.html"), "w", encoding="utf-8") as f:
                        f.write(res.text)
            elif filetype in ['.jpg', '.png', '.jpeg', '.gif']:
                with open(os.path.join(export_dir, f"{filename}{filetype}"), "wb") as f:
                    f.write(res.content)
            else:
                with open(os.path.join(export_dir, f"{filename}{filetype}"), "w", encoding="utf-8") as f:
                    f.write(res.text)
        return extender


    # -------------------------------------------------- #
    # 显示请求URL
    @staticmethod
    def disp():
        """
        @func: 显示请求的URL
        @return(func): 扩展器函数
        @warning: 该扩展器绑定到(req)hook节点
        @exp:
            > RequestsExtender.load({"req": [RequestsExtender.disp()]})
        """
        def extender(req):
            print(f"[{req['method']}] -> ({req['url']})")
        return extender
    


# Test
if __name__ ==  "__main__":
    
    # 显示请求参数
    def disp(req):
        print(f"[{req['method']}] -> ({req['url']})")

    # 添加请求头
    def add_headers(req):
        req.setdefault("headers", {}).update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-CN,zh;q=0.9"
        })

    # 导出数据
    def export(res, req):
        with open("./test.html", "w", encoding="utf-8") as f:
            f.write(res.text)

    # 异常处理
    def error(err, req):
        print("-------------------- ERROR --------------------")
        print(f"[URL]: {req['url']}")
        print(err)

    # 加载扩展
    RequestsExtender.load({
        "req": [disp, add_headers], 
        "res": [export], 
        "err": [error]
    })

    # 测试请求
    res = requests.get("https://fanyi.baidu.com/")
    
    
# Name: curl to request
# Date: 2022-09-15
# Author: Ais
# Desc: 将curl命令文本(str)转换成req对象(dict)


import re
import sys
import json
import traceback


# CURL转换器
class CTR(object):
    """
    @class: CURL转换器
    @desc: 将curl命令文本(str)转换成req对象(dict)
    @property(static): 
        * CURL_PARSER_CLASS(class): 自定义解析器类
        * PARSE_URL_PARAMS(bool): 是否解析 url params 参数
        * PARSE_POST_DATA(bool): 是否解析 post data 参数
        * DISP_PARSE_ERROR(bool): 显示解析异常
        * ENABLE_RESPONSE_EXPORT_CODE(bool): 是否添加请求数据导出代码
        * TAB(str): 制表符
    @method(static): 
        * translator: 将curl命令文本转换成对应的req对象代码
        * exporter: 将requests_objs填充进模板代码并导出到指定文件
    @exp: 
        > python CTR.py curl.txt(curl文本文件)
    """

    # 自定义解析器类
    CURL_PARSER_CLASS = None
    # 是否解析 url params 参数
    PARSE_URL_PARAMS = True
    # 是否解析 post data 参数
    PARSE_POST_DATA = True
    # 显示解析的URL
    DISP_PARSE_URL = False
    # 显示解析异常
    DISP_PARSE_ERROR = False
    # 是否添加请求数据导出代码
    ENABLE_RESPONSE_EXPORT_CODE = False
    # 制表符
    TAB = "    "

    # -------------------------------------------------- #
    # curl解析器
    class Parser(object):
        
        def __init__(self):
            """
            @desc: 逐行扫描curl命令文本，并根据解析函数表(opts)进行解析。
            """
            # requests对象容器: 
            self.req = {"url": "", "method": "GET", "headers": {}, "cookies": {}, "notes":[]}
            # 解析函数表
            self.pfunc = {}
            self.bind_parsefunc()

        # 解析
        def parse(self, text):
            # 逐行解析
            for line in text.split("\n"):
                # 去除空字符串
                line = line.strip()
                if not re.sub(r"\s", "", line):
                    continue
                # 根据flag调用绑定的解析函数
                for flag, parsefunc in self.pfunc.items():
                    line[:len(flag)] == flag and parsefunc(line, self.req)
            return self.req

        # 绑定解析函数(装饰器)
        def parsefunc(self, flag):
            def bind_func(func):
                self.pfunc[flag] = func
                return func
            return bind_func

        # 解析函数表
        def bind_parsefunc(self):
            # ---------- 解析[注释] ---------- #
            @self.parsefunc("#")
            def add_note(text, req):
                req["notes"].append(text)
            # ---------- 解析[url] ---------- #
            @self.parsefunc("curl")
            def parse_url(text, req):
                url_txt = re.search(r"\'(\S+?)\'", text).groups()[0]
                url, params = url_txt.split("?", 1) if ("?" in text and "=" in text and CTR.PARSE_URL_PARAMS) else (url_txt, None)
                req["url"] = url
                req["params"] = {kv.split("=")[0]:kv.split("=")[1] for kv in params.split("&")} if params else {}
            # ---------- 解析[headers] ---------- #
            @self.parsefunc("-H")
            def parse_header(text, req):
                key, val = re.search(r"\'(.+)\'", text).group().strip("'").split(": ", 1)
                if key.upper() == "COOKIE":
                    req["cookies"] = {c.split("=", 1)[0]:c.split("=", 1)[1] for c in val.split("; ")}
                else:
                    req["headers"][key] = val
            # ---------- 解析[post_data] ---------- #
            @self.parsefunc("--data-raw")
            def parse_post_data(text, req):
                req["method"] = "POST"
                pdata = re.search(r"\'(.+)\'", text).group().strip("'")
                if CTR.PARSE_POST_DATA:
                    try:
                        req["data"] = json.loads(pdata)
                    except: 
                        req["data"] = {d.split("=", 1)[0]:d.split("=", 1)[1] for d in pdata.split("&")}
                else:
                    req["data"] = pdata


    # -------------------------------------------------- #
    # 转换器
    @staticmethod
    def translator(curl_text):
        """
        @func: 将curl命令文本转换成对应的req对象代码
        @params: 
            * curl_text(str): 待转换的curl命令文本
        @return(list:dict): requests_objs
        """
        Parser = CTR.CURL_PARSER_CLASS or CTR.Parser
        # return [Parser().parse(text) for text in curl_text.split("--compressed")[:-1]]
        requests_objs = []
        for text in curl_text.split("--compressed")[:-1]:
            if "curl" not in text:
                continue
            try:
                req = Parser().parse(text)
                requests_objs.append(req)
                CTR.DISP_PARSE_URL and print(f"[{req['method']}] -> ({req['url']})")
            except: 
                if CTR.DISP_PARSE_ERROR:
                    print("-----------" * 4)
                    print(">>> [CURL]")
                    print(text)
                    print(">>> [ERR]")
                    print(traceback.format_exc())
        return requests_objs

    # -------------------------------------------------- #
    # 导出器
    @staticmethod
    def exporter(requests_objs, export_path):
        """
        @func: 将requests_objs填充进模板代码并导出到指定文件
        @params: 
            * requests_objs(list:dict): translator方法转换的对象
            * export_path(str): 导出的文件路径
        """
        # 输出代码
        out_code = "import requests\n\n"
        # 字典模板
        def dict_templates(data):
            # return "{{\n{}\n    }}".format("\n".join([(f'\t\t"{k}": "{v}",' if ("'" in v) else f"\t\t'{k}': '{v}',") for k, v in data.items()]))
            t = []
            for k, v in data.items():
                if isinstance(v, str):
                    t.append(f'{CTR.TAB*2}"{k}": "{v}",' if ("'" in v) else f"{CTR.TAB*2}'{k}': '{v}',")
                else:
                    t.append(f'{CTR.TAB*2}"{k}": {v},')
            return "{{\n{}\n    }}".format("\n".join(t))
        # 构建输出代码
        n = 0
        for req in requests_objs:
            res = f'res{n if n>0 else ""}'
            templates = [
                "\n".join(req["notes"]),
                f'{res} = requests.{req["method"].lower()}(',
                f'{CTR.TAB}url = \"{req["url"]}\",',
            ]
            req["headers"] and templates.append(f'{CTR.TAB}headers = {dict_templates(req["headers"])},')
            req["cookies"] and templates.append(f'{CTR.TAB}cookies = {dict_templates(req["cookies"])},')
            req["params"] and templates.append(f'{CTR.TAB}params = {dict_templates(req["params"])},')
            req["method"] == "POST" and templates.append(f'{CTR.TAB}data = {dict_templates(req["data"]) if isinstance(req["data"], dict) else req["data"]}')
            templates.append(")")
            if CTR.ENABLE_RESPONSE_EXPORT_CODE:
                templates += [
                    f'with open("./{res}.html", "w", encoding="utf-8") as f:',
                    f'{CTR.TAB}f.write({res}.text)'
                ]
            templates.append("\n\n")
            out_code += "\n".join(templates)
            n += 1

        # 导出代码
        with open(export_path, "w") as f:
            f.write(out_code)


# Test
if __name__ == "__main__":

    import argparse
    # 构建命令行解析器
    parser = argparse.ArgumentParser(description="将curl命令文本(str)转换成req对象(dict)")
    # 添加命令行参数
    parser.add_argument("curl_filepath", type=str, help="curl文件输入路径")
    parser.add_argument("-o", "--out", type=str, default="./out.py", help="req代码输出路径")
    parser.add_argument("-res", "--res_out", action="store_true", help="添加res数据导出代码")
    parser.add_argument("-du", "--disp_url", action="store_true", help="显示解析的URL")
    parser.add_argument("-de", "--disp_err", action="store_true", help="显示解析异常")
    # 解析参数
    args = parser.parse_args()
    # 调用CURL转换器
    CTR.DISP_PARSE_URL = args.disp_url
    CTR.DISP_PARSE_ERROR = args.disp_err
    CTR.ENABLE_RESPONSE_EXPORT_CODE = args.res_out
    with open(args.curl_filepath, 'r', encoding="utf-8") as f:
        CTR.exporter(CTR.translator(f.read()), args.out)


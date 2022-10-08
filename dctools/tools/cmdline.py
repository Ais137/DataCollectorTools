# Name: cmdline
# Date: 2022-10-07
# Author: Ais
# Desc: None


import sys
from importlib import import_module
from pkgutil import iter_modules


# 工具命令类
class ToolCommand(object):

    # 命令映射表
    cmds = {}

    # 绑定工具命令
    @staticmethod
    def cmd(cmd_name, cmd_desc):
        """
        @func: 通过该装饰器绑定工具命令到映射表
        @params: 
            * cmd_name: 命令名 
            * cmd_desc: 命令功能概述 
        @exp
            @ToolCommand.cmd("Test", "test command")
            def test():
                pass
        """
        def add_cmd(cmd_func):
            ToolCommand.cmds[cmd_name] = {
                "desc": cmd_desc,
                "func": cmd_func
            }
            return cmd_func
        return add_cmd

    # 导入命令行表
    @staticmethod 
    def _load_cmd_from_module(module_path="dctools.tools"):
        """
        @func: 遍历导入指定路径下的模块，构建命令映射表(cmds)
        @params: 
            * module_path: 模块名
        """
        mods = [import_module(module_path)]
        while mods:
            mod = mods.pop(0)
            for _, subpath, ispkg in iter_modules(mod.__path__):
                fullpath = mod.__name__ + '.' + subpath
                if ispkg:
                    mods.append(import_module(fullpath))
                else:
                    import_module(fullpath)

    @staticmethod
    def _list_cmds():
        """
        @func: 列举命令映射表中的命令
        """
        print("----------" * 5)
        # print("数据采集(爬虫)开发工具集:\n")
        print("Usage:")
        print("  dctools <command> [args]\n")
        print("Available commands:")
        for cmd_name, cmder in sorted(ToolCommand.cmds.items()):
            print(f"  {cmd_name:<15} {cmder.get('desc')}")

    @staticmethod
    def execute():
        """
        @func: 执行入口
        """
        # 导入命令行表
        ToolCommand._load_cmd_from_module()
        # 解析命令
        args = sys.argv[1:]
        cmd = args.pop(0) if args else None
        if cmd is None:
            ToolCommand._list_cmds()
        elif cmd in ToolCommand.cmds:
            print("----------" * 5)
            ToolCommand.cmds[cmd]["func"](args)
        else:
            raise ValueError(f"cmd({cmd}) is not exists")
        


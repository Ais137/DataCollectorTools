# Name: modify_chromedriver_cdc
# Date: 2022-09-21
# Author: Ais
# Desc: 修改chromedriver_$cdc特征值($cdc_asdjflasutopfhvcZLmcfl_)


import re
import random
import argparse
import traceback


# 随机化chromedriver_$cdc特征值
def randomization_chromedriver_cdc(chromedriver_path, n=5, cover=False, disp=False):
    """
    @func: 查找chromedriver中的$cdc特征值，并对其进行修改
    @params: 
        * chromedriver_path(str:path): 待修改的chromedriver路径 
        * n(int:>0): 修改时替换的子串长度
        * cover(bool): 覆盖模式开关，False(生成新文件)，True(覆盖原始文件)
        * disp(bool): 调试开关
    """
    disp and print("----------"*5)
    disp and print("修改chromedriver_$cdc特征值")
    try:
        # 导入原始 chromedriver 二进制代码
        chromedriver_bin_src = b""
        with open(chromedriver_path, "rb") as f:
            chromedriver_bin_src = f.read()
        disp and print(f"[load]: {chromedriver_path}")
        # 查找($cdc)特征值
        cdc_search_res = re.search(b"\$cdc_(\w+)_", chromedriver_bin_src)
        # 特征值
        src_cdc = cdc_search_res.group(1)
        disp and print(f"[src_cdc]: {src_cdc}")
        # 特征值位置
        src_cdc_start, src_cdc_end = cdc_search_res.span()
        # 生成随机字符串
        n = min(n, 22)
        alphabet = list("abcdefghijklmnopqrstuvwxwz")
        sub_cdc = "".join([random.choice(alphabet) for i in range(n)]).encode()
        disp and print(f"[sub_cdc]: {sub_cdc}")
        # 构建新的特征值
        new_cdc = b"$cdc_" + sub_cdc + src_cdc[n:] + b"_"
        disp and print(f"[new_cdc]: {sub_cdc + src_cdc[n:]}")
        # 替换原始特征值
        modified_chromedriver = chromedriver_bin_src[:src_cdc_start] + new_cdc + chromedriver_bin_src[src_cdc_start + len(new_cdc):] 
        # 导出目标文件
        export_path = chromedriver_path if cover else "./m_chromedriver.exe"
        with open(export_path, "wb") as f:
            f.write(modified_chromedriver)
        disp and print(f"[out]: {export_path}")
        disp and print("[success]: modify chromedriver $cdc success")
    except: 
        print(f"[failed]: modify chromedriver $cdc failed")
        print(f"[error]: {traceback.format_exc()}")


if __name__ ==  "__main__":
    
    # 构建命令行解析器
    parser = argparse.ArgumentParser(description="修改chromedriver_$cdc特征值")
    # 添加命令行参数
    parser.add_argument("chromedriver_path", type=str, help="待修改的chromedriver路径")
    parser.add_argument("-n", "--n", type=int, default=5, help="修改时替换的子串长度 -> [1, 22]")
    parser.add_argument("-c", "--cover", action="store_true", help="覆盖原始文件")
    parser.add_argument("-d", "--disp", action="store_true", help="显示修改过程")
    # 解析参数
    args = parser.parse_args()
    # 修改特征值
    randomization_chromedriver_cdc(args.chromedriver_path, args.n, cover=args.cover, disp=args.disp)
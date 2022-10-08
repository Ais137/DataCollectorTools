# Name: setup
# Date: 2022-09-30
# Author: Ais
# Desc: None


from setuptools import setup, find_packages


setup(
    name="dctools",
    version="0.0.1",
    author="ais",
    # 概述
    description="用于封装和记录在数据采集(爬虫)开发过程中的一些工具和常用代码块",
    # 项目主页
    url="https://github.com/Ais137/DataCollectorTools",
    # 目标包
    packages=find_packages(),
    # 源码包中的资源文件(MANIFEST.in)
    include_package_data=True,
    # 依赖包
    install_requires=[],
)
# Name: 人工滑动轨迹样本
# Date: 2022-09-16
# Author: Ais
# Desc: None
"""  
# 场景描述
在进行缺口滑动验证吗的绕过时，即使准确的计算出缺口的偏移量，
目标服务器也可能会检测滑动轨迹来进行人机识别(反爬)，因此需要
构建一种算法来模拟人工的滑动轨迹。

# 设计思想:
通过一个人工轨迹捕获器(Artificial_Trail_Samples_Capturer)，按照指定间隔(d=50)生成一个
人工轨迹样本库。当计算出验证码的缺口偏移量(offset)时，在该样本库中匹配一个轨迹长度与该
缺口偏移量最接近的样本，并通过一种“插值”算法将该样本的轨迹长度与目标偏移量匹配。

# 轨迹结构
* [in]: artificial_trail_samples(人工轨迹样本)
```
[
    [x1, y1, t1], 
    [x2, y2, t2],
    ...
    [xn, yn, tn]  -> [x轴偏移量, y轴偏移量, 时间间隔]
]
```
* [out]: trail_samples(轨迹样本)
```
{
    "x_offset": x轴总偏移量,
    "y_offset": y轴总偏移量,
    "t_offset": 总时间间隔,
    "tn": 轨迹点数量,
    "start": 起始状态,
    "offset": [[x1, y1, t1], ...] -> 偏移序列,
    "d_offset": [[dx1, dy1, dt1], ...] -> 增量偏移序列
}
```

# 插值算法
设 ts 为某个轨迹的“增量偏移序列”，n为轨迹点数量，offset为目标总偏移量。
    ts = [d1, d2, d3, ..., dx]
则有偏移量的增量 d = offset - sum(ts), (sum(ts)为当前轨迹的总偏移量)
分解增量令 d = dn*n + di
其中 
    “整体插值增量” -> dn = int(d/n)
    “间隔插值增量” -> di = d%n
* 整体插值: 当 offset>=n 时有 dn>0:
        [d1, d2, d3, d4, ..., dx]
    +   [dn, dn, dn, dn, ..., dn]
    ->  [d1+dn, d2+dn, d3+dn, ..., dx+dn]
* 间隔插值: 当 di>0 | offset<n 时
        [d1, d2, d3, d4, ..., dx]
    +   [1,  0,  1,  0, ...,  di]
    ->  [d1+1, d2+0, d3+1, ..., dx+di]
    其中插值间距为 round(n/di)
由上述可知，增量偏移序列的轨迹点增量为
    ts[i] = ts[i] + dn + di
"""

import json
import random


# 人工轨迹样本
class ArtificialTrailSamples(object):

    # ------------------------------------------------------- #
    # 构建轨迹样本库
    @staticmethod
    def build_trail_samples(artificial_trail_samples_path, trail_samples_export_path="./ts.json", sort_by="x_offset"):
        """
        @func: 通过人工轨迹样本(捕获器捕获轨迹)构建轨迹样本库
        @params: 
            * artificial_trail_samples_path(str): 人工轨迹样本文件路径
            * trail_samples_export_path(str): 轨迹样本库导出路径
            * sort_by(str): 排序方式
        @return(file): 轨迹样本库
        """
        # 轨迹样本容器
        trail_samples = []
        # 导入人工轨迹样本数据
        artificial_trail_samples = []
        with open(artificial_trail_samples_path, "r", encoding="utf-8") as f:
            artificial_trail_samples = json.loads(f.read())
        # 构建轨迹样本数据
        for ats in artificial_trail_samples:
            # 构建轨迹
            trail = ArtificialTrailSamples.Trail(offset=ats).to_dict()
            # 排序
            index = [i for i in range(len(trail_samples)) if trail[sort_by] > trail_samples[i][sort_by]]
            trail_samples.insert(index[-1]+1, trail) if index else trail_samples.insert(0, trail)
            # print([ts[sort_by] for ts in trail_samples])
        # 导出轨迹数据
        with open(trail_samples_export_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(trail_samples, ensure_ascii=False))
        return len(trail_samples)

    # d_offset -> offset
    @staticmethod
    def build_offset(d_offset, start=[]):
        """
        @func: d_offset(增量偏移序列) -> offset(偏移序列)
        @params: 
            * d_offset(list:list): 增量偏移序列
            * start(list): 起始状态
        @return(list): d_offset(增量偏移序列)
        """
        n = len(d_offset[0])
        offset = [start or ([0] * n)]
        [offset.append([offset[i][k]+d_offset[i][k] for k in range(n)]) for i in range(len(d_offset))]
        return offset

    # offset -> d_offset
    @staticmethod
    def build_d_offset(offset):
        """
        @func: offset(偏移序列) -> d_offset(增量偏移序列) 
        @params: 
            * offset(list:list): 偏移序列
        @return(list): d_offset(增量偏移序列)
        """
        return [[offset[i+1][k]-offset[i][k] for k in range(len(offset[0]))] for i in range(len(offset)-1)]


    # ------------------------------------------------------- #
    # 插值算法
    @staticmethod
    def interpolator(ts, offset):
        """
        @func: 通过插值算法将轨迹的总偏移量移动到目标值
        @params: 
            * ts(list): 轨迹的增量偏移序列(Trail.d_offset) 
            * offset(int): 轨迹的目标总偏移量(Trail.x_offset) 
        @return(list): ts 
        @algorithm:
            设 ts 为某个轨迹的“增量偏移序列”，n为轨迹点数量，offset为目标总偏移量。
                ts = [d1, d2, d3, ..., dx]
            则有偏移量的增量 d = offset - sum(ts), (sum(ts)为当前轨迹的总偏移量)
            分解增量令 d = dn*n + di
            其中 
                “整体插值增量” -> dn = int(d/n)
                “间隔插值增量” -> di = d%n
            * 整体插值: 当 offset>=n 时有 dn>0:
                    [d1, d2, d3, d4, ..., dx]
                +   [dn, dn, dn, dn, ..., dn]
                ->  [d1+dn, d2+dn, d3+dn, ..., dx+dn]
            * 间隔插值: 当 di>0 | offset<n 时
                    [d1, d2, d3, d4, ..., dx]
                +   [1,  0,  1,  0, ...,  di]
                ->  [d1+1, d2+0, d3+1, ..., dx+di]
                其中插值间距为 round(n/di)
            由上述可知，增量偏移序列的轨迹点增量为
                ts[i] = ts[i] + dn + di
        """
        # 轨迹点数量
        n = len(ts)
        # 计算偏移量的增量
        d = offset - sum(ts)
        # 分解增量
        dn, di = int(d/n), (abs(d)%n)
        # (d >= n): 整体插值 -> [dn, dn, dn, ...0]
        if dn:
            for i in range(n):
                ts[i] += dn
        # (d < n):  间隔插值 -> [1, ..., 1, ..., 1, ...]
        if di:
            for i in list(range(0, n, round(n/di)))[:di]:
                ts[i] += (1 if d>0 else -1)
        return ts

    # 插值算法验证
    @staticmethod
    def test_interpolator(interpolator, ts, d, disp_len=10):
        """
        @func: 用于验证和测试插值算法的有效性
        @params: 
            * interpolator(callable): 插值器
            * ts(list): 测试轨迹
            * d(int): 插值范围 -> [sum(ts)-d, sum(ts)+d]
        @return: None
        """
        # 当前测试轨迹总偏移量
        ts_offset = sum(ts)
        print(f"{ts[:disp_len]}\n{'------'*8}")
        # 测试
        for i in range(ts_offset-d, ts_offset+d+1):
            # 对轨迹进行插值
            _ts = interpolator(ts[:], i)
            # 插值增量序列
            dts = [_ts[k]-ts[k] for k in range(len(ts))]
            # 输出结果
            print(f"{_ts[:disp_len]} -> d({i}, {sum(_ts)}, {i-ts_offset}): {dts}")

    
    # ------------------------------------------------------- #
    # 构建器
    def __init__(self, frange=(-50, 50), trail_interpolator=None):
        """
        @class: 人工轨迹样本库
        @desc: 通过对轨迹样本库中的轨迹进行插值来生成目标轨迹
        @property: 
            * frange(tuple): 轨迹查找范围
            * trail_interpolator(callable): 轨迹插值器
        @method: 
            * load: 导入轨迹样本
            * build: 构建目标轨迹
        @exp: 
            ts = ArtificialTrailSamples().load("./ts.json").build(x_offset=325, t_offset=3000)
        """
        # 轨迹样本存储容器
        self.__trail_samples = []
        # 轨迹查找范围
        self.frange = frange
        # 轨迹插值器
        self.trail_interpolator = trail_interpolator

    # 导入轨迹样本
    def load(self, trail_samples_path):
        """
        @func: 导入轨迹样本
        @params: 
            * trail_samples_path(str): 轨迹样本库路径
        """
        with open(trail_samples_path, "r") as f:
            self.__trail_samples = [ArtificialTrailSamples.Trail(
                offset = ts["offset"],
                d_offset = ts["d_offset"],
                interpolator = self.trail_interpolator
            ) for ts in json.loads(f.read())]
        return self

    # 构建目标轨迹
    def build(self, x_offset, t_offset=None):
        """
        @func: 构建目标轨迹
        @params: 
            * x_offset(int:>0): x轴总偏移量
            * t_offset(int:>0): 总时间间隔
        @return: 
        """
        # 随机选择一个邻近轨迹
        ts = random.choice([ts for ts in self.__trail_samples if (x_offset+self.frange[0] <= ts.x_offset <= x_offset+self.frange[1])]).copy()
        # 对轨迹样本进行插值
        ts.x_offset = x_offset
        if t_offset:
            ts.t_offset = t_offset
        return ts


    # ------------------------------------------------------- #
    # 轨迹容器
    class Trail(object):
    
        def __init__(self, offset=[], d_offset=[], start=[0, 0, 0], interpolator=None):
            """
            @class: Trail
            @desc: 轨迹数据容器
            @params:
                * offset(list:list): 轨迹偏移序列
                * d_offset(list:list): 轨迹增量偏移序列
                * start(list): 起始状态
                * interpolator(callable): 插值器
            @property: 
                * __offset(list): 偏移序列
                * __d_offset(list): 增量偏移序列
                * interpolator(callable): 插值器 -> def func(ts, offset, w=0)
            @method: 
                * __interpolator: 轨迹插值算法
                * display: 以图像的方式显示轨迹结构
                * slider: 通过selenium进行轨迹的滑动模拟
                * (get)d_offset: d_offset迭代器
                * (get)dx|dy|dt: d_offset分量迭代器
                * (set)x_offset: 设置轨迹总偏移量(x_offset) -> 对轨迹的d_offset[x]序列进行插值
                * (set)t_offset: 设置轨迹总时间间隔(t_offset) -> 对轨迹的d_offset[t]序列进行插值
                * (set)start: 设置offset序列的起始状态 -> 根据start重构offset序列
                * to_dict(): 转换成字典
                * copy(): 复制轨迹
            @exp: 
            """
            # 偏移序列
            self.__offset = offset[:] or ArtificialTrailSamples.build_offset(d_offset, start)
            # 增量偏移序列
            self.__d_offset = d_offset[:] or ArtificialTrailSamples.build_d_offset(offset)
            # 插值器(插值算法实现)
            self.interpolator = interpolator or self.__interpolator

        # 轨迹长度(tn)
        def __len__(self):
            return len(self.__offset)

        # 可迭代对象
        def __iter__(self):
            return iter(self.__offset)

        # 转化成字符串
        def __str__(self) -> str:
            return json.dumps(self.to_dict())

        # 插值算法
        def __interpolator(self, ts, offset, w=0):
            """
            @func: 通过插值算法将轨迹的总偏移量移动到目标值
            @params: 
                * ts(list): 轨迹的增量偏移序列
                * offset(int): 轨迹的目标总偏移量
                * w(int): 轨迹分量索引 -> {0:x_offset, 1:y_offset, 2:t_offset}
            """
            # 轨迹点数量
            n = len(ts)
            # 计算偏移量的增量
            d = offset - sum([t[w] for t in ts])
            # 分解增量
            dn, di = int(d/n), (abs(d)%n)
            # (d >= n): 整体插值 -> [dn, dn, dn, ...0]
            if dn:
                for i in range(n):
                    ts[i][w] += dn
            # (d < n):  间隔插值 -> [1, ..., 1, ..., 1, ...]
            if di:
                for i in list(range(0, n, round(n/di)))[:di]:
                    ts[i][w] += (1 if d>0 else -1)
            return ts

        # 绘制轨迹
        def display(self):
            """
            @func: 以图像的方式显示轨迹结构
            """
            import matplotlib.pyplot as plt
            print("-----------" * 5)
            print(f"TRAIL_SAMPLES(tn={len(self)}): ")
            print(f"[x_offset]: ---> {self.x_offset}")
            print(f"[y_offset]: ---> {self.y_offset}")
            print(f"[t_offset]: ---> {self.t_offset}")
            print(f"[start]: ------> {self.start}")
            print(f"[end]: --------> {[self.x_offset, self.y_offset, self.t_offset]}")
            # 绘制图像
            n = list(range(len(self)))
            fig, ax = plt.subplots(2, 2, figsize=(12, 8))
            # 绘制x分量
            ax[0][0].plot(n, [p[0] for p in self.__offset])
            ax[0][0].set_ylabel("x")
            ax[0][0].set_xlabel("n")
            # 绘制y分量
            ax[0][1].plot(n, [p[1] for p in self.__offset])
            ax[0][1].set_ylabel("y")
            ax[0][1].set_xlabel("n")
            # 绘制dx分量
            ax[1][0].plot(n[:-1], [p[0] for p in self.__d_offset])
            ax[1][0].set_ylabel("dx")
            ax[1][0].set_xlabel("n")
            # 绘制dy分量
            ax[1][1].plot(n[:-1], [p[1] for p in self.__d_offset])
            ax[1][1].set_ylabel("dy")
            ax[1][1].set_xlabel("n")
            plt.show()
            return self

        # 滑动轨迹
        def slider(self, driver, slider_xpath, delay=None, release=True):
            """
            @func: 通过selenium进行轨迹的滑动模拟，用于滑动缺口验证码的轨迹模式识别绕过
            @params: 
                * driver(webdriver): 驱动
                * slider_xpath(str:xpath): 目标滑块元素的xpath表达式
                * delay(int): 总体滑动延时，当启用该参数时，轨迹的dt序列将被短路
                * release(bool): 是否释放滑块
            @exp: 
                ats.build(x_offset=230).slider(executer.driver, slider_xpath = '//div[@class="slider"]')
            """
            import time
            from selenium.webdriver.common.by import By
            from selenium.webdriver import ActionChains
            # 获取滑块元素
            slider_element = driver.find_element(By.XPATH, slider_xpath)
            # 点击滑块并保持
            ActionChains(driver).click_and_hold(slider_element).perform()
            # 计算平均延迟时间(将短路轨迹中的dt序列)
            _dt = (delay/len(self.__d_offset)/1000) if delay else 0
            # 根据轨迹参数(d_offset)进行滑动
            for dx, dy, dt in self.__d_offset:
                # duration = 250 会导致滑动延迟
                ActionChains(driver, duration=0).move_by_offset(xoffset=dx, yoffset=dy).perform()
                # 滑动延时
                time.sleep(_dt or (dt/1000 if dt>=0 else 0.001))
            # 释放滑块
            release and ActionChains(driver).release().perform()
            return self

        # d_offset序列
        @property
        def d_offset(self):
            return iter(self.__d_offset)

        # d_offset序列分量
        @property
        def dx(self):
            return (d[0] for d in self.__d_offset)
        @property
        def dy(self):
            return (d[1] for d in self.__d_offset)
        @property
        def dt(self):
            return (d[2] for d in self.__d_offset)

        # x轴总偏移量
        @property
        def x_offset(self):
            return self.__offset[-1][0] - self.__offset[0][0]
        @x_offset.setter
        def x_offset(self, offset):
            # 插值并重构offset 
            self.interpolator(self.__d_offset, offset, w=0)
            self.__offset = ArtificialTrailSamples.build_offset(self.__d_offset)
        
        # y轴总偏移量
        @property
        def y_offset(self):
            return self.__offset[-1][1] - self.__offset[0][1]
        
        # 总时间间隔
        @property
        def t_offset(self):
            return self.__offset[-1][2] - self.__offset[0][2]
        @t_offset.setter
        def t_offset(self, t):
            self.interpolator(self.__d_offset, t, w=2)
            self.__offset = ArtificialTrailSamples.build_offset(self.__d_offset)

        # 轨迹起始状态
        @property
        def start(self):
            return self.__offset[0]
        @start.setter
        def start(self, s):
            self.__offset = ArtificialTrailSamples.build_offset(self.__d_offset, s)

        # 转换成字典
        def to_dict(self):
            return {
                # x轴总偏移量
                "x_offset": self.x_offset,
                # y轴总偏移量
                "y_offset": self.y_offset,
                # 总时间间隔
                "t_offset": self.t_offset,
                # 轨迹点数量
                "tn": len(self),
                # 起始状态
                "start": self.start,
                # 偏移序列
                "offset": self.__offset,
                # 增量偏移序列
                "d_offset": self.__d_offset
            }

        # 复制
        def copy(self):
            return ArtificialTrailSamples.Trail(
                offset = [[self.__offset[i][k] for k in range(len(self.__offset[i]))] for i in range(len(self.__offset))],
                d_offset = [[self.__d_offset[i][k] for k in range(len(self.__d_offset[i]))] for i in range(len(self.__d_offset))],
                interpolator = self.interpolator
            )

    

# Test
if __name__ ==  "__main__":

    # --------------------------------------------
    # 测试插值算法
    # ArtificialTrailSamples.test_interpolator(
    #     # 插值器
    #     interpolator = ArtificialTrailSamples.interpolator,
    #     # 测试轨迹
    #     ts = [1, 2, 1, 3, 4, 1, 1, 2],
    #     # 插值范围
    #     d = 10
    # )

    # --------------------------------------------
    # 构建轨迹样本库
    # ArtificialTrailSamples.build_trail_samples(
    #     # 人工轨迹样本文件路径
    #     artificial_trail_samples_path = "./trail_samples.json",
    #     # 轨迹样本库导出路径
    #     trail_samples_export_path = "./ts.json",
    #     # 排序方式
    #     sort_by = "x_offset"
    # )

    # --------------------------------------------
    # 生成轨迹
    ts = ArtificialTrailSamples().load("./ts.json").build(x_offset=325, t_offset=3000).display()



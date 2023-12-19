import sys

from matplotlib.artist import Artist

import tkinter as tk
from matplotlib.text import Text
from matplotlib.lines import Line2D

from Plt import random_color_array, Plt, Axes


# 画图必须继承 Plt 类, Plt类不可以实例化
class TestShowMap(Plt):
    """
    需要重写函数：
        1. data_iterators

        2. parsed_data

        3. draw_geometric_type

        4. on_pick

        5. set_label

        6. with_function

    关键方法：
        1. add_sub_axes : 添加一个子图到 flg 中, 返回一个子图 Axes 对象
        :param kwargs
            is_dynamic_drawing: 是否自动滚动显示
            is_interact_with: 是否交互
            rect : 子图窗口的参数 tuple (left, bottom, width, height)
            参考官网：https://matplotlib.org/3.8.1/api/figure_api.html#matplotlib.figure.Figure.add_axes

        2. self.update_date : 添加数据到数据中转站
    """

    def __init__(self):
        """
        初始化是必须调用超类 Plt 的 初始化方法《__init__》
            超类 Plt 参数说明
                1. window_size :        窗口的大小，数组类型: (width, height), 默认: (8, 4)
                2. is_dynamic_drawing : 是否动态画图，默认: false
                3. is_interact_with :   是否交互,开启需要在 on_pick 方法里实现交互内容，默认: false. 参考官网：https://matplotlib.org/3.8.1/users/explain/figure/event_handling.html#event-handling-and-picking
        """
        super().__init__(window_size=(8, 4), is_dynamic_drawing=False, is_interact_with=False)

    def data_iterators(self):
        """
        有多次显示的数据在 data_iterators 方法里处理
            (1) 数量大可以把 data_iterators 写成迭代器,数据中转站会自动获取数据
            (2) 数量小就调用 update_data 方法把数据直接添加到数据中转站 ——> self.update_data(数据)
        """
        pass

    def parsed_data(self, data):
        """
         解析数据
            (1) 主要拆分数据，对数据进一步处理
            (2) 把数据保存到当前类变量中，变量自定义
        """
        pass

    def draw_geometric_type(self):
        """
        添加要画的几何图形和其他类型，使用解析完成的数据， 并且返回所有的子图对象
        """

    def with_function(self):
        """
        这方法只需要调用《self.continuous_draw -> 连续绘制方法》 或 《self.draw -> 绘制一次方法》
        """
        pass

    def on_pick(self, el):
        """
        交互事件，event交互事件传进来的参数
        """
        pass

    def set_label(self):
        """
        设置子画布的标签等，对标签进一步处理
        """
        pass


# 例子
import os


class MinTextWin:
    def __init__(self, root):
        self.root = root
        # 创建 StringVar
        self.entry_var = tk.StringVar()

        # 绑定 StringVar 的 trace，以便在文本变化时调用 on_var_change 函数
        self.entry_var.trace_add('write', self.on_var_change)
        self.entry = tk.Entry(self.root.root, width=2, textvariable=self.entry_var)
        self.artist = None
        self.gid = None
        self.entry.bind('<Key>', self.on_key)

    def on_key(self, event):
        if event.keysym == "Return" or event.keysym == "KP_Enter" or event.keycode == 36 or event.keycode == 104:
            if self.artist is not None:
                if not self.root.update_sub_data(self.artist, self.gid, self.entry.get()):
                    return
            self.entry.pack_forget()
            self.root.root.focus_set()
            self.entry.place(x=sys.maxsize, y=sys.maxsize)

    def on_var_change(self, *args):
        entry_width = len(self.entry.get())
        self.entry.config(width=entry_width)

    def creat_min_win_update_lane_text_box(self, x, y, gid=None, text="", artist=None):
        self.entry.pack()
        self.artist = artist
        self.gid = gid
        self.entry.place(x=self.root.mouse_x, y=self.root.mouse_y)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)
        self.entry.focus_set()
        self.entry.select_range(0, tk.END)


class Axes1(Axes):
    def __init__(self, plt):
        super().__init__(plt=plt, is_dynamically_drawn=True, is_interact_with=True, rect=[0.05, 0.1, 0.4, 0.8])
        self.plt = plt

        # 绑定事件
        self.bind_pick('on_pick_mouse_left', self.on_pick_mouse_left)

    def on_pick_mouse_left(self, event):
        print("Axes1: ", event.artist)
        self.plt.on_pick_mouse_left(event)


class TestMapShow(Plt):

    def __init__(self):
        # 随机获取颜色
        self.color = random_color_array(50, "hex")

        # 读取的数据目录
        self.file_path = os.path.join(os.path.dirname(__file__), "test_data")

        # 超类的初始化
        super().__init__(window_size=(8, 8), is_dynamic_drawing=True, is_interact_with=True)

        # # 添加一个子图
        # left, bottom, width, height = 0.05, 0.1, 0.4, 0.8
        # self.ax1 = self.add_sub_axes(is_dynamically_drawn=True, is_interact_with=True,
        #                              rect=[left, bottom, width, height])
        # # 子图绑定事件
        # self.ax1.bind_pick('on_pick_mouse_left', self.on_pick_mouse_left)

        # 添加一个子图
        self.ax1 = Axes1(self)
        self.add_sub_axes(self.ax1)

        # 存放处理好的数据
        self.data = []

        self.ax1_max_xaxis = 0

        self.min_text_win = MinTextWin(self)

    # 数据读取
    def data_iterators(self):
        file_name = sorted(os.listdir(self.file_path))
        file_path = map(lambda x: os.path.join(self.file_path, x), file_name)
        for i in file_path:
            file_name = os.path.basename(i)
            data = self.get_json_data(i)
            yield data, file_name

    # 数据解析，放到self.data 中
    def parsed_data(self, data):
        if data is None:
            return
        data, file_name = data
        self.title_label = file_name
        for i in data:
            lane = {"dir": i["dir"], "num": i["num"], "lx": [], "ly": [], "rx": [], "ry": []}
            for pt in i["left_points"]:
                lane["lx"].append(pt["x"])
                lane["ly"].append(pt["y"])
            for pt in i["right_points"]:
                lane["rx"].append(pt["x"])
                lane["ry"].append(pt["y"])
            self.data.append(lane)

    # 在子图中添加要画的几何
    def draw_geometric_type(self):
        self.ax1.cla()

        for idx, i in enumerate(self.data):
            self.ax1_max_xaxis = max(max(i["lx"]), self.ax1_max_xaxis)

            l_line = Line2D(i["ly"], i["lx"], color=self.color[idx])
            l_line.set_gid("123")
            self.ax1.add_line(l_line)

            r_line = Line2D(i["ry"], i["rx"], color=self.color[idx])
            r_line.set_gid("124")
            self.ax1.add_line(r_line)

            dir_text_x = (i["ly"][0] + i["ry"][0]) / 2
            dir_text_y = (i["lx"][0] + i["lx"][-1]) / 2
            dir_text = self.ax1.text(dir_text_x, dir_text_y, i["dir"],
                                     color=self.color[idx])  # Use ax1.text to add text
            dir_text.set_gid("125")

            num_text = self.ax1.text(dir_text_x, dir_text_y - 5, i["num"],
                                     color=self.color[idx])  # Use ax1.text to add text
            num_text.set_gid("126")

        self.data.clear()

    # 处理画图的函数
    def with_function(self):
        self.continuous_draw(1)
        pass

    # 对元素的交互
    def on_pick(self, event):
        """

        event.mouseevent : 获取点击位置包括相对窗口位置和plt的图的位置，鼠标按钮编号，以及Axes对象

        event.artis : 获取被点击的元素

        event.ind or event.mouseevent.ind: 获取元素索引

        event.artist.get_gid() : 获取id
        """

    def on_pick_mouse_left(self, event):
        print("test.py")
        if isinstance(event.artist, Text):
            # 获取鼠标点击的坐标
            print()
            x, y = event.mouseevent.x, event.mouseevent.y
            self.min_text_win.creat_min_win_update_lane_text_box(x, y, event.artist.get_gid(), event.artist.get_text(),
                                                                 event.artist)

    def update_sub_data(self, artist: Artist, gid=None, new_data=""):
        if new_data == "":
            return False
        artist.set_text(new_data)
        self.repaint()
        return True

    # 对子图标签的设置
    def set_label(self):
        self.ax1.invert_xaxis()
        self.ax1.set_xticks(self.generate_range(end=(self.ax1_max_xaxis / 2), step=5)[::-1])
        self.ax1.set_title(self.title_label)

    def test_draggable(self, e):
        print("设备事件触发", e)


if __name__ == '__main__':
    # 实例化
    live_plot = TestMapShow()
    # 运行
    live_plot.run()

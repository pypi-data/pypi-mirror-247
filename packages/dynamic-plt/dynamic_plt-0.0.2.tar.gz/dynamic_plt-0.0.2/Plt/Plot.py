import sys
from typing import Any, Union

import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

from .Core import Window
from .Core import Utils
from .Core import PltDraggablePlot
from .Core import Axes


class Plt(ABC, Window, Utils):
    def __init__(self,
                 window_size=(8, 6),
                 is_dynamic_drawing=False,
                 is_interact_with=False,
                 ):
        """
        :param window_size: 窗口大小
        :param is_dynamic_drawing: 是否自动滚动显示
        :param is_interact_with: 是否交互
        """
        super().__init__(window_size=(window_size[0] * 100, (6 if window_size[1] < 6 else window_size[1]) * 100))
        self.window_size = window_size
        self.event = PltDraggablePlot(self)

        self.__is_dynamic_drawing = is_dynamic_drawing
        self.__is_interact_with = is_interact_with
        self.__fig_ax = []
        self.__interact_ax = []
        self.__fig = plt.figure()
        self.__ax = Axes
        self.__is_close_win = False
        self.__iter = None
        self.__timer_id = None
        self.__is_pause = False
        self.__data = []
        self.__ion_index = 0
        self.__draw_pause_interval = 0.01
        self.__sleep_interval = 0.01
        self.__is_data_iterators = False
        self.__dyn_subplt = []

        self.canvas = self.plt_add_tk(self.__fig)
        self.__init_fig()

    def __bind_event(self):
        """
        绑定事件
        :return:
        """
        self.mpl_connect("key_press_event", self.__on_key_press_event)
        self.mpl_connect("button_press_event", self.event.on_press)
        self.mpl_connect('button_release_event', self.event.on_release)
        self.mpl_connect('motion_notify_event', self.event.on_motion)
        self.mpl_connect('scroll_event', self.event.on_scroll)
        self.mpl_connect('axes_leave_event', self.event.on_leave)
        if self.__is_interact_with:
            self.mpl_connect('pick_event', self.on_pick)

    def add_sub_axes(self, ax: Axes = None, *args, **kwargs) -> Axes:
        """
        :param ax: 子图
        :param kwargs
            1. is_dynamic_drawing : 是否自动滚动显示
            2. is_interact_with : 是否交互
            3. rect : 子图窗口的参数 tuple (left, bottom, width, height)
        :return: Axes
        """
        if ax is None:
            rect = kwargs.pop('rect') if 'rect' in kwargs else (0.1, 0.1, 0.8, 0.8)
            ax = Axes(self, fig=self.__fig, rect=rect, *args, **kwargs)

        self.__fig.add_axes(ax)
        if ax.is_dynamic_drawing:
            self.__dyn_subplt.append(ax)
        if self.__is_interact_with and ax.is_interact_with:
            self.__interact_ax.append(ax)
        self.__fig_ax.append((self.__fig, ax))
        self.set_ax(ax)
        return ax

    def get_is_pause(self):
        """
        :return: 是否暂停
        """
        return self.__is_pause

    def set_ax(self, ax: Axes):
        """
        :param ax: Axes
        :return:
        """
        self.__ax = ax

    def get_fig(self):
        """
        :return: figure
        """
        return self.__fig

    def __init_fig(self):
        self.set_plt_window_size()
        self.__bind_event()

        if hasattr(self, "data_iterators"):
            self.__iter = self.data_iterators()
            self.__is_data_iterators = hasattr(self.__iter, "__iter__") or hasattr(self.__iter, "__getitem__")

        if self.__is_data_iterators:
            try:
                self.__data.append(next(self.__iter))
            except StopIteration:
                raise StopIteration(
                        Exception(f'{self.__class__.__name__} member function "data_iterators" is not an iterator.'))

    def set_plt_window_size(self, window_size: any = None):
        if window_size is not None:
            self.window_size = window_size
        self.__fig.set_size_inches(self.window_size[0], self.window_size[1])

    def __key_control_dynamic_drawing(self):
        self.__clear_dyn_subplt()
        self.draw_geometric_type()
        self.set_label()
        self.canvas.draw()

    def __next_data(self, event=None):
        self.__start_dynamic_draw()
        if event is None:
            return

    def __last_data(self, event=None):
        if self.__ion_index > 1:
            self.__ion_index -= 2
            self.__start_dynamic_draw()
        if event is None:
            return

    def __start_dynamic_draw(self):
        data = None
        if self.__ion_index < len(self.__data) - 1:
            self.__ion_index += 1
            data = self.__data[self.__ion_index]
        else:
            if self.__is_data_iterators:
                try:
                    data = next(self.__iter)
                except StopIteration:
                    return False
                self.update_data(data)
        if data:
            self.__subclassfuncs(data)
            return True
        return False

    def __dynamic_drawing_event(self, event):
        if not self.__is_dynamic_drawing:
            return
        self.__is_pause = not self.__is_pause
        if not self.__is_pause:
            self.__start_timer(self.__sleep_interval)

    def __start_timer(self, sleep_interval):
        self.__sleep_interval = sleep_interval
        self.__timer_id = self.start_timer(self.__start_continuous_draw, self.__sleep_interval)

    def __start_continuous_draw(self):
        if self.win_close:
            return
        if not self.__is_dynamic_drawing:
            self.stop_timer(self.__timer_id)
            raise ValueError(Exception("Please set 'is_dynamic_drawing' to true."))
        if self.__is_dynamic_drawing:
            if self.root.state() != "normal":
                self.__timer_id = self.start_timer(self.__start_continuous_draw, self.__sleep_interval)
                return
            if self.__is_close_win or self.__is_pause:
                return
            if self.__start_dynamic_draw():
                self.__timer_id = self.start_timer(self.__start_continuous_draw, self.__sleep_interval)
        else:
            self.__start_dynamic_draw()

    def repaint(self):
        self.canvas.draw()

    def __subclassfuncs(self, data):
        self.parsed_data(data)
        self.__key_control_dynamic_drawing()

    def __clear_dyn_subplt(self):
        for i in self.__dyn_subplt:
            i.cla()

    def continuous_draw(self, sleep_interval=1):
        """
        动态画图方法
        :param sleep_interval: 间隔时间, 单位: S
        :return:
        """
        self.__ion_index = 0
        self.__start_timer(sleep_interval)

    def draw(self):
        if not self.__data:
            raise ValueError(Exception("Please use 'self.update_data' method to add test_data!"))
        data = self.__data[0]
        if data:
            self.__subclassfuncs(data)

    def update_data(self, data):
        self.__data.append(data)
        self.__ion_index = len(self.__data) - 1

    def show(self, **kwargs):
        self.with_function()
        if self.__data:
            super().show()

    def on_window_resize(self, event):
        self.canvas.draw()

    def __dynamic_draw(self):
        self.show()

    def __draw(self):
        self.show()

    def run(self):
        if self.__is_dynamic_drawing:
            self.__dynamic_draw()
        else:
            self.__draw()

    def __on_key_press_event(self, event):
        if event.key == " ":
            self.__dynamic_drawing_event(event)
        elif event.key == "right" or event.key == "down":
            if self.__is_dynamic_drawing and not self.__is_pause:
                return
            self.__next_data(event)
        elif event.key == "left" or event.key == "up":
            if self.__is_dynamic_drawing and not self.__is_pause:
                return
            self.__last_data(event)
        self.event.on_key(event)

    def mpl_connect(self, s: str, obj: Union):
        """
        注册设备类
        :param s: str
            - 'key_mouse_event' : 注册设备事件类
            - 'key_press_event' : 键盘按键按下事件
            - 'key_release_event' : 键盘按键抬起事件
            - 'button_press_event' : 鼠标按键按下事件
            - 'button_release_event' : 鼠标按键抬起事件
            - 'motion_notify_event' : 鼠标移动事件
            - 'scroll_event' : 鼠标滚轮事件
            - 'draw_event' : 画图的事件
            - 'pick_event' ： 鼠标拾取事件
            - 'resize_event' ： plt图大小变化事件
            - 'figure_enter_event' ： 鼠标进入事件
            - 'figure_leave_event' ： 鼠标离开事件
            - 'axes_enter_event' ： 坐标轴对象上鼠标进入事件
            - 'axes_leave_event' ： 坐标轴对象上鼠标离开事件

        :param obj: 类或func
        :return:
        """

        # 关闭事件不可使用
        if s == "close_event":
            return

        if s == "key_mouse_event":
            self.event = obj(self)
            return
        else:
            return self.__fig.canvas.mpl_connect(s, obj)

    def get_data(self, index: int = None) -> Any:
        """
        获取指定位置的数据，默认获取当前帧数据
        :param index: 数据索引
        :return:
        """
        if index:
            return self.__data[index]
        return self.__data[self.__ion_index]

    def get_next_data(self) -> Any:
        """
        获取下一帧数据
        :return:
        """
        if self.__ion_index < len(self.__data) - 1:
            return self.__data[self.__ion_index + 1]

    def get_last_data(self) -> Any:
        """
        获取上一帧数据
        :return:
        """
        if self.__ion_index > 0:
            return self.__data[self.__ion_index - 1]

    # 画下一帧
    def draw_next(self):
        """
        画下一帧
        :return:
        """
        if self.__is_dynamic_drawing and not self.__is_pause:
            return
        self.__next_data()

    # 画上一帧
    def draw_last(self):
        """
        画上一帧
        :return:
        """
        if self.__is_dynamic_drawing and not self.__is_pause:
            return
        self.__last_data()

    def on_win_closing(self):
        super().on_win_closing()
        plt.close()
        sys.exit(0)

    @abstractmethod
    def data_iterators(self):
        """
        获取数据处理
        数据处理，处理成自己想要的结构，供self.parsed_data()解析使用\n
        数据少-->调用update_data\n
        数据多-->写成yield迭代器\n
        :return: None
        """

    @abstractmethod
    def draw_geometric_type(self) -> [Axes]:
        """
        添加要绘制的元素对象
        :return: None
        """

    @abstractmethod
    def with_function(self):
        """
        self.continuous_draw -> 连续绘制方法\n
        self.draw -> 绘制一次方法
        :return: None
        """

    @abstractmethod
    def parsed_data(self, data):
        """
        解析数据
        解析要画的几何图形的数据
        :param data:
        :return: None
        """

    @abstractmethod
    def on_pick(self, el):
        """
        元素交互事件触发函数，参数使用参考：https://matplotlib.org/3.8.1/users/explain/figure/event_handling.html#event-handling-and-picking
        :param el: 触发的事件的元素
        :return: None
        """

    @abstractmethod
    def set_label(self):
        """
         设置图例的标签
        :return: None
        """
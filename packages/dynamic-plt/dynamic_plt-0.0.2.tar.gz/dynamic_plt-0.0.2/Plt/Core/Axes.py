from typing import Union, Callable

from matplotlib.backend_bases import PickEvent
from matplotlib.axes import Axes as _Axes

from . import AxesDraggablePlot


class Axes(_Axes):
    """
    Axes 类，继承自 matplotlib.axes.Axes，用于绘图。
       官方参考：https://matplotlib.org/3.8.1/api/figure_api.html#matplotlib.figure.Figure.add_axes
    """

    def __init__(self, plt, *args, **kwargs):
        """
        :param plt: Plt 对象
        :param kwargs:
            fig :  父图
            rect : 位置
            is_interact_with : 是否交互
            is_dynamic_drawing : 是否动态绘制
        """
        self.plt = plt
        self.__fig = None
        self.__rect = None
        self.event = AxesDraggablePlot(self)
        self.is_interact_with = False
        self.is_dynamic_drawing = False
        self.kwargs = kwargs
        self.args = args

        self.init()
        super().__init__(self.__fig, self.__rect, *args, **kwargs)

    def init(self):
        """
        初始化
        :return:
        """
        if "fig" in self.kwargs:
            self.__fig = self.kwargs.pop("fig")
        if "rect" in self.kwargs:
            self.__rect = self.kwargs.pop("rect")
        if "is_interact_with" in self.kwargs:
            self.is_interact_with = self.kwargs.pop("is_interact_with")
        if "is_dynamic_drawing" in self.kwargs:
            self.is_dynamic_drawing = self.kwargs.pop("is_dynamic_drawing")

        if self.__fig is None:
            self.__fig = self.plt.get_fig()

        self.__bind_event()

    def __bind_event(self):
        """
        绑定事件
        :return:
        """
        self.mpl_connect("button_press_event", self.event.on_press)
        self.mpl_connect('button_release_event', self.event.on_release)
        self.mpl_connect('motion_notify_event', self.event.on_motion)
        self.mpl_connect('scroll_event', self.event.on_scroll)
        self.mpl_connect('axes_leave_event', self.event.on_leave)

        if self.is_interact_with:
            self.mpl_connect('pick_event', self.event.on_pick)

    def __set_all_el_picker(self):
        """
        设置所有元素可拾取
        :return:
        """
        if not self.is_interact_with:
            return
        all_el = self.get_children()
        for i in all_el:
            i.set_picker(True)

    def event_func(self, event, func):
        """
        :param event: 触发事件
        :param func: 事件回调函数
        :return:
        """

        inaxes = None
        if hasattr(event, "inaxes"):
            inaxes = event.inaxes
        if inaxes is None and hasattr(event, "artist") and hasattr(event.artist, "axes"):
            inaxes = event.artist.axes
        if inaxes is None:
            return
        if inaxes == self:
            func(event)

    def mpl_connect(self, s: str, obj: Union):
        """
        绑定事件
        :param s: 事件类型
        :param obj: 回调函数
        :return:
        """
        self.__fig.canvas.mpl_connect(s, lambda event: self.event_func(event, obj))

    def bind_pick(self, s, callback: Callable):
        """
        绑定元素交互事件
        :param s: 事件类型
        :param callback: 回调函数
        :return:
        """
        if s not in self.event.event:
            raise Exception("Event type error: %s" % s)
        self.event.add_pick_event(s, callback)

    def draw(self, renderer=None):
        super().draw(renderer)
        self.__set_all_el_picker()
import time
from typing import Callable

from matplotlib.backend_bases import PickEvent

from .Window import Window


class AxesDraggablePlot:
    event = [
        "on_pick_mouse_scroll",
        "on_pick_mouse_left",
        "on_pick_mouse_right",
        "on_pick_mouse_left_double",
        "on_pick_mouse_right_double",
        "on_pick_mouse"
    ]
    """
    event : 它们表示图中元素与鼠标事件关联的事件处理程序的名称。这些事件处理程序将在用户与鼠标进行交互时被调用。
        on_pick_mouse_scroll：当用户使用鼠标滚轮时，触发该事件。
        on_pick_mouse_left：当用户按下鼠标左键时，触发该事件。
        on_pick_mouse_right：当用户按下鼠标右键时，触发该事件。
        on_pick_mouse_left_double : 当用户双击鼠标左键时，触发该事件。
        on_pick_mouse_right_double : 当用户双击鼠标右键时，触发该事件。
        on_pick_mouse : 当用户与鼠标进行交互时，触发该事件。
        您可以使用 ` self.bind_pick ` 绑定这是事件，以便在用户单击、释放或滚动鼠标时执行特定的操作。
    """

    def __init__(self, ax):
        """
        self.plt 可以操作plt实例化的成员
        :param ax: Axes
        """
        self.axes = ax
        self.plt = ax.plt
        self.__is_mouse_1_on_press = False
        self.__is_mouse_3_on_press = False
        self.__event = {}
        for et in AxesDraggablePlot.event:
            self.__event[et] = []

    def on_press(self, event):
        """
        鼠标按下事件
        :param event:
        :return:
        """
        ax = event.inaxes
        if ax is None:
            return
        if event.button == 1 or event.button == 3:
            self.plt.toolbar.press_pan(event)
            self.__is_mouse_1_on_press = True if event.button == 1 else self.__is_mouse_1_on_press
            self.__is_mouse_3_on_press = True if event.button == 3 else self.__is_mouse_3_on_press

    def on_release(self, event):
        """
        鼠标弹起事件
        :param event:
        :return:
        """
        ax = event.inaxes
        if ax is None:
            return
        if event.button == 1 or event.button == 3:
            self.plt.toolbar.release_pan(event)
            self.__is_mouse_1_on_press = False if event.button == 1 else self.__is_mouse_1_on_press
            self.__is_mouse_3_on_press = False if event.button == 3 else self.__is_mouse_3_on_press

    def on_motion(self, event):
        """
        鼠标移动事件
        :param event:
        :return:
        """
        ax = event.inaxes
        if ax is None:
            return
        if event.xdata is None and event.ydata is None:
            return

        self.move_subplt(event)

        self.update_ticks(event)

        time.sleep(0.1)

    def move_subplt(self, event):
        if not self.__is_mouse_1_on_press:
            return
        self.plt.toolbar.mouse_move(event)

    def update_ticks(self, event):
        if not self.__is_mouse_3_on_press:
            return
        self.plt.toolbar.mouse_move(event)

    @staticmethod
    def on_scroll(event):
        """
        鼠标滚轮事件
        :param event:
        :return:
        """
        ax = event.inaxes
        if ax is None:
            return
        if event.button == 'up':
            # 鼠标向上滚动，放大画面
            ax.set_xlim(ax.get_xlim()[0] * 0.9, ax.get_xlim()[1] * 0.9)
            ax.set_ylim(ax.get_ylim()[0] * 0.9, ax.get_ylim()[1] * 0.9)
        else:
            # 鼠标向下滚动，缩小画面
            ax.set_xlim(ax.get_xlim()[0] * 1.1, ax.get_xlim()[1] * 1.1)
            ax.set_ylim(ax.get_ylim()[0] * 1.1, ax.get_ylim()[1] * 1.1)
        ax.figure.canvas.draw()

    def on_leave(self, event):
        """
        鼠标离开事件
        :param event:
        :return:
        """
        self.__is_mouse_1_on_press = False
        self.__is_mouse_3_on_press = False

    def on_key(self, event):
        """
        键盘事件按键
        :param event:
        :return:
        """

    def on_pick(self, event):
        """
        :param event: 事件
        :return:
        """
        if self.axes.is_dynamically_drawn and not self.plt.get_is_pause():
            return
        if isinstance(event, PickEvent):
            self.__callback('on_pick_mouse', event)
            if event.mouseevent.button == 1:
                self.__callback('on_pick_mouse_left_double' if event.mouseevent.dblclick else 'on_pick_mouse_left',
                                event)
            elif event.mouseevent.button == 3:
                self.__callback('on_pick_mouse_right_double' if event.mouseevent.dblclick else 'on_pick_mouse_right',
                                event)
            elif event.mouseevent.button == 'down' or event.mouseevent.button == 'up':
                self.__callback('on_pick_mouse_scroll', event)

    def __callback(self, s, event):
        """
        执行回调函数
        :param s:
        :return:
        """
        if s not in self.__event:
            return
        for i in self.__event[s]:
            if not callable(i):
                continue
            if i.__code__.co_argcount > 0:
                i(event)
            else:
                i()

    def add_pick_event(self, s, callback: Callable):
        """
        添加鼠标点击事件
        :param s: 事件类型
        :param callback: 回调函数
        :return:
        """
        if s not in self.event:
            raise Exception("Event type error: %s" % s)
        self.__event[s].append(callback)

    def del_pick_event(self, s, callback=None):
        """
        删除鼠标点击事件
        :param s: 事件类型
        :param callback: 回调函数
        :return:
        """
        if s not in self.event:
            raise Exception("Event type error: %s" % s)
        if callback is None:
            self.__event = []
        else:
            self.__event.pop(callback)


class PltDraggablePlot:
    def __init__(self, plt_object: Window):
        """
        self.plt 可以操作plt实例化的成员
        :param plt_object: plt实例化对象
        """
        self.plt = plt_object

    def on_press(self, event):
        """
        鼠标按下事件
        :param event:
        :return:
        """

    def on_release(self, event):
        """
        鼠标弹起事件
        :param event:
        :return:
        """

    def on_motion(self, event):
        """
        鼠标移动事件
        :param event:
        :return:
        """

    @staticmethod
    def on_scroll(event):
        """
        鼠标滚轮事件
        :param event:
        :return:
        """

    def on_leave(self, event):
        """
        鼠标离开事件
        :param event:
        :return:
        """

    def on_key(self, event):
        """
        键盘事件按键
        :param event:
        :return:
        """

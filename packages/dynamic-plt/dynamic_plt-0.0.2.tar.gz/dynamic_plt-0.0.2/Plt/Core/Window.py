from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk as _NavigationToolbar2Tk
import tkinter as tk


class NavigationToolbar2Tk(_NavigationToolbar2Tk):
    toolitems = [t for t in _NavigationToolbar2Tk.toolitems if t[0] not in ('Pan', 'Zoom')]

    def __init__(self, canvas, window=None):
        super().__init__(canvas, window=window)


class Window(object):
    # 此列表包含可用'on_'格式的事件名称
    event = [
        'on_close',  # 当窗口被关闭时调用
        'on_key_press',  # 当键被按下时调用
        'on_key_release',  # 当键被释放时调用
        'on_mouse_press',  # 当鼠标按钮被按下时调用
        'on_mouse_release',  # 当鼠标按钮被释放时调用
        'on_mouse_motion',  # 当鼠标移动时调用
        'on_mouse_enter',  # 当鼠标进入窗口时调用
        'on_mouse_leave',  # 当鼠标离开窗口时调用
    ]

    # 初始化函数，设置窗口大小
    def __init__(self, window_size=(800, 600)):
        self.window_size = window_size
        self.root_width = window_size[0]
        self.root_height = window_size[1]
        self.root = tk.Tk()
        self.toolbar = None
        self.win_close = False
        self.start_timer(self.__window_init)
        self.init_window_style()
        self.mouse_x = 0
        self.mouse_y = 0
        self.__event = {}

    def init_window_style(self):
        """
        初始化窗口样式
        :return:
        """
        self.root.geometry(f"{self.root_width}x{self.root_height}")

    def __window_init(self):
        """
        窗口初始化
        :return:
        """
        if self.root.state() == "normal":
            self.root_event_registration()
            return
        self.start_timer(self.__window_init)

    def set_title(self, title="TK"):
        """
        设置窗口标题
        :param title
        :return:
        """
        self.root.title(title)

    def start_timer(self, func, time_ms=1.0):
        """
        启动定时器
        :param func:
        :param time_ms:
        :return:
        """
        return self.root.after(int(time_ms * 1000), func)

    def stop_timer(self, timer_id):
        """
        停止定时器
        :param timer_id:
        :return:
        """
        self.root.after_cancel(timer_id)

    def show(self):
        """
        显示窗口
        :return:
        """
        self.root.mainloop()

    def on_window_resize(self, event):
        """
        窗口大小改变事件
        :param event:
        :return:
        """

    def on_mouse_move(self, event):
        """
        鼠标移动事件
        :param event:
        :return:
        """
        self.mouse_x = event.x
        self.mouse_y = event.y

    def on_mouse_left_click(self, event):
        """
        鼠标左键按下事件
        :param event:
        :return:
        """
        self.mouse_x = event.x
        self.mouse_y = event.y

    def on_mouse_press(self, event):
        """
        鼠标按下事件
        :param event:
        :return:
        """
        if event.num == 1:
            self.on_mouse_left_click(event)

    def on_mouse_release(self, event):
        """
        鼠标释放事件
        :param event:
        :return:
        """

    def root_event_registration(self):
        """
        窗口事件注册
        :return:
        """
        self.root.bind("<Configure>", self.on_window_resize)
        self.root.protocol("WM_DELETE_WINDOW", self.on_win_closing)
        self.root.bind("<Motion>", self.on_mouse_move)
        self.root.bind("<Button>", self.on_mouse_press)
        self.root.bind("<ButtonRelease>", self.on_mouse_release)

    def on_win_closing(self):
        """
        窗口关闭事件
        :return:
        """
        self.win_close = True
        self.root.destroy()

    def plt_add_tk(self, __fig) -> FigureCanvasTkAgg:
        """
        添加tk
        :param __fig:
        :return:
        """
        canvas = FigureCanvasTkAgg(__fig, master=self.root)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # 创建Matplotlib的导航工具栏
        self.toolbar = NavigationToolbar2Tk(canvas, self.root)
        self.toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        return canvas

    def get_all_widgets(self, root=None):
        """
        获取所有控件
        :param root:
        :return:
        """
        if root is None:
            root = self.root
        widgets = []

        def recursive_get_widgets(parent):
            for widget in parent.winfo_children():
                widgets.append(widget)
                if isinstance(widget, tk.Toplevel):
                    recursive_get_widgets(widget)

        recursive_get_widgets(root)
        return widgets

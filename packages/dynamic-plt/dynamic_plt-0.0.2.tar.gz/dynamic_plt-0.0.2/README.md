# 类说明

## Plt 类说明

Plt 类是基于matplotlib二次封装的。

主要功能有通过鼠标键盘控制显示，绑定事件

### 参数说明

``window_size``: 窗口大小  
``is_dynamic_drawing``: 滚动显示
``is_interact_with``: 元素交互

### 成员变量说明

``canvas``:  画布

### 成员函数说明

#### ``add_sub_axes``:  添加子图

      add_sub_axes(ax: Axes = None, *args, **kwargs) -> Axes:

| 参数     | 说明                                                                                                    |
|--------|-------------------------------------------------------------------------------------------------------|
| ax     | Aexes对象。默认None，自动创建                                                                                   |
| kwargs | 参数:<br />       rect 子图位置<br />       is_dynamic_drawing 是否自动滚动显示<br />       is_interact_with 是否允许交互 |



#### ``get_is_pause``: 动态画图状态

      get_is_pause():



#### ``set_ax``: 设置当前处理的axes

      set_ax(ax: Axes):

| 参数    | 说明     |
|-------|--------|
| ax| Axes对象 |



#### 

``get_data``: 获取指定位置的数据，默认获取当前帧数据

| 参数    | 说明 |
|-------|----|
| index | 索引 |  

``get_next_data``: 获取下帧数

``get_last_data``: 获取上一帧数据

``add_sub_axes``: 添加子图

| 参数                   | 说明                                          |
|----------------------|---------------------------------------------|
| is_dynamically_drawn | 是否为动态更新的子图                                  |
| rect                 | 子图的位置和大小tuple (left, bottom, width, height) |

``update_data`` : 添加数据到数据中心

``mpl_connect``: plt的事件绑定方法

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

``continuous_draw``: 动态画图方法

| 参数             | 说明            |
|----------------|---------------|
| sleep_interval | 动态画图事件间隔，默认1s |

``draw``: 静态画图方法

``show``: 运行窗口

``data_iterators``:  获取数据

``parsed_data``:   解析数据

| 参数   | 说明                                   |
|------|--------------------------------------|
| data | 数据中心传进来的数据 ``data_iterators``返回的数据结构 |

``draw_geometric_type``:  添加要绘制的元素对象

``with_function``:  画图方法

    continuous_draw和draw调用一个

``on_pick``:    元素交互事件触发函数

    -参考：https://matplotlib.org/3.8.1/users/explain/figure/event_handling.html#event-handling-and-picking

### 窗口扩展

可以使用tkinter对窗口扩展。

``root``: 主窗口对象

## 例子

1. 必须继承Plt类
2. 必须重写一下函数
    1. ``data_iterators``:  获取数据处理
    2. ``parsed_data``:   解析数据
    3. ``draw_geometric_type``:  添加要绘制的元素对象
    4. ``with_function``:  画图方法
    5. ``on_pick``:    元素交互事件触发函数

```python3
from Plt.Plot import Plt, DraggablePlot
import os
import random
from Plt.Core.Color import random_color_array

# 随机获取颜色
color_set = random_color_array(50, "hex")


# 使用交互事件必须继承 DraggablePlot 类
class TestDraggablePlot(DraggablePlot):

    # 使用鼠标按下事件，需要重写此方法，并且调用基类方法
    def on_press(self, event):
        super().on_press(event)
        self.plt.test_draggable()

    # 使用鼠标弹起事件，需要重写此方法，并且调用基类方法
    def on_release(self, event):
        super().on_release(event)

    # 使用鼠标滑轮事件，需要重写此方法，并且调用基类方法
    def on_scroll(self, event):
        super().on_scroll(event)

    # 使用键盘按键事件，需要重写此方法，并且调用基类方法
    def on_key(self, event):
        super().on_key(event)


class TestMapShow(Plt):
    def __init__(self):
        super().__init__(window_size=(8, 4), is_dynamic_drawing=False, is_interact_with=False)
        # 添加子图
        left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
        self.ax1 = self.add_sub_axes(True, [left, bottom, width, height])

        # 存放处理好的数据
        self.data = []

        # 绑定设备触发类
        self.mpl_connect("key_mouse_event", TestDraggablePlot)

    def data_iterators(self):
        # 文件目录
        file_path = os.path.join(os.path.dirname(__file__), "test/test_data")
        # 排序
        file_name = sorted(os.listdir(file_path))
        # 路径拼接
        file_path = map(lambda x: os.path.join(file_path, x), file_name)

        for i in file_path:
            # 获取文件名
            file_name = os.path.basename(i)
            # 读取文件
            data = self.get_json_data(i)
            # 迭代器返回数据
            yield data, file_name

    def parsed_data(self, data):
        # 判断是否有数据
        if data is not None:
            return
        # 解析数据
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
        for idx, i in enumerate(self.data):
            self.ax1_max_xaxis = max(max(i["lx"]), self.ax1_max_xaxis)
            self.ax1.plot(i["ly"], i["lx"], color=color_set[idx])
            self.ax1.plot(i["ry"], i["rx"], color=color_set[idx])
            dir_text_x = (i["ly"][0] + i["ry"][0]) / 2
            dir_text_y = (i["lx"][0] + i["lx"][-1]) / 2
            self.ax1.text(dir_text_x, dir_text_y, i["dir"], color=color_set[idx])
            self.ax1.text(dir_text_x, dir_text_y - 5, i["num"], color=color_set[idx])
        # 动态画图一直要记得清理数据
        self.data.clear()

    # 处理画图的函数
    def with_function(self):
        self.continuous_draw(1)
        pass

    # 对元素的交互
    def on_pick(self, event):
        # 改变颜色
        event.artist.set_color(random.choice(color_set))

    # 设置图例的标签
    def set_label(self):
        self.ax1.invert_xaxis()
        self.ax1.set_xticks(self.generate_range(end=(self.ax1_max_xaxis / 2), step=5)[::-1])
        self.ax1.set_title(self.title_label)

    def test_draggable(self):
        print("被触发啦")


if __name__ == '__main__':
    # 实例化
    live_plot = TestMapShow()
    # 运行
    live_plot.run()


```
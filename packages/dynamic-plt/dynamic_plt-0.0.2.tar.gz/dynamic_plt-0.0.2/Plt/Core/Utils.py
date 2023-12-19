import os
import time
import json


class Utils:
    @staticmethod
    def generate_range(start: int or float = 0, end: int or float = 100, step: int or float = 1) -> [int or float]:
        """
        生成一个包含正向和反向范围的数组
        :param start: 开始位置
        :param end: 结束位置
        :param step: 步长
        :return:
        """
        start = int(start)
        end = int(end) + 1
        step = int(step)
        forward_range = list(range(start, end, step))
        backward_range = list(range(start, -end, -step))
        return forward_range + backward_range

    @staticmethod
    def get_json_data(path: str) -> dict:
        """
        读取json文件
        :param path: json文件路径
        :return:
        """
        if not os.path.exists(path):
            return {}
        with open(path, 'r') as file:
            return json.load(file)

    @staticmethod
    def __time_sleep(sleep_interval):
        """
        睡眠
        :param sleep_interval: 睡眠时间
        :return:
        """
        while sleep_interval > 0:
            time.sleep(0.001)
            sleep_interval -= 0.001

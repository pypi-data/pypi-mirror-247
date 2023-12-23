from collections.abc import Iterable
import math, sys, time


class multi_sub_progress:
    """
    控制台的进度条
    """

    def __init__(self):
        """
        初始化函数
        """
        self._iter_stack = []
        self._print_str = ""
        self._print_logs = []

    def iter_bar(self, iter_item, value=0, key=None, max=None):
        """
        进度条的遍历方法
        :param iter_item: 主遍历对象
        :param value: value起始
        :param key: 遍历名称
        :param max: 遍历的数量
        :return: 可遍历对象
        """

        def get_length(iter_item):
            if isinstance(iter_item, Iterable):
                try:
                    return len(iter_item)
                except TypeError:
                    # 'iter_item' is an iterable but doesn't have a __len__ method.
                    # It could be something like an infinite generator.
                    raise Exception("该对象为无限长度的可迭代对象")
            else:
                raise Exception("需要指定max值")

        if max is None:
            max = get_length(iter_item)

        self.start(key, max, value)
        for _iter in iter_item:
            yield _iter
            self.one_done()

        self.stop_current()

    def start(self, key, max, value=0):
        if key is None:
            key = f"Iter {len(self._iter_stack)}"
        self._iter_stack.append({
            'key': key,
            'value': value,
            'max': max,
            'start': time.time(),
            'avg_cost': 0,
            'plus_cost': 0
        })

    def set_value(self, v):
        self._iter_stack[-1]['value'] = v

        if self._iter_stack[-1]['value'] != 0:
            avg_cost = (time.time() - self._iter_stack[-1]['start']) / self._iter_stack[-1]['value']
            sur_plus = avg_cost * (self._iter_stack[-1]['max'] - self._iter_stack[-1]['value'])
            self._iter_stack[-1]['avg_cost'] = avg_cost
            self._iter_stack[-1]['plus_cost'] = sur_plus
        else:
            self._iter_stack[-1]['avg_cost'] = 0
            self._iter_stack[-1]['plus_cost'] = 0

        self._flush_()

    def one_done(self):
        self.set_value(self._iter_stack[-1]['value'] + 1)

    def stop_current(self):
        self._iter_stack.pop(-1)

    # def update_process_value(self, v):
    #     """
    #     强制更新进度条的进度数值
    #     :param v: 要更新的数值
    #     :return: 无返回
    #     """
    #     self._iter_stack[-1]['value'] = v

    def process_print(self, str):
        """
        打印过程中的状态信息（覆盖输出）
        :param str: 状态信息
        :return: 无返回
        """
        self._print_str = str

    def print_log(self, str):
        """
        过程中打印log（不覆盖，使用换行）
        :param str: 状态信息
        :return: 无返回
        """
        self._print_logs.append(str + "\n")


class multi_progress_web:
    def __init__(self):
        self.all_bars = {}

    def get_new_bar(self, name):
        self.all_bars[name] = multi_sub_progress()
        return self.all_bars[name]

    def get_all_value(self):
        pass

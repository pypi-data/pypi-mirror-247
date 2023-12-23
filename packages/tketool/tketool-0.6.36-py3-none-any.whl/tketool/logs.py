import logging, sys
from enum import Enum
from prettytable import PrettyTable, ALL


class Custom_Handler(logging.Handler):

    def __init__(self):
        super().__init__()
        self.in_processbar = False

    def emit(self, record):

        if record.levelno == 60:
            rp_msg = record.msg.replace("\n", "")
            if self.in_processbar:
                sys.stdout.write('\r')
                sys.stdout.write(rp_msg)
                sys.stdout.flush()
            else:
                sys.stdout.write('\n')
                sys.stdout.write(rp_msg)
                sys.stdout.flush()
            self.in_processbar = True
        elif record.levelno == 61:
            if self.in_processbar:
                sys.stdout.write('\r')
                sys.stdout.write(record.msg)
                sys.stdout.flush()
            else:
                sys.stdout.write('\n')
                sys.stdout.write(record.msg)
                sys.stdout.flush()
            self.in_processbar = False
        else:
            rp_msg = record.msg.replace("\n", "")
            if self.in_processbar:
                sys.stdout.write('\r')
                sys.stdout.write(rp_msg)
                sys.stdout.flush()
            else:
                sys.stdout.write('\n')
                sys.stdout.write(rp_msg)
                sys.stdout.flush()
            self.in_processbar = False

        pass


logging.addLevelName(60, "process_bar")
logging.addLevelName(61, "multirow")
current_handle = Custom_Handler()
current_logger = logging.getLogger("tke_main")
current_logger.setLevel(logging.DEBUG)


def set_logger(target_logger):
    for handler in target_logger.handlers[:]:
        target_logger.removeHandler(handler)
    target_logger.addHandler(current_handle)


set_logger(current_logger)


def log(str):
    global current_logger
    current_logger.info(str)
    # print(f"{str}\n")  # Using \033[0m to reset the color after printing


def log_multi_row(str):
    global current_logger
    current_logger.log(61, str)


class log_color_enum(Enum):
    DEFAULT = ""
    RED = "\033[91m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"


def convert_print_color(*args):
    """
    函数返回带有指定颜色的字符串。

    :param args: 可变数量的参数，每个参数可以是字符串或一个包含字符串和log_color_enum的元组。
    :return: 拼接好的带有颜色代码的字符串
    """
    result = []

    for arg in args:
        if isinstance(arg, tuple) and len(arg) == 2 and isinstance(arg[1], log_color_enum):
            # 元组包含字符串和颜色枚举
            result.append(f"{arg[1].value}{arg[0]}\033[0m")
        else:
            # 只有字符串
            result.append(arg)

    return ''.join(result)


def _truncate_content(content, max_length):
    return (content[:max_length] + '..') if len(content) > max_length else content


def print_table(table_col: [str], rows: [[str]], truncate_string=30):
    xtable = PrettyTable()
    xtable.field_names = table_col
    for _r in rows:
        if truncate_string is not None:
            xtable.add_row([_truncate_content(rr) for rr in _r])
        else:
            xtable.add_row(_r)
    log_multi_row(str(xtable))

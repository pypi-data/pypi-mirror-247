# by kejiang v1101
from enum import Enum
import time, abc
import functools


class plugin_invoke_Enum(Enum):
    Never = 0
    Epoch_begin = 1
    Epoch_end = 2
    Batch_begin = 3
    Batch_end = 4
    Begin = 5
    End = 6
    After_Backward = 7
    Update = 8


class device_use_enum(Enum):
    Auto = 1
    CPU = 2


class dtype_enum(Enum):
    Auto = 1
    Float16 = 2
    Float32 = 3


class update_mode_enum(Enum):
    Per_Step = 1,
    Per_Epoch = 2,


class global_state_board():
    def __init__(self, train_obj, epoch_count, sample_set, pb, input_convert_func, label_convert_func):
        self.trainer_type_name = type(train_obj).__name__
        self.trainer = train_obj
        self.model = train_obj.model
        self.loss_obj = train_obj.loss
        self.optimizer = train_obj.optimizer
        self.model_folder = train_obj.out_folder
        self.epoch_count = epoch_count
        self.sample_set = sample_set
        self.update_mode = train_obj.update_mode
        self.progress_bar = pb
        self.input_convert_func = input_convert_func
        self.label_convert_func = label_convert_func

        self.batch_count = sample_set.count()

        self.update_parameter_count = -1

        self.log_stack = []
        self.parameter_update_times = 0

        self.plugin_datas = {}
        self.step = 0

    def log(self, lg_s):
        self.log_stack.append(lg_s)


class epoch_state_board():
    def __init__(self, epoch_idx):
        self.epoch_idx = epoch_idx
        self.epoch_loss = 0
        self.start_time = time.time()
        self.end_time = 0

        self.plugin_datas = {}


class step_state_board():
    def __init__(self, batch_idx, batch_item, global_state: global_state_board):
        self.batch_idx = batch_idx
        self.ori_item = batch_item
        self.start_time = time.time()
        self.end_time = 0
        self.converted_input = global_state.input_convert_func(batch_item)
        self.converted_label = global_state.label_convert_func(batch_item)
        self.logit = []
        self.loss_value = 0.0
        self.loss_tensor = None
        self.plugin_datas = {}


def invoke_at(types: [plugin_invoke_Enum]):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper._invoke_at = types
        return wrapper

    return decorator


class trainer_plugin_base(metaclass=abc.ABCMeta):

    def get_plugin_map(self) -> {}:
        run_dict = {}
        for name in dir(self):
            method = getattr(self, name)
            if hasattr(method, '_invoke_at'):
                for enum in method._invoke_at:
                    # 将每个enum和对应的方法添加到run_dict中
                    if enum not in run_dict:
                        run_dict[enum] = []
                    run_dict[enum].append(method)

        return run_dict

    @abc.abstractmethod
    def Invoke(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        pass

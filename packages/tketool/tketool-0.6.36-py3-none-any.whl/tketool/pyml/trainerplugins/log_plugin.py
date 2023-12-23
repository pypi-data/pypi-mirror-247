from tketool.pyml.pytrainer import *
from tketool.pyml.trainbase import *
import os, pickle
from tketool.logs import log


class log_plugin(trainer_plugin_base):
    def Invoke(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        pass

    def _log(self, content):
        log(content)
        # 打开文件，如果文件不存在，则创建
        with open(self.save_file, "a") as log_file:  # 'a' 表示 append mode，即增量方式
            log_file.write(content + "\n")

    def _log_stackcontent(self, global_state: global_state_board):
        for message in global_state.log_stack:
            self._log(message)
        global_state.log_stack.clear()

    @invoke_at([plugin_invoke_Enum.Begin])
    def start(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        self.save_file = os.path.join(global_state.model_folder, "log.txt")

    @invoke_at([plugin_invoke_Enum.End])
    def end(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        self._log_stackcontent(global_state)

    @invoke_at([plugin_invoke_Enum.Epoch_begin])
    def epoch_begin(self, global_state: global_state_board, epoch_state: epoch_state_board,
                    step_state: step_state_board):
        self._log_stackcontent(global_state)

    @invoke_at([plugin_invoke_Enum.Epoch_end])
    def epoch_end(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        if self.show_in_epoch:
            pb = global_state.progress_bar  # base_wall["pb"]
            epoch = epoch_state.epoch_idx  # epoch_wall['current_epoch_idx']
            loss = epoch_state.epoch_loss  # epoch_wall['epoch_loss']
            self._log(f"Epoch [{epoch + 1}], Total Loss: {loss:.4f}")
        self._log_stackcontent(global_state)

    @invoke_at([plugin_invoke_Enum.Batch_begin])
    def batch_begin(self, global_state: global_state_board, epoch_state: epoch_state_board,
                    step_state: step_state_board):
        self._log_stackcontent(global_state)

    @invoke_at([plugin_invoke_Enum.Batch_end])
    def batch_end(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        if self.show_in_batch:
            pb = global_state.progress_bar  # base_wall["pb"]
            batch = step_state.batch_idx
            loss = step_state.loss_value  # epoch_wall['epoch_loss']
            self._log(f"Batch [{batch + 1}], Total Loss: {loss:.4f}")
        self._log_stackcontent(global_state)

    def __init__(self, show_in_batch=False, show_in_epoch=True):
        self.save_file = None
        self.show_in_batch = show_in_batch
        self.show_in_epoch = show_in_epoch

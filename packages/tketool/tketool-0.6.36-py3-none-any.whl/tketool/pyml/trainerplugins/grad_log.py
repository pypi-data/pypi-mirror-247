from tketool.pyml.pytrainer import *
import os, pickle


class grad_log(trainer_plugin_base):

    @invoke_at([plugin_invoke_Enum.Batch_end])
    def Invoke(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        for group in global_state.optimizer.param_groups:
            for param_tensor in group['params']:
                for name, param_model in global_state.model.named_parameters():
                    if param_tensor is param_model:
                        log_str = (f"name: {name} ({param_tensor.data.shape}): "
                                   f"value: [{param_tensor.data.min().item()}, {param_tensor.data.max().item()}] "
                                   f"grad: [{param_tensor.grad.min().item() if param_tensor.grad is not None else 0}, "
                                   f"{param_tensor.grad.max().item() if param_tensor.grad is not None else 0}]")
                        global_state.log_stack.append(log_str)

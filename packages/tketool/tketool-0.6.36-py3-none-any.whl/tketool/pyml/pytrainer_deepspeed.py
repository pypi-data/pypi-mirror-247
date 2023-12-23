from tketool.pyml.pytrainer import *
import argparse, deepspeed
from deepspeed.utils import logger as ds_logger
from tketool.logs import set_logger

set_logger(ds_logger)


class pytrainer_deepspeed(pymodel_trainer):
    def __init__(self, model: torch.nn.Module, loss_obj,
                 **kwargs):
        super().__init__(model, loss_obj, **kwargs)
        self.model_engine = None

    @invoke_at([plugin_invoke_Enum.Batch_begin])
    def _drive_batch_data(self, global_state: global_state_board, epoch_state: epoch_state_board,
                          step_state: step_state_board):
        def move_to_drive(tensor_or_dict):
            if isinstance(tensor_or_dict, dict):
                return {k: v.to(self.model_engine.local_rank) for k, v in tensor_or_dict.items()}

            else:
                return tensor_or_dict.to(self.model_engine.local_rank)

        step_state.converted_input = move_to_drive(step_state.converted_input)
        step_state.converted_label = move_to_drive(step_state.converted_label)

    @invoke_at([plugin_invoke_Enum.Begin])
    def init_deepspeed(self, global_state: global_state_board, epoch_state: epoch_state_board,
                       step_state: step_state_board):
        deepspeed_config = {
            "fp16": {
                "enabled": True
            },
            "train_batch_size": 3,
            "zero_optimization": {
                "stage": 2,
                "allgather_partitions": True,
                "reduce_scatter": True
            },
            "activation_checkpointing": {
                "partition_activations": True,
                "cpu_checkpointing": True
            },
        }

        self.model_engine, global_state.optimizer, _, _ = deepspeed.initialize(model=global_state.model,
                                                                               optimizer=global_state.optimizer,
                                                                               config_params=deepspeed_config, )

    def invoke_model(self, global_state: global_state_board, epoch_state: epoch_state_board,
                     step_state: step_state_board):
        return self.model_engine(step_state.converted_input)

    def backward(self, global_state: global_state_board, epoch_state: epoch_state_board,
                 step_state: step_state_board):
        self.model_engine.backward(step_state.loss_tensor)

    def step(self, global_state: global_state_board, epoch_state: epoch_state_board,
             step_state: step_state_board):
        self.model_engine.step()

from tketool.pyml.pytrainer import *
from accelerate import Accelerator
from accelerate import init_empty_weights, infer_auto_device_map, load_checkpoint_in_model, dispatch_model


class pytrainer_accelerate(pymodel_trainer):
    def __init__(self, model: torch.nn.Module, loss_obj,
                 use_cpu=False,
                 use_gpu_ids=None,
                 no_split_module_classes=[],
                 max_use_per_gpu=1.0,
                 **kwargs):
        super().__init__(model, loss_obj, **kwargs)

        self.accelerator = Accelerator(cpu=use_cpu)

        if self.accelerator.device.type == "cuda":
            if use_gpu_ids is not None:
                max_memory = {}  # {int(cuda): '8GiB' for cuda in ['0', '1', '2', '3']}
                for cuda_id in use_gpu_ids:
                    device = torch.device(f"cuda:{int(cuda_id)}")
                    prop = torch.cuda.get_device_properties(device)
                    gpu_memory = round(prop.total_memory / (1024 ** 3) * max_use_per_gpu, 1)
                    max_memory[int(cuda_id)] = f"{gpu_memory}GiB"
            else:
                max_memory = None

            self.device_map = infer_auto_device_map(self.model, max_memory=max_memory,
                                                    no_split_module_classes=no_split_module_classes)
            self.model = dispatch_model(self.model, device_map=self.device_map)

    @invoke_at([plugin_invoke_Enum.Batch_begin])
    def _drive_batch_data(self, global_state: global_state_board, epoch_state: epoch_state_board,
                          step_state: step_state_board):
        def move_to_drive(tensor_or_dict):
            if isinstance(tensor_or_dict, dict):
                return {k: v.to(self.accelerator.device) for k, v in tensor_or_dict.items()}

            else:
                return tensor_or_dict.to(self.accelerator.device)

        step_state.converted_input = move_to_drive(step_state.converted_input)
        step_state.converted_label = move_to_drive(step_state.converted_label)

    def backward(self, global_state: global_state_board, epoch_state: epoch_state_board,
                 step_state: step_state_board):
        self.accelerator.backward(step_state.loss_tensor)
        # step_state.loss_tensor.backward()

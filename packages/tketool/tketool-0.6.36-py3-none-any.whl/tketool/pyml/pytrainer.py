# by kejiang v1101
import os.path
from prettytable import PrettyTable, ALL
import torch
from tketool.mlsample.SampleSet import SampleSet
from tketool.utils.progressbar import process_status_bar
from tketool.files import create_folder_if_not_exists
import time
from datetime import datetime
from tketool.pyml.trainbase import *

optimizer_dict = {
    "adamw": torch.optim.AdamW,
    "adam": torch.optim.Adam,
    "sgd": torch.optim.SGD,
}


class pymodel_trainer(trainer_plugin_base):
    def Invoke(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        pass

    def __init__(self,
                 model: torch.nn.Module,
                 loss_obj,
                 update_mode=update_mode_enum.Per_Step,
                 output_folder=None,
                 plugins=[],
                 optimizer_type="adamw",
                 learn_rate=0.01):
        self.model = model
        self.loss = loss_obj
        self.optimizer = optimizer_dict[optimizer_type](
            [{
                'params': p,
                'name': name
            } for name, p in model.named_parameters() if p.requires_grad], lr=learn_rate)

        if output_folder is None:
            self.out_folder = os.path.join("model", f"{datetime.now().strftime('%m_%d_%H_%M')}")
        else:
            self.out_folder = output_folder
        self.update_mode = update_mode
        create_folder_if_not_exists(self.out_folder)
        create_folder_if_not_exists(self.out_folder, 'saved_model')

        self.plugin = {}
        for pl in [self] + plugins:
            for ty, funs in pl.get_plugin_map().items():
                if ty not in self.plugin:
                    self.plugin[ty] = []
                for sub_fun in funs:
                    self.plugin[ty].append(sub_fun)

    def _invoke_plugin(self, plugin_enum, base_wall, epoch_wall, batch_wall):
        if plugin_enum not in self.plugin:
            return

        for pl in self.plugin[plugin_enum]:
            pl(base_wall, epoch_wall, batch_wall)

    @invoke_at([plugin_invoke_Enum.Begin])
    def _statistics(self, global_state: global_state_board, epoch_state: epoch_state_board,
                    step_state: step_state_board):

        xtable = PrettyTable()
        xtable.field_names = ["name", "shape", "size", ]
        global_state.update_parameter_count = 0

        for group in global_state.optimizer.param_groups:
            param_count = sum(p.numel() for p in group['params'])
            xtable.add_row([group['name'], "", param_count])
            for p in group['params']:
                xtable.add_row(["", p.shape, p.numel()])
            global_state.update_parameter_count += param_count
        xtable.add_row(["total", "", global_state.update_parameter_count])
        global_state.log("parameters info: \n" + str(xtable))

    def zero_grad(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        global_state.optimizer.zero_grad()

    def invoke_model(self, global_state: global_state_board, epoch_state: epoch_state_board,
                     step_state: step_state_board):
        return global_state.model(step_state.converted_input)

    def calculate_loss(self, global_state: global_state_board, epoch_state: epoch_state_board,
                       step_state: step_state_board):
        return global_state.loss_obj(step_state.logit, step_state.converted_label)

    def backward(self, global_state: global_state_board, epoch_state: epoch_state_board,
                 step_state: step_state_board):
        step_state.loss_tensor.backward()

    def step(self, global_state: global_state_board, epoch_state: epoch_state_board,
             step_state: step_state_board):
        global_state.optimizer.step()

    def train(self,
              sample_set: SampleSet,
              epoch=100,
              input_convert_func=lambda x: x,
              label_convert_func=lambda x: x
              ):
        pb = process_status_bar()
        self.model.train()

        global_state = global_state_board(self, epoch, sample_set, pb, input_convert_func, label_convert_func)

        self._invoke_plugin(plugin_invoke_Enum.Begin, global_state, None, None)

        for epoch in pb.iter_bar(range(epoch), key='epoch'):

            epoch_state = epoch_state_board(epoch)

            self._invoke_plugin(plugin_invoke_Enum.Epoch_begin, global_state, epoch_state, None)

            if global_state.update_mode == update_mode_enum.Per_Epoch:
                self.zero_grad(plugin_invoke_Enum.Epoch_begin, global_state, epoch_state, None)
                # global_state.optimizer.zero_grad()

            batch_size = global_state.batch_count
            batch_dataset = global_state.sample_set
            for idx, item in pb.iter_bar(enumerate(batch_dataset), key='batch', max=batch_size):
                batch_state = step_state_board(idx, item, global_state)

                self._invoke_plugin(plugin_invoke_Enum.Batch_begin, global_state, epoch_state, batch_state)

                # optimizer = base_wall['optimizer']
                # model = base_wall['model']
                # loss = base_wall['loss']

                # batch_X = batch_state.converted_input  # batch_wall['Convert_x']
                # batch_Y = batch_state.converted_label  # batch_wall['Convert_y']

                if global_state.update_mode == update_mode_enum.Per_Step:
                    self.zero_grad(global_state, epoch_state, batch_state)
                    # global_state.optimizer.zero_grad()

                # logit= model(batch_x)
                batch_state.logit = self.invoke_model(global_state, epoch_state, batch_state)

                # loss_tensor=loss(logit, batch_Y)
                loss_value = self.calculate_loss(global_state, epoch_state, batch_state)

                # loss_value= loss_tensor.item()
                if torch.is_tensor(loss_value):
                    batch_state.loss_value = loss_value.item()
                    batch_state.loss_tensor = loss_value
                else:
                    raise Exception("Loss must be a tensor.")

                epoch_state.epoch_loss += batch_state.loss_value

                batch_state.end_time = time.time()

                self.backward(global_state, epoch_state, batch_state)
                # accelerator.backward(loss_tensor)
                # loss_tensor.backward()

                self._invoke_plugin(plugin_invoke_Enum.After_Backward, global_state, epoch_state, batch_state)

                if global_state.update_mode == update_mode_enum.Per_Step:
                    self.step(global_state, epoch_state, batch_state)
                    # global_state.optimizer.step()
                    self._invoke_plugin(plugin_invoke_Enum.Update, global_state, epoch_state, batch_state)
                    global_state.parameter_update_times += 1

                global_state.step += 1
                self._invoke_plugin(plugin_invoke_Enum.Batch_end, global_state, epoch_state, batch_state)

                del batch_state

            if global_state.update_mode == update_mode_enum.Per_Epoch:
                self.step(global_state, epoch_state, None)
                # global_state.optimizer.step()
                self._invoke_plugin(plugin_invoke_Enum.Update, global_state, epoch_state, None)
                global_state.parameter_update_times += 1

            epoch_state.end_time = time.time()

            self._invoke_plugin(plugin_invoke_Enum.Epoch_end, global_state, epoch_state, None)

            del epoch_state

        self._invoke_plugin(plugin_invoke_Enum.End, global_state, None, None)

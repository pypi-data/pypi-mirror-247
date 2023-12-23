import pickle, os, threading
from flask import Flask, send_from_directory, send_file, url_for, redirect
import logging
from jinja2 import Environment, FileSystemLoader, PackageLoader
from tketool.pyml.pytrainer import *


class dashboard_plugin(trainer_plugin_base):

    def __init__(self, port=None):
        self.epoch_data = []
        self.step_data = []
        self.port = port

        env = Environment(loader=PackageLoader('tketool.pyml', 'trainerplugins'))
        # env = Environment(loader=FileSystemLoader('pyml/trainerplugins/'))
        self.template = env.get_template("webreport_temp.html")

    @invoke_at([plugin_invoke_Enum.Begin])
    def start(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        # load data from file to self.epoch_data
        # path = os.path.join(global_state.model_folder, 'epoch_data.pkl')
        # try:
        #     with open(path, 'rb') as f:
        #         while True:
        #             try:
        #                 self.epoch_data.append(pickle.load(f))
        #             except EOFError:
        #                 break  # No more data in the file
        # except FileNotFoundError:
        #     pass  # It's okay if the file doesn't exist

        if self.port is not None:
            self.start_flask_server(global_state)

    @invoke_at([plugin_invoke_Enum.Update])
    def update(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        if step_state is not None:
            step_loss = step_state.loss_value
        else:
            step_loss = epoch_state.epoch_loss

        self.step_data.append(step_loss)

        self.refresh_page(global_state)

    def _scale_data(self, data: list):
        len_list = []
        if len(data) > 200:
            len_list.append(data[0])
            for x in range(2, len(data) - 1):
                len_list.append((data[x] + data[x - 1]) / 2)
            len_list.append(data[-1])
        else:
            len_list = data
        return len_list

    def refresh_page(self, global_state: global_state_board):

        self.epoch_data = self._scale_data(self.epoch_data)
        self.step_data = self._scale_data(self.step_data)

        model_info = {
            "epoch_count": global_state.epoch_count,  # base_wall['epoch_count'],
            "set_name": global_state.sample_set.set_name,  # base_wall['train_set'].set_name,
            "model_folder": global_state.model_folder,  # base_wall['model_folder'],
            "train_epoch": len(self.epoch_data),
            "parameter_update_times": global_state.parameter_update_times,
            "parameter_count": global_state.update_parameter_count,
            "drive_type": str(global_state),
            "type_precision": str(""),
            # base_wall['parameter_update_times'],
        }

        # Separate epoch data into different lists for plotting
        epoch_loss_index = list(range(len(self.epoch_data)))
        epoch_loss = self.epoch_data

        all_keys_data = {"step": self.step_data}

        template_vars = {"model_info": model_info,
                         "epoch_index": epoch_loss_index,
                         "epoch_loss": epoch_loss,
                         "all_keys": all_keys_data,
                         "all_keys_data_length": max([len(v) for v in all_keys_data.values()])
                         }

        wpath = os.path.join(global_state.model_folder, 'web_report.html')
        with open(wpath, 'w') as f:
            f.write(self.template.render(template_vars))

    @invoke_at([plugin_invoke_Enum.Epoch_end])
    def epoch_end(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        epoch_loss = epoch_state.epoch_loss  # epoch_wall['epoch_loss']
        # epoch_data = (epoch_loss, {})
        self.epoch_data.append(epoch_loss)

        self.refresh_page(global_state)

    def start_flask_server(self, global_state: global_state_board):
        app = Flask(__name__, static_folder=os.path.join(os.getcwd(), global_state.model_folder))

        app.logger.setLevel(logging.ERROR)
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        @app.route('/')
        def serve_dashboard():
            return redirect(url_for('static', filename='web_report.html'))

        thread = threading.Thread(target=app.run, kwargs={'port': self.port, 'host': '0.0.0.0'})
        thread.start()

    def Invoke(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        pass

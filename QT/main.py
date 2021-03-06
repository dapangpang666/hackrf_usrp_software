import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QFileDialog

# from PyQt5.uic import compileUi

# with open(r"D:\Tensorflow\code\hackrf_usrp_software\QT\window_ui1.py", "wt", encoding="utf-8") as py_file:
#     ui_file = open(r"D:\Tensorflow\code\hackrf_usrp_software\QT\test.ui", "r", encoding="utf-8")
#     compileUi(ui_file, py_file)
#     ui_file.close()

from window_ui import Ui_MainWindow
from functools import partial
import time, json
import subprocess
import threading
from os.path import join as pjoin


def save_config(config_path, CONFIG):
    with open(config_path, "w") as f:
        json.dump(CONFIG, f)


_config = {
    "tran_kind": 'hackrf',
    'tran_address_u': 'serial=',
    'tran_address_h': 'hackrf=',
    'tran_model': 'bpsk',
    'GNUradio_file': 'D:/GNU-radio/bin',
    'data_file': 'F:/shoufa/',
    'tran_data_path_modulated': 'F:/source_data/LFM.dat',
    'tran_data_path_unmodulated': 'F:/source_data/when_you_old.txt',
    "source_kind": 'hackrf',
    'source_address_u': 'serial=',
    'source_address_h': 'hackrf='}

# home_dir = pjoin(os.path.expanduser("~"), ".uhd_ui")
home_dir = pjoin(os.getcwd(), ".uhd_ui")
if not os.path.exists(home_dir):
    os.makedirs(home_dir)
config_path = pjoin(home_dir, "config.json")
config_keys = ['tran_address_h',  "tran_kind", 'tran_model', 'tran_data_path_modulated',
               'tran_address_u', 'GNUradio_file', "source_kind", 'tran_data_path_unmodulated',
               'source_address_u', 'source_address_h', 'data_file']
i_model = ['gmsk', 'bpsk', 'qpsk', '8psk', 'qam8',  'qam16', 'qam64', 'others']
i_kind = ['hackrf', 'usrp']
CONFIG = {}
if not os.path.exists(config_path):
    # 初始化CONFIG，方便保存数据
    for key in config_keys:
        CONFIG[key] = _config[key]
    save_config(config_path, CONFIG)
else:
    with open(config_path, "r") as f:
        CONFIG = json.load(f)
        for key in config_keys:
            if key not in CONFIG:
                CONFIG[key] = _config[key]
tran_kind = CONFIG["tran_kind"]
tran_address_u = CONFIG["tran_address_u"]
tran_address_h = CONFIG["tran_address_h"]
tran_model = CONFIG["tran_model"]
GNUradio_file = CONFIG["GNUradio_file"]
tran_data_path_unmodulated = CONFIG["tran_data_path_unmodulated"]
tran_data_path_modulated = CONFIG["tran_data_path_modulated"]
source_kind = CONFIG["source_kind"]
source_address_u = CONFIG["source_address_u"]
source_address_h = CONFIG["source_address_h"]
data_file = CONFIG["data_file"]
run_gr_name = 'run_gr.bat'


def dispaly_all(ui):
    ui.GNUradio_file_text.setText(str(GNUradio_file))
    ui.data_file_text.setText(str(data_file))

    if tran_kind == 'usrp':
        ui.tran_address_text.setText(str(tran_address_u))
    else:
        ui.tran_address_text.setText(str(tran_address_h))

    if source_kind == 'usrp':
        ui.rece_address_text.setText(str(source_address_u))
    else:
        ui.rece_address_text.setText(str(source_address_h))

    if tran_model in ['gmsk', 'bpsk', 'qpsk', '8psk', 'qam8',  'qam16', 'qam64', ]:
        ui.tran_data_file_text.setText(str(tran_data_path_unmodulated))
    else:
        ui.tran_data_file_text.setText(str(tran_data_path_modulated))

    ui.tran_model_box.setCurrentIndex(i_model.index(tran_model))
    ui.tran_kind_box.setCurrentIndex(i_kind.index(tran_kind))
    ui.rece_kind_box.setCurrentIndex(i_kind.index(source_kind))


def cmd_in_out(ui, command):
    subp = subprocess.Popen(command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding="utf-8")
    ui.textBrowser.append(subp.stdout.read())
    ui.textBrowser.moveCursor(ui.textBrowser.textCursor().End)


def set_tran_kind(ui):
    global CONFIG, tran_kind
    tran_kind = ui.tran_kind_box.currentText()
    if tran_kind == 'usrp':
        ui.tran_address_text.setText(str(tran_address_u))
    else:
        ui.tran_address_text.setText(str(tran_address_h))
    CONFIG["tran_kind"] = tran_kind
    save_config(config_path, CONFIG)


def set_rece_kind(ui):
    global CONFIG, source_kind
    source_kind = ui.rece_kind_box.currentText()
    if source_kind == 'usrp':
        ui.rece_address_text.setText(str(source_address_u))
    else:
        ui.rece_address_text.setText(str(source_address_h))
    CONFIG["source_kind"] = source_kind
    save_config(config_path, CONFIG)


def set_tran_address(ui):
    global CONFIG, tran_address_u, tran_address_h
    tran_address = ui.tran_address_text.text()
    tran_kind = ui.tran_kind_box.currentText()
    if tran_kind == 'usrp':
        tran_address_u = tran_address
        CONFIG["tran_address_u"] = tran_address
    else:
        tran_address_h = tran_address
        CONFIG["tran_address_h"] = tran_address
    save_config(config_path, CONFIG)


def find_tran_address(ui):
    tran_kind = ui.tran_kind_box.currentText()
    if tran_kind == 'hackrf':
        run_gr_path = GNUradio_file+'/'+run_gr_name
        cmd_in_out(ui, run_gr_path+' bin/hackrf_address_get.py')
    else:
        cmd_in_out(ui, 'uhd_find_devices')


def set_rece_address(ui):
    global CONFIG, source_address_u, source_address_h
    rece_address = ui.rece_address_text.text()
    rece_kind = ui.rece_kind_box.currentText()
    if rece_kind == 'usrp':
        source_address_u = rece_address
        CONFIG["source_address_u"] = rece_address
    else:
        source_address_h = rece_address
        CONFIG["source_address_h"] = rece_address
    save_config(config_path, CONFIG)


def find_rece_address(ui):
    rece_kind = ui.rece_kind_box.currentText()
    if rece_kind == 'hackrf':
        run_gr_path = GNUradio_file+'/'+run_gr_name
        cmd_in_out(ui, run_gr_path+' bin/hackrf_address_get.py')
    else:
        cmd_in_out(ui, 'uhd_find_devices')


def set_GNUradio_file(ui):
    global CONFIG, GNUradio_file
    GNUradio_file = ui.GNUradio_file_text.text()
    CONFIG["GNUradio_file"] = GNUradio_file
    save_config(config_path, CONFIG)


def set_tran_data_file(ui):
    global CONFIG, tran_data_path_unmodulated, tran_data_path_modulated
    if tran_model in ['gmsk', 'bpsk', 'qpsk', '8psk', 'qam8',  'qam16', 'qam64', ]:
        tran_data_path_unmodulated = ui.tran_data_file_text.text()
        CONFIG["tran_data_path_unmodulated"] = tran_data_path_unmodulated
    else:
        tran_data_path_modulated = ui.tran_data_file_text.text()
        CONFIG["tran_data_path_modulated"] = tran_data_path_modulated
    save_config(config_path, CONFIG)


def set_data_file(ui):
    global CONFIG, data_file
    data_file = ui.data_file_text.text()
    CONFIG["data_file"] = data_file
    save_config(config_path, CONFIG)


def set_tran_model(ui):
    global CONFIG, tran_model
    tran_model = i_model[ui.tran_model_box.currentIndex()]
    CONFIG["tran_model"] = tran_model
    # print(CONFIG["stop_len"])
    if tran_model in ['gmsk', 'bpsk', 'qpsk', '8psk', 'qam8',  'qam16', 'qam64', ]:
        ui.tran_data_file_text.setText(str(tran_data_path_unmodulated))
    else:
        ui.tran_data_file_text.setText(str(tran_data_path_modulated))
    save_config(config_path, CONFIG)
    # print(CONFIG["stop_len"])


def start_only_tran(ui):
    run_gr_path = GNUradio_file+'/'+run_gr_name
    command_only_tran = run_gr_path+' bin/transimeter.py'
    # event_shoufa = threading.Event()
    th_only_tran = threading.Thread(target=cmd_in_out,
                                    args=(ui, command_only_tran))
    th_only_tran.start()


def start_only_rece(ui):
    run_gr_path = GNUradio_file+'/'+run_gr_name
    command_only_rece = run_gr_path+' bin/recevier.py'
    # event_shoufa = threading.Event()
    th_only_rece = threading.Thread(target=cmd_in_out,
                                    args=(ui, command_only_rece))
    th_only_rece.start()


def start_rece_tran(ui):
    run_gr_path = GNUradio_file+'/'+run_gr_name
    command_rece_tran = run_gr_path+' bin/transimeter_and_recevier.py'
    # event_shoufa = threading.Event()
    th_rece_tran = threading.Thread(target=cmd_in_out,
                                    args=(ui, command_rece_tran))
    th_rece_tran.start()


def open_gnu_dir(ui):
    new_dir = QFileDialog.getExistingDirectory(None,
                                               "选择 GNU Radio 路径",
                                               ui.GNUradio_file_text.text(),
                                               QFileDialog.ShowDirsOnly)
    if new_dir == "":
        return
    else:
        if ui.GNUradio_file_text.text() == new_dir:
            return
        else:
            ui.GNUradio_file_text.setText(new_dir)
            ui.textBrowser.append("GNURadio Path has been changed to: " + new_dir)
            set_GNUradio_file(ui)


def open_saved_dir(ui):
    new_dir = QFileDialog.getExistingDirectory(None,
                                               "选择数据存储文件路径:",
                                               ui.data_file_text.text(),
                                               QFileDialog.ShowDirsOnly)
    if new_dir == "":
        return
    else:
        if ui.data_file_text.text() == new_dir:
            return
        else:
            ui.data_file_text.setText(new_dir)
            ui.textBrowser.append("数据存储文件路径 has been changed to: " + new_dir)
            set_data_file(ui)


def open_source_dir(ui):
    new_dir = QFileDialog.getOpenFileName(None,
                                          "选择发射文件路径",
                                          ui.tran_data_file_text.text()
                                          )[0]
    if new_dir == "":
        return
    else:
        if ui.tran_data_file_text.text() == new_dir:
            return
        else:
            ui.tran_data_file_text.setText(new_dir)
            ui.textBrowser.append("发射文件路径 has been changed to: " + new_dir)
            set_tran_data_file(ui)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    dispaly_all(ui)
    ui.tran_address_text.editingFinished.connect(partial(set_tran_address, ui))
    ui.rece_address_text.editingFinished.connect(partial(set_rece_address, ui))
    ui.GNUradio_file_text.editingFinished.connect(partial(set_GNUradio_file, ui))
    ui.data_file_text.editingFinished.connect(partial(set_data_file, ui))
    ui.tran_data_file_text.editingFinished.connect(partial(set_tran_data_file, ui))
    ui.tran_model_box.currentIndexChanged.connect(partial(set_tran_model, ui))
    ui.tran_kind_box.currentIndexChanged.connect(partial(set_tran_kind, ui))
    ui.rece_kind_box.currentIndexChanged.connect(partial(set_rece_kind, ui))
    ui.f_tran_ad_btn.clicked.connect(partial(find_tran_address, ui))
    ui.f_rece_ad_btn.clicked.connect(partial(find_rece_address, ui))
    ui.only_tran_btn.clicked.connect(partial(start_only_tran, ui))
    ui.only_rece_btn.clicked.connect(partial(start_only_rece, ui))
    ui.rece_tran_btn.clicked.connect(partial(start_rece_tran, ui))
    
    ui.select_gnu_path_btn.clicked.connect(partial(open_gnu_dir, ui))
    ui.select_save_path_btn.clicked.connect(partial(open_saved_dir, ui))
    ui.select_source_path_btn.clicked.connect(partial(open_source_dir, ui))
    
    sys.exit(app.exec_())

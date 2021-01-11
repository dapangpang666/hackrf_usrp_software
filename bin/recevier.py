#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Recevier
# GNU Radio version: 3.7.13.5
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
import threading
from os.path import join as pjoin
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import sip
import sys
import time
import osmosdr
import json, os
from gnuradio import qtgui


_config = {
    'sample_num': 10*1000*1000,
    'rf_gain_rec': 10,
    'file_num': 5,
    'data_file': 'F:/shoufa',
    'center_freq': 2300*1000*1000,
    'samp_rate': 2*1000*1000,
    'GNUradio_file': 'D:/GNU-radio/bin',
    'if_gain_rec': 50,
    'bb_gain_rec': 50,
    "source_kind": 'hackrf',
    'source_address_u': 'serial=',
    'source_address_h': 'hackrf='}


class recevier(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Recevier")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Recevier")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        # self.top_scroll_layout = Qt.QGridLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "recevier")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.home_dir = pjoin(os.path.expanduser("~"), ".uhd_ui")
        self.config_path = pjoin(self.home_dir, "config.json")

        self.config_keys = ['sample_num', 'if_gain_rec', 'bb_gain_rec',
                            'rf_gain_rec', 'file_num', 'data_file',
                            'center_freq',
                            'samp_rate', 'source_address_h',
                            'GNUradio_file', "source_kind",
                            'source_address_u']
        self.CONFIG = {}
        if not os.path.exists(self.config_path):
            # 初始化CONFIG，方便保存数据
            for key in self.config_keys:
                self.CONFIG[key] = _config[key]
            self.save_config()
        else:
            with open(self.config_path, "r") as f:
                self.CONFIG = json.load(f)
                for key in self.config_keys:
                    if key not in self.CONFIG:
                        self.CONFIG[key] = _config[key]
        self.sample_num = self.CONFIG["sample_num"]
        self.rf_gain_rec = self.CONFIG["rf_gain_rec"]
        self.file_num = self.CONFIG["file_num"]
        self.center_freq = self.CONFIG["center_freq"]
        self.samp_rate = self.CONFIG["samp_rate"]
        self.if_gain_rec = self.CONFIG["if_gain_rec"]
        self.bb_gain_rec = self.CONFIG["bb_gain_rec"]
        self.source_kind = self.CONFIG["source_kind"].encode('gbk')
        self.source_address_u = self.CONFIG["source_address_u"].encode('gbk')
        self.source_address_h = self.CONFIG["source_address_h"].encode('gbk')
        self.GNUradio_file = self.CONFIG["GNUradio_file"].encode('gbk')
        self.data_file = self.CONFIG["data_file"].encode('gbk')
        if not os.path.exists(self.data_file):
            os.makedirs(self.data_file)
        self.data_file_start = self.data_file+'/start.dat'
        ##################################################
        # Blocks
        ##################################################
        self._rf_gain_rec_range = Range(-50, 100, 1, self.rf_gain_rec, 200)
        self._rf_gain_rec_win = RangeWidget(self._rf_gain_rec_range, self.set_rf_gain_rec, u"接收机增益", "counter_slider", float)
        self.top_grid_layout.addWidget(self._rf_gain_rec_win, 3, 6, 1, 3)

        _start_btn_push_button = Qt.QPushButton(u'开始采集')
        _start_btn_push_button.pressed.connect(lambda: self.set_start_btn())
        self.top_grid_layout.addWidget(_start_btn_push_button, 3, 0, 1, 3)

        _end_btn_push_button = Qt.QPushButton(u'结束采集')
        _end_btn_push_button.pressed.connect(lambda: self.set_end_btn())
        self.top_grid_layout.addWidget(_end_btn_push_button, 3, 3, 1, 3)

        self._center_freq_tool_bar = Qt.QToolBar(self)
        self._center_freq_tool_bar.addWidget(Qt.QLabel(u"载频"+": "))
        self._center_freq_line_edit = Qt.QLineEdit(eng_notation.num_to_str(self.center_freq))
        self._center_freq_tool_bar.addWidget(self._center_freq_line_edit)
        self._center_freq_line_edit.returnPressed.connect(
        	lambda: self.set_center_freq(eng_notation.str_to_num(str(self._center_freq_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._center_freq_tool_bar, 4, 0, 1, 3)

        self._source_kind_options = ('hackrf', 'usrp', )
        self._source_kind_labels = (str(self._source_kind_options[0]), str(self._source_kind_options[1]), )
        self._source_kind_tool_bar = Qt.QToolBar(self)
        self._source_kind_tool_bar.addWidget(Qt.QLabel("source_kind"+": "))
        self._source_kind_combo_box = Qt.QComboBox()
        self._source_kind_tool_bar.addWidget(self._source_kind_combo_box)
        for label in self._source_kind_labels: self._source_kind_combo_box.addItem(label)
        self._source_kind_callback = lambda i: Qt.QMetaObject.invokeMethod(self._source_kind_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._source_kind_options.index(i)))
        self._source_kind_callback(self.source_kind)
        self._source_kind_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_source_kind(self._source_kind_options[i]))
        self.top_grid_layout.addWidget(self._source_kind_tool_bar, 4, 3, 1, 3)

        self._source_address_tool_bar = Qt.QToolBar(self)
        self._source_address_tool_bar.addWidget(Qt.QLabel("source_address"+": "))
        if self.source_kind == 'usrp':
            self._source_address_line_edit = Qt.QLineEdit(str(self.source_address_u))
        else:
            self._source_address_line_edit = Qt.QLineEdit(str(self.source_address_h))
        self._source_address_tool_bar.addWidget(self._source_address_line_edit)
        self._source_address_line_edit.returnPressed.connect(
        	lambda: self.set_source_address(str(self._source_address_line_edit.text().toAscii())))
        self.top_grid_layout.addWidget(self._source_address_tool_bar, 5, 3, 1, 3)

        self._if_gain_rec_tool_bar = Qt.QToolBar(self)
        self._if_gain_rec_tool_bar.addWidget(Qt.QLabel(u"接收机if增益(仅对hackrf有效)"+": "))
        self._if_gain_rec_line_edit = Qt.QLineEdit(str(self.if_gain_rec))
        self._if_gain_rec_tool_bar.addWidget(self._if_gain_rec_line_edit)
        self._if_gain_rec_line_edit.returnPressed.connect(
        	lambda: self.set_if_gain_rec(int(str(self._if_gain_rec_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._if_gain_rec_tool_bar, 1, 6, 1, 3)

        self._bb_gain_rec_tool_bar = Qt.QToolBar(self)
        self._bb_gain_rec_tool_bar.addWidget(Qt.QLabel(u"接收机bb增益(仅对hackrf有效)"+": "))
        self._bb_gain_rec_line_edit = Qt.QLineEdit(str(self.bb_gain_rec))
        self._bb_gain_rec_tool_bar.addWidget(self._bb_gain_rec_line_edit)
        self._bb_gain_rec_line_edit.returnPressed.connect(
        	lambda: self.set_bb_gain_rec(int(str(self._bb_gain_rec_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._bb_gain_rec_tool_bar, 2, 6, 1, 3)

        self._samp_rate_tool_bar = Qt.QToolBar(self)
        self._samp_rate_tool_bar.addWidget(Qt.QLabel(u"采样率"+": "))
        self._samp_rate_line_edit = Qt.QLineEdit(eng_notation.num_to_str(self.samp_rate))
        self._samp_rate_tool_bar.addWidget(self._samp_rate_line_edit)
        self._samp_rate_line_edit.returnPressed.connect(
        	lambda: self.set_samp_rate(eng_notation.str_to_num(str(self._samp_rate_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._samp_rate_tool_bar, 4, 6, 1, 3)
        self._data_file_tool_bar = Qt.QToolBar(self)
        self._data_file_tool_bar.addWidget(Qt.QLabel(u"数据目录"+": "))
        self._data_file_line_edit = Qt.QLineEdit(str(self.data_file))
        self._data_file_tool_bar.addWidget(self._data_file_line_edit)
        self._data_file_line_edit.returnPressed.connect(
        	lambda: self.set_data_file(str(str(self._data_file_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._data_file_tool_bar, 1, 0, 1, 5)
        self._GNUradio_file_tool_bar = Qt.QToolBar(self)
        self._GNUradio_file_tool_bar.addWidget(Qt.QLabel(u"GNUradio目录"+": "))
        self._GNUradio_file_line_edit = Qt.QLineEdit(str(self.GNUradio_file))
        self._GNUradio_file_tool_bar.addWidget(self._GNUradio_file_line_edit)
        self._GNUradio_file_line_edit.returnPressed.connect(
        	lambda: self.set_GNUradio_file(str(str(self._GNUradio_file_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._GNUradio_file_tool_bar, 2, 0, 1, 5)

        if self.source_kind == 'usrp':
            self.uhd_usrp_source_0 = uhd.usrp_source(
                ",".join((self.source_address_u, self.source_address_u)),
                uhd.stream_args(
                    cpu_format="fc32",
                    channels=range(1),
                ),
            )
            self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
            self.uhd_usrp_source_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)
            self.uhd_usrp_source_0.set_center_freq(self.center_freq, 0)
            self.uhd_usrp_source_0.set_gain(self.rf_gain_rec, 0)
            self.uhd_usrp_source_0.set_antenna('RX2', 0)
            self.uhd_usrp_source_0.set_auto_dc_offset(True, 0)
            self.uhd_usrp_source_0.set_auto_iq_balance(True, 0)
        else:
            self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + self.source_address_h )
            self.osmosdr_source_0.set_time_now(osmosdr.time_spec_t(time.time()), osmosdr.ALL_MBOARDS)
            self.osmosdr_source_0.set_sample_rate(self.samp_rate)
            self.osmosdr_source_0.set_center_freq(self.center_freq, 0)
            self.osmosdr_source_0.set_freq_corr(0, 0)
            self.osmosdr_source_0.set_dc_offset_mode(0, 0)
            self.osmosdr_source_0.set_iq_balance_mode(0, 0)
            self.osmosdr_source_0.set_gain_mode(False, 0)
            self.osmosdr_source_0.set_gain(self.rf_gain_rec, 0)
            self.osmosdr_source_0.set_if_gain(self.if_gain_rec, 0)
            self.osmosdr_source_0.set_bb_gain(self.bb_gain_rec, 0)
            self.osmosdr_source_0.set_antenna('', 0)

        self._sample_num_tool_bar = Qt.QToolBar(self)
        self._sample_num_tool_bar.addWidget(Qt.QLabel(u"样本点数"+": "))
        self._sample_num_line_edit = Qt.QLineEdit(eng_notation.num_to_str(self.sample_num))
        self._sample_num_tool_bar.addWidget(self._sample_num_line_edit)
        self._sample_num_line_edit.returnPressed.connect(
        	lambda: self.set_sample_num(eng_notation.str_to_num(str(self._sample_num_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._sample_num_tool_bar, 5, 0, 1, 3)
        self._file_num_tool_bar = Qt.QToolBar(self)
        self._file_num_tool_bar.addWidget(Qt.QLabel(u"文件数量"+": "))
        self._file_num_line_edit = Qt.QLineEdit(str(self.file_num))
        self._file_num_tool_bar.addWidget(self._file_num_line_edit)
        self._file_num_line_edit.returnPressed.connect(
        	lambda: self.set_file_num(eng_notation.str_to_num(str(self._file_num_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._file_num_tool_bar, 5, 6, 1, 3)

        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, self.data_file_start, False)
        self.blocks_file_sink_0_0.set_unbuffered(True)

        self.blocks_copy_0 = blocks.copy(gr.sizeof_gr_complex*1)
        self.blocks_copy_0.set_enabled(False)

        self.blocks_copy_1 = blocks.copy(gr.sizeof_gr_complex*1)
        self.blocks_copy_1.set_enabled(True)

        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
        	1024, #size
        	self.samp_rate, #samp_rate
        	"time", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 6, 0, 3, 3)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	self.center_freq, #fc
        	self.samp_rate, #bw
        	"freq", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 6, 6, 3, 3)
        self.textBrowser = Qt.QTextBrowser()
        self.textBrowser.setObjectName(u"当前状态")
        self.top_grid_layout.addWidget(self.textBrowser, 6, 3, 3, 3)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_copy_0, 0), (self.blocks_file_sink_0_0, 0))
        if self.source_kind == 'usrp':
            self.connect((self.uhd_usrp_source_0, 0), (self.blocks_copy_0, 0))
            self.connect((self.uhd_usrp_source_0, 0), (self.blocks_copy_1, 0))
        else:
            self.connect((self.osmosdr_source_0, 0), (self.blocks_copy_0, 0))
            self.connect((self.osmosdr_source_0, 0), (self.blocks_copy_1, 0))
        self.connect((self.blocks_copy_1, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_copy_1, 0), (self.qtgui_time_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "recevier")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.CONFIG, f)

    def set_start_btn(self):
        event = threading.Event()
        th = threading.Thread(target=self.save_file, args=(0, event))
        th.start()
        self.textBrowser.append(u'开始采集')
        self.blocks_copy_1.set_enabled(False)


    def save_file(self, _, event):
        self.end_sig = False
        delay_time = self.sample_num/self.samp_rate
        self.data_file_temp = self.data_file+'/test_rece/'
        if not os.path.exists(self.data_file_temp):
            os.makedirs(self.data_file_temp)
        for i in range(self.file_num):
            if self.end_sig == True:
                break
            self.data_file_true = self.data_file_temp+self.new_file()
            self.blocks_file_sink_0_0.open(self.data_file_true)
            self.blocks_copy_0.set_enabled(True)
            event.wait(delay_time)
            self.blocks_copy_0.set_enabled(False)
            self.textBrowser.append(u'第{}个文件采集完毕，共{}个文件'.format(i+1, self.file_num))
            event.wait(1)
        self.blocks_file_sink_0_0.open(self.data_file_start)
        self.blocks_copy_0.set_enabled(True)
        event.wait(0.1)
        self.blocks_copy_0.set_enabled(False)
        self.blocks_copy_1.set_enabled(True)

    def set_end_btn(self):
        self.end_sig = True
        self.textBrowser.append(u'结束采集')
        self.blocks_copy_1.set_enabled(True)

    def get_source_kind(self):
        return self.source_kind

    def set_source_kind(self, source_kind):
        self.source_kind = source_kind
        if self.source_kind == 'usrp':
            Qt.QMetaObject.invokeMethod(self._source_address_line_edit, "setText", Qt.Q_ARG("QString", str(self.source_address_u)))
        else:
            Qt.QMetaObject.invokeMethod(self._source_address_line_edit, "setText", Qt.Q_ARG("QString", str(self.source_address_h)))
        self.textBrowser.append(u'接受设备更改为:'+source_kind)
        self.textBrowser.append(u'请重新加载设备')
        self._source_kind_callback(self.source_kind)
        self.CONFIG["source_kind"] = source_kind
        self.save_config()

    def get_source_address(self):
        if self.source_kind == 'usrp':
            return self.source_address_u
        else:
            return self.source_address_h

    def set_source_address(self, source_address):
        if self.source_kind == 'usrp':
            self.source_address_u = source_address
            Qt.QMetaObject.invokeMethod(self._source_address_line_edit, "setText", Qt.Q_ARG("QString", str(self.source_address_u)))
            self.CONFIG["source_address_u"] = source_address
        else:
            self.source_address_h = source_address
            Qt.QMetaObject.invokeMethod(self._source_address_line_edit, "setText", Qt.Q_ARG("QString", str(self.source_address_h)))
            self.CONFIG["source_address_h"] = source_address
        self.textBrowser.append(u'接受设备地址更改为:'+source_address)
        self.textBrowser.append(u'请重新加载设备')
        self.save_config()

    def get_sample_num(self):
        return self.sample_num

    def set_sample_num(self, sample_num):
        self.sample_num = sample_num
        self.textBrowser.append(u'样本点数更改为:'+str(self.sample_num))
        Qt.QMetaObject.invokeMethod(self._sample_num_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(sample_num)))
        self.CONFIG["sample_num"] = self.sample_num
        self.save_config()

    def get_rf_gain_rec(self):
        return self.rf_gain_rec

    def set_rf_gain_rec(self, rf_gain_rec):
        self.textBrowser.append(u'增益更改为:'+str(rf_gain_rec))
        self.rf_gain_rec = rf_gain_rec
        if self.source_kind == 'usrp':
            self.uhd_usrp_source_0.set_gain(self.rf_gain_rec, 0)
        else:
            self.osmosdr_source_0.set_gain(self.rf_gain_rec, 0)
        self.CONFIG["rf_gain_rec"] = self.rf_gain_rec
        self.save_config()

    def set_if_gain_rec(self, if_gain_rec):
        self.if_gain_rec = if_gain_rec
        if self.source_kind == 'hackrf':
            self.osmosdr_source_0.set_if_gain(self.if_gain_rec, 0)
        self.textBrowser.append(u'接收机if增益更改为:'+str(if_gain_rec))
        self.CONFIG["if_gain_rec"] = self.if_gain_rec
        self.save_config()

    def set_bb_gain_rec(self, bb_gain_rec):
        self.bb_gain_rec = bb_gain_rec
        if self.source_kind == 'hackrf':
            self.osmosdr_source_0.set_bb_gain(self.bb_gain_rec, 0)
        self.textBrowser.append(u'接收机bb增益更改为:'+str(bb_gain_rec))
        self.CONFIG["bb_gain_rec"] = self.bb_gain_rec
        self.save_config()


    def get_file_num(self):
        return self.file_num

    def set_file_num(self, file_num):
        self.textBrowser.append(u'文件数量更改为:'+str(file_num))
        self.file_num = int(file_num)
        Qt.QMetaObject.invokeMethod(self._file_num_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.file_num)))
        self.CONFIG["file_num"] = self.file_num
        self.save_config()

    def get_data_file(self):
        return self.data_file

    def set_data_file(self, data_file):
        self.data_file = data_file
        self.textBrowser.append(u'数据目录更改为:'+str(data_file))
        Qt.QMetaObject.invokeMethod(self._data_file_line_edit, "setText", Qt.Q_ARG("QString", str(self.data_file)))
        self.blocks_file_sink_0_0.open(self.data_file)
        self.CONFIG["data_file"] = self.data_file
        self.save_config()

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.textBrowser.append(u'载频更改为:'+str(center_freq))
        Qt.QMetaObject.invokeMethod(self._center_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(center_freq)))
        if self.source_kind == 'usrp':
            self.uhd_usrp_source_0.set_center_freq(self.center_freq, 0)
        else:
            self.osmosdr_source_0.set_center_freq(self.center_freq, 0)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.CONFIG["center_freq"] = self.center_freq
        self.save_config()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.textBrowser.append(u'采样率更改为:'+str(self.samp_rate))
        Qt.QMetaObject.invokeMethod(self._samp_rate_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(samp_rate)))
        if self.source_kind == 'usrp':
            self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        else:
            self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.CONFIG["samp_rate"] = self.samp_rate
        self.save_config()

    def get_GNUradio_file(self):
        return self.GNUradio_file

    def set_GNUradio_file(self, GNUradio_file):
        self.GNUradio_file = GNUradio_file
        self.textBrowser.append(u'GNUradio目录更改为:'+str(GNUradio_file))
        Qt.QMetaObject.invokeMethod(self._GNUradio_file_line_edit, "setText", Qt.Q_ARG("QString", str(self.GNUradio_file)))
        self.CONFIG["GNUradio_file"] = self.GNUradio_file
        self.save_config()

    def new_file(self):
        new_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
        new_time = new_time.replace(':', '-')
        freq_name = '_fc_{}'.format(int(self.center_freq))
        sample_rate__name = '_bw_{}'.format(int(self.samp_rate))
        len__name = '_N_{}'.format(int(self.sample_num))
        new_name = new_time+freq_name+sample_rate__name+len__name+'.dat'
        return new_name


def main(top_block_cls=recevier, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()

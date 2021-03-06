#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Transimeter
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
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import blocks
from gnuradio import analog
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import osmosdr
import pmt
import sip
import sys, os
import threading
from os.path import join as pjoin
import time, json
from gnuradio import uhd
from gnuradio import qtgui

MS = 2048


_config = {
    'samp_rate': 2*1000*1000,
    'rf_gain_tran': 50,
    'if_gain_tran': 50,
    'bb_gain_tran': 50,
    'stop_len': 10000,
    'center_freq': 2300*1000*1000,
    'tran_data_path_modulated': 'F:/source_data/LFM.dat',
    'tran_data_path_unmodulated': 'F:/source_data/when you old.txt',
    "tran_kind": 'hackrf',
    'tran_address_u': 'serial=',
    'tran_address_h': 'hackrf=',
    'tran_model': 'bpsk'}


class transimeter(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Transimeter")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Transimeter")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
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

        self.settings = Qt.QSettings("GNU Radio", "transimeter")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        # self.home_dir = pjoin(os.path.expanduser("~"), ".uhd_ui")
        self.home_dir = pjoin(os.getcwd(), ".uhd_ui")
        if not os.path.exists(self.home_dir):
            os.makedirs(self.home_dir)
        
        self.config_path = pjoin(self.home_dir, "config.json")
        self.config_keys = ['center_freq', 'samp_rate', 'tran_address_h',
                            'rf_gain_tran', "tran_kind", 'tran_model',
                            'tran_address_u', 'stop_len', 'if_gain_tran',
                            'tran_data_path_modulated', 'tran_data_path_unmodulated',
                            'bb_gain_tran']
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
        self.rf_gain_tran = self.CONFIG["rf_gain_tran"]
        self.if_gain_tran = self.CONFIG["if_gain_tran"]
        self.bb_gain_tran = self.CONFIG["bb_gain_tran"]
        self.tran_kind = self.CONFIG["tran_kind"].encode('gbk')
        self.tran_address_u = self.CONFIG["tran_address_u"].encode('gbk')
        self.tran_address_h = self.CONFIG["tran_address_h"].encode('gbk')
        self.stop_len = self.CONFIG["stop_len"]
        self.tran_model = self.CONFIG["tran_model"].encode('gbk')
        self.tran_data_path_unmodulated = self.CONFIG["tran_data_path_unmodulated"].encode('gbk')
        self.tran_data_path_modulated = self.CONFIG["tran_data_path_modulated"].encode('gbk')

        self.center_freq = self.CONFIG["center_freq"]
        self.samp_rate = self.CONFIG["samp_rate"]
        
        self.add_SNR_value = add_SNR_value = 20.0
        self.trans_test = trans_test = False
        self.Add_SNR = Add_SNR = False
        self.volume = volume = 1

        ##################################################
        # Blocks
        ##################################################
        _trans_test_check_box = Qt.QCheckBox(u"发射信号")
        self._trans_test_choices = {True: True, False: False}
        self._trans_test_choices_inv = dict((v,k) for k,v in self._trans_test_choices.iteritems())
        self._trans_test_callback = lambda i: Qt.QMetaObject.invokeMethod(_trans_test_check_box, "setChecked", Qt.Q_ARG("bool", self._trans_test_choices_inv[i]))
        self._trans_test_callback(self.trans_test)
        _trans_test_check_box.stateChanged.connect(lambda i: self.set_trans_test(self._trans_test_choices[bool(i)]))
        self.top_grid_layout.addWidget(_trans_test_check_box, 3, 0, 1, 1)

        self._tran_model_options = ('gmsk', 'bpsk', 'qpsk', '8psk', 'qam8',  'qam16', 'qam64', 'others',)
        self._tran_model_labels = (str(self._tran_model_options[0]), str(self._tran_model_options[1]),
                                    str(self._tran_model_options[2]),  str(self._tran_model_options[3]),
                                    str(self._tran_model_options[4]),  str(self._tran_model_options[5]),
                                    str(self._tran_model_options[6]),  str(self._tran_model_options[7]))
        self._tran_model_tool_bar = Qt.QToolBar(self)
        self._tran_model_tool_bar.addWidget(Qt.QLabel(u"调制方式"+": "))
        self._tran_model_combo_box = Qt.QComboBox()
        self._tran_model_tool_bar.addWidget(self._tran_model_combo_box)
        for label in self._tran_model_labels: self._tran_model_combo_box.addItem(label)
        self._tran_model_callback = lambda i: Qt.QMetaObject.invokeMethod(self._tran_model_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._tran_model_options.index(i)))
        self._tran_model_callback(self.tran_model)
        self._tran_model_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_tran_model(self._tran_model_options[i]))
        self.top_grid_layout.addWidget(self._tran_model_tool_bar, 1, 0, 1, 1)

        self._tran_kind_options = ('hackrf', 'usrp', )
        self._tran_kind_labels = (str(self._tran_kind_options[0]), str(self._tran_kind_options[1]), )
        self._tran_kind_tool_bar = Qt.QToolBar(self)
        self._tran_kind_tool_bar.addWidget(Qt.QLabel(u"发射机种类"+": "))
        self._tran_kind_combo_box = Qt.QComboBox()
        self._tran_kind_tool_bar.addWidget(self._tran_kind_combo_box)
        for label in self._tran_kind_labels: self._tran_kind_combo_box.addItem(label)
        self._tran_kind_callback = lambda i: Qt.QMetaObject.invokeMethod(self._tran_kind_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._tran_kind_options.index(i)))
        self._tran_kind_callback(self.tran_kind)
        self._tran_kind_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_tran_kind(self._tran_kind_options[i]))
        self.top_grid_layout.addWidget(self._tran_kind_tool_bar, 2, 6, 1, 1)

        self._tran_address_tool_bar = Qt.QToolBar(self)
        self._tran_address_tool_bar.addWidget(Qt.QLabel(u"发射机地址"+": "))
        if self.tran_kind == 'usrp':
            self._tran_address_line_edit = Qt.QLineEdit(str(self.tran_address_u))
        else:
            self._tran_address_line_edit = Qt.QLineEdit(str(self.tran_address_h))
        self._tran_address_tool_bar.addWidget(self._tran_address_line_edit)
        self._tran_address_line_edit.returnPressed.connect(
        	lambda: self.set_tran_address(str(self._tran_address_line_edit.text().toAscii())))
        self.top_grid_layout.addWidget(self._tran_address_tool_bar, 2, 7, 1, 1)

        self._center_freq_tool_bar = Qt.QToolBar(self)
        self._center_freq_tool_bar.addWidget(Qt.QLabel(u"载频"+": "))
        self._center_freq_line_edit = Qt.QLineEdit(eng_notation.num_to_str(self.center_freq))
        self._center_freq_tool_bar.addWidget(self._center_freq_line_edit)
        self._center_freq_line_edit.returnPressed.connect(
        	lambda: self.set_center_freq(eng_notation.str_to_num(str(self._center_freq_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._center_freq_tool_bar, 2, 0, 1, 1)

        self._samp_rate_tool_bar = Qt.QToolBar(self)
        self._samp_rate_tool_bar.addWidget(Qt.QLabel(u"采样率"+": "))
        self._samp_rate_line_edit = Qt.QLineEdit(eng_notation.num_to_str(self.samp_rate))
        self._samp_rate_tool_bar.addWidget(self._samp_rate_line_edit)
        self._samp_rate_line_edit.returnPressed.connect(
        	lambda: self.set_samp_rate(eng_notation.str_to_num(str(self._samp_rate_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._samp_rate_tool_bar, 3, 6, 1, 1)

        self._stop_len_tool_bar = Qt.QToolBar(self)
        self._stop_len_tool_bar.addWidget(Qt.QLabel(u"发射机方波长度"+": "))
        self._stop_len_line_edit = Qt.QLineEdit(eng_notation.num_to_str(self.stop_len))
        self._stop_len_tool_bar.addWidget(self._stop_len_line_edit)
        self._stop_len_line_edit.returnPressed.connect(
        	lambda: self.set_stop_len(eng_notation.str_to_num(str(self._stop_len_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._stop_len_tool_bar, 3, 2, 1, 1)

        self._rf_gain_tran_range = Range(-50, 100, 1, self.rf_gain_tran, 200)
        self._rf_gain_tran_win = RangeWidget(self._rf_gain_tran_range, self.set_rf_gain_tran, u"发射机增益", "counter_slider", float)
        self.top_grid_layout.addWidget(self._rf_gain_tran_win, 4, 0, 1, 3)

        self._if_gain_tran_range = Range(-50, 100, 1, self.if_gain_tran, 200)
        self._if_gain_tran_win = RangeWidget(self._if_gain_tran_range, self.set_if_gain_tran, u"发射机if增益(仅对hackrf有效)", "counter_slider", float)
        self.top_grid_layout.addWidget(self._if_gain_tran_win, 4, 3, 1, 3)

        self._bb_gain_tran_range = Range(-50, 100, 1, self.bb_gain_tran, 200)
        self._bb_gain_tran_win = RangeWidget(self._bb_gain_tran_range, self.set_bb_gain_tran, u"发射机bb增益(仅对hackrf有效)", "counter_slider", float)
        self.top_grid_layout.addWidget(self._bb_gain_tran_win, 4, 6, 1, 3)

        _Add_SNR_check_box = Qt.QCheckBox(u'额外信噪比')
        self._Add_SNR_choices = {True: True, False: False}
        self._Add_SNR_choices_inv = dict((v,k) for k,v in self._Add_SNR_choices.iteritems())
        self._Add_SNR_callback = lambda i: Qt.QMetaObject.invokeMethod(_Add_SNR_check_box, "setChecked", Qt.Q_ARG("bool", self._Add_SNR_choices_inv[i]))
        self._Add_SNR_callback(self.Add_SNR)
        _Add_SNR_check_box.stateChanged.connect(lambda i: self.set_Add_SNR(self._Add_SNR_choices[bool(i)]))
        self.top_grid_layout.addWidget(_Add_SNR_check_box, 3, 3, 1, 1)

        self._add_SNR_value_tool_bar = Qt.QToolBar(self)
        self._add_SNR_value_line_edit = Qt.QLineEdit(eng_notation.num_to_str(self.add_SNR_value))
        self._add_SNR_value_tool_bar.addWidget(self._add_SNR_value_line_edit)
        self._add_SNR_value_line_edit.returnPressed.connect(
        	lambda: self.set_add_SNR_value(eng_notation.str_to_num(str(self._add_SNR_value_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._add_SNR_value_tool_bar, 3, 5, 1, 1)

        self.textBrowser = Qt.QTextBrowser()
        self.textBrowser.setObjectName(u"当前状态")
        self.top_grid_layout.addWidget(self.textBrowser, 5, 3, 1, 3)


        ##################################################
        # transimeter
        ##################################################
        _wave_nums = 10
        wave_width = _wave_nums*MS  # 50ms
        gui_update_time_interval = 1.0  # _wave_nums/200
        self.qtgui_time_sink_x_1_0 = qtgui.time_sink_c(
        	wave_width, #size
        	self.samp_rate, #samp_rate
        	"trans_time", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_1_0.set_update_time(gui_update_time_interval)
        self.qtgui_time_sink_x_1_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1_0.enable_autoscale(True)
        self.qtgui_time_sink_x_1_0.enable_grid(False)
        self.qtgui_time_sink_x_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_1_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_1_0.disable_legend()

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
                    self.qtgui_time_sink_x_1_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_1_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_0_win, 5, 0, 1, 3)
        self.qtgui_freq_sink_x_1_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	self.center_freq, #fc
        	self.samp_rate, #bw
        	"trans_fre", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_1_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_1_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_1_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_1_0.enable_grid(False)
        self.qtgui_freq_sink_x_1_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1_0.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_1_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_1_0.set_plot_pos_half(not True)

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
                self.qtgui_freq_sink_x_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_1_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_1_0_win, 5, 6, 1, 3)

        if self.tran_kind == 'usrp':
            self.uhd_usrp_sink_0 = uhd.usrp_sink(
                ",".join((self.tran_address_u, self.tran_address_u)),
                uhd.stream_args(
                    cpu_format="fc32",
                    channels=range(1),
                ),
            )
            self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
            self.uhd_usrp_sink_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)
            self.uhd_usrp_sink_0.set_center_freq(self.center_freq, 0)
            self.uhd_usrp_sink_0.set_gain(self.rf_gain_tran, 0)
            self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        else:
            self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + self.tran_address_h )
            self.osmosdr_sink_0.set_sample_rate(self.samp_rate)
            self.osmosdr_sink_0.set_time_now(osmosdr.time_spec_t(time.time()), osmosdr.ALL_MBOARDS)
            self.osmosdr_sink_0.set_freq_corr(0, 0)
            self.osmosdr_sink_0.set_center_freq(self.center_freq, 0)
            self.osmosdr_sink_0.set_gain(self.rf_gain_tran, 0)
            self.osmosdr_sink_0.set_if_gain(self.if_gain_tran, 0)
            self.osmosdr_sink_0.set_bb_gain(self.bb_gain_tran, 0)
            self.osmosdr_sink_0.set_antenna('', 0)
            self.osmosdr_sink_0.set_bandwidth(0, 0)

        if self.tran_model in ['bpsk', 'gmsk']:
            constellation_points_use = 2
            bits_per_symbol_use = 1
        elif self.tran_model in ['qpsk']:
            constellation_points_use = 4
            bits_per_symbol_use = 2
        elif self.tran_model in ['8psk', 'qam8']:
            constellation_points_use = 8
            bits_per_symbol_use = 3
        elif self.tran_model in ['qam16']:
            constellation_points_use = 16
            bits_per_symbol_use = 4
        elif self.tran_model in ['qam64']:
            constellation_points_use = 64
            bits_per_symbol_use = 6
        elif self.tran_model in ['others']:
            pass
        else:
            constellation_points_use = 1
            bits_per_symbol_use = 1
            self.textBrowser.append(u'所选调制类型暂不支持')

        if self.tran_model == 'gmsk':
            self.digital_gmsk_mod_0 = digital.gmsk_mod(
                samples_per_symbol=2,
                bt=0.35,
                verbose=False,
                log=False,
            )
        elif self.tran_model in ['bpsk', 'qpsk', '8psk', 'qam8',  'qam16', 'qam64', ]:
            self.digital_psk_mod_0 = digital.psk.psk_mod(
            constellation_points=constellation_points_use,
            mod_code="gray",
            differential=True,
            samples_per_symbol=2,
            excess_bw=0.35,
            verbose=False,
            log=False,
            )
        else:
            pass


        if self.tran_model in ['gmsk', 'bpsk', 'qpsk', '8psk', 'qam8',  'qam16', 'qam64', ]:
            self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, self.tran_data_path_unmodulated, True)
            self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        else:
            self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, self.tran_data_path_modulated, True)
            self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)

        self.blocks_copy_0 = blocks.copy(gr.sizeof_gr_complex*1)
        self.blocks_copy_0.set_enabled(False)

        if self.tran_model in ['gmsk', 'bpsk', 'qpsk', '8psk', 'qam8',  'qam16', 'qam64', ]:
            self.blks2_packet_encoder_0 = grc_blks2.packet_mod_b(grc_blks2.packet_encoder(
                    samples_per_symbol=8,
                    bits_per_symbol=bits_per_symbol_use,
                    preamble='',
                    access_code='',
                    pad_for_usrp=False,
                ),
                payload_length=200,
            )

            self.analog_sig_source_x_0 = analog.sig_source_c(self.samp_rate, analog.GR_SQR_WAVE, self.samp_rate/self.stop_len, 1, 0)
        
            self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
            self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
            self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, self.samp_rate,True)
        else:
            self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, self.samp_rate,True)
            self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)

        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 0, 0)

        self.blocks_add_xx_0 = blocks.add_vcc(1)
        
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((self.volume, ))



        ##################################################
        # Connections
        ##################################################
        # tran
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_copy_0, 0))
        self.connect((self.blocks_copy_0, 0), (self.qtgui_freq_sink_x_1_0, 0))
        self.connect((self.blocks_copy_0, 0), (self.qtgui_time_sink_x_1_0, 0))
        if self.tran_model in ['gmsk', 'bpsk', 'qpsk', '8psk', 'qam8',  'qam16', 'qam64', ]:
            self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
            self.connect((self.blocks_throttle_0, 0), (self.blks2_packet_encoder_0, 0))
            self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
            self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_0, 1))
            self.connect((self.analog_noise_source_x_0, 0), (self.blocks_multiply_xx_1, 1))
            self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_multiply_xx_1, 0))
            self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_add_xx_0, 0))
            if self.tran_model == 'gmsk':
                self.connect((self.digital_gmsk_mod_0, 0), (self.blocks_multiply_xx_0, 0))
                self.connect((self.blks2_packet_encoder_0, 0), (self.digital_gmsk_mod_0, 0))
            else:
                self.connect((self.digital_psk_mod_0, 0), (self.blocks_multiply_xx_0, 0))
                self.connect((self.blks2_packet_encoder_0, 0), (self.digital_psk_mod_0, 0))
        else:
            self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
            self.connect((self.blocks_throttle_0, 0), (self.blocks_add_xx_0, 1))
            self.connect((self.analog_noise_source_x_0, 0), (self.blocks_multiply_xx_1, 1))
            self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_xx_1, 0))
            self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_add_xx_0, 0))

        if self.tran_kind == 'usrp':
            self.connect((self.blocks_copy_0, 0), (self.uhd_usrp_sink_0, 0))
        else:
            self.connect((self.blocks_copy_0, 0), (self.osmosdr_sink_0, 0))

    ##################################################
    # Founctions
    ##################################################
    def closeEvent(self, event):
        self.set_trans_test(False)
        self.settings = Qt.QSettings("GNU Radio", "transimeter")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.CONFIG, f)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_1_0.set_samp_rate(self.samp_rate)
        self.qtgui_freq_sink_x_1_0.set_frequency_range(self.center_freq, self.samp_rate)
        if self.tran_model in ['gmsk', 'bpsk', 'qpsk', '8psk', 'qam8',  'qam16', 'qam64', ]:
            self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
            self.analog_sig_source_x_0.set_frequency(self.samp_rate/self.stop_len)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        if self.tran_kind == 'usrp':
            self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        else:
            self.osmosdr_sink_0.set_sample_rate(self.samp_rate)
        self.textBrowser.append(u'samp_rate更改为:'+str(samp_rate))
        self.CONFIG["samp_rate"] = self.samp_rate
        self.save_config()

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0.set_k((self.volume, ))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        Qt.QMetaObject.invokeMethod(self._center_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.center_freq)))
        self.qtgui_freq_sink_x_1_0.set_frequency_range(self.center_freq, self.samp_rate)
        if self.tran_kind == 'usrp':
            self.uhd_usrp_sink_0.set_center_freq(self.center_freq, 0)
        else:
            self.osmosdr_sink_0.set_center_freq(self.center_freq, 0)
        self.textBrowser.append(u'center_freq更改为:'+str(center_freq))
        self.CONFIG["center_freq"] = self.center_freq
        self.save_config()

    ##################################################
    # trans
    ##################################################
    def get_trans_test(self):
        return self.trans_test

    def set_trans_test(self, trans_test):
        self.trans_test = trans_test
        self._trans_test_callback(self.trans_test)
        if self.trans_test:
            self.end_sig = False
            event_test = threading.Event()
            th = threading.Thread(target=self.source_out, args=(0, event_test))
            th.start()
        else:
            self.end_sig = True

    def source_out(self, _, event_test):
        self.blocks_copy_0.set_enabled(True)
        delay_time = self.stop_len/self.samp_rate
        while True:
            if self.end_sig:
                self.blocks_copy_0.set_enabled(False)
                break
            event_test.wait(delay_time)

    def get_rf_gain_tran(self):
        return self.rf_gain_tran

    def set_rf_gain_tran(self, rf_gain_tran):
        self.rf_gain_tran = rf_gain_tran
        if self.tran_kind == 'usrp':
            self.uhd_usrp_sink_0.set_gain(self.rf_gain_tran, 0)
        else:
            self.osmosdr_sink_0.set_gain(self.rf_gain_tran, 0)
        self.textBrowser.append(u'rf_gain_tran更改为:'+str(rf_gain_tran))
        self.CONFIG["rf_gain_tran"] = self.rf_gain_tran
        self.save_config()

    def set_if_gain_tran(self, if_gain_tran):
        self.if_gain_tran = if_gain_tran
        if self.tran_kind == 'usrp':
            self.uhd_usrp_sink_0.set_gain(self.if_gain_tran, 0)
        else:
            self.osmosdr_sink_0.set_if_gain(self.if_gain_tran, 0)
        self.textBrowser.append(u'if_gain_tran更改为:'+str(if_gain_tran))
        self.CONFIG["if_gain_tran"] = self.if_gain_tran
        self.save_config()

    def set_bb_gain_tran(self, bb_gain_tran):
        self.bb_gain_tran = bb_gain_tran
        if self.tran_kind == 'usrp':
            self.uhd_usrp_sink_0.set_gain(self.bb_gain_tran, 0)
        else:
            self.osmosdr_sink_0.set_bb_gain(self.bb_gain_tran, 0)
        self.textBrowser.append(u'bb_gain_tran更改为:'+str(bb_gain_tran))
        self.CONFIG["bb_gain_tran"] = self.bb_gain_tran
        self.save_config()

    def get_tran_kind(self):
        return self.tran_kind

    def set_tran_kind(self, tran_kind):
        self.tran_kind = tran_kind
        if self.tran_kind == 'usrp':
            Qt.QMetaObject.invokeMethod(self._tran_address_line_edit, "setText", Qt.Q_ARG("QString", str(self.tran_address_u)))
        else:
            Qt.QMetaObject.invokeMethod(self._tran_address_line_edit, "setText", Qt.Q_ARG("QString", str(self.tran_address_h)))
        self.textBrowser.append(u'接受设备更改为:'+tran_kind)
        self.textBrowser.append(u'请重新加载设备')
        self._tran_kind_callback(self.tran_kind)
        self.CONFIG["tran_kind"] = tran_kind
        self.save_config()
    
    def get_tran_model(self):
        return self.tran_model
    
    def set_tran_model(self, tran_model):
        self.tran_model = tran_model
        self.textBrowser.append(u'调制方式更改为:'+tran_model)
        self.textBrowser.append(u'请重新加载设备')
        self._tran_model_callback(self.tran_model)
        self.CONFIG["tran_model"] = tran_model
        self.save_config()

    def set_Add_SNR(self, Add_SNR):
        self.Add_SNR = Add_SNR
        self._Add_SNR_callback(self.Add_SNR)
        if self.Add_SNR:
            self.textBrowser.append(u'添加额外信噪比')
            add_SNR_value = eng_notation.str_to_num(str(self.add_SNR_value))
            self.analog_noise_source_x_0.set_amplitude(1/(10**(add_SNR_value/20)))
        else:
            self.textBrowser.append(u'取消额外信噪比')
            self.analog_noise_source_x_0.set_amplitude(0)

    def set_add_SNR_value(self, add_SNR_value):
        self.add_SNR_value = add_SNR_value
        Qt.QMetaObject.invokeMethod(self._add_SNR_value_line_edit, "setText", Qt.Q_ARG("QString", str(self.add_SNR_value)))
        if self.Add_SNR:
            self.analog_noise_source_x_0.set_amplitude(1/(10**(add_SNR_value/20)))
            self.textBrowser.append(u'额外信噪比:'+str(add_SNR_value))

    def get_stop_len(self):
        return self.stop_len

    def set_stop_len(self, stop_len):
        self.stop_len = stop_len
        Qt.QMetaObject.invokeMethod(self._stop_len_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.stop_len)))
        if self.tran_model in ['gmsk', 'bpsk', 'qpsk', '8psk', 'qam8',  'qam16', 'qam64', ]:
            self.analog_sig_source_x_0.set_frequency(self.samp_rate/self.stop_len)
            self.textBrowser.append(u'stop_len更改为:'+str(stop_len))
            self.CONFIG["stop_len"] = self.stop_len
            self.save_config()
        else:
            self.textBrowser.append(u'该调制方式与发射机方波长度无关')

    def get_tran_address(self):
        if self.tran_kind == 'usrp':
            return self.tran_address_u
        else:
            return self.tran_address_h

    def set_tran_address(self, tran_address):
        if self.tran_kind == 'usrp':
            self.tran_address_u = tran_address
            Qt.QMetaObject.invokeMethod(self._tran_address_line_edit, "setText", Qt.Q_ARG("QString", str(self.tran_address_u)))
            self.CONFIG["tran_address_u"] = tran_address
        else:
            self.tran_address_h = tran_address
            Qt.QMetaObject.invokeMethod(self._tran_address_line_edit, "setText", Qt.Q_ARG("QString", str(self.tran_address_h)))
            self.CONFIG["tran_address_h"] = tran_address
        self.textBrowser.append(u'接受设备地址更改为:'+tran_address)
        self.textBrowser.append(u'请重新加载设备')
        self.save_config()



def main(top_block_cls=transimeter, options=None):

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

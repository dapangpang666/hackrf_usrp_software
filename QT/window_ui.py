# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Tensorflow\code\hackrf_usrp_software\QT\test.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 640)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(16)
        self.label_7.setFont(font)
        self.label_7.setLineWidth(1)
        self.label_7.setTextFormat(QtCore.Qt.AutoText)
        self.label_7.setScaledContents(False)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_2.addWidget(self.label_7)
        spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(150, 0))
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.GNUradio_file_text = QtWidgets.QLineEdit(self.centralwidget)
        self.GNUradio_file_text.setObjectName("GNUradio_file_text")
        self.horizontalLayout_4.addWidget(self.GNUradio_file_text)
        self.select_gnu_path_btn = QtWidgets.QPushButton(self.centralwidget)
        self.select_gnu_path_btn.setObjectName("select_gnu_path_btn")
        self.horizontalLayout_4.addWidget(self.select_gnu_path_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(150, 0))
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_5.addWidget(self.label_8)
        self.data_file_text = QtWidgets.QLineEdit(self.centralwidget)
        self.data_file_text.setObjectName("data_file_text")
        self.horizontalLayout_5.addWidget(self.data_file_text)
        self.select_save_path_btn = QtWidgets.QPushButton(self.centralwidget)
        self.select_save_path_btn.setObjectName("select_save_path_btn")
        self.horizontalLayout_5.addWidget(self.select_save_path_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(150, 0))
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_6.addWidget(self.label_9)
        self.tran_data_file_text = QtWidgets.QLineEdit(self.centralwidget)
        self.tran_data_file_text.setObjectName("tran_data_file_text")
        self.horizontalLayout_6.addWidget(self.tran_data_file_text)
        self.select_source_path_btn = QtWidgets.QPushButton(self.centralwidget)
        self.select_source_path_btn.setObjectName("select_source_path_btn")
        self.horizontalLayout_6.addWidget(self.select_source_path_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.tran_kind_box = QtWidgets.QComboBox(self.centralwidget)
        self.tran_kind_box.setObjectName("tran_kind_box")
        self.tran_kind_box.addItem("")
        self.tran_kind_box.addItem("")
        self.horizontalLayout.addWidget(self.tran_kind_box)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.tran_address_text = QtWidgets.QLineEdit(self.centralwidget)
        self.tran_address_text.setObjectName("tran_address_text")
        self.horizontalLayout.addWidget(self.tran_address_text)
        self.f_tran_ad_btn = QtWidgets.QPushButton(self.centralwidget)
        self.f_tran_ad_btn.setObjectName("f_tran_ad_btn")
        self.horizontalLayout.addWidget(self.f_tran_ad_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem4 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.rece_kind_box = QtWidgets.QComboBox(self.centralwidget)
        self.rece_kind_box.setObjectName("rece_kind_box")
        self.rece_kind_box.addItem("")
        self.rece_kind_box.addItem("")
        self.horizontalLayout_2.addWidget(self.rece_kind_box)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.rece_address_text = QtWidgets.QLineEdit(self.centralwidget)
        self.rece_address_text.setObjectName("rece_address_text")
        self.horizontalLayout_2.addWidget(self.rece_address_text)
        self.f_rece_ad_btn = QtWidgets.QPushButton(self.centralwidget)
        self.f_rece_ad_btn.setObjectName("f_rece_ad_btn")
        self.horizontalLayout_2.addWidget(self.f_rece_ad_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem5 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem5)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem6)
        self.only_tran_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.only_tran_btn.sizePolicy().hasHeightForWidth())
        self.only_tran_btn.setSizePolicy(sizePolicy)
        self.only_tran_btn.setMinimumSize(QtCore.QSize(30, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.only_tran_btn.setFont(font)
        self.only_tran_btn.setObjectName("only_tran_btn")
        self.horizontalLayout_7.addWidget(self.only_tran_btn)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem7)
        self.rece_tran_btn = QtWidgets.QPushButton(self.centralwidget)
        self.rece_tran_btn.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.rece_tran_btn.setFont(font)
        self.rece_tran_btn.setObjectName("rece_tran_btn")
        self.horizontalLayout_7.addWidget(self.rece_tran_btn)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem8)
        self.only_rece_btn = QtWidgets.QPushButton(self.centralwidget)
        self.only_rece_btn.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.only_rece_btn.setFont(font)
        self.only_rece_btn.setObjectName("only_rece_btn")
        self.horizontalLayout_7.addWidget(self.only_rece_btn)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem9)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.tran_model_box = QtWidgets.QComboBox(self.centralwidget)
        self.tran_model_box.setObjectName("tran_model_box")
        self.tran_model_box.addItem("")
        self.tran_model_box.addItem("")
        self.tran_model_box.addItem("")
        self.tran_model_box.addItem("")
        self.tran_model_box.addItem("")
        self.tran_model_box.addItem("")
        self.tran_model_box.addItem("")
        self.tran_model_box.addItem("")
        self.horizontalLayout_3.addWidget(self.tran_model_box)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        spacerItem10 = QtWidgets.QSpacerItem(20, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem10)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_3.addWidget(self.textBrowser)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "hackrf_usrp"))
        self.label_7.setText(_translate("MainWindow", "HackRF和USRP信号自动收发"))
        self.label.setText(_translate("MainWindow", "GNUradio_bin路径:"))
        self.select_gnu_path_btn.setText(_translate("MainWindow", "选择"))
        self.label_8.setText(_translate("MainWindow", "数据存储文件路径:"))
        self.select_save_path_btn.setText(_translate("MainWindow", "选择"))
        self.label_9.setText(_translate("MainWindow", "发射文件路径:"))
        self.select_source_path_btn.setText(_translate("MainWindow", "选择"))
        self.label_3.setText(_translate("MainWindow", "发射机类型:"))
        self.tran_kind_box.setItemText(0, _translate("MainWindow", "hackrf"))
        self.tran_kind_box.setItemText(1, _translate("MainWindow", "usrp"))
        self.label_5.setText(_translate("MainWindow", "发射机地址:"))
        self.f_tran_ad_btn.setText(_translate("MainWindow", "查询地址"))
        self.label_4.setText(_translate("MainWindow", "接收机类型:"))
        self.rece_kind_box.setItemText(0, _translate("MainWindow", "hackrf"))
        self.rece_kind_box.setItemText(1, _translate("MainWindow", "usrp"))
        self.label_6.setText(_translate("MainWindow", "接收机地址:"))
        self.f_rece_ad_btn.setText(_translate("MainWindow", "查询地址"))
        self.only_tran_btn.setText(_translate("MainWindow", "仅发送"))
        self.rece_tran_btn.setText(_translate("MainWindow", "收发"))
        self.only_rece_btn.setText(_translate("MainWindow", "仅接收"))
        self.label_2.setText(_translate("MainWindow", "信号调制类型："))
        self.tran_model_box.setItemText(0, _translate("MainWindow", "GMSK"))
        self.tran_model_box.setItemText(1, _translate("MainWindow", "BPSK"))
        self.tran_model_box.setItemText(2, _translate("MainWindow", "QPSK"))
        self.tran_model_box.setItemText(3, _translate("MainWindow", "8PSK"))
        self.tran_model_box.setItemText(4, _translate("MainWindow", "QAM8"))
        self.tran_model_box.setItemText(5, _translate("MainWindow", "QAM16"))
        self.tran_model_box.setItemText(6, _translate("MainWindow", "QAM64"))
        self.tran_model_box.setItemText(7, _translate("MainWindow", "others"))

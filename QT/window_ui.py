# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(787, 646)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.GNUradio_file_text = QtWidgets.QLineEdit(self.centralwidget)
        self.GNUradio_file_text.setGeometry(QtCore.QRect(180, 70, 501, 24))
        self.GNUradio_file_text.setObjectName("GNUradio_file_text")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 70, 141, 21))
        self.label.setObjectName("label")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setEnabled(True)
        self.label_7.setGeometry(QtCore.QRect(320, 20, 211, 51))
        self.label_7.setLineWidth(1)
        self.label_7.setTextFormat(QtCore.Qt.AutoText)
        self.label_7.setScaledContents(False)
        self.label_7.setObjectName("label_7")
        self.tran_address_text = QtWidgets.QLineEdit(self.centralwidget)
        self.tran_address_text.setGeometry(QtCore.QRect(310, 190, 371, 24))
        self.tran_address_text.setObjectName("tran_address_text")
        self.rece_address_text = QtWidgets.QLineEdit(self.centralwidget)
        self.rece_address_text.setGeometry(QtCore.QRect(310, 240, 371, 24))
        self.rece_address_text.setObjectName("rece_address_text")
        self.only_tran_btn = QtWidgets.QPushButton(self.centralwidget)
        self.only_tran_btn.setGeometry(QtCore.QRect(40, 280, 121, 51))
        self.only_tran_btn.setObjectName("only_tran_btn")
        self.rece_tran_btn = QtWidgets.QPushButton(self.centralwidget)
        self.rece_tran_btn.setGeometry(QtCore.QRect(210, 280, 121, 51))
        self.rece_tran_btn.setObjectName("rece_tran_btn")
        self.only_rece_btn = QtWidgets.QPushButton(self.centralwidget)
        self.only_rece_btn.setGeometry(QtCore.QRect(390, 280, 121, 51))
        self.only_rece_btn.setObjectName("only_rece_btn")
        self.f_tran_ad_btn = QtWidgets.QPushButton(self.centralwidget)
        self.f_tran_ad_btn.setGeometry(QtCore.QRect(690, 190, 93, 28))
        self.f_tran_ad_btn.setObjectName("f_tran_ad_btn")
        self.f_rece_ad_btn = QtWidgets.QPushButton(self.centralwidget)
        self.f_rece_ad_btn.setGeometry(QtCore.QRect(690, 240, 93, 28))
        self.f_rece_ad_btn.setObjectName("f_rece_ad_btn")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 240, 269, 23))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.rece_kind_box = QtWidgets.QComboBox(self.layoutWidget)
        self.rece_kind_box.setObjectName("rece_kind_box")
        self.rece_kind_box.addItem("")
        self.rece_kind_box.addItem("")
        self.horizontalLayout_2.addWidget(self.rece_kind_box)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(30, 190, 269, 23))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.tran_kind_box = QtWidgets.QComboBox(self.layoutWidget1)
        self.tran_kind_box.setObjectName("tran_kind_box")
        self.tran_kind_box.addItem("")
        self.tran_kind_box.addItem("")
        self.horizontalLayout.addWidget(self.tran_kind_box)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 350, 771, 241))
        self.textBrowser.setObjectName("textBrowser")
        self.data_file_text = QtWidgets.QLineEdit(self.centralwidget)
        self.data_file_text.setGeometry(QtCore.QRect(180, 110, 501, 24))
        self.data_file_text.setObjectName("data_file_text")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(40, 110, 141, 21))
        self.label_8.setObjectName("label_8")
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(540, 290, 185, 23))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.tran_model_box = QtWidgets.QComboBox(self.layoutWidget2)
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
        self.tran_data_file_text = QtWidgets.QLineEdit(self.centralwidget)
        self.tran_data_file_text.setGeometry(QtCore.QRect(180, 150, 501, 24))
        self.tran_data_file_text.setObjectName("tran_data_file_text")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(40, 150, 141, 21))
        self.label_9.setObjectName("label_9")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 787, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "hackrf_usrp"))
        self.label.setText(_translate("MainWindow", "GNUradio_bin路径:"))
        self.label_7.setText(_translate("MainWindow", "HackRF和USRP信号自动收发"))
        self.only_tran_btn.setText(_translate("MainWindow", "仅发送"))
        self.rece_tran_btn.setText(_translate("MainWindow", "收发"))
        self.only_rece_btn.setText(_translate("MainWindow", "仅接收"))
        self.f_tran_ad_btn.setText(_translate("MainWindow", "查询地址"))
        self.f_rece_ad_btn.setText(_translate("MainWindow", "查询地址"))
        self.label_4.setText(_translate("MainWindow", "接收机类型:"))
        self.rece_kind_box.setItemText(0, _translate("MainWindow", "hackrf"))
        self.rece_kind_box.setItemText(1, _translate("MainWindow", "usrp"))
        self.label_6.setText(_translate("MainWindow", "接收机地址:"))
        self.label_3.setText(_translate("MainWindow", "发射机类型:"))
        self.tran_kind_box.setItemText(0, _translate("MainWindow", "hackrf"))
        self.tran_kind_box.setItemText(1, _translate("MainWindow", "usrp"))
        self.label_5.setText(_translate("MainWindow", "发射机地址:"))
        self.label_8.setText(_translate("MainWindow", "数据存储文件路径:"))
        self.label_2.setText(_translate("MainWindow", "信号调制类型："))
        self.tran_model_box.setItemText(0, _translate("MainWindow", "GMSK"))
        self.tran_model_box.setItemText(1, _translate("MainWindow", "BPSK"))
        self.tran_model_box.setItemText(2, _translate("MainWindow", "QPSK"))
        self.tran_model_box.setItemText(3, _translate("MainWindow", "8PSK"))
        self.tran_model_box.setItemText(4, _translate("MainWindow", "QAM8"))
        self.tran_model_box.setItemText(5, _translate("MainWindow", "QAM16"))
        self.tran_model_box.setItemText(6, _translate("MainWindow", "QAM64"))
        self.tran_model_box.setItemText(7, _translate("MainWindow", "others"))
        self.label_9.setText(_translate("MainWindow", "发射文件路径:"))

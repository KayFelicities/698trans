# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore
from PyQt4 import QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_Kaytest(object):

    def setupUi(self, Kaytest):
        Kaytest.setObjectName(_fromUtf8("Kaytest"))
        Kaytest.resize(462, 568)
        self.centralwidget = QtGui.QWidget(Kaytest)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.input_box = QtGui.QTextEdit(self.centralwidget)
        self.input_box.setGeometry(QtCore.QRect(10, 20, 441, 81))
        self.input_box.setObjectName(_fromUtf8("input_box"))
        self.output_box = QtGui.QTextEdit(self.centralwidget)
        self.output_box.setEnabled(True)
        self.output_box.setGeometry(QtCore.QRect(10, 150, 441, 371))
        self.output_box.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.output_box.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.output_box.setAutoFillBackground(False)
        self.output_box.setObjectName(_fromUtf8("output_box"))
        self.translate_button = QtGui.QPushButton(self.centralwidget)
        self.translate_button.setGeometry(QtCore.QRect(100, 110, 75, 23))
        self.translate_button.setObjectName(_fromUtf8("translate_button"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 0, 81, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("微软雅黑"))
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 81, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("微软雅黑"))
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.clear_button = QtGui.QPushButton(self.centralwidget)
        self.clear_button.setGeometry(QtCore.QRect(260, 110, 75, 23))
        self.clear_button.setObjectName(_fromUtf8("clear_button"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(40, 520, 371, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("微软雅黑"))
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        Kaytest.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Kaytest)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 462, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        Kaytest.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(Kaytest)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Kaytest.setStatusBar(self.statusbar)

        self.retranslateUi(Kaytest)
        QtCore.QObject.connect(self.translate_button, QtCore.SIGNAL(
            _fromUtf8("clicked()")), self.output_box.paste)
        QtCore.QObject.connect(self.clear_button, QtCore.SIGNAL(
            _fromUtf8("clicked()")), self.input_box.clear)
        QtCore.QObject.connect(self.clear_button, QtCore.SIGNAL(
            _fromUtf8("clicked()")), self.output_box.clear)
        QtCore.QMetaObject.connectSlotsByName(Kaytest)

    def retranslateUi(self, Kaytest):
        Kaytest.setWindowTitle(_translate("Kaytest", "698报文解析工具_V1.1  终端开发部内测版(2016.11.17)", None))
        self.translate_button.setText(_translate("Kaytest", "解析", None))
        self.label.setText(_translate("Kaytest", "输入报文：", None))
        self.label_3.setText(_translate("Kaytest", "解析结果：", None))
        self.clear_button.setText(_translate("Kaytest", "清空", None))
        self.label_5.setText(_translate(
            "Kaytest", "Copyright(C), 2005-2020,Sanxing Medical & Electric Co.,Ltd.", None))

import config
from shared_functions import *  # NOQA
import link_layer
import data_translate
import communication
import param
from PyQt4 import QtCore
from PyQt4 import QtGui
from task_window import Ui_TaskWindow


class TaskWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_TaskWindow):
    def __init__(self):
        super(TaskWindow, self).__init__()
        self.setupUi(self)
        self.res_b.clicked.connect(self.clear_res)

    def clear_res(self):
        self.res_b.setText('')

    def read_res(self, re_text):
        res = param.read_set_dar(re_text)
        if res == 'ok':
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
        else:
            self.res_b.setStyleSheet('color: red')
            self.res_b.setText('失败：' + res)
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(config.serial_window.re_text_to_box)

    def read_res_SA(self, re_text):
        res = param.read_set_dar(re_text)
        if res == 'ok':
            config.serial_window.SA_box.setText(self.SA_box.text())
            config.serial_window.SA_len_box.setText(str(len(self.SA_box.text()) // 2))
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
        else:
            self.res_b.setStyleSheet('color: red')
            self.res_b.setText('失败：' + res)
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(config.serial_window.re_text_to_box)

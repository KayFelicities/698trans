'''main'''
import sys
import os
import config
from PyQt4 import QtGui
sys.path.append('UI\\')
from trans_ui import TransWindow
from serial_ui import SerialWindow
from menu_ui import ConfigWindow
from param_ui import ParamWindow
from task_ui import TaskWindow
from about_ui import AboutWindow

if __name__ == "__main__":
    APP = QtGui.QApplication(sys.argv)
    config.trans_window = TransWindow()
    config.serial_window = SerialWindow()
    config.about_window = AboutWindow()
    config.config_window = ConfigWindow()
    config.param_window = ParamWindow()
    config.task_window = TaskWindow()
    # config.trans_window.show()
    config.serial_window.show()
    # config.param_window.show()
    # config.task_window.show()
    APP.exec_()
    # print('window close')
    # config.serial_check = False
    # config.socket_check = False
    # config.server_check = False
    os._exit(0)

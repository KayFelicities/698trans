from PyQt4 import QtGui
import sys
import config
import os
sys.path.append('UI\\')
from trans_ui import *   # NOQA
from serial_ui import *   # NOQA
from menu_ui import *   # NOQA
from param_ui import *   # NOQA
from task_ui import *   # NOQA
from about_ui import *  # NOQA

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
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
    app.exec_()
    # print('window close')
    # config.serial_check = False
    # config.socket_check = False
    # config.server_check = False
    os._exit(0)

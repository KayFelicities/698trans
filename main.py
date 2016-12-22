import config
from PyQt4 import QtGui
import sys
sys.path.append('UI\\')
from trans_ui import *   # NOQA
from serial_ui import *   # NOQA
from menu_ui import *   # NOQA

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    config.trans_window = TransWindow()
    config.serial_window = SerialWindow()
    config.about_window = AboutWindow()
    config.config_window = ConfigWindow()
    config.trans_window.show()
    app.exec_()
    # print('window close')
    config.serial_check = False

import config
from PyQt4 import QtGui
import sys
sys.path.append('UI\\')
from ui import *   # NOQA

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    config.trans_child = TransWindow()
    config.serial_child = SerialWindow()
    config.trans_child.show()
    app.exec_()
    # print('window close')
    config.serial_check = False

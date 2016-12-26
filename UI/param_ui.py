import config
from PyQt4 import QtCore
from PyQt4 import QtGui
from param_window import Ui_ParamWindow


class ParamWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_ParamWindow):
    def __init__(self):
        super(ParamWindow, self).__init__()
        self.setupUi(self)
        self.DT_read_b.clicked.connect(self.DT_read)
        self.DT_set_b.clicked.connect(self.DT_set)
        self.DT_set_now_b.clicked.connect(self.DT_set_now)

    def DT_read(self):
        pass

    def DT_set(self):
        pass

    def DT_set_now(self):
        pass

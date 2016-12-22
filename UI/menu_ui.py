import config
from PyQt4 import QtCore
from PyQt4 import QtGui
from about_window import Ui_AboutWindow
from config_window import Ui_ConfigWindow


class AboutWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_AboutWindow):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.setupUi(self)


class ConfigWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_ConfigWindow):
    def __init__(self):
        super(ConfigWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowStaysOnTopHint)
        self.ok_b.clicked.connect(self.ok_quit)
        self.reset_b.clicked.connect(self.reset)
        self.cancel_b.clicked.connect(self.hide)

    def read_param(self):
        self.baud_rate_box.setText(str(config.serial_param['baudrate']))
        self.IP_box.setText(config.socket_param['IP'])
        self.port_box.setText(str(config.socket_param['port']))

    def ok_quit(self):
        baudrate = self.baud_rate_box.text().replace(' ', '')
        if len(baudrate) > 0:
            try:
                config.serial_param['baudrate'] = int(baudrate)
            except Exception as e:
                print(e)
        IP = self.IP_box.text().replace(' ', '')
        if IP.count('.') == 3:
            config.socket_param['IP'] = IP
        port = self.port_box.text().replace(' ', '')
        if len(baudrate) > 0:
            try:
                config.socket_param['port'] = int(port)
            except Exception as e:
                print(e)
        self.hide()

    def reset(self):
        self.baud_rate_box.setText('9600')
        self.IP_box.setText('121.40.80.159')
        self.port_box.setText('20084')

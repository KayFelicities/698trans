import config
from PyQt4 import QtCore
from PyQt4 import QtGui
import serial
import serial.tools.list_ports
import binascii
import sys
sys.path.append('UI\\')
from shared_functions import *  # NOQA
from link_layer import *  # NOQA
from apdu import *  # NOQA
from about_window import Ui_AboutWindow
from main_window import Ui_MainWindow
from serial_mode_window import Ui_SerialWindow


class MainWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.child = AboutWindow()
        self.translate_button.clicked.connect(self.trans_botton)
        self.clear_button.clicked.connect(self.clear_botton)
        self.show_level.clicked.connect(self.show_level_check_box)
        self.always_top.clicked.connect(self.always_top_check_box)
        self.input_box.textChanged.connect(self.calc_len_box)
        self.about.triggered.connect(self.show_about_window)
        config.show_level = self.show_level.isChecked()

    def trans_botton(self):
        input_text = self.input_box.toPlainText()
        if 1:  # 0 for debug
            try:
                all_translate(input_text)
            except Exception:
                output('报文解析过程出现问题，请检查报文。若报文无问题请反馈665593，谢谢！')
        else:
            all_translate(input_text)
        self.output_box.setText(config.output_text)
        config.output_text = ''

    def clear_botton(self):
        self.input_box.setFocus()

    def show_level_check_box(self):
        config.show_level = self.show_level.isChecked()
        self.trans_botton()

    def always_top_check_box(self):
        if (self.always_top.isChecked() is True):
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(QtCore.Qt.Widget)
            self.show()

    def calc_len_box(self):
        input_text = self.input_box.toPlainText()
        input_len = calc_len(input_text)
        self.len_box.setText(input_len)
        # self.crc_box.setText(crc_calc)

    def show_about_window(self):
        self.child.show()


class SerialWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_SerialWindow):
    def __init__(self):
        super(SerialWindow, self).__init__()
        self.setupUi(self)
        self.child = AboutWindow()
        self.send_input_box.textChanged.connect(self.send_trans)
        self.receive_input_box.textChanged.connect(self.receive_trans)
        self.send_clear_button.clicked.connect(self.send_clear_botton)
        self.open_button.clicked.connect(self.open_serial)
        self.close_button.clicked.connect(self.close_serial)
        self.send_button.clicked.connect(self.send_data)
        self.show_level.clicked.connect(self.show_level_check_box)
        self.always_top.clicked.connect(self.always_top_check_box)
        self.send_input_box.textChanged.connect(self.calc_len_box)
        self.about.triggered.connect(self.show_about_window)
        config.show_level = self.show_level.isChecked()
        self.com_list.addItems(self.port_list())

    def port_list(self):
        com_List = []
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            com_List.append(port[0])
        return com_List

    def open_serial(self):
        config.serial = serial.Serial()
        config.serial.port = self.com_list.currentText()
        config.serial.baudrate = 115200
        config.serial.bytesize = 8
        config.serial.parity = 'E'
        config.serial.stopbits = 1
        try:
            config.serial.open()
            print(config.serial.isOpen())
            self.open_button.setText(self.com_list.currentText() + '已打开')
            self.close_button.setText('关闭')
        except Exception:
            self.open_button.setText(self.com_list.currentText() + '打开失败')
            self.close_button.setText('关闭')

    def close_serial(self):
        config.serial.close()
        self.close_button.setText(self.com_list.currentText() + '已关闭')
        self.open_button.setText('打开')

    def send_data(self):
        input_text = self.send_input_box.toPlainText()
        send_d = '0001020304'
        config.serial.write(eval(send_d))

    def send_trans(self):
        input_text = self.send_input_box.toPlainText()
        if 1:  # 0 for debug
            try:
                all_translate(input_text)
            except Exception:
                output('报文解析过程出现问题，请检查报文。若报文无问题请反馈665593，谢谢！')
        else:
            all_translate(input_text)
        self.send_output_box.setText(config.output_text)
        config.output_text = ''

    def receive_trans(self):
        input_text = self.receive_input_box.toPlainText()
        if 1:  # 0 for debug
            try:
                all_translate(input_text)
            except Exception:
                output('报文解析过程出现问题，请检查报文。若报文无问题请反馈665593，谢谢！')
        else:
            all_translate(input_text)
        self.receive_output_box.setText(config.output_text)
        config.output_text = ''

    def send_clear_botton(self):
        self.send_input_box.setFocus()

    def show_level_check_box(self):
        config.show_level = self.show_level.isChecked()
        self.send_trans()
        self.receive_trans()

    def always_top_check_box(self):
        if (self.always_top.isChecked() is True):
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(QtCore.Qt.Widget)
            self.show()

    def calc_len_box(self):
        input_text = self.send_input_box.toPlainText()
        input_len = calc_len(input_text)
        self.send_button.setText('发送（' + input_len + '）')
        # self.crc_box.setText(crc_calc)

    def show_about_window(self):
        self.child.show()


class AboutWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_AboutWindow):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.setupUi(self)


def all_translate(input_text):
    offset = 0
    if len(input_text) < 5:
        output('请输入698报文')
        return
    data = data_format(input_text)
    data_check = check_data(data)
    if data_check == 'ok':
        offset += take_link_layer_1(data[offset:])
        offset += take_APDU(data[offset:])  # 解应用层
        offset += take_link_layer_2(data[0:], offset)  # 处理链路层末尾
    elif data_check == 'format_error':  # 格式错误，尝试解apdu
        offset += take_APDU(data[offset:])  # 解应用层
    else:
        output('报文非法')
        return

    if offset != len(data):
        print('offset, len(data): ', offset, len(data))
        output('报文解析过程出现问题，请检查报文。若报文无问题请反馈665593，谢谢！')
    return offset


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myUI = SerialWindow()
    myUI.show()
    sys.exit(app.exec_())

import config
from PyQt4 import QtCore
from PyQt4 import QtGui
import serial
import serial.tools.list_ports
import struct
import sys
import threading
import time
sys.path.append('UI\\')
from shared_functions import *  # NOQA
from link_layer import *  # NOQA
from apdu import *  # NOQA
from about_window import Ui_AboutWindow
from trans_window import Ui_TransWindow
from serial_window import Ui_SerialWindow


class TransWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_TransWindow):
    def __init__(self):
        super(TransWindow, self).__init__()
        self.setupUi(self)
        config.show_level = self.show_level.isChecked()
        config.auto_trans = self.auto_trans.isChecked()
        self.about_child = AboutWindow()
        if config.auto_trans is True:
            self.input_box.textChanged.connect(self.start_trans)
            self.translate_button.setVisible(False)
        else:
            self.input_box.textChanged.disconnect(self.start_trans)
            self.translate_button.setVisible(True)
        self.translate_button.clicked.connect(self.start_trans)
        self.clear_button.clicked.connect(self.clear_box)
        self.show_level.clicked.connect(self.show_level_check_box)
        self.auto_trans.clicked.connect(self.auto_trans_check_box)
        self.always_top.clicked.connect(self.always_top_check_box)
        self.input_box.textChanged.connect(self.calc_len_box)
        self.about.triggered.connect(self.show_about_window)
        self.serial_mode_button.clicked.connect(self.shift_serial_window)

    def start_trans(self):
        input_text = self.input_box.toPlainText()
        try:
            all_translate(input_text)
        except Exception as e:
            print(e)
            output('\n\n报文解析过程出现问题，请检查报文。若报文无问题请反馈665593，谢谢！')
        self.output_box.setText(config.output_text)
        config.output_text = ''

    def clear_box(self):
        self.input_box.setFocus()

    def show_level_check_box(self):
        config.show_level = self.show_level.isChecked()
        self.start_trans()

    def auto_trans_check_box(self):
        config.auto_trans = self.auto_trans.isChecked()
        if config.auto_trans is True:
            self.input_box.textChanged.connect(self.start_trans)
            self.translate_button.setVisible(False)
        else:
            self.input_box.textChanged.disconnect(self.start_trans)
            self.translate_button.setVisible(True)
        self.start_trans()

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
        self.clear_button.setText('清空' + input_len)

    def show_about_window(self):
        self.about_child.show()

    def shift_serial_window(self):
        self.hide()
        config.serial_child.show()


class SerialWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_SerialWindow):
    _receive_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(SerialWindow, self).__init__()
        self.setupUi(self)
        self.about_child = AboutWindow()
        config.show_level = self.show_level.isChecked()
        self._receive_signal.connect(self.take_receive_data)
        config.auto_trans = self.auto_trans.isChecked()
        if config.auto_trans is True:
            self.send_input_box.textChanged.connect(self.send_trans)
        else:
            self.send_input_box.textChanged.disconnect(self.send_trans)
        self.receive_input_box.textChanged.connect(self.receive_trans)
        self.send_clear_button.clicked.connect(self.send_clear_botton)
        self.open_button.clicked.connect(self.open_serial)
        self.close_button.clicked.connect(self.close_serial)
        self.send_button.clicked.connect(self.send_data)
        self.show_level.clicked.connect(self.show_level_check_box)
        self.always_top.clicked.connect(self.always_top_check_box)
        self.auto_trans.clicked.connect(self.auto_trans_check_box)
        self.send_input_box.textChanged.connect(self.calc_len_box)
        self.com_list.addItems(self.port_list())
        self.about.triggered.connect(self.show_about_window)
        self.trans_mode_button.clicked.connect(self.shift_trans_window)

    def serial_run(self):
        while True:
            try:
                data_wait = config.serial.inWaiting()
            except Exception:
                print('serial_run quit')
                break
            re_text = ''
            while data_wait > 0:
                re_data = config.serial.readline()
                for re_char in re_data:
                    re_text += '{0:02X} '.format(re_char)
                time.sleep(0.03)
                data_wait = config.serial.inWaiting()
            if re_text != '':
                self._receive_signal.emit(re_text)
            if config.serial_check is False:
                print('serial_run quit')
                break

    def take_receive_data(self, re_text):
        self.receive_input_box.setText(re_text)

    def port_list(self):
        com_List = []
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            com_List.append(port[0])
        return com_List

    def open_serial(self):
        try:
            config.serial = serial.Serial(self.com_list.currentText(), 9600, 8, 'E', 1, timeout=0.05)
            config.serial.close()
            config.serial.open()
            config.serial_check = True
            threading.Thread(target=self.serial_run).start()
            self.open_button.setText(self.com_list.currentText() + '已打开')
            self.close_button.setText('关闭')
            self.calc_len_box()
        except Exception:
            self.open_button.setText(self.com_list.currentText() + '打开失败')
            self.close_button.setText('关闭')

    def close_serial(self):
        config.serial.close()
        self.close_button.setText(self.com_list.currentText() + '已关闭')
        self.open_button.setText('打开')
        self.send_button.setText('请打开串口')

    def send_data(self):
        input_text = self.send_input_box.toPlainText()
        data = data_format(input_text)
        send_d = b''
        for char in data:
            send_d += struct.pack('B', int(char, 16))
        config.serial.write(send_d)

    def auto_trans_check_box(self):
        config.auto_trans = self.auto_trans.isChecked()
        if config.auto_trans is True:
            self.send_input_box.textChanged.connect(self.send_trans)
        else:
            self.send_input_box.textChanged.disconnect(self.send_trans)
        self.send_trans()

    def send_trans(self):
        input_text = self.send_input_box.toPlainText()
        if 1:  # 0 for debug
            try:
                all_translate(input_text)
            except Exception:
                output('\n\n报文解析过程出现问题，请检查报文。若报文无问题请反馈665593，谢谢！')
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
                output('\n\n报文解析过程出现问题，请检查报文。若报文无问题请反馈665593，谢谢！')
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

    def show_about_window(self):
        self.about_child.show()

    def shift_trans_window(self):
        self.hide()
        config.trans_child.show()


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
        output('\n\n报文解析过程出现问题，请检查报文。若报文无问题请反馈665593，谢谢！')
    return offset


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    config.trans_child = TransWindow()
    config.serial_child = SerialWindow()
    config.trans_child.show()
    app.exec_()
    # print('window close')
    config.serial_check = False

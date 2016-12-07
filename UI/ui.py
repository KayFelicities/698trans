import config
from PyQt4 import QtCore
from PyQt4 import QtGui
import serial
import serial.tools.list_ports
import struct
import threading
import time
import traceback
from shared_functions import *  # NOQA
from link_layer import *  # NOQA
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
        len_message = str(input_len) + '字节(' + str(hex(input_len)) + ')'
        self.clear_button.setText('清空（' + len_message + '）')

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
            self.translate_button.setVisible(False)
        else:
            self.send_input_box.textChanged.disconnect(self.send_trans)
            self.translate_button.setVisible(True)
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
        config.serial_check = False
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
            self.translate_button.setVisible(False)
        else:
            self.send_input_box.textChanged.disconnect(self.send_trans)
            self.translate_button.setVisible(True)
        self.send_trans()

    def send_trans(self):
        input_text = self.send_input_box.toPlainText()
        try:
            input_type, server_addr, server_addr_len, client_addr = all_translate(input_text)
            if input_type == 'full':
                self.server_addr_box.setText(server_addr)
                self.server_addr_len_box.setText(server_addr_len)
                self.client_addr_box.setText(client_addr)
            elif input_type == 'apdu':
                input_text = self.add_link_layer(input_text)
                self.send_input_box.setText(input_text)

        except Exception as e:
            print(e)
            traceback.print_exc()
            output('\n\n报文解析过程出现问题，请检查报文。若报文无问题请反馈665593，谢谢！')
        self.send_output_box.setText(config.output_text)
        config.output_text = ''

    def add_link_layer(self, input_text):
        apdu_start = '68 '
        C = '43 '
        server_addr = self.server_addr_box.text()
        print('server_addr', server_addr)
        server_addr_len = int(self.server_addr_len_box.text())
        server_addr_data = data_format(server_addr)
        for count in range(server_addr_len):
            server_addr_data.insert(0, '00')
        server_addr_text_list = server_addr_data[-server_addr_len:]
        print(server_addr_text_list)
        server_addr_text = ''
        for server_addr_member in server_addr_text_list:
            server_addr_text += server_addr_member + ' '
        client_addr_text = self.client_addr_box.text() + ' '
        apdu_len = calc_len(input_text)
        full_len = 7 + server_addr_len + apdu_len + 2
        print(full_len)
        L = '{0:02X} {1:02X} '.format(full_len & 0xff, (full_len >> 8) & 0xff)  # 低位在前
        apdu_start += L + C + '{0:02X} '.format(server_addr_len - 1) + server_addr_text + client_addr_text
        hcs_data = data_format(apdu_start)
        hcs = get_fcs(hcs_data[1:], len(hcs_data) - 1)
        HCS = '{0:02X} {1:02X} '.format(full_len & 0xff, (hcs >> 8) & 0xff)  # 低位在前
        apdu_start += HCS

        fcs_data = data_format(apdu_start + input_text)
        fcs = get_fcs(fcs_data[1:], len(fcs_data) - 1)
        FCS = '{0:02X} {1:02X} '.format(full_len & 0xff, (fcs >> 8) & 0xff)  # 低位在前

        full_text = apdu_start + '\n' + input_text + '\n' + FCS + '16'
        return full_text

    def receive_trans(self):
        input_text = self.receive_input_box.toPlainText()
        try:
            all_translate(input_text)
        except Exception as e:
            print(e)
            output('\n\n报文解析过程出现问题，请检查报文。若报文无问题请反馈665593，谢谢！')
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
        len_message = str(input_len) + '字节(' + str(hex(input_len)) + ')'
        if config.serial_check is True:
            self.send_button.setText('发送（' + len_message + '）')
        else:
            self.send_button.setText('请打开串口')

    def show_about_window(self):
        self.about_child.show()

    def shift_trans_window(self):
        self.hide()
        config.trans_child.show()


class AboutWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_AboutWindow):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.setupUi(self)

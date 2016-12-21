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
from trans_ui import AboutWindow
from serial_window import Ui_SerialWindow


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
        self.quick_fix_button.clicked.connect(self.quick_fix)
        self.translate_button.clicked.connect(self.send_trans)
        self.send_clear_button.clicked.connect(self.send_clear_botton)
        self.receive_clear_button.clicked.connect(self.receive_clear_botton)
        self.open_button.clicked.connect(self.open_serial)
        self.close_button.clicked.connect(self.close_serial)
        self.send_button.clicked.connect(self.send_data)
        self.show_level.clicked.connect(self.set_level_visible)
        self.always_top.clicked.connect(self.set_always_top)
        self.auto_trans.clicked.connect(self.set_auto_trans)
        self.send_input_box.textChanged.connect(self.calc_send_box_len)
        self.receive_input_box.textChanged.connect(self.calc_receive_box_len)
        self.com_list.addItems(self.port_list())
        self.about.triggered.connect(self.show_about_window)
        self.trans_mode_button.clicked.connect(self.shift_trans_window)

    def port_list(self):
        com_List = []
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            com_List.append(port[0])
        return com_List

    def open_serial(self):
        if config.serial_check is False:
            try:
                config.serial = serial.Serial(self.com_list.currentText(), 9600, 8, 'E', 1, timeout=0.05)
                config.serial.close()
                config.serial.open()
                config.serial_check = True
                threading.Thread(target=self.serial_run).start()
                self.open_button.setText(self.com_list.currentText() + '已打开')
                self.close_button.setText('关闭')
                self.send_button.setEnabled(True)
                self.calc_send_box_len()
            except Exception as e:
                print(e)
                traceback.print_exc()
                self.open_button.setText(self.com_list.currentText() + '打开失败')
                self.close_button.setText('关闭')

    def close_serial(self):
        if config.serial_check is True:
            config.serial.close()
            config.serial_check = False
            self.open_button.setText('打开')
            self.send_button.setText('请打开串口')
            self.send_button.setEnabled(False)
            self.close_button.setText('刷新')
        else:
            self.com_list.clear()
            self.com_list.addItems(self.port_list())

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

    def send_data(self):
        input_text = self.send_input_box.toPlainText()
        data = data_format(input_text)
        send_d = b''
        for char in data:
            send_d += struct.pack('B', int(char, 16))
        config.serial.write(send_d)

    def take_receive_data(self, re_text):
        self.receive_input_box.setText(re_text)

    def quick_fix(self):
        self.send_trans()
        input_text = self.send_input_box.toPlainText()
        data_in = data_format(input_text)
        if config.good_L is not None:
            data_in[1], data_in[2] = config.good_L[0], config.good_L[1]
        else:
            if config.good_HCS is not None:
                ret_dict = get_addr(data_in)
                hcs_pos = 6 + int(ret_dict['server_addr_len'])
                data_in[hcs_pos], data_in[hcs_pos + 1] = config.good_HCS[0], config.good_HCS[1]
                input_text = ''
                for data in data_in:
                    input_text += data + ' '
                self.send_input_box.setText(input_text)
                self.send_trans()
            if config.good_FCS is not None:
                data_in[-3], data_in[-2] = config.good_FCS[0], config.good_FCS[1]
        input_text = ''
        for data in data_in:
            input_text += data + ' '
        self.send_input_box.setText(input_text)

    def send_trans(self):
        input_text = self.send_input_box.toPlainText()
        try:
            data_in = data_format(input_text)
            ret_dict = all_translate(data_in)
            if ret_dict['res'] == 'ok':
                if ret_dict['input_type'] == 'full':
                    if config.good_L is not None or config.good_HCS is not None or config.good_FCS is not None:  # 长度或校验错误
                        fix_type = '长度域' if config.good_L is not None else '校验码'
                        self.quick_fix_button.setText('修正' + fix_type)
                    else:
                        self.quick_fix_button.setText('修正格式')
                    addr_dict = get_addr(data_in)
                    self.server_addr_box.setText(addr_dict['server_addr'])
                    self.server_addr_len_box.setText(addr_dict['server_addr_len'])
                    self.client_addr_box.setText(addr_dict['client_addr'])
                elif ret_dict['input_type'] == 'apdu':
                    input_text = self.add_link_layer(input_text)
                    self.send_input_box.setText(input_text)
                    if config.auto_trans is True:
                        data_in = data_format(input_text)
                        all_translate(data_in)
        except Exception as e:
            print(e)
            traceback.print_exc()
            output('\n\n报文解析过程出现问题，请检查报文。若报文无问题请反馈665593，谢谢！')
        self.send_output_box.setText(config.output_text)
        config.output_text = ''

    def receive_trans(self):
        input_text = self.receive_input_box.toPlainText()
        try:
            data_in = data_format(input_text)
            all_translate(data_in)
        except Exception as e:
            print(e)
            output('\n\n报文解析过程出现问题，请检查报文。若报文无问题请反馈665593，谢谢！')
        self.receive_output_box.setText(config.output_text)
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
        server_addr_text_list.reverse()
        print('server_addr_text_list:', server_addr_text_list)
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
        # print('hcd_data:', hcs_data[1:], 'len:', len(hcs_data) - 1)
        hcs = get_fcs(hcs_data[1:], len(hcs_data) - 1)
        HCS = '{0:02X} {1:02X} '.format(hcs & 0xff, (hcs >> 8) & 0xff)  # 低位在前
        apdu_start += HCS

        fcs_data = data_format(apdu_start + input_text)
        fcs = get_fcs(fcs_data[1:], len(fcs_data) - 1)
        FCS = '{0:02X} {1:02X} '.format(fcs & 0xff, (fcs >> 8) & 0xff)  # 低位在前

        full_text = apdu_start + '\n' + input_text + '\n' + FCS + '16'
        return full_text

    def send_clear_botton(self):
        self.send_input_box.setFocus()

    def receive_clear_botton(self):
        self.receive_input_box.setFocus()

    def set_auto_trans(self):
        config.auto_trans = self.auto_trans.isChecked()
        if config.auto_trans is True:
            self.send_input_box.textChanged.connect(self.send_trans)
            self.translate_button.setVisible(False)
        else:
            self.send_input_box.textChanged.disconnect(self.send_trans)
            self.translate_button.setVisible(True)
        self.send_trans()

    def set_level_visible(self):
        config.show_level = self.show_level.isChecked()
        self.send_trans()
        self.receive_trans()

    def set_always_top(self):
        if (self.always_top.isChecked() is True):
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(QtCore.Qt.Widget)
            self.show()

    def calc_send_box_len(self):
        input_text = self.send_input_box.toPlainText()
        input_len = calc_len(input_text)
        len_message = str(input_len) + '字节(' + str(hex(input_len)) + ')'
        if config.serial_check is True:
            self.send_button.setText('发送（' + len_message + '）')
        else:
            self.send_button.setText('请打开串口')

    def calc_receive_box_len(self):
        input_text = self.receive_input_box.toPlainText()
        input_len = calc_len(input_text)
        len_message = str(input_len) + '字节(' + str(hex(input_len)) + ')'
        self.receive_clear_button.setText('清空（' + len_message + '）')

    def show_about_window(self):
        self.about_child.show()

    def shift_trans_window(self):
        self.hide()
        config.trans_child.show()

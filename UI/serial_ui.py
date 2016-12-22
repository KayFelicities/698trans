import config
from PyQt4 import QtCore
from PyQt4 import QtGui
import serial
import serial.tools.list_ports
import socket
import struct
import threading
import time
import traceback
from shared_functions import *  # NOQA
from link_layer import *  # NOQA
from serial_window import Ui_SerialWindow


class SerialWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_SerialWindow):
    _receive_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(SerialWindow, self).__init__()
        self.setupUi(self)
        config.show_level = self.show_level_cb.isChecked()
        self._receive_signal.connect(self.take_receive_data)
        config.auto_trans = self.auto_trans_cb.isChecked()
        if config.auto_trans is True:
            self.send_input_box.textChanged.connect(self.send_trans)
            self.translate_button.setVisible(False)
        else:
            self.send_input_box.textChanged.disconnect(self.send_trans)
            self.translate_button.setVisible(True)
        if config.auto_linklayer is True:
            self.fix_linklayer_button.setVisible(False)
        else:
            self.fix_linklayer_button.setVisible(True)
        self.fix_linklayer_button.clicked.connect(self.fix_linklayer)
        self.receive_input_box.textChanged.connect(self.receive_trans)
        self.quick_fix_button.clicked.connect(self.quick_fix)
        self.translate_button.clicked.connect(self.send_trans)
        self.send_clear_button.clicked.connect(self.send_clear_botton)
        self.receive_clear_button.clicked.connect(self.receive_clear_botton)
        self.connect_button.clicked.connect(self.connect)
        self.disconnect_button.clicked.connect(self.disconnect)
        self.send_button.clicked.connect(self.send_data)
        self.auto_linklayer_cb.clicked.connect(self.set_auto_linklayer)
        self.show_level_cb.clicked.connect(self.set_level_visible)
        self.always_top_cb.clicked.connect(self.set_always_top)
        self.auto_trans_cb.clicked.connect(self.set_auto_trans)
        self.send_input_box.textChanged.connect(self.calc_send_box_len)
        self.receive_input_box.textChanged.connect(self.calc_receive_box_len)
        self.com_list.addItems(self.port_list())
        self.about.triggered.connect(self.show_about_window)
        self.config.triggered.connect(self.show_config_window)
        self.trans_mode_button.clicked.connect(self.shift_trans_window)

    def port_list(self):
        com_List = []
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            com_List.append(port[0])
        com_List.append('前置机')
        return com_List

    def connect(self):
        if config.serial_check is False and config.socket_check is False:
            if self.com_list.currentText() == '前置机':
                self.connect_socket()
            else:
                self.connect_serial()

    def connect_socket(self):
        try:
            config.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            config.socket.connect((config.socket_param['IP'], config.socket_param['port']))
            config.socket_check = True
            threading.Thread(target=self.socket_run).start()
            self.connect_button.setText(self.com_list.currentText() + '已连接')
            self.disconnect_button.setText('断开')
            self.send_button.setEnabled(True)
            self.calc_send_box_len()
        except Exception:
            traceback.print_exc()
            self.connect_button.setText(self.com_list.currentText() + '连接失败')

    def connect_serial(self):
        try:
            config.serial = serial.Serial(
                self.com_list.currentText(),
                config.serial_param['baudrate'],
                config.serial_param['bytesize'],
                config.serial_param['parity'],
                config.serial_param['stopbits'],
                timeout=config.serial_param['timeout'])
            config.serial.close()
            config.serial.open()
            config.serial_check = True
            threading.Thread(target=self.serial_run).start()
            self.connect_button.setText(self.com_list.currentText() + '已连接')
            self.disconnect_button.setText('断开')
            self.send_button.setEnabled(True)
            self.calc_send_box_len()
        except Exception:
            traceback.print_exc()
            self.connect_button.setText(self.com_list.currentText() + '连接失败')

    def disconnect(self):
        if config.serial_check is True:
            self.close_serial()
        elif config.socket_check is True:
            self.close_socket()

    def close_serial(self):
        if config.serial_check is True:
            config.serial.close()
            config.serial_check = False
            self.connect_button.setText('连接')
            self.send_button.setText('请建立连接')
            self.send_button.setEnabled(False)
            self.disconnect_button.setText('刷新')
        else:  # 刷新列表
            self.com_list.clear()
            self.com_list.addItems(self.port_list())

    def close_socket(self):
        if config.socket_check is True:
            config.socket.close()
            config.socket_check = False
            self.connect_button.setText('连接')
            self.send_button.setText('请建立连接')
            self.send_button.setEnabled(False)
            self.disconnect_button.setText('刷新')
        else:  # 刷新列表
            self.com_list.clear()
            self.com_list.addItems(self.port_list())

    def serial_run(self):
        while True:
            try:
                data_wait = config.serial.inWaiting()
            except Exception:
                traceback.print_exc()
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

    def socket_run(self):
        while True:
            try:
                re_byte = config.socket.recv(4096)
                re_text = ''.join(['%02X ' % x for x in re_byte])
                print(re_text)
            except Exception:
                traceback.print_exc()
                break
            if re_text != '':
                self._receive_signal.emit(re_text)
            if config.socket_check is False:
                print('socket_run quit')
                break

    def send_data(self):
        input_text = self.send_input_box.toPlainText()
        data = data_format(input_text)
        send_d = b''
        for char in data:
            send_d += struct.pack('B', int(char, 16))
        if config.serial_check is True:
            config.serial.write(send_d)
        if config.socket_check is True:
            config.socket.sendall(send_d)

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
                hcs_pos = 6 + int(ret_dict['SA_len'])
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
                self.quick_fix_button.setText('修正校验码' if config.good_HCS is not None or config.good_FCS is not None else '修正格式')
                if ret_dict['input_type'] == 'full' and config.auto_linklayer is True:
                    if self.is_good_linklayer() is False:
                        self.fix_linklayer()
                        input_text = self.send_input_box.toPlainText()
                        data_in = data_format(input_text)
                        all_translate(data_in)
                elif ret_dict['input_type'] == 'apdu':
                    input_text = self.add_link_layer(input_text)
                    self.send_input_box.setText(input_text)
                    if config.auto_trans is True:
                        data_in = data_format(input_text)
                        all_translate(data_in)
            else:
                self.quick_fix_button.setText('修正长度域' if config.good_L is not None else '修正格式')
        except Exception:
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

    def is_good_linklayer(self):
        input_text = self.send_input_box.toPlainText()
        data_in = data_format(input_text)
        SA_type = self.SA_type_list.currentText()
        SA_len_h = {
            '单地址': 0,
            '通配地址': 1,
            '组地址': 2,
            '广播地址': 3,
        }[SA_type]
        if SA_len_h != ((int(data_in[4], 16) >> 4) & 0xf):
            print('SA_len_h', SA_len_h, (int(data_in[4], 16) >> 4) & 0xf)
            return False
        SA_len = int(data_in[4], 16) + 1
        if SA_len != int(self.SA_len_box.text()):
            return False
        SA_data_in = data_in[4 + SA_len: 4: -1]
        SA_box_data = data_format(self.SA_box.text())
        if SA_data_in != SA_box_data:
            print('SA_data_in', SA_data_in, SA_box_data)
            return False
        if data_in[5 + SA_len] != self.CA_box.text():
            print('data_in')
            return False
        return True

    def fix_linklayer(self):
        input_text = self.send_input_box.toPlainText()
        data_in = data_format(input_text)
        SA_len = int(data_in[4], 16) + 1
        apdu_in = data_in[5 + SA_len + 3: -3]
        apdu_text = ''
        for text in apdu_in:
            apdu_text += text + ' '
        print('apdu_text:', apdu_text)
        self.send_input_box.setText(self.add_link_layer(apdu_text))

    def add_link_layer(self, input_text):
        apdu_start = '68 '
        C = '43 '
        SA = self.SA_box.text()
        SA_len = int(self.SA_len_box.text())
        if SA_len > 16 or SA_len < 1:
            SA_len = 6
            self.SA_len_box.setText('6')
        SA_data = data_format(SA)
        SA_content = ''
        for count in range(SA_len):
            SA_data.insert(0, '00')
        SA_data = SA_data[-SA_len:]
        for SA_member in SA_data:
            SA_content += SA_member
        self.SA_box.setText(SA_content)
        SA_data.reverse()
        print('SA_data:', SA_data)
        SA_text = ''
        for SA_member in SA_data:
            SA_text += SA_member + ' '
        CA = data_format(self.CA_box.text())
        self.CA_box.setText(CA[-1])
        CA_text = CA[-1] + ' '
        apdu_len = calc_len(input_text)
        full_len = 7 + SA_len + apdu_len + 2
        print(full_len)
        SA_type = self.SA_type_list.currentText()
        SA_len_h = {
            '单地址': 0,
            '通配地址': 1,
            '组地址': 2,
            '广播地址': 3,
        }[SA_type]
        SA_ = ((SA_len_h << 6) | ((SA_len - 1) & 0xf)) & 0xff  # 地址类型、逻辑地址、地址长度
        # print('SA_len_h, SA_, SA_len:', SA_len_h, SA_, SA_len)
        L = '{0:02X} {1:02X} '.format(full_len & 0xff, (full_len >> 8) & 0xff)  # 低位在前
        apdu_start += L + C + '{0:02X} '.format(SA_) + SA_text + CA_text
        hcs_data = data_format(apdu_start)
        # print('hcd_data:', hcs_data[1:], 'len:', len(hcs_data) - 1)
        hcs = get_fcs(hcs_data[1:], len(hcs_data) - 1)
        HCS = '{0:02X} {1:02X} '.format(hcs & 0xff, (hcs >> 8) & 0xff)  # 低位在前
        apdu_start += HCS

        fcs_data = data_format(apdu_start + input_text)
        fcs = get_fcs(fcs_data[1:], len(fcs_data) - 1)
        FCS = '{0:02X} {1:02X} '.format(fcs & 0xff, (fcs >> 8) & 0xff)  # 低位在前

        full_text = apdu_start + input_text + FCS + '16'
        return full_text

    def send_clear_botton(self):
        self.send_input_box.setFocus()

    def receive_clear_botton(self):
        self.receive_input_box.setFocus()

    def set_auto_linklayer(self):
        config.auto_linklayer = self.auto_linklayer_cb.isChecked()
        if config.auto_linklayer is True:
            self.fix_linklayer_button.setVisible(False)
        else:
            self.fix_linklayer_button.setVisible(True)

    def set_auto_trans(self):
        config.auto_trans = self.auto_trans_cb.isChecked()
        if config.auto_trans is True:
            self.send_input_box.textChanged.connect(self.send_trans)
            self.translate_button.setVisible(False)
        else:
            self.send_input_box.textChanged.disconnect(self.send_trans)
            self.translate_button.setVisible(True)
        self.send_trans()

    def set_level_visible(self):
        config.show_level = self.show_level_cb.isChecked()
        self.send_trans()
        self.receive_trans()

    def set_always_top(self):
        if (self.always_top_cb.isChecked() is True):
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(QtCore.Qt.Widget)
            self.show()

    def calc_send_box_len(self):
        input_text = self.send_input_box.toPlainText()
        input_len = calc_len(input_text)
        len_message = str(input_len) + '字节(' + str(hex(input_len)) + ')'
        if config.serial_check is True or config.socket_check is True:
            self.send_button.setText('发送（' + len_message + '）')
        else:
            self.send_button.setText('请打开串口')

    def calc_receive_box_len(self):
        input_text = self.receive_input_box.toPlainText()
        input_len = calc_len(input_text)
        len_message = str(input_len) + '字节(' + str(hex(input_len)) + ')'
        self.receive_clear_button.setText('清空（' + len_message + '）')

    def show_about_window(self):
        config.about_window.show()

    def show_config_window(self):
        config.config_window.read_param()
        config.config_window.show()

    def shift_trans_window(self):
        self.hide()
        config.trans_window.show()

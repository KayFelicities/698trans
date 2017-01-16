import config
from PyQt4 import QtCore
from PyQt4 import QtGui
import traceback
from shared_functions import *  # NOQA
from serial_window import Ui_SerialWindow
import link_layer
import communication


class SerialWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_SerialWindow):
    _receive_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(SerialWindow, self).__init__()
        self.setupUi(self)
        config.show_level = self.show_level_cb.isChecked()
        self._receive_signal.connect(self.re_text_to_box)
        # self._get_SA_signal.connect(self.read_SA)
        config.auto_trans = self.auto_trans_cb.isChecked()
        if config.auto_trans is True:
            self.send_input_box.textChanged.connect(self.send_trans)
            self.translate_button.setVisible(False)
        else:
            self.send_input_box.textChanged.disconnect(self.send_trans)
            self.translate_button.setVisible(True)
        self.receive_input_box.textChanged.connect(self.receive_trans)
        self.read_SA_b.clicked.connect(self.get_SA)
        self.quick_fix_button.clicked.connect(self.quick_fix)
        self.translate_button.clicked.connect(self.send_trans)
        self.send_clear_button.clicked.connect(self.send_clear_botton)
        self.receive_clear_button.clicked.connect(self.receive_clear_botton)
        self.link_b.clicked.connect(self.link_try)
        self.unlink_b.clicked.connect(self.close_link)
        self.server_start_b.clicked.connect(self.start_server)
        self.server_stop_b.clicked.connect(self.stop_server)
        self.send_button.clicked.connect(self.send_data)
        self.auto_fix_cb.clicked.connect(self.set_auto_fix)
        self.show_level_cb.clicked.connect(self.set_level_visible)
        self.always_top_cb.clicked.connect(self.set_always_top)
        self.auto_trans_cb.clicked.connect(self.set_auto_trans)
        self.send_input_box.textChanged.connect(self.calc_send_box_len)
        self.receive_input_box.textChanged.connect(self.calc_receive_box_len)
        self.com_list.addItems(communication.serial_com_scan())
        self.about_menu.triggered.connect(self.show_about_window)
        self.config_menu.triggered.connect(self.show_config_window)
        self.param_menu.triggered.connect(self.show_param_window)
        self.task_menu.triggered.connect(self.show_task_window)
        self.trans_mode_button.clicked.connect(self.shift_trans_window)

    def start_server(self):
        server_port = int(self.server_port_box.text())
        if config.server_check is False:
            if communication.start_server(server_port) == 'ok':
                self.server_start_b.setText('成功')
                self.read_SA_b.setText('等待登录')
            else:
                self.server_start_b.setText('失败')

    def stop_server(self):
        communication.close_server()
        self.server_start_b.setText('启动')
        self.read_SA_b.setText('读取')
        if config.serial_check is False and config.socket_check is False:
            self.send_button.setEnabled(False)
            self.read_SA_b.setEnabled(False)

    def link_try(self):
        if config.serial_check is False and config.socket_check is False:
            if self.com_list.currentText() == '前置机':
                if communication.link_socket() == 'ok':
                    self.link_b.setText(self.com_list.currentText() + '已连接')
                    self.unlink_b.setText('断开')
                    self.send_button.setEnabled(True)
                    self.read_SA_b.setEnabled(True)
                    self.calc_send_box_len()
                else:
                    self.link_b.setText(self.com_list.currentText() + '连接失败')
            else:
                serial_com = self.com_list.currentText()
                if communication.link_serial(serial_com) == 'ok':
                    self.link_b.setText(self.com_list.currentText() + '已连接')
                    self.unlink_b.setText('断开')
                    self.send_button.setEnabled(True)
                    self.read_SA_b.setEnabled(True)
                    self.calc_send_box_len()
                else:
                    self.link_b.setText(self.com_list.currentText() + '连接失败')

    def close_link(self):
        if config.serial_check is True or config.socket_check is True:
            communication.close_serial()
            communication.close_socket()
            self.link_b.setText('连接')
            self.send_button.setText('请建立连接')
            if config.server_check is False:
                self.send_button.setEnabled(False)
                self.read_SA_b.setEnabled(False)
            self.unlink_b.setText('刷新')
        else:
            self.com_list.clear()
            self.com_list.addItems(communication.serial_com_scan())

    def send_data(self):
        self._receive_signal.disconnect()
        self._receive_signal.connect(self.re_text_to_box)
        input_text = self.send_input_box.toPlainText()
        communication.send(input_text)

    def re_text_to_box(self, re_text):
        self.receive_input_box.setText(re_text)

    def get_SA(self):
        self.read_SA_b.setText('读取')
        input_text = '682100434FAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA10CC1C05010140000200007D1B16'
        self._receive_signal.disconnect()
        self._receive_signal.connect(self.read_SA)
        communication.send(input_text)

    def read_SA(self, re_text):
        data = link_layer.data_format(re_text)
        ret_dict = link_layer.get_SA_CA(data)
        self.SA_box.setText(ret_dict['SA'])
        self.SA_len_box.setText(ret_dict['SA_len'])
        self.read_SA_b.setText('成功')
        self._receive_signal.disconnect()
        self._receive_signal.connect(self.re_text_to_box)

    def quick_fix(self):
        if self.is_good_linklayer() is False:
            self.fix_addr()
            self.send_trans()
        else:
            input_text = self.send_input_box.toPlainText()
            data_in = link_layer.data_format(input_text)
            if config.good_L is not None:
                data_in[1], data_in[2] = config.good_L[0], config.good_L[1]
            else:
                if config.good_HCS is not None:
                    ret_dict = link_layer.get_SA_CA(data_in)
                    hcs_pos = 6 + int(ret_dict['SA_len'])
                    data_in[hcs_pos], data_in[hcs_pos + 1] = config.good_HCS[0], config.good_HCS[1]
                    input_text = ''
                    for data in data_in:
                        input_text += data + ' '
                    print('input_text', input_text)
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
            data_in = link_layer.data_format(input_text, auto_add_0=False)
            print('data_in', data_in)
            ret_dict = link_layer.all_translate(data_in)
            if ret_dict['res'] == 'ok':
                self.quick_fix_button.setText(
                    '修正地址' if self.is_good_linklayer() is False
                    else '修正校验码' if config.good_HCS is not None or config.good_FCS is not None
                    else '修正格式'
                )
                if ret_dict['input_type'] == 'full' and config.auto_fix is True:
                    if self.is_good_linklayer() is False:
                        self.fix_addr()
                        input_text = self.send_input_box.toPlainText()
                        data_in = link_layer.data_format(input_text)
                        link_layer.all_translate(data_in)
                elif ret_dict['input_type'] == 'apdu':
                    input_text = link_layer.add_link_layer(input_text)
                    self.send_input_box.setText(input_text)
                    data_in = link_layer.data_format(input_text)
                    link_layer.all_translate(data_in)
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
            data_in = link_layer.data_format(input_text)
            link_layer.all_translate(data_in)
        except Exception as e:
            print(e)
            output('\n\n报文解析过程出现问题，请检查报文。若报文无问题请反馈665593，谢谢！')
        self.receive_output_box.setText(config.output_text)
        config.output_text = ''

    def is_good_linklayer(self):
        input_text = self.send_input_box.toPlainText()
        box_SA_type = self.SA_type_list.currentText()
        box_SA_len = int(self.SA_len_box.text())
        box_SA_text = self.SA_box.text()
        return link_layer.is_same_addr(input_text, box_SA_type, box_SA_text, box_SA_len)

    def fix_addr(self):
        apdu_text = link_layer.get_apdu_text(self.send_input_box.toPlainText())
        self.send_input_box.setText(link_layer.add_link_layer(apdu_text))

    def send_clear_botton(self):
        self.send_input_box.setFocus()

    def receive_clear_botton(self):
        self.receive_input_box.setFocus()

    def set_auto_fix(self):
        config.auto_fix = self.auto_fix_cb.isChecked()

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
        input_len = link_layer.calc_text_len(input_text)
        len_message = str(input_len) + '字节(' + str(hex(input_len)) + ')'
        if config.serial_check is True or config.socket_check is True or config.server_check is True:
            self.send_button.setText('发送（' + len_message + '）')
        else:
            self.send_button.setText('请建立连接')

    def calc_receive_box_len(self):
        input_text = self.receive_input_box.toPlainText()
        input_len = link_layer.calc_text_len(input_text)
        len_message = str(input_len) + '字节(' + str(hex(input_len)) + ')'
        self.receive_clear_button.setText('清空（' + len_message + '）')

    def show_about_window(self):
        config.about_window.show()

    def show_config_window(self):
        config.config_window.read_param()
        config.config_window.show()

    def show_param_window(self):
        config.param_window.show()

    def show_task_window(self):
        config.task_window.show()

    def shift_trans_window(self):
        self.hide()
        config.trans_window.show()

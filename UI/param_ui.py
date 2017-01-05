import config
from shared_functions import *  # NOQA
import link_layer
import data_translate
import communication
import param
from PyQt4 import QtCore
from PyQt4 import QtGui
from param_window import Ui_ParamWindow


class ParamWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_ParamWindow):
    def __init__(self):
        super(ParamWindow, self).__init__()
        self.setupUi(self)
        self.res_b.clicked.connect(self.clear_res)
        self.DT_read_b.clicked.connect(self.DT_read)
        self.DT_set_b.clicked.connect(self.DT_set)
        self.DT_set_now_b.clicked.connect(self.DT_set_now)
        self.SA_read_b.clicked.connect(self.SA_read)
        self.SA_set_b.clicked.connect(self.SA_set)
        self.S_ip_read_b.clicked.connect(self.ip_read)
        self.S_ip_set_b.clicked.connect(self.ip_set)
        self.local_read_b.clicked.connect(self.local_net_read)
        self.local_set_b.clicked.connect(self.local_net_set)
        self.C_read_b.clicked.connect(self.communication_read)
        self.C_set_b.clicked.connect(self.communication_set)
        self.esam_r_info_b.clicked.connect(self.esam_info_read)
        self.esam_r_certi_b.clicked.connect(self.esam_certi_read)

    def clear_res(self):
        self.res_b.setText('')

    def DT_read(self):
        self.res_b.setText('')
        apdu_text = '0501014000020000'
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(self.re_DT)
        communication.send(config.serial_window.add_link_layer(apdu_text))

    def DT_set(self):
        self.res_b.setText('')
        DT_box_content = self.DT_box.dateTime()
        self.set_DT(DT_box_content)

    def DT_set_now(self):
        self.res_b.setText('')
        DT_now = QtCore.QDateTime.currentDateTime()
        # print('DT_now', DT_now)
        self.set_DT(DT_now)

    def set_DT(self, DT):
        # self.DT_box.setDateTime(DT)
        DT_list = DT.toString('yyyy.MM.dd.hh.mm.ss').split('.')
        DT_text = '1C%04X' % int(DT_list[0])
        for DT in DT_list[1:]:
            DT_text += '%02X' % int(DT)
        print(DT_text)
        apdu_text = '06010D40000200' + DT_text + '00'
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(self.read_res)
        communication.send(config.serial_window.add_link_layer(apdu_text))

    def re_DT(self, re_text):
        data = link_layer.data_format(re_text)
        offset = 0
        ret_dict = link_layer.get_addr(data)
        offset += 5 + int(ret_dict['SA_len']) + 10
        if data[offset] == '01':
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
            offset += 2
            DT_read = QtCore.QDateTime(
                (int(data[offset], 16) << 8) | int(data[offset + 1], 16),
                int(data[offset + 2], 16),
                int(data[offset + 3], 16),
                int(data[offset + 4], 16),
                int(data[offset + 5], 16),
                int(data[offset + 6], 16),
            )
            # print('DT_read', DT_read)
            self.DT_box.setDateTime(DT_read)
        else:
            self.res_b.setStyleSheet('color: red')
            self.res_b.setText('失败：' + data_translate.dar_explain[data[offset + 1]])
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(config.serial_window.re_text_to_box)

    def SA_read(self):
        self.res_b.setText('')
        apdu_text = '0501004001020000'
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(self.re_SA)
        communication.send(config.serial_window.add_link_layer(apdu_text))

    def SA_set(self, DT):
        self.res_b.setText('')
        SA_text = self.SA_box.text().replace(' ', '')
        if len(SA_text) % 2 == 1:
            SA_text += 'F'
        self.SA_box.setText(SA_text)
        print('SA_text', SA_text)
        SA_len = len(SA_text) // 2
        apdu_text = '06010D4001020009' + '%02X' % (SA_len) + SA_text + '00'
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(self.read_res_SA)
        communication.send(config.serial_window.add_link_layer(apdu_text))

    def re_SA(self, re_text):
        data = link_layer.data_format(re_text)
        offset = 0
        ret_dict = link_layer.get_addr(data)
        offset += 5 + int(ret_dict['SA_len']) + 10
        if data[offset] == '01':
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
            offset += 2
            SA_len = int(data[offset], 16)
            self.SA_len_box.setText(str(SA_len))
            SA_text = ''
            for d in data[offset + 1: offset + 1 + SA_len]:
                SA_text += d
            self.SA_box.setText(SA_text)
        else:
            self.res_b.setStyleSheet('color: red')
            self.res_b.setText('失败：' + data_translate.dar_explain[data[offset + 1]])
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(config.serial_window.re_text_to_box)

    def ip_read(self):
        self.res_b.setText('')
        apdu_text = '0501004500030000'
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(self.re_ip)
        communication.send(config.serial_window.add_link_layer(apdu_text))

    def ip_set(self, DT):
        self.res_b.setText('')
        ip_text = param.format_ip(self.S_ip_box.text())
        port_text = '%04X' % int(self.S_port_box.text().replace(' ', ''))
        apdu_text = '06010D45000300010102020904' + ip_text + '12' + port_text + '00'
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(self.read_res)
        communication.send(config.serial_window.add_link_layer(apdu_text))

    def re_ip(self, re_text):
        data = link_layer.data_format(re_text)
        offset = 0
        ret_dict = link_layer.get_addr(data)
        offset += 5 + int(ret_dict['SA_len']) + 10
        if data[offset] == '01':
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
            offset += 7
            ip_text = param.get_ip(data[offset:])
            self.S_ip_box.setText(ip_text)
            port_text = str(int(data[offset + 5] + data[offset + 6], 16))
            self.S_port_box.setText(port_text)
        else:
            self.res_b.setStyleSheet('color: red')
            self.res_b.setText('失败：' + data_translate.dar_explain[data[offset + 1]])
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(config.serial_window.re_text_to_box)

    def local_net_read(self):
        self.res_b.setText('')
        apdu_text = '0501004510040000'
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(self.re_local_net)
        communication.send(config.serial_window.add_link_layer(apdu_text))

    def local_net_set(self, DT):
        self.res_b.setText('')
        ip_mode = '%02X' % self.local_ip_mode_l.currentIndex()
        ip_text = param.format_ip(self.local_ip_box.text())
        ip_mask = param.format_ip(self.local_mask_box.text())
        gate = param.format_ip(self.local_gate_addr_box.text())
        ppp_usr = param.format_octet(self.ppp_usr_box.text())
        ppp_pw = param.format_octet(self.ppp_pw_box.text())
        apdu_text = '06010D45100400 0206 16' + ip_mode + '0904' + ip_text + '0904' + ip_mask + '0904' + gate + ppp_usr + ppp_pw + '00'
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(self.read_res)
        communication.send(config.serial_window.add_link_layer(apdu_text))

    def re_local_net(self, re_text):
        data = link_layer.data_format(re_text)
        offset = 0
        ret_dict = link_layer.get_addr(data)
        offset += 5 + int(ret_dict['SA_len']) + 10
        if data[offset] == '01':
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
            offset += 4
            self.local_ip_mode_l.setCurrentIndex({'00': 0, '01': 1, '02': 2}[data[offset]])
            offset += 3
            self.local_ip_box.setText(param.get_ip(data[offset:]))
            offset += 6
            self.local_mask_box.setText(param.get_ip(data[offset:]))
            offset += 6
            self.local_gate_addr_box.setText(param.get_ip(data[offset:]))
            offset += 4
            ret = param.get_octet(data[offset:])
            self.ppp_usr_box.setText(ret['octet'])
            offset += ret['offset']
            ret = param.get_octet(data[offset:])
            self.ppp_pw_box.setText(ret['octet'])
            offset += ret['offset']
        else:
            self.res_b.setStyleSheet('color: red')
            self.res_b.setText('失败：' + data_translate.dar_explain[data[offset + 1]])
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(config.serial_window.re_text_to_box)

    def communication_read(self):
        self.res_b.setText('')
        apdu_text = '0501004500020000'
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(self.re_communication)
        communication.send(config.serial_window.add_link_layer(apdu_text))

    def communication_set(self, DT):
        self.res_b.setText('')
        work_mode_text = '16' + '%02X' % self.C_work_mode_l.currentIndex()
        online_mode_text = '16' + '%02X' % self.C_online_mode_l.currentIndex()
        connect_mode_text = '16' + '%02X' % self.C_connect_mode_l.currentIndex()
        connect_app_mode_text = '16' + '%02X' % self.C_connect_app_mode_l.currentIndex()
        listen_port_text = '0100'   # 暂时不可设置
        APN_text = param.format_visible_string(self.C_APN_box.text())
        usr_text = param.format_visible_string(self.C_usr_box.text())
        pw_text = param.format_visible_string(self.C_pw_box.text())
        proxy_addr_text = param.format_octet(self.C_proxy_addr_box.text())
        proxy_port_text = param.format_long_unsigned(self.C_proxy_prot_box.text())
        overtm_retry_num_text = '0401' + '%02X' % ((int(self.C_retry_box.text()) << 6) | int(self.C_over_tm_box.text()))
        heart_tm_text = param.format_long_unsigned(self.C_heart_tm_box.text())
        apdu_text = '06010D45000200 020C' + work_mode_text + online_mode_text + \
            connect_mode_text + connect_app_mode_text + listen_port_text + APN_text + \
            usr_text + pw_text + proxy_addr_text + proxy_port_text + overtm_retry_num_text + heart_tm_text + '00'
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(self.read_res)
        communication.send(config.serial_window.add_link_layer(apdu_text))

    def re_communication(self, re_text):
        data = link_layer.data_format(re_text)
        offset = 0
        ret_dict = link_layer.get_addr(data)
        offset += 5 + int(ret_dict['SA_len']) + 10
        if data[offset] == '01':
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
            offset += 4
            self.C_work_mode_l.setCurrentIndex({'00': 0, '01': 1, '02': 2}[data[offset]])
            offset += 2
            self.C_online_mode_l.setCurrentIndex({'00': 0, '01': 1}[data[offset]])
            offset += 2
            self.C_connect_mode_l.setCurrentIndex({'00': 0, '01': 1}[data[offset]])
            offset += 2
            self.C_connect_app_mode_l.setCurrentIndex({'00': 0, '01': 1}[data[offset]])
            offset += 2
            array_num = int(data[offset], 16)
            offset += 1
            listen_port_text = ''
            for count in range(array_num):
                listen_port_text += str(param.get_long_unsigned(data[offset:])) + ' '
                offset += 3
            self.C_listen_port_box.setText(listen_port_text)
            ret = param.get_visible(data[offset:])
            self.C_APN_box.setText(ret['visible'])
            offset += ret['offset']
            ret = param.get_visible(data[offset:])
            self.C_usr_box.setText(ret['visible'])
            offset += ret['offset']
            ret = param.get_visible(data[offset:])
            self.C_pw_box.setText(ret['visible'])
            offset += ret['offset']
            ret = param.get_octet(data[offset:])
            self.C_proxy_addr_box.setText(ret['octet'])
            offset += ret['offset']
            self.C_proxy_prot_box.setText(str(param.get_long_unsigned(data[offset:])))
            offset += 3
            offset += 2
            overtm_retry_num_byte = int(data[offset], 16)
            self.C_retry_box.setText(str(overtm_retry_num_byte >> 6))
            self.C_over_tm_box.setText(str(overtm_retry_num_byte & 0x3f))
            offset += 1
            print(data[offset:])
            self.C_heart_tm_box.setText(str(param.get_long_unsigned(data[offset:])))
            offset += 3
        else:
            self.res_b.setStyleSheet('color: red')
            self.res_b.setText('失败：' + data_translate.dar_explain[data[offset + 1]])
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(config.serial_window.re_text_to_box)

    def esam_info_read(self):
        self.res_b.setText('')
        apdu_text = '0502 0107 F1000200 F1000300 F1000400 F1000500 F1000600 F1000700 F1000800 00'
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(self.re_esam_info)
        communication.send(config.serial_window.add_link_layer(apdu_text))

    def re_esam_info(self, re_text):
        data = link_layer.data_format(re_text)
        offset = 0
        ret_dict = link_layer.get_addr(data)
        offset += 5 + int(ret_dict['SA_len']) + 7
        res_sum = True
        offset += 4
        if data[offset] == '01':
            offset += 1
            ret = param.get_octet(data[offset:])
            self.esam_no_box.setText(ret['octet'])
            offset += ret['offset']
        else:
            offset += 1
            res_sum = False
            self.esam_no_box.setText('失败：' + data_translate.dar_explain[data[offset + 1]])
        offset += 4
        if data[offset] == '01':
            offset += 1
            ret = param.get_octet(data[offset:])
            self.esam_ver_box.setText(ret['octet'])
            offset += ret['offset']
        else:
            offset += 1
            res_sum = False
            self.esam_ver_box.setText('失败：' + data_translate.dar_explain[data[offset + 1]])
        offset += 4
        if data[offset] == '01':
            offset += 1
            ret = param.get_octet(data[offset:])
            self.esam_key_box.setText(ret['octet'])
            offset += ret['offset']
        else:
            offset += 1
            res_sum = False
            self.esam_key_box.setText('失败：' + data_translate.dar_explain[data[offset + 1]])
        offset += 4
        if data[offset] == '01':
            offset += 1
            self.esam_dialog_tm_box.setText(str(param.get_double_long_unsigned(data[offset:])))
            offset += 5
        else:
            offset += 1
            res_sum = False
            self.esam_dialog_tm_box.setText('失败：' + data_translate.dar_explain[data[offset + 1]])
        offset += 4
        if data[offset] == '01':
            offset += 1
            self.esam_dialog_remain_box.setText(str(param.get_double_long_unsigned(data[offset:])))
            offset += 5
        else:
            offset += 1
            res_sum = False
            self.esam_dialog_remain_box.setText('失败：' + data_translate.dar_explain[data[offset + 1]])
        offset += 4
        if data[offset] == '01':
            offset += 3
            self.esam_addr_ctr_box.setText(str(param.get_double_long_unsigned(data[offset:])))
            offset += 5
            self.esam_rpt_ctr_box.setText(str(param.get_double_long_unsigned(data[offset:])))
            offset += 5
            self.esam_app_radio_box.setText(str(param.get_double_long_unsigned(data[offset:])))
            offset += 5
        else:
            offset += 1
            res_sum = False
            self.esam_addr_ctr_box.setText('失败：' + data_translate.dar_explain[data[offset + 1]])
            self.esam_rpt_ctr_box.setText('失败：' + data_translate.dar_explain[data[offset + 1]])
            self.esam_app_radio_box.setText('失败：' + data_translate.dar_explain[data[offset + 1]])
        offset += 4
        if data[offset] == '01':
            offset += 3
            ret = param.get_octet(data[offset:])
            self.esam_terminal_ver_box.setText(ret['octet'])
            offset += ret['offset']
            ret = param.get_octet(data[offset:])
            self.esam_host_ver_box.setText(ret['octet'])
            offset += ret['offset']
        else:
            offset += 1
            res_sum = False
            self.esam_terminal_ver_box.setText('失败：' + data_translate.dar_explain[data[offset + 1]])
            self.esam_host_ver_box.setText('失败：' + data_translate.dar_explain[data[offset + 1]])

        if res_sum is True:
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(config.serial_window.re_text_to_box)

    def esam_certi_read(self):
        self.res_b.setText('')
        if self.esam_certi_l.currentIndex() == 0:
            apdu_text = '0502 0102 F1000900 F1000A00 00'
        else:
            apdu_text = '0502 0102 F1000B00 F1000C00 00'
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(self.re_esam_certi)
        communication.send(config.serial_window.add_link_layer(apdu_text))

    def re_esam_certi(self, re_text):
        data = link_layer.data_format(re_text)
        offset = 0
        ret_dict = link_layer.get_addr(data)
        offset += 5 + int(ret_dict['SA_len']) + 7
        res_sum = True
        offset += 4
        if data[offset] == '01':
            offset += 1
            ret = param.get_octet(data[offset:])
            self.esam_certi_ver_box.setText(ret['octet'])
            offset += ret['offset']
        else:
            offset += 1
            res_sum = False
            self.esam_certi_ver_box.setText('失败：' + data_translate.dar_explain[data[offset + 1]])
        offset += 4
        if data[offset] == '01':
            offset += 1
            ret = param.get_octet(data[offset:])
            self.esam_certi_box.setText(ret['octet'])
            self.esam_certi_len_box.setText(str(ret['len']) + '字节')
            offset += ret['offset']
        else:
            offset += 1
            res_sum = False
            self.esam_certi_box.setText('失败：' + data_translate.dar_explain[data[offset + 1]])

        if res_sum is True:
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(config.serial_window.re_text_to_box)

    def read_res(self, re_text):
        res = param.read_set_dar(re_text)
        if res == 'ok':
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
        else:
            self.res_b.setStyleSheet('color: red')
            self.res_b.setText('失败：' + res)
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(config.serial_window.re_text_to_box)

    def read_res_SA(self, re_text):
        res = param.read_set_dar(re_text)
        if res == 'ok':
            config.serial_window.SA_box.setText(self.SA_box.text())
            config.serial_window.SA_len_box.setText(str(len(self.SA_box.text()) // 2))
            self.res_b.setStyleSheet('color: green')
            self.res_b.setText('成功')
        else:
            self.res_b.setStyleSheet('color: red')
            self.res_b.setText('失败：' + res)
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(config.serial_window.re_text_to_box)

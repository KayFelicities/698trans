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

    def clear_res(self):
        self.res_b.setText('')

    def DT_read(self):
        self.res_b.setText('')
        apdu_text = '0501014000020000'
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(self.read_DT)
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

    def read_DT(self, re_text):
        data = link_layer.data_format(re_text)
        offset = 0
        ret_dict = link_layer.get_addr(data)
        offset += 5 + int(ret_dict['SA_len']) + 10
        if data[offset] == '01':
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
            self.res_b.setText('失败：' + data_translate.dar_explain[data[offset + 1]])
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(config.serial_window.re_text_to_box)

    def SA_read(self):
        self.res_b.setText('')
        apdu_text = '0501004001020000'
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(self.read_SA)
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

    def read_SA(self, re_text):
        data = link_layer.data_format(re_text)
        offset = 0
        ret_dict = link_layer.get_addr(data)
        offset += 5 + int(ret_dict['SA_len']) + 10
        if data[offset] == '01':
            self.res_b.setText('成功')
            offset += 2
            SA_len = int(data[offset], 16)
            self.SA_len_box.setText(str(SA_len))
            SA_text = ''
            for d in data[offset + 1: offset + 1 + SA_len]:
                SA_text += d
            self.SA_box.setText(SA_text)
        else:
            self.res_b.setText('失败：' + data_translate.dar_explain[data[offset + 1]])
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(config.serial_window.re_text_to_box)

    def ip_read(self):
        self.res_b.setText('')
        apdu_text = '0501004500030000'
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(self.read_ip)
        communication.send(config.serial_window.add_link_layer(apdu_text))

    def ip_set(self, DT):
        self.res_b.setText('')
        ip_text = param.format_ip(self.S_ip_box.text())
        port_text = '%04X' % int(self.S_port_box.text().replace(' ', ''))
        apdu_text = '06010D45000300010102020904' + ip_text + '12' + port_text + '00'
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(self.read_res)
        communication.send(config.serial_window.add_link_layer(apdu_text))

    def read_ip(self, re_text):
        data = link_layer.data_format(re_text)
        offset = 0
        ret_dict = link_layer.get_addr(data)
        offset += 5 + int(ret_dict['SA_len']) + 10
        if data[offset] == '01':
            self.res_b.setText('成功')
            offset += 7
            ip_text = param.get_ip(data[offset:])
            self.S_ip_box.setText(ip_text)
            port_text = str(int(data[offset + 5] + data[offset + 6], 16))
            self.S_port_box.setText(port_text)
        else:
            self.res_b.setText('失败：' + data_translate.dar_explain[data[offset + 1]])
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(config.serial_window.re_text_to_box)

    def local_net_read(self):
        self.res_b.setText('')
        apdu_text = '0501004510040000'
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(self.read_local_net)
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

    def read_local_net(self, re_text):
        data = link_layer.data_format(re_text)
        offset = 0
        ret_dict = link_layer.get_addr(data)
        offset += 5 + int(ret_dict['SA_len']) + 10
        if data[offset] == '01':
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
            self.res_b.setText('失败：' + data_translate.dar_explain[data[offset + 1]])
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(config.serial_window.re_text_to_box)

    def read_res(self, re_text):
        res = param.read_set_dar(re_text)
        if res == 'ok':
            self.res_b.setText('成功')
        else:
            self.res_b.setText('失败：' + res)
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(config.serial_window.re_text_to_box)

    def read_res_SA(self, re_text):
        res = param.read_set_dar(re_text)
        if res == 'ok':
            config.serial_window.SA_box.setText(self.SA_box.text())
            config.serial_window.SA_len_box.setText(str(len(self.SA_box.text()) // 2))
            self.res_b.setText('成功')
        else:
            self.res_b.setText('失败：' + res)
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(config.serial_window.re_text_to_box)

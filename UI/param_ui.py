import config
from shared_functions import *  # NOQA
from take_re_data import *  # NOQA
from link_layer import *  # NOQA
import data_translate
from PyQt4 import QtCore
from PyQt4 import QtGui
from param_window import Ui_ParamWindow


class ParamWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_ParamWindow):
    def __init__(self):
        super(ParamWindow, self).__init__()
        self.setupUi(self)
        self.DT_set_res_t.clicked.connect(self.clear_res)
        self.DT_read_b.clicked.connect(self.DT_read)
        self.DT_set_b.clicked.connect(self.DT_set)
        self.DT_set_now_b.clicked.connect(self.DT_set_now)

    def clear_res(self):
        self.DT_set_res_t.setText('')

    def DT_read(self):
        self.DT_set_res_t.setText('')
        apdu_text = '0501014000020000'
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(self.read_DT)
        config.serial_window.send(config.serial_window.add_link_layer(apdu_text))

    def DT_set(self):
        self.DT_set_res_t.setText('')
        DT_box_content = self.DT_box.dateTime()
        self.set_DT(DT_box_content)

    def DT_set_now(self):
        self.DT_set_res_t.setText('')
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
        config.serial_window.send(config.serial_window.add_link_layer(apdu_text))

    def read_DT(self, re_text):
        data = data_format(re_text)
        offset = 0
        ret_dict = get_addr(data)
        offset += 5 + int(ret_dict['SA_len']) + 10
        if data[offset] == '01':
            self.DT_set_res_t.setText('成功')
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
            self.DT_set_res_t.setText('失败：' + data_translate.dar_explain[data[offset + 1]])
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(config.serial_window.take_receive_data)

    def read_res(self, re_text):
        data = data_format(re_text)
        offset = 0
        ret_dict = get_addr(data)
        offset += 5 + int(ret_dict['SA_len']) + 10
        if data[offset] == '00':
            self.DT_set_res_t.setText('成功')
        else:
            self.DT_set_res_t.setText('失败：' + data_translate.dar_explain[data[offset]])
        config.serial_window._receive_signal.disconnect()
        config.serial_window._receive_signal.connect(config.serial_window.take_receive_data)

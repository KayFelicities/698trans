import config
from PyQt4 import QtGui
import sys
sys.path.append('UI\\')
from shared_functions import *  # NOQA
from link_layer import *  # NOQA
from get_service import *  # NOQA
from set_service import *  # NOQA
from action_service import *  # NOQA
from report_service import *  # NOQA
from proxy_service import *  # NOQA
from connect_service import *  # NOQA
from security_service import *  # NOQA
from testgui import Ui_Kaytest


class UItest(QtGui.QMainWindow, QtGui.QWidget, Ui_Kaytest):
    def __init__(self):
        super(UItest, self).__init__()
        self.setupUi(self)
        self.translate_button.clicked.connect(self.buttontest)
        self.input_box.textChanged.connect(self.my_calc_len_and_crc)

    def buttontest(self):
        input_text = self.input_box.toPlainText()
        # try:
        my_translate(input_text)
        # except:
        #    output('此条报文解析过程中出现错误')
        self.output_box.setText(config.text_test)
        config.text_test = ''

    def my_calc_len_and_crc(self):
        input_text = self.input_box.toPlainText()
        input_len, crc_calc = calc_len_and_crc(input_text)
        self.len_box.setText(input_len)
        self.crc_box.setText(crc_calc)


def my_translate(input_text):
    offset = 0
    data = data_format(input_text)
    if check_data(data) is not True:  # 非法
        output('报文非法')
        return
    offset += take_link_layer_1(data[offset:])
    # 解应用层
    output('=' * 60 + 'APDU')
    offset_temp, service_type = take_service_type(data[offset:])
    offset += offset_temp
    offset += {
        '01': link_request, '02': connect_request, '03': release_request,
        '81': link_response, '82': connect_response, '83': release_response,
        '0501': get0501, '0502': get0502, '0503': get0503, '0504': get0504,
        '0505': get0505,
        '8501': get8501, '8502': get8502, '8503': get8503, '8504': get8504,
        '8505': get8505,
        '0601': set0601, '0602': set0602, '0603': set0603,
        '8601': set8601, '8602': set8602, '8603': set8603,
        '0701': act0701, '0702': act0702, '0703': act0703,
        '8701': act8701, '8702': act8702, '8703': act8703,
        '0801': rep0801, '0802': rep0802,
        '8801': rep8801, '8802': rep8802,
        '0901': pro0901, '0902': pro0902, '0903': pro0903, '0904': pro0904,
        '0905': pro0905, '0906': pro0906, '0907': pro0907,
        '8901': pro8901, '8902': pro8902, '8903': pro8903, '8904': pro8904,
        '8905': pro8905, '8906': pro8906, '8907': pro8907,
        '10': security_request, '90': security_response,
    }[service_type](data[offset:])
    output('^' * 60 + 'APDU')
    # 处理链路层末尾
    offset += take_link_layer_2(data[0:], offset)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myUI = UItest()
    myUI.show()
    sys.exit(app.exec_())

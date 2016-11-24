import config
from PyQt4 import QtGui
import sys

from shared_functions import *  # NOQA
from link_layer import *  # NOQA
from sRunFun import *  # NOQA
from get_service import *  # NOQA
from set_service import *  # NOQA
from action_service import *  # NOQA
from report_service import *  # NOQA
from proxy_service import *  # NOQA
from Other import connect_service
from security_service import *  # NOQA
from testgui import Ui_Kaytest


class UItest(QtGui.QMainWindow, QtGui.QWidget, Ui_Kaytest):

    def __init__(self):
        super(UItest, self).__init__()
        self.setupUi(self)
        self.translate_button.clicked.connect(self.buttontest)

    def buttontest(self):
        input_text = self.input_box.toPlainText()
        # try:
        my_translate(input_text)
        # except:
        #    output('此条报文解析过程中出现错误')
        self.output_box.setText(config.text_test)
        config.text_test = ''


def my_translate(input_text):
    offset = 0
    data_in = data_format(input_text)
    if check_data(data_in) is not True:  # 非法
        output('报文非法')
        return
    offset += take_link_layer_1(data_in[offset:])

    # 解应用层
    show_service_type(offset, *data_in)
    if data_in[offset] in ['01', '02', '03', '81', '82', '83', '84']:
        offset += connect_service(offset, *data_in)  # 连接管理

    elif data_in[offset] in ['10', '90']:
        print('data_in[offset]', data_in[offset])
        if data_in[offset] == '10':
            offset += 1
            offset += security_request(offset, *data_in)
        elif data_in[offset] == '90':
            offset += 1
            offset += security_response(offset, *data_in)
    else:
        server_type = data_in[offset] + data_in[offset + 1]
        offset += 2
        offset += {
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
        }[server_type](data_in[offset:])
    # 处理链路层末尾
    take_link_layer_2(data_in[offset:])


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myUI = UItest()
    myUI.show()
    sys.exit(app.exec_())

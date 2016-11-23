import config
from PyQt4 import QtGui
import sys

from shared_functions import *  # NOQA
from sRunFun import *  # NOQA
from GET_Request import *  # NOQA
from GET_Response import *  # NOQA
from SET_Request import *  # NOQA
from SET_Response import *  # NOQA
from Action_Request import *  # NOQA
from Action_Response import *  # NOQA
from Rep_Noti import *  # NOQA
from Rep_Response import *  # NOQA
from Pro_Request import *  # NOQA
from Pro_Response import *  # NOQA
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
    input_text = input_text.replace(' ', '').replace('\n', '').upper()  # 处理空格和换行
    data_len = int(len(input_text) / 2)
    output('报文总长：' + str(data_len) + '字节(' + str(hex(data_len)) + ')\n')
    # 处理FE前缀
    k = 0
    while input_text[k * 2:(k + 1) * 2] == 'FE':
        k += 1
    input_text = input_text[k * 2:]
    print('原始报文： ' + input_text + '\n')
    # 写入list
    data_in = []
    for k in range(0, int(len(input_text) / 2)):
        data_in.append(input_text[k * 2:(k + 1) * 2])
    # print(data_in)
    # 判断合法性
    if Verify(*data_in) is not True:  # 非法
        return
    # 解链路层
    ShowLen(*data_in)  # 显示长度
    ShowCtrl(*data_in)  # 显示控制域
    offset = 1 + 2 + 1  # 68 长度 长度 控制码
    offset += lShowAddr(*data_in)  # 地址
    offset += lShowHCS(offset, *data_in)  # 帧头校验
    offset += lShowFenZen(offset, *data_in)  # 分帧
    # 解应用层
    show_service_type(offset, *data_in)
    apdu_len = 0
    if data_in[offset] in ['01', '02', '03', '81', '82', '83', '84']:
        apdu_len = connect_service(offset, *data_in)  # 连接管理

    elif data_in[offset] in ['10', '90']:
        print('data_in[offset]', data_in[offset])
        if data_in[offset] == '10':
            offset += 1
            apdu_len = security_request(offset, *data_in)
        elif data_in[offset] == '90':
            offset += 1
            apdu_len = security_response(offset, *data_in)
    else:
        server_type = data_in[offset] + data_in[offset + 1]
        offset = offset + 2
        apdu_len = {
            '0501': Get0501, '0502': Get0502, '0503': Get0503, '0504': Get0504,
            '0505': Get0505,
            '8501': Get8501, '8502': Get8502, '8503': Get8503, '8504': Get8504,
            '8505': Get8505,
            '0601': Set0601, '0602': Set0602, '0603': Set0603,
            '8601': Set8601, '8602': Set8602, '8603': Set8603,
            '0701': Action0701, '0702': Action0702, '0703': Action0703,
            '8701': Action8701, '8702': Action8702, '8703': Action8703,
            '0801': Rep0801, '0802': Rep0801,  # 与0801一致
            '8801': Rep8801, '8802': Rep8802,
            '0901': Pro0901, '0902': Pro0902, '0903': Pro0903, '0904': Pro0904,
            '0905': Pro0905, '0906': Pro0906, '0907': Pro0907,
            '8901': Pro8901, '8902': Pro8902, '8903': Pro8903, '8904': Pro8904,
            '8905': Pro8905, '8906': Pro8906, '8907': Pro8907,
        }[server_type](offset, *data_in)
    # 处理链路层末尾
    offset = offset + apdu_len
    ShowOther(offset, *data_in)
    ShowFCS16(*data_in)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myUI = UItest()
    myUI.show()
    sys.exit(app.exec_())

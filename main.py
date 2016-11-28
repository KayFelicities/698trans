import config
from PyQt4 import QtGui
import sys
sys.path.append('UI\\')
from shared_functions import *  # NOQA
from link_layer import *  # NOQA
from apdu import *  # NOQA
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
        #     output('此条报文解析过程中出现错误')
        self.output_box.setText(config.text_test)
        config.text_test = ''

    def my_calc_len_and_crc(self):
        input_text = self.input_box.toPlainText()
        input_len = calc_len(input_text)
        self.len_box.setText(input_len)
        # self.crc_box.setText(crc_calc)


def my_translate(input_text):
    offset = 0
    if len(input_text) < 5:
        output('请输入698报文')
        return
    data = data_format(input_text)
    if check_data(data) is not True:  # 非法
        output('报文非法')
        return
    offset += take_link_layer_1(data[offset:])
    offset += take_APDU(data[offset:])  # 解应用层
    offset += take_link_layer_2(data[0:], offset)  # 处理链路层末尾


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myUI = UItest()
    myUI.show()
    sys.exit(app.exec_())

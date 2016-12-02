import config
from PyQt4 import QtGui
import sys
sys.path.append('UI\\')
from shared_functions import *  # NOQA
from link_layer import *  # NOQA
from apdu import *  # NOQA
from about_window import Ui_AboutWindow
from main_window import Ui_MainWindow


class MainWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.child = AboutWindow()
        self.translate_button.clicked.connect(self.trans_botton)
        self.clear_button.clicked.connect(self.clear_botton)
        self.input_box.textChanged.connect(self.calc_len_box)
        self.about.triggered.connect(self.show_about_window)

    def trans_botton(self):
        input_text = self.input_box.toPlainText()
        if 1:  # 0 for debug
            try:
                all_translate(input_text)
            except:
                output('报文解析过程出现问题，请检查报文。若报文无问题请反馈665593，谢谢！')
        else:
            all_translate(input_text)
        self.output_box.setText(config.output_text)
        config.output_text = ''

    def clear_botton(self):
        self.input_box.setFocus()

    def calc_len_box(self):
        input_text = self.input_box.toPlainText()
        input_len = calc_len(input_text)
        self.len_box.setText(input_len)
        # self.crc_box.setText(crc_calc)

    def show_about_window(self):
        self.child.show()


class AboutWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_AboutWindow):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.setupUi(self)


def all_translate(input_text):
    offset = 0
    if len(input_text) < 5:
        output('请输入698报文')
        return
    data = data_format(input_text)
    data_check = check_data(data)
    if data_check == 'ok':
        offset += take_link_layer_1(data[offset:])
        offset += take_APDU(data[offset:])  # 解应用层
        offset += take_link_layer_2(data[0:], offset)  # 处理链路层末尾
    elif data_check == 'format_error':  # 格式错误，尝试解apdu
        offset += take_APDU(data[offset:])  # 解应用层
    else:
        output('报文非法')
        return

    if offset != len(data):
        print('offset, len(data): ', offset, len(data))
        output('报文解析过程出现问题，请检查报文。若报文无问题请反馈665593，谢谢！')
    return offset


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myUI = MainWindow()
    myUI.show()
    sys.exit(app.exec_())

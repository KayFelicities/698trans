import config
from PyQt4 import QtCore
from PyQt4 import QtGui
import traceback
from shared_functions import *  # NOQA
from link_layer import *  # NOQA
from about_window import Ui_AboutWindow
from trans_window import Ui_TransWindow


class TransWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_TransWindow):
    def __init__(self):
        super(TransWindow, self).__init__()
        self.setupUi(self)
        config.show_level = self.show_level.isChecked()
        config.auto_trans = self.auto_trans.isChecked()
        self.about_child = AboutWindow()
        if config.auto_trans is True:
            self.input_box.textChanged.connect(self.start_trans)
            self.translate_button.setVisible(False)
        else:
            self.input_box.textChanged.disconnect(self.start_trans)
            self.translate_button.setVisible(True)
        self.quick_fix_button.clicked.connect(self.quick_fix)
        self.translate_button.clicked.connect(self.start_trans)
        self.clear_button.clicked.connect(self.clear_box)
        self.show_level.clicked.connect(self.set_level_visible)
        self.auto_trans.clicked.connect(self.set_auto_trans)
        self.always_top.clicked.connect(self.set_always_top)
        self.input_box.textChanged.connect(self.calc_len_box)
        self.about.triggered.connect(self.show_about_window)
        self.serial_mode_button.clicked.connect(self.shift_serial_window)

    def start_trans(self):
        input_text = self.input_box.toPlainText()
        try:
            data_in = data_format(input_text)
            ret_dict = all_translate(data_in)
            if ret_dict['res'] == 'ok':
                self.quick_fix_button.setText('修正校验码' if config.good_HCS is not None or config.good_FCS is not None else '修正格式')
            else:
                self.quick_fix_button.setText('修正长度域' if config.good_L is not None else '修正格式')
        except Exception as e:
            print(e)
            traceback.print_exc()
            output('\n\n报文解析过程出现问题，请检查报文。若报文无问题请反馈665593，谢谢！')
        self.output_box.setText(config.output_text)
        config.output_text = ''

    def clear_box(self):
        self.input_box.setFocus()

    def set_level_visible(self):
        config.show_level = self.show_level.isChecked()
        self.start_trans()

    def quick_fix(self):
        input_text = self.input_box.toPlainText()
        data_in = data_format(input_text)
        if config.good_L is not None:
            data_in[1], data_in[2] = config.good_L[0], config.good_L[1]
        else:
            if config.good_HCS is not None:
                ret_dict = get_addr(data_in)
                hcs_pos = 6 + int(ret_dict['server_addr_len'])
                data_in[hcs_pos], data_in[hcs_pos + 1] = config.good_HCS[0], config.good_HCS[1]
                input_text = ''
                for data in data_in:
                    input_text += data + ' '
                self.input_box.setText(input_text)
                self.start_trans()
            if config.good_FCS is not None:
                data_in[-3], data_in[-2] = config.good_FCS[0], config.good_FCS[1]
        input_text = ''
        for data in data_in:
            input_text += data + ' '
        self.input_box.setText(input_text)

    def set_auto_trans(self):
        config.auto_trans = self.auto_trans.isChecked()
        if config.auto_trans is True:
            self.input_box.textChanged.connect(self.start_trans)
            self.translate_button.setVisible(False)
        else:
            self.input_box.textChanged.disconnect(self.start_trans)
            self.translate_button.setVisible(True)
        self.start_trans()

    def set_always_top(self):
        if (self.always_top.isChecked() is True):
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(QtCore.Qt.Widget)
            self.show()

    def calc_len_box(self):
        input_text = self.input_box.toPlainText()
        input_len = calc_len(input_text)
        len_message = str(input_len) + '字节(' + str(hex(input_len)) + ')'
        self.clear_button.setText('清空（' + len_message + '）')

    def show_about_window(self):
        self.about_child.show()

    def shift_serial_window(self):
        self.hide()
        config.serial_child.show()


class AboutWindow(QtGui.QMainWindow, QtGui.QWidget, Ui_AboutWindow):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.setupUi(self)

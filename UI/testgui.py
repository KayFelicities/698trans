# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Kaytest(object):
    def setupUi(self, Kaytest):
        Kaytest.setObjectName(_fromUtf8("Kaytest"))
        Kaytest.resize(450, 606)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/698/698.ico")), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/698/698.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/698/698.ico")), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/698/698.ico")), QtGui.QIcon.Selected, QtGui.QIcon.On)
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/698/698.ico")), QtGui.QIcon.Disabled, QtGui.QIcon.On)
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/698/698.ico")), QtGui.QIcon.Active, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/698/698.ico")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/698/698.ico")), QtGui.QIcon.Active, QtGui.QIcon.On)
        Kaytest.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(Kaytest)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setMargin(3)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.translate_button = QtGui.QPushButton(self.centralwidget)
        self.translate_button.setObjectName(_fromUtf8("translate_button"))
        self.horizontalLayout.addWidget(self.translate_button)
        self.clear_button = QtGui.QPushButton(self.centralwidget)
        self.clear_button.setObjectName(_fromUtf8("clear_button"))
        self.horizontalLayout.addWidget(self.clear_button)
        spacerItem = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.len_box = QtGui.QLineEdit(self.centralwidget)
        self.len_box.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.len_box.sizePolicy().hasHeightForWidth())
        self.len_box.setSizePolicy(sizePolicy)
        self.len_box.setMaximumSize(QtCore.QSize(160, 16777215))
        self.len_box.setObjectName(_fromUtf8("len_box"))
        self.horizontalLayout.addWidget(self.len_box)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.input_box = QtGui.QTextEdit(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.input_box.sizePolicy().hasHeightForWidth())
        self.input_box.setSizePolicy(sizePolicy)
        self.input_box.setAcceptDrops(False)
        self.input_box.setToolTip(_fromUtf8(""))
        self.input_box.setStatusTip(_fromUtf8(""))
        self.input_box.setWhatsThis(_fromUtf8(""))
        self.input_box.setAccessibleName(_fromUtf8(""))
        self.input_box.setAccessibleDescription(_fromUtf8(""))
        self.input_box.setAutoFillBackground(False)
        self.input_box.setStyleSheet(_fromUtf8(""))
        self.input_box.setFrameShape(QtGui.QFrame.NoFrame)
        self.input_box.setFrameShadow(QtGui.QFrame.Sunken)
        self.input_box.setMidLineWidth(1)
        self.input_box.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.input_box.setDocumentTitle(_fromUtf8(""))
        self.input_box.setLineWrapMode(QtGui.QTextEdit.WidgetWidth)
        self.input_box.setOverwriteMode(False)
        self.input_box.setAcceptRichText(True)
        self.input_box.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.input_box.setObjectName(_fromUtf8("input_box"))
        self.output_box = QtGui.QTextEdit(self.splitter)
        self.output_box.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.output_box.sizePolicy().hasHeightForWidth())
        self.output_box.setSizePolicy(sizePolicy)
        self.output_box.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.output_box.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.output_box.setAutoFillBackground(False)
        self.output_box.setObjectName(_fromUtf8("output_box"))
        self.verticalLayout.addWidget(self.splitter)
        self.splitter.raise_()
        Kaytest.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Kaytest)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 450, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        Kaytest.setMenuBar(self.menubar)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(Kaytest)
        QtCore.QObject.connect(self.clear_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.output_box.clear)
        QtCore.QObject.connect(self.clear_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.input_box.clear)
        QtCore.QMetaObject.connectSlotsByName(Kaytest)
        Kaytest.setTabOrder(self.input_box, self.translate_button)
        Kaytest.setTabOrder(self.translate_button, self.output_box)
        Kaytest.setTabOrder(self.output_box, self.len_box)
        Kaytest.setTabOrder(self.len_box, self.clear_button)

    def retranslateUi(self, Kaytest):
        Kaytest.setWindowTitle(_translate("Kaytest", "698解析工具_V2.0Beta(2016.11.29)", None))
        self.translate_button.setText(_translate("Kaytest", "解析", None))
        self.clear_button.setText(_translate("Kaytest", "清空", None))
        self.label.setText(_translate("Kaytest", "长度:", None))
        self.input_box.setHtml(_translate("Kaytest", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.output_box.setHtml(_translate("Kaytest", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">解析结果：</p></body></html>", None))
        self.menu.setTitle(_translate("Kaytest", "关于", None))

import icon_rc

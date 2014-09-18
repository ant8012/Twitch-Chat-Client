# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created: Sun Sep  7 20:13:34 2014
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setEnabled(True)
        Dialog.resize(659, 454)
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.gridLayout.setContentsMargins(0, -1, -1, -1)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 3, 1, 1, 1)
        self.streamcheckBox = QtGui.QCheckBox(Dialog)
        self.streamcheckBox.setEnabled(True)
        self.streamcheckBox.setAcceptDrops(False)
        self.streamcheckBox.setCheckable(True)
        self.streamcheckBox.setTristate(False)
        self.streamcheckBox.setObjectName(_fromUtf8("streamcheckBox"))
        self.gridLayout.addWidget(self.streamcheckBox, 3, 0, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.cancel = QtGui.QPushButton(Dialog)
        self.cancel.setObjectName(_fromUtf8("cancel"))
        self.gridLayout.addWidget(self.cancel, 7, 4, 1, 1)
        self.apply_settings = QtGui.QPushButton(Dialog)
        self.apply_settings.setObjectName(_fromUtf8("apply_settings"))
        self.gridLayout.addWidget(self.apply_settings, 7, 3, 1, 1)
        self.autoLogin = QtGui.QCheckBox(Dialog)
        self.autoLogin.setObjectName(_fromUtf8("autoLogin"))
        self.gridLayout.addWidget(self.autoLogin, 7, 0, 1, 1)
        self.stream = QtGui.QLineEdit(Dialog)
        self.stream.setEnabled(True)
        self.stream.setAutoFillBackground(False)
        self.stream.setDragEnabled(True)
        self.stream.setObjectName(_fromUtf8("stream"))
        self.gridLayout.addWidget(self.stream, 3, 2, 1, 2)
        self.password = QtGui.QLineEdit(Dialog)
        self.password.setText(_fromUtf8(""))
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName(_fromUtf8("password"))
        self.gridLayout.addWidget(self.password, 2, 2, 1, 2)
        self.username = QtGui.QLineEdit(Dialog)
        self.username.setObjectName(_fromUtf8("username"))
        self.gridLayout.addWidget(self.username, 0, 2, 1, 2)
        self.disableLiveStreamer = QtGui.QCheckBox(Dialog)
        self.disableLiveStreamer.setObjectName(_fromUtf8("disableLiveStreamer"))
        self.gridLayout.addWidget(self.disableLiveStreamer, 4, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_3.setText(_translate("Dialog", "Stream:", None))
        self.streamcheckBox.setText(_translate("Dialog", "Load Stream on login", None))
        self.label_2.setText(_translate("Dialog", "Passowrd:", None))
        self.label.setText(_translate("Dialog", "User name:", None))
        self.cancel.setText(_translate("Dialog", "Cancel", None))
        self.apply_settings.setText(_translate("Dialog", "Ok", None))
        self.autoLogin.setText(_translate("Dialog", "Auto Login on Startup", None))
        self.disableLiveStreamer.setText(_translate("Dialog", "Disable livestreamer", None))


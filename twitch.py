# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'twitch.ui'
#
# Created: Sun Sep  7 18:57:45 2014
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

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName(_fromUtf8("mainWindow"))
        mainWindow.resize(382, 709)
        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.displayBox = QtGui.QTextBrowser(self.centralwidget)
        self.displayBox.setObjectName(_fromUtf8("displayBox"))
        self.verticalLayout.addWidget(self.displayBox)
        self.chat_box = QtGui.QLineEdit(self.centralwidget)
        self.chat_box.setEnabled(False)
        self.chat_box.setAutoFillBackground(False)
        self.chat_box.setMaxLength(400)
        self.chat_box.setObjectName(_fromUtf8("chat_box"))
        self.verticalLayout.addWidget(self.chat_box)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 382, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(mainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        mainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(mainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionLogin = QtGui.QAction(mainWindow)
        self.actionLogin.setObjectName(_fromUtf8("actionLogin"))
        self.actionLogout = QtGui.QAction(mainWindow)
        self.actionLogout.setObjectName(_fromUtf8("actionLogout"))
        self.actionSettings = QtGui.QAction(mainWindow)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        self.actionchangeStream = QtGui.QAction(mainWindow)
        self.actionchangeStream.setEnabled(False)
        self.actionchangeStream.setObjectName(_fromUtf8("actionchangeStream"))
        self.actionClearScreen = QtGui.QAction(mainWindow)
        self.actionClearScreen.setObjectName(_fromUtf8("actionClearScreen"))
        self.actionOpen_vlc = QtGui.QAction(mainWindow)
        self.actionOpen_vlc.setObjectName(_fromUtf8("actionOpen_vlc"))
        self.actionOpenCloseStream = QtGui.QAction(mainWindow)
        self.actionOpenCloseStream.setEnabled(False)
        self.actionOpenCloseStream.setObjectName(_fromUtf8("actionOpenCloseStream"))
        self.menuFile.addAction(self.actionLogin)
        self.menuFile.addAction(self.actionLogout)
        self.menuFile.addAction(self.actionchangeStream)
        self.menuFile.addAction(self.actionOpenCloseStream)
        self.menuFile.addAction(self.actionClearScreen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(_translate("mainWindow", "MainWindow", None))
        self.menuFile.setTitle(_translate("mainWindow", "File", None))
        self.actionExit.setText(_translate("mainWindow", "Exit", None))
        self.actionLogin.setText(_translate("mainWindow", "Login", None))
        self.actionLogin.setShortcut(_translate("mainWindow", "F1", None))
        self.actionLogout.setText(_translate("mainWindow", "Logout", None))
        self.actionLogout.setShortcut(_translate("mainWindow", "F2", None))
        self.actionSettings.setText(_translate("mainWindow", "Settings", None))
        self.actionSettings.setShortcut(_translate("mainWindow", "F10", None))
        self.actionchangeStream.setText(_translate("mainWindow", "Change Stream", None))
        self.actionchangeStream.setShortcut(_translate("mainWindow", "F3", None))
        self.actionClearScreen.setText(_translate("mainWindow", "Clear Chat", None))
        self.actionClearScreen.setShortcut(_translate("mainWindow", "F5", None))
        self.actionOpen_vlc.setText(_translate("mainWindow", "Open vlc", None))
        self.actionOpenCloseStream.setText(_translate("mainWindow", "Open stream", None))
        self.actionOpenCloseStream.setShortcut(_translate("mainWindow", "F4", None))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'twitch.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TwitchWindow(object):
    def setupUi(self, TwitchWindow):
        TwitchWindow.setObjectName("TwitchWindow")
        TwitchWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(TwitchWindow)
        self.centralwidget.setObjectName("centralwidget")
        TwitchWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(TwitchWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 18))
        self.menubar.setObjectName("menubar")
        TwitchWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(TwitchWindow)
        self.statusbar.setObjectName("statusbar")
        TwitchWindow.setStatusBar(self.statusbar)

        self.retranslateUi(TwitchWindow)
        QtCore.QMetaObject.connectSlotsByName(TwitchWindow)

    def retranslateUi(self, TwitchWindow):
        _translate = QtCore.QCoreApplication.translate
        TwitchWindow.setWindowTitle(_translate("TwitchWindow", "MainWindow"))


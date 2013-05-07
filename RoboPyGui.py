# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RoboPyGui.ui'
#
# Created: Tue May  7 09:29:24 2013
#      by: PyQt4 UI code generator 4.10
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

class Ui_RoboMainWnd(object):
    def setupUi(self, RoboMainWnd):
        RoboMainWnd.setObjectName(_fromUtf8("RoboMainWnd"))
        RoboMainWnd.resize(703, 168)
        self.centralwidget = QtGui.QWidget(RoboMainWnd)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        RoboMainWnd.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(RoboMainWnd)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 703, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        RoboMainWnd.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(RoboMainWnd)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        RoboMainWnd.setStatusBar(self.statusbar)
        self.roboActionOpen = QtGui.QAction(RoboMainWnd)
        self.roboActionOpen.setObjectName(_fromUtf8("roboActionOpen"))
        self.roboActionSave = QtGui.QAction(RoboMainWnd)
        self.roboActionSave.setObjectName(_fromUtf8("roboActionSave"))
        self.menuFile.addAction(self.roboActionOpen)
        self.menuFile.addAction(self.roboActionSave)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(RoboMainWnd)
        QtCore.QMetaObject.connectSlotsByName(RoboMainWnd)

    def retranslateUi(self, RoboMainWnd):
        RoboMainWnd.setWindowTitle(_translate("RoboMainWnd", "RoboPy", None))
        self.menuFile.setTitle(_translate("RoboMainWnd", "File", None))
        self.roboActionOpen.setText(_translate("RoboMainWnd", "Open", None))
        self.roboActionSave.setText(_translate("RoboMainWnd", "Save", None))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RoboPyGui.ui'
#
# Created: Mon Jun  9 11:49:09 2014
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

class Ui_RoboMainWnd(object):
    def setupUi(self, RoboMainWnd):
        RoboMainWnd.setObjectName(_fromUtf8("RoboMainWnd"))
        RoboMainWnd.resize(703, 168)
        self.centralwidget = QtGui.QWidget(RoboMainWnd)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        RoboMainWnd.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(RoboMainWnd)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 703, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuLoad = QtGui.QMenu(self.menuFile)
        self.menuLoad.setObjectName(_fromUtf8("menuLoad"))
        RoboMainWnd.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(RoboMainWnd)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        RoboMainWnd.setStatusBar(self.statusbar)
        self.roboActionSave = QtGui.QAction(RoboMainWnd)
        self.roboActionSave.setObjectName(_fromUtf8("roboActionSave"))
        self.roboActionOpen_2 = QtGui.QAction(RoboMainWnd)
        self.roboActionOpen_2.setObjectName(_fromUtf8("roboActionOpen_2"))
        self.roboActionLoadInRam = QtGui.QAction(RoboMainWnd)
        self.roboActionLoadInRam.setObjectName(_fromUtf8("roboActionLoadInRam"))
        self.roboActionOpen = QtGui.QAction(RoboMainWnd)
        self.roboActionOpen.setObjectName(_fromUtf8("roboActionOpen"))
        self.actionLoad_Sequentially = QtGui.QAction(RoboMainWnd)
        self.actionLoad_Sequentially.setObjectName(_fromUtf8("actionLoad_Sequentially"))
        self.actionOpen_Next = QtGui.QAction(RoboMainWnd)
        self.actionOpen_Next.setObjectName(_fromUtf8("actionOpen_Next"))
        self.menuLoad.addAction(self.roboActionOpen)
        self.menuLoad.addAction(self.roboActionLoadInRam)
        self.menuFile.addAction(self.menuLoad.menuAction())
        self.menuFile.addAction(self.roboActionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionLoad_Sequentially)
        self.menuFile.addAction(self.actionOpen_Next)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(RoboMainWnd)
        QtCore.QMetaObject.connectSlotsByName(RoboMainWnd)

    def retranslateUi(self, RoboMainWnd):
        RoboMainWnd.setWindowTitle(_translate("RoboMainWnd", "RoboPy", None))
        self.menuFile.setTitle(_translate("RoboMainWnd", "File", None))
        self.menuLoad.setTitle(_translate("RoboMainWnd", "Load", None))
        self.roboActionSave.setText(_translate("RoboMainWnd", "Save", None))
        self.roboActionOpen_2.setText(_translate("RoboMainWnd", "Read from disk", None))
        self.roboActionLoadInRam.setText(_translate("RoboMainWnd", "Load in memory", None))
        self.roboActionOpen.setText(_translate("RoboMainWnd", "Read from disk", None))
        self.actionLoad_Sequentially.setText(_translate("RoboMainWnd", "Load list of Files Sequentially", None))
        self.actionOpen_Next.setText(_translate("RoboMainWnd", "Open Next", None))


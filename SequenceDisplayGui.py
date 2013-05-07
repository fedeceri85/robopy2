# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SequenceDisplayGui.ui'
#
# Created: Tue May  7 15:04:27 2013
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

class Ui_SequenceDisplayWnd(object):
    def setupUi(self, SequenceDisplayWnd):
        SequenceDisplayWnd.setObjectName(_fromUtf8("SequenceDisplayWnd"))
        SequenceDisplayWnd.resize(640, 480)
        self.centralwidget = QtGui.QWidget(SequenceDisplayWnd)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ImageFrameWidget = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.ImageFrameWidget.sizePolicy().hasHeightForWidth())
        self.ImageFrameWidget.setSizePolicy(sizePolicy)
        self.ImageFrameWidget.setObjectName(_fromUtf8("ImageFrameWidget"))
        self.verticalLayout.addWidget(self.ImageFrameWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.CurrentFrameSpinBox = QtGui.QSpinBox(self.centralwidget)
        self.CurrentFrameSpinBox.setObjectName(_fromUtf8("CurrentFrameSpinBox"))
        self.horizontalLayout.addWidget(self.CurrentFrameSpinBox)
        self.CurrentFrameSlider = QtGui.QSlider(self.centralwidget)
        self.CurrentFrameSlider.setOrientation(QtCore.Qt.Horizontal)
        self.CurrentFrameSlider.setObjectName(_fromUtf8("CurrentFrameSlider"))
        self.horizontalLayout.addWidget(self.CurrentFrameSlider)
        spacerItem = QtGui.QSpacerItem(178, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        SequenceDisplayWnd.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(SequenceDisplayWnd)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        SequenceDisplayWnd.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(SequenceDisplayWnd)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        SequenceDisplayWnd.setStatusBar(self.statusbar)

        self.retranslateUi(SequenceDisplayWnd)
        QtCore.QMetaObject.connectSlotsByName(SequenceDisplayWnd)

    def retranslateUi(self, SequenceDisplayWnd):
        SequenceDisplayWnd.setWindowTitle(_translate("SequenceDisplayWnd", "SequenceDisplay", None))


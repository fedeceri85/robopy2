# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AviSettingsGui.ui'
#
# Created: Fri Aug  2 11:54:06 2013
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

class Ui_aviSettingsWnd(object):
    def setupUi(self, aviSettingsWnd):
        aviSettingsWnd.setObjectName(_fromUtf8("aviSettingsWnd"))
        aviSettingsWnd.setWindowModality(QtCore.Qt.WindowModal)
        aviSettingsWnd.resize(647, 480)
        self.verticalLayout = QtGui.QVBoxLayout(aviSettingsWnd)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.selectFileButton = QtGui.QPushButton(aviSettingsWnd)
        self.selectFileButton.setObjectName(_fromUtf8("selectFileButton"))
        self.gridLayout.addWidget(self.selectFileButton, 0, 0, 1, 1)
        self.fileNameEdit = QtGui.QLineEdit(aviSettingsWnd)
        self.fileNameEdit.setObjectName(_fromUtf8("fileNameEdit"))
        self.gridLayout.addWidget(self.fileNameEdit, 0, 1, 1, 3)
        self.label = QtGui.QLabel(aviSettingsWnd)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.fpsSpinBox = QtGui.QSpinBox(aviSettingsWnd)
        self.fpsSpinBox.setMinimum(1)
        self.fpsSpinBox.setProperty("value", 25)
        self.fpsSpinBox.setObjectName(_fromUtf8("fpsSpinBox"))
        self.gridLayout.addWidget(self.fpsSpinBox, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 3, 1, 1)
        self.label_2 = QtGui.QLabel(aviSettingsWnd)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.widthSpinBox = QtGui.QSpinBox(aviSettingsWnd)
        self.widthSpinBox.setMinimum(4)
        self.widthSpinBox.setMaximum(100000)
        self.widthSpinBox.setProperty("value", 25)
        self.widthSpinBox.setObjectName(_fromUtf8("widthSpinBox"))
        self.gridLayout.addWidget(self.widthSpinBox, 2, 1, 1, 1)
        self.heightSpinBox = QtGui.QSpinBox(aviSettingsWnd)
        self.heightSpinBox.setMinimum(4)
        self.heightSpinBox.setMaximum(100000)
        self.heightSpinBox.setProperty("value", 25)
        self.heightSpinBox.setObjectName(_fromUtf8("heightSpinBox"))
        self.gridLayout.addWidget(self.heightSpinBox, 2, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 3, 1, 1)
        self.label_3 = QtGui.QLabel(aviSettingsWnd)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.firstFrameSpinBox = QtGui.QSpinBox(aviSettingsWnd)
        self.firstFrameSpinBox.setMinimum(1)
        self.firstFrameSpinBox.setMaximum(10000000)
        self.firstFrameSpinBox.setProperty("value", 25)
        self.firstFrameSpinBox.setObjectName(_fromUtf8("firstFrameSpinBox"))
        self.gridLayout.addWidget(self.firstFrameSpinBox, 3, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 3, 3, 1, 1)
        self.label_4 = QtGui.QLabel(aviSettingsWnd)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.lastFrameSpinBox = QtGui.QSpinBox(aviSettingsWnd)
        self.lastFrameSpinBox.setMinimum(1)
        self.lastFrameSpinBox.setMaximum(1000000000)
        self.lastFrameSpinBox.setProperty("value", 25)
        self.lastFrameSpinBox.setObjectName(_fromUtf8("lastFrameSpinBox"))
        self.gridLayout.addWidget(self.lastFrameSpinBox, 4, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 4, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem4 = QtGui.QSpacerItem(20, 296, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.buttonBox = QtGui.QDialogButtonBox(aviSettingsWnd)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(aviSettingsWnd)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), aviSettingsWnd.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), aviSettingsWnd.reject)
        QtCore.QMetaObject.connectSlotsByName(aviSettingsWnd)

    def retranslateUi(self, aviSettingsWnd):
        aviSettingsWnd.setWindowTitle(_translate("aviSettingsWnd", "Avi settings", None))
        self.selectFileButton.setText(_translate("aviSettingsWnd", "File", None))
        self.label.setText(_translate("aviSettingsWnd", "Fps:", None))
        self.label_2.setText(_translate("aviSettingsWnd", "Size:", None))
        self.label_3.setText(_translate("aviSettingsWnd", "First frame:", None))
        self.label_4.setText(_translate("aviSettingsWnd", "Last frame:", None))


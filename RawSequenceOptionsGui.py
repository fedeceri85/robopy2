# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RawSequenceOptionsGui.ui'
#
# Created: Sat Jul 27 13:11:13 2013
#      by: PyQt4 UI code generator 4.10.2
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
        Dialog.resize(215, 231)
        Dialog.setAutoFillBackground(False)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.rebinComboBox = QtGui.QComboBox(Dialog)
        self.rebinComboBox.setObjectName(_fromUtf8("rebinComboBox"))
        self.rebinComboBox.addItem(_fromUtf8(""))
        self.rebinComboBox.addItem(_fromUtf8(""))
        self.rebinComboBox.addItem(_fromUtf8(""))
        self.rebinComboBox.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.rebinComboBox)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.LCcheckBox = QtGui.QCheckBox(Dialog)
        self.LCcheckBox.setObjectName(_fromUtf8("LCcheckBox"))
        self.verticalLayout.addWidget(self.LCcheckBox)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setEnabled(False)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.leftLCSpinBox = QtGui.QSpinBox(Dialog)
        self.leftLCSpinBox.setEnabled(False)
        self.leftLCSpinBox.setObjectName(_fromUtf8("leftLCSpinBox"))
        self.horizontalLayout_2.addWidget(self.leftLCSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setEnabled(False)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.rightLCSpinBox = QtGui.QSpinBox(Dialog)
        self.rightLCSpinBox.setEnabled(False)
        self.rightLCSpinBox.setObjectName(_fromUtf8("rightLCSpinBox"))
        self.horizontalLayout_3.addWidget(self.rightLCSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Raw Sequence Options", None))
        self.label.setText(_translate("Dialog", "Rebin", None))
        self.rebinComboBox.setItemText(0, _translate("Dialog", "1", None))
        self.rebinComboBox.setItemText(1, _translate("Dialog", "2", None))
        self.rebinComboBox.setItemText(2, _translate("Dialog", "4", None))
        self.rebinComboBox.setItemText(3, _translate("Dialog", "8", None))
        self.LCcheckBox.setText(_translate("Dialog", "Line correction", None))
        self.label_2.setText(_translate("Dialog", "Left", None))
        self.label_3.setText(_translate("Dialog", "Right", None))


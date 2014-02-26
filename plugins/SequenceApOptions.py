# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SequenceApOptions.ui'
#
# Created: Fri Sep 20 13:01:07 2013
#      by: PyQt4 UI code generator 4.10.3
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
        Dialog.resize(172, 172)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.timeScaleSpinBox = QtGui.QDoubleSpinBox(Dialog)
        self.timeScaleSpinBox.setDecimals(3)
        self.timeScaleSpinBox.setProperty("value", 0.05)
        self.timeScaleSpinBox.setObjectName(_fromUtf8("timeScaleSpinBox"))
        self.horizontalLayout.addWidget(self.timeScaleSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.dataScaleFactor = QtGui.QDoubleSpinBox(Dialog)
        self.dataScaleFactor.setDecimals(3)
        self.dataScaleFactor.setProperty("value", 3.0)
        self.dataScaleFactor.setObjectName(_fromUtf8("dataScaleFactor"))
        self.horizontalLayout_2.addWidget(self.dataScaleFactor)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.xSpinBox = QtGui.QSpinBox(Dialog)
        self.xSpinBox.setMaximum(10000)
        self.xSpinBox.setObjectName(_fromUtf8("xSpinBox"))
        self.horizontalLayout_3.addWidget(self.xSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_4.addWidget(self.label_4)
        self.ySpinBox = QtGui.QSpinBox(Dialog)
        self.ySpinBox.setMaximum(10000)
        self.ySpinBox.setProperty("value", 400)
        self.ySpinBox.setObjectName(_fromUtf8("ySpinBox"))
        self.horizontalLayout_4.addWidget(self.ySpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_5.addWidget(self.label_5)
        self.lwSpinBox = QtGui.QDoubleSpinBox(Dialog)
        self.lwSpinBox.setDecimals(2)
        self.lwSpinBox.setMaximum(4.0)
        self.lwSpinBox.setProperty("value", 1.0)
        self.lwSpinBox.setObjectName(_fromUtf8("lwSpinBox"))
        self.horizontalLayout_5.addWidget(self.lwSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_6.addWidget(self.label_6)
        self.frameSpanSpinBox = QtGui.QSpinBox(Dialog)
        self.frameSpanSpinBox.setMaximum(1000)
        self.frameSpanSpinBox.setProperty("value", 25)
        self.frameSpanSpinBox.setObjectName(_fromUtf8("frameSpanSpinBox"))
        self.horizontalLayout_6.addWidget(self.frameSpanSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Calcium AP options", None))
        self.label.setText(_translate("Dialog", "Time scale factor", None))
        self.label_2.setText(_translate("Dialog", "Data scale factor", None))
        self.label_3.setText(_translate("Dialog", "x", None))
        self.label_4.setText(_translate("Dialog", "y", None))
        self.label_5.setText(_translate("Dialog", "Linewidth", None))
        self.label_6.setText(_translate("Dialog", "frame Span", None))


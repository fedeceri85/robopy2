# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProcessOptionsGui.ui'
#
# Created: Mon May 20 12:02:32 2013
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

class Ui_ProcessOptionsDlg(object):
    def setupUi(self, ProcessOptionsDlg):
        ProcessOptionsDlg.setObjectName(_fromUtf8("ProcessOptionsDlg"))
        ProcessOptionsDlg.resize(463, 392)
        self.verticalLayout = QtGui.QVBoxLayout(ProcessOptionsDlg)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.PO_TabWidget = QtGui.QTabWidget(ProcessOptionsDlg)
        self.PO_TabWidget.setObjectName(_fromUtf8("PO_TabWidget"))
        self.FrameOptionsTab = QtGui.QWidget()
        self.FrameOptionsTab.setObjectName(_fromUtf8("FrameOptionsTab"))
        self.widget = QtGui.QWidget(self.FrameOptionsTab)
        self.widget.setGeometry(QtCore.QRect(20, 10, 405, 86))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setHorizontalSpacing(15)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.FirstFrameLabel = QtGui.QLabel(self.widget)
        self.FirstFrameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.FirstFrameLabel.setObjectName(_fromUtf8("FirstFrameLabel"))
        self.gridLayout.addWidget(self.FirstFrameLabel, 0, 0, 1, 1)
        self.FirstFrameSpinBox = QtGui.QSpinBox(self.widget)
        self.FirstFrameSpinBox.setMinimum(1)
        self.FirstFrameSpinBox.setMaximum(99999)
        self.FirstFrameSpinBox.setObjectName(_fromUtf8("FirstFrameSpinBox"))
        self.gridLayout.addWidget(self.FirstFrameSpinBox, 0, 1, 1, 1)
        self.ProcessTypeLabel = QtGui.QLabel(self.widget)
        self.ProcessTypeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ProcessTypeLabel.setObjectName(_fromUtf8("ProcessTypeLabel"))
        self.gridLayout.addWidget(self.ProcessTypeLabel, 0, 2, 1, 1)
        self.ProcessTypeComboBox = QtGui.QComboBox(self.widget)
        self.ProcessTypeComboBox.setObjectName(_fromUtf8("ProcessTypeComboBox"))
        self.ProcessTypeComboBox.addItem(_fromUtf8(""))
        self.ProcessTypeComboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.ProcessTypeComboBox, 0, 3, 2, 1)
        self.LastFrameLabel = QtGui.QLabel(self.widget)
        self.LastFrameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.LastFrameLabel.setObjectName(_fromUtf8("LastFrameLabel"))
        self.gridLayout.addWidget(self.LastFrameLabel, 1, 0, 2, 1)
        self.LastFrameSpinBox = QtGui.QSpinBox(self.widget)
        self.LastFrameSpinBox.setMinimum(1)
        self.LastFrameSpinBox.setMaximum(99999)
        self.LastFrameSpinBox.setObjectName(_fromUtf8("LastFrameSpinBox"))
        self.gridLayout.addWidget(self.LastFrameSpinBox, 1, 1, 2, 1)
        self.FirstWavelengthLabel = QtGui.QLabel(self.widget)
        self.FirstWavelengthLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.FirstWavelengthLabel.setObjectName(_fromUtf8("FirstWavelengthLabel"))
        self.gridLayout.addWidget(self.FirstWavelengthLabel, 2, 2, 1, 1)
        self.FirstWavelengthSpinBox = QtGui.QSpinBox(self.widget)
        self.FirstWavelengthSpinBox.setMinimum(1)
        self.FirstWavelengthSpinBox.setMaximum(99999)
        self.FirstWavelengthSpinBox.setObjectName(_fromUtf8("FirstWavelengthSpinBox"))
        self.gridLayout.addWidget(self.FirstWavelengthSpinBox, 2, 3, 1, 1)
        self.CycleSizeLabel = QtGui.QLabel(self.widget)
        self.CycleSizeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.CycleSizeLabel.setObjectName(_fromUtf8("CycleSizeLabel"))
        self.gridLayout.addWidget(self.CycleSizeLabel, 3, 0, 1, 1)
        self.CycleSizeSpinBox = QtGui.QSpinBox(self.widget)
        self.CycleSizeSpinBox.setMinimum(1)
        self.CycleSizeSpinBox.setMaximum(99999)
        self.CycleSizeSpinBox.setObjectName(_fromUtf8("CycleSizeSpinBox"))
        self.gridLayout.addWidget(self.CycleSizeSpinBox, 3, 1, 1, 1)
        self.SecondWavelengthLabel = QtGui.QLabel(self.widget)
        self.SecondWavelengthLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.SecondWavelengthLabel.setObjectName(_fromUtf8("SecondWavelengthLabel"))
        self.gridLayout.addWidget(self.SecondWavelengthLabel, 3, 2, 1, 1)
        self.SecondWavelengthSpinBox = QtGui.QSpinBox(self.widget)
        self.SecondWavelengthSpinBox.setMinimum(1)
        self.SecondWavelengthSpinBox.setMaximum(99999)
        self.SecondWavelengthSpinBox.setObjectName(_fromUtf8("SecondWavelengthSpinBox"))
        self.gridLayout.addWidget(self.SecondWavelengthSpinBox, 3, 3, 1, 1)
        self.PO_TabWidget.addTab(self.FrameOptionsTab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.PO_TabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.PO_TabWidget)

        self.retranslateUi(ProcessOptionsDlg)
        self.PO_TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ProcessOptionsDlg)

    def retranslateUi(self, ProcessOptionsDlg):
        ProcessOptionsDlg.setWindowTitle(_translate("ProcessOptionsDlg", "Dialog", None))
        self.FirstFrameLabel.setText(_translate("ProcessOptionsDlg", "First frame:", None))
        self.ProcessTypeLabel.setText(_translate("ProcessOptionsDlg", "Process type:", None))
        self.ProcessTypeComboBox.setItemText(0, _translate("ProcessOptionsDlg", "Single wavelength", None))
        self.ProcessTypeComboBox.setItemText(1, _translate("ProcessOptionsDlg", "Ratiometric", None))
        self.LastFrameLabel.setText(_translate("ProcessOptionsDlg", "Last frame:", None))
        self.FirstWavelengthLabel.setText(_translate("ProcessOptionsDlg", "First wavelength:", None))
        self.CycleSizeLabel.setText(_translate("ProcessOptionsDlg", "Cycle size:", None))
        self.SecondWavelengthLabel.setText(_translate("ProcessOptionsDlg", "Second wavelength:", None))
        self.PO_TabWidget.setTabText(self.PO_TabWidget.indexOf(self.FrameOptionsTab), _translate("ProcessOptionsDlg", "Frame options", None))
        self.PO_TabWidget.setTabText(self.PO_TabWidget.indexOf(self.tab_2), _translate("ProcessOptionsDlg", "Tab 2", None))


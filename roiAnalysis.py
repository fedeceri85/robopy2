from roiAnalysis_gui import Ui_MainWindow
from PyQt4 import QtCore, QtGui
import numpy as np
import PyQt4.Qwt5
from PyQt4.Qwt5.qplt import *

class MainWindow(Ui_MainWindow, PyQt4.QtGui.QMainWindow):
    
    
    def __init__(self, parent=None):
        PyQt4.QtGui.QMainWindow.__init__(self, parent=None)
        self.setupUi(self)
        self.show()
        self.curve = Qwt.QwtPlotCurve("Vm")
        self.curve_2 = Qwt.QwtPlotCurve("Vm2")
        self.curve_3= Qwt.QwtPlotCurve("Vm3")
        self.curve_2.attach(self.qwtPlot)
        self.curve_3.attach(self.qwtPlot)
      
        self.curve.attach(self.qwtPlot)
        self.qwtPlot.setTitle("")
        self.qwtPlot.setAxisTitle(Qwt.QwtPlot.xBottom, "Frame")
        self.qwtPlot.setAxisTitle(Qwt.QwtPlot.yLeft, "Fluorescence")
        self.curve.setPen(PyQt4.Qt.QPen(PyQt4.Qt.Qt.red))
        self.curve_2.setPen(PyQt4.Qt.QPen(PyQt4.Qt.Qt.green))
        self.curve_3.setPen(PyQt4.Qt.QPen(PyQt4.Qt.Qt.blue))



    def makePlot(self,y):
    
        self.curve.setData(np.arange(y.size),y)
        self.qwtPlot.replot()
    def makePlot2(self,y):
    
        self.curve_2.setData(np.arange(y.size),y)
        self.qwtPlot.replot()    

    def makePlot3(self,y):
    
        self.curve_3.setData(np.arange(y.size),y)
        self.qwtPlot.replot()

if __name__ == "__main__":
    app = PyQt4.QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.makePlot(np.arange(100))

    window.show()

    sys.exit(app.exec_())


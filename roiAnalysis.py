# -*- coding: utf-8 -*-
"""
This example demonstrates the use of RemoteGraphicsView to improve performance in
applications with heavy load. It works by starting a second process to handle 
all graphics rendering, thus freeing up the main process to do its work.

In this example, the update() function is very expensive and is called frequently.
After update() generates a new set of data, it can either plot directly to a local
plot (bottom) or remotely via a RemoteGraphicsView (top), allowing speed comparison
between the two cases. IF you have a multi-core CPU, it should be obvious that the 
remote case is much faster.
"""

from PyQt4 import QtGui,QtCore
import numpy as np
import pyqtgraph as pg

#QtGui.QApplication.setGraphicsSystem('raster')
#mw = QtGui.QMainWindow()
#mw.resize(800,800)


class MainWindow(QtGui.QMainWindow):
    
    
      def __init__(self, parent=None):
            QtGui.QMainWindow.__init__(self, parent=parent)
            self.show()
            #win = pg.GraphicsWindow(title="Basic plotting examples")
            self.view = pg.PlotWidget(self)

            # self.view = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
            pg.setConfigOptions(antialias=True)  ## this will be expensive for the local plot
            #self.view.pg.setConfigOptions(antialias=True)  ## prettier plots at no cost to the main process! 
            self.view.setWindowTitle('pyqtgraph example: RemoteSpeedTest')
            self.resize(1000,600)
            #win.setWindowTitle('pyqtgraph example: Plotting')

            # Enable antialiasing for prettier plots
            pg.setConfigOptions(antialias=True)
            self.setCentralWidget(self.view)    
            self.curve = self.view.plot()


      def makePlot(self,y):
            self.curve.setData(y)
            #self.lplt.plot(np.arange(size(y)),y, clear=True, _callSync='off')  ## We do not expect a return value.

from PyQt4 import QtGui,QtCore
import numpy as np
import pyqtgraph as pg
import sys
#QtGui.QApplication.setGraphicsSystem('raster')
#mw = QtGui.QMainWindow()
#mw.resize(800,800)


class plotWindow(pg.GraphicsWindow):
    
    
	def __init__(self, parent=None):
		pg.setConfigOptions(antialias=True)
		pg.setConfigOption('background', 'w')
		pg.setConfigOption('foreground', 'k')
		pg.GraphicsWindow.__init__(self, parent=parent)
		#win = pg.GraphicsWindow(title="Basic plotting examples")
		# self.view = pg.PlotWidget(self)

		# self.view = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
		#self.view.pg.setConfigOptions(antialias=True)  ## prettier plots at no cost to the main process! 
		# self.view.setWindowTitle('pyqtgraph example: RemoteSpeedTest')
		self.resize(800,600)
		#win.setWindowTitle('pyqtgraph example: Plotting')

		# Enable antialiasing for prettier plots


		# self.setCentralWidget(self.view)    
		# self.curve = self.view.plot()
		self.curve = []
		x2 = np.linspace(-100, 100, 1000)
		data2 = np.sin(x2) / x2

		self.p8 = self.addPlot(title="Region Selection")
		pl8 = self.p8.plot()#data2, pen=(255,255,255,200))

		self.nextRow()

		self.p9 = self.addPlot(title="Zoom on selected region")
		pl9 = self.p9.plot()


		self.show()

	def updatePlot(self):
	    self.p9.setXRange(*self.lr.getRegion(), padding=0)

	def updateRegion(self):
	    self.lr.setRegion(self.p9.getViewBox().viewRange()[0])
	def plot(self,x,y,xlabel='',ylabel='',colors = None):
		self.p8.clear()
		self.p9.clear()
		self.lr = pg.LinearRegionItem([0,10])
		self.lr.setZValue(-10)
		self.p8.addItem(self.lr)
		self.lr.sigRegionChanged.connect(self.updatePlot)
		self.p9.sigXRangeChanged.connect(self.updateRegion)
		self.updatePlot()
		for i in xrange(y.shape[1]):
			if colors is not None:
				color = colors[i]
			else:
				color = [255,255,255,255]
			self.p8.plot(x,y[:,i],pen=color)#, pen=(255,255,255,200))
			self.p9.plot(x,y[:,i],pen=color)#, pen=(255,255,255,200))
		self.p8.setLabel('left',ylabel)
		self.p8.setLabel('bottom',xlabel)
		self.p9.setLabel('left',ylabel)
		self.p9.setLabel('bottom',xlabel)
	    #self.lplt.plot(np.arange(size(y)),y, clear=True, _callSync='off')  ## We do not expect a return value.



if __name__ =='__main__':
	app = QtGui.QApplication(sys.argv)
	robopy = MainWindow()
	robopy.show()

	#ipshell = InteractiveShellEmbed()
	#ipshell()
	
	ans = app.exec_()

	sys.exit(ans)
from PyQt4 import QtGui,QtCore
import numpy as np
import pyqtgraph as pg
import sys
from math import log10, floor
from verticalScaleBar import verticalScaleBar
#QtGui.QApplication.setGraphicsSystem('raster')
#mw = QtGui.QMainWindow()
#mw.resize(800,800)


class plotWindow(pg.GraphicsWindow):
    
    
	def __init__(self, parent=None,scalebar = True,useViewBox = False):
		pg.setConfigOptions(antialias=True)
		pg.setConfigOption('background', 'w')
		pg.setConfigOption('foreground', 'k')
		pg.GraphicsWindow.__init__(self)
		self.useViewBox = useViewBox
		#win = pg.GraphicsWindow(title="Basic plotting examples")
		# self.view = pg.PlotWidget(self)

		# self.view = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
		#self.view.pg.setConfigOptions(antialias=True)  ## prettier plots at no cost to the main process! 
		# self.view.setWindowTitle('pyqtgraph example: RemoteSpeedTest')
		self.resize(800,350)
		#win.setWindowTitle('pyqtgraph example: Plotting')

		# Enable antialiasing for prettier plots
		self.scalebar = scalebar

		# self.setCentralWidget(self.view)    
		# self.curve = self.view.plot()
		self.curve = []

		self.p8 = self.addPlot(title="Region Selection")
		pl8 = self.p8.plot()#data2, pen=(255,255,255,200))
		if self.useViewBox:
			self.nextRow()

			self.p9 = self.addPlot(title="Zoom on selected region")
			pl9 = self.p9.plot()
		
		vb = self.p8.getViewBox()
		xsize = vb.viewRange()[0][1] - vb.viewRange()[0][0]
		ysize = vb.viewRange()[1][1] - vb.viewRange()[1][0]
		self.scale = pg.ScaleBar(size=round_to_1(xsize/10.0),suffix='s')                                                                                                                                                                   
		self.scale.setParentItem(vb)
		self.scale.anchor((0, 1), (1, 1), offset=(-20, -10))
		self.vscale = verticalScaleBar(size=round_to_1(ysize/5.0),suffix='s')                                                                                                                                                                   
		self.vscale.setParentItem(vb)
		self.vscale.anchor((0, 1), (1, 1), offset=(-20, -10))

		self.xlabel = ''
		self.ylabel = ''
		self.marker = pg.InfiniteLine(pos=0,pen = (0,0,0))
		self.markerpos = 0
		self.p8.addItem(self.marker)
		self.p8.sigXRangeChanged.connect(self.updateSB)
		self.updateSB()
		self.show()

	def updateSB(self):
		try:
			self.scale.scene().removeItem(self.scale)
			self.vscale.scene().removeItem(self.vscale)
		except:
			pass
		if self.scalebar:
			vb = self.p8.getViewBox()
			xsize = vb.viewRange()[0][1] - vb.viewRange()[0][0]
			ysize = vb.viewRange()[1][1] - vb.viewRange()[1][0]

			self.scale = pg.ScaleBar(size=round_to_1(xsize/10.0),suffix=self.xlabel)                                                                                                                                                                   
			self.scale.setParentItem(vb)
			self.scale.anchor((0, 1), (1, 1), offset=(-20, -10))
			self.vscale = verticalScaleBar(size=round_to_1(ysize/5.0),suffix=self.ylabel)                                                                                                                                                                   
			self.vscale.setParentItem(vb)
			self.vscale.anchor((0, 1), (1, 1), offset=(-20, -5))
			self.scale.text.setText(pg.functions.siFormat(round_to_1(xsize/10.0),suffix=self.xlabel),color=(0,0,0))
			#vb.autoRange()

	def updatePlot(self):
	    self.p9.setXRange(*self.lr.getRegion(), padding=0)

	def updateRegion(self):
	    self.lr.setRegion(self.p9.getViewBox().viewRange()[0])

	def plot(self,x,y,xlabel='',ylabel='',colors = None,title = None,scalebars = False):
		self.p8.clear()
		if self.useViewBox:
			self.p9.clear()
			self.lr = pg.LinearRegionItem([0,10])
			self.lr.setZValue(-10)
			self.p8.addItem(self.lr)
			self.lr.sigRegionChanged.connect(self.updatePlot)
			self.p9.sigXRangeChanged.connect(self.updateRegion)
			self.updatePlot()
		
		self.p8.setTitle(title)
		self.marker = pg.InfiniteLine(pos=self.markerpos,pen = (0,0,0))
		self.p8.addItem(self.marker)
		diff = 0	
		for i in xrange(y.shape[1]):
			if colors is not None:
				color = colors[i]
			else:
				color = [255,255,255,255]

			if scalebars:
				if i>0:
					diff = diff+y[:,i-1].max()
				else:
					diff = 0
			self.p8.plot(x,y[:,i]+diff,pen=color)#, pen=(255,255,255,200))
			if self.useViewBox:
				self.p9.plot(x,y[:,i],pen=color)#, pen=(255,255,255,200))
		self.p8.setLabel('left',ylabel)
		self.p8.setLabel('bottom',xlabel)
		if self.useViewBox:
			self.p9.setLabel('left',ylabel)
			self.p9.setLabel('bottom',xlabel)
		self.xlabel = xlabel
		self.ylabel = ylabel
		if scalebars:
			self.scalebar = True
			self.p8.hideAxis('bottom')
			self.p8.hideAxis('left')
			self.updateSB()


		else:
			try:
				self.scale.scene().removeItem(self.scale)
				self.vscale.scene().removeItem(self.vscale)

				self.scalebar = False
			except:
				pass
		vb = self.p8.getViewBox()
		vb.autoRange()
	    #self.lplt.plot(np.arange(size(y)),y, clear=True, _callSync='off')  ## We do not expect a return value.

def round_to_1(x):
	return round(x, -int(floor(log10(x))))

if __name__ =='__main__':
	app = QtGui.QApplication(sys.argv)
	robopy = plotWindow()
	robopy.show()

	#ipshell = InteractiveShellEmbed()
	#ipshell()
	
	ans = app.exec_()

	sys.exit(ans)
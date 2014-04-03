import sys, os, matplotlib
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import cm
#from pubTools import oneColumnFigure as Figure
class MPlot(QDialog):
	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.setWindowTitle("Plot")
		
		self.resize(600,480)
		
		self.axes = None
		self.mplToolbar = None
		
		self.initPlotParams()
		
		self.createMainFrame()
		
	def initPlotParams(self):
		
		self.micro=u'\u03bc'
		self.delta=u'\u0394'
		self.labelSize=8
		self.fontFamily='Arial'
		self.figSize=(3.5,2.5)
		
	def createMainFrame(self):
		self.mainFrame = QWidget(self)
		
		hlay = QHBoxLayout(self)
		hlay.addWidget(self.mainFrame)
		
		self.dpi = 200
		#self.fig = Figure(self.figSize, dpi = self.dpi,addAxes=False)
		self.fig = Figure()
		self.canvas = FigureCanvas(self.fig)
		
		hlay = QHBoxLayout(self.mainFrame)
		hlay.addWidget(self.canvas)
		#self.canvas.setParent(self.mainFrame)
		
		self.axes = self.fig.add_subplot(111)
		self.axes.xaxis.set_ticks_position('bottom')
		self.axes.yaxis.set_ticks_position('left')
		
		self.mplToolbar = NavigationToolbar(self.canvas, self.mainFrame)
		
	def plot(self, x,data):
		self.axes.plot(x,data)
		
	def imshow(self,img):
		self.axes.imshow(img,cmap = cm.gray)
       

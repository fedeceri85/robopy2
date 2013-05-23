from PyQt4 import QtCore, QtGui, QtOpenGL
from PyQt4.QtGui import *
from PyQt4.QtOpenGL import *
from PyQt4.QtCore import *
from Roi import Roi
import sys
import matplotlib
'''
Main Image display widget ontop of QGLWidget (to use opengl hardware)
computer running must be opengl es 2.0 capable
'''
class ImageDisplayWidget(QGLWidget):
	def __init__(self, parent=None):
		#QGLWidget.__init__(self, parent=parent)
		super(ImageDisplayWidget, self).__init__(QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers), parent=parent)
		
		self.gradient = QRadialGradient()
		self.createGradient()
		self.setMouseTracking(True)
		
		self.SequenceDisplay = parent
		self.ImagePositionX = 0
		self.ImagePositionY = 0
		
		self.ImageZoom = 1.0
		self.ImageZoomSteps = 1
		
		self.IsMouseDown = 0
		self.RightMouseButtonClicked = 0
		self.DrawRoiStatus = "idle"
		self.rois = list()
		
	def createGradient(self):
		self.gradient.setCoordinateMode(QGradient.ObjectBoundingMode);
		self.gradient.setCenter(0.45, 0.50);
		self.gradient.setFocalPoint(0.40, 0.45);
		self.gradient.setColorAt(0.0, QColor(105, 146, 182));
		self.gradient.setColorAt(0.4, QColor(81, 113, 150));
		self.gradient.setColorAt(0.8, QColor(16, 56, 121));
	
	def paintEvent(self, event):
		painter = QPainter()
		painter.begin(self)
		
		painter.setPen(Qt.NoPen)
		painter.setBrush(self.gradient)
		painter.drawRect(self.rect())
		
		#draw image if it exists
		painter.scale(self.ImageZoom, self.ImageZoom)
		self.drawSequenceImage(painter)
		
		if len(self.rois) > 0:
			for i in self.rois:
				self.drawRoi(painter, i)
		
		painter.end()
		
	def drawSequenceImage(self, painter):
		p = self.SequenceDisplay
		
		if p.FrameImage != None:
			painter.drawImage(self.ImagePositionX, self.ImagePositionY, p.FrameImage)
			
	def drawRoi(self, painter, r):
		pen = QPen(r.color)
		pen2 = QPen(r.color,4)
		painter.setPen(pen)
		
		painter.drawPolyline(r)
		painter.setPen(pen2)
		painter.drawPoints(r)

		if r.mapSize > 0:
			painter.setPen(pen)
			painter.drawLine(r.last(), r.first())
			
			x,y = r.computeMassCenter()
			painter.drawText(QPoint(x,y), QString("%1").arg(r.ordinal + 1))
			
				
			
	def wheelEvent(self, event):
		if event.delta() > 0:
			self.ImageZoomSteps = self.ImageZoomSteps + 1
		else:
			self.ImageZoomSteps = self.ImageZoomSteps - 1
			
		self.ImageZoom = pow(1.25, self.ImageZoomSteps)
		self.repaint()
		
	def mousePressEvent(self, event):
		self.IsMouseDown = 1
		if event.button() == Qt.RightButton:
			self.RightMouseButtonClicked = 1
		else:
			self.RightMouseButtonClicked = 0
		
	def mouseReleaseEvent(self, event):
		
		if self.IsMouseDown == 1 and self.RightMouseButtonClicked == 1:
			
			a,b = self.screenToImage(event.x(), event.y())
			
			if self.DrawRoiStatus == "idle":
				self.DrawRoiStatus = "drawing"
				self.rois.append(Roi())

				
			self.rois[-1].addPoint(a,b)
			self.repaint()
		
		self.IsMouseDown = 0
		
	def screenToImage(self,x,y):
		a = x / self.ImageZoom
		b = y / self.ImageZoom
		
		return a,b
		
	def mouseMoveEvent(self, event):
		a,b = self.screenToImage(event.x(), event.y())
		self.emit(QtCore.SIGNAL("mousePositionChanged(int, int)"), a, b)
		#event.accept()
		
	def mouseDoubleClickEvent(self, event):
		if self.DrawRoiStatus == "drawing":
			self.DrawRoiStatus = "idle"
			
			#a,b = self.screenToImage(event.x(), event.y())
			#self.rois[-1].addPoint(a,b)
			
			self.rois[-1].computePointMap()
			self.rois[-1].ordinal = len(self.rois) - 1
			
			colorCycle = matplotlib.rcParams["axes.color_cycle"]
			
			roiCol = matplotlib.colors.colorConverter.to_rgb(colorCycle[self.rois[-1].ordinal % len(colorCycle)])
			
			c = QColor()
			c.setRgbF(roiCol[0], roiCol[1], roiCol[2])
			self.rois[-1].color = c
			
			self.emit(QtCore.SIGNAL("roiRecomputeNeeded(bool)"), True)
			
			self.SequenceDisplay.tiffSequence.rois.append(self.rois[-1])
			self.repaint()

			

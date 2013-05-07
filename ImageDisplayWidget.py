from PyQt4 import QtCore, QtGui, QtOpenGL
from PyQt4.QtGui import *
from PyQt4.QtOpenGL import *
from PyQt4.QtCore import *
import sys
#Main Image display widget ontop of QGLWidget (to use opengl hardware)
#computer running must be opengl es2.0 capable

class ImageDisplayWidget(QGLWidget):
	def __init__(self, parent=None):
		#QGLWidget.__init__(self, parent=parent)
		super(ImageDisplayWidget, self).__init__(QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers), parent=parent)
		
		self.gradient = QRadialGradient()
		self.createGradient()
		
		self.SequenceDisplay = parent
		self.ImagePositionX = 0
		self.ImagePositionY = 0
		self.ImageZoom = 1.0
		
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
		self.drawSequenceImage(painter)
		
		painter.end()
		
	def drawSequenceImage(self, painter):
		p = self.SequenceDisplay
		
		if p.FrameImage != None:
			painter.drawImage(self.ImagePositionX, self.ImagePositionY, p.FrameImage)

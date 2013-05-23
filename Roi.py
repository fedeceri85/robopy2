import PyQt4
from PyQt4.QtCore import *
from PyQt4.QtGui import QPolygon, QColor
import numpy as np
#import pdb
'''
Module that holds a polygonal roi
'''

class Roi(QPolygon):
	def __init__(self):
		super(Roi, self).__init__()
		
		self.color = QColor(Qt.green)
		self.ordinal = -1
		
		self.clearPointMap()
	
	def clearPointMap(self):
		self.pointMap = list()
		self.mapSize = 0
		
	
	def computePointMap(self):
		#pdb.set_trace()
		rf = self.boundingRect()
		r = QRect(rf.left(), rf.top(), rf.width(), rf.height())
		
		self.clearPointMap()
		for i in xrange(r.top(), r.bottom()+1, 1):
			lPointsX = list()
			for j in xrange(r.left(), r.right() + 1, 1):
				pt = QPoint(j,i)
				if self.containsPoint(pt, Qt.OddEvenFill):
					lPointsX.append(j)
					self.mapSize = self.mapSize + 1
					
			if len(lPointsX) > 0:
				self.pointMap.append([np.array(lPointsX), i])
				
	def addPoint(self, x, y):
		self.append(QPoint(x,y))
		
	def computeAverage(self, im):
		avg = 0.0
		for i in self.pointMap:
			avg = avg + im[i[1], i[0]].sum()
			
		return avg/self.mapSize
		
	def computeMassCenter(r):
		x = 0.0
		y = 0.0
		
		if r.size() < 1:
			return x,y
		
		for i in xrange(0, r.size()):
			p = r.point(i)
			x = x + p.x()
			y = y + p.y()
			
		x = x / r.size()
		y = y / r.size()
		
		return x,y
		

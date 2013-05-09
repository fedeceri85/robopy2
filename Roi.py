import PyQt4
from PyQt4.QtCore import *
from PyQt4.QtGui import QPolygon
import numpy as np
'''
Module that holds a polygonal roi
'''

class Roi(QPolygon):
	def __init__(self):
		super(Roi, self).__init__()
		
		self.clearPointMap()
	
	def clearPointMap(self):
		self.pointMap = list()
		self.mapSize = 0
		
	
	def computePointMap(self):
		rf = self.boundingRect()
		r = QRect(rf.left(), rf.top(), rf.width(), rf.height())
		
		self.clearPointMap()
		for i in xrange(r.top(), r.bottom()+1):
			l = list()
			for j in xrange(r.left(), r.right() + 1):
				pt = QPoint(i,j)
				if self.contains(pt):
					l.append(np.array([j,i]))
					
			if not l == []:
				self.pointMap.append(np.array(l))
				
	def addPoint(self, x, y):
		self.append(QPoint(x,y))

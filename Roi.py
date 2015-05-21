import PyQt4
from PyQt4.QtCore import *
from PyQt4.QtGui import QPolygon, QColor
import numpy as np
from math import cos,sin
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

	def removePoint(self,n):
		self.remove(n)

	def downsample(self,n):
		p = range(self.size())
		toKeep = p[::n]
		toRemove = list(set(p).difference(set(toKeep)))
		toRemove.sort(reverse=True)
		for i in toRemove:
			self.removePoint(i)
		
	def computeAverage(self, im):
		avg = 0.0
		for i in self.pointMap:
			avg = avg + im[i[1], i[0]].sum()
		return avg/(self.mapSize*1.0)
			
	def move(self,x,y):

		self.translate(x,y)
		# for i in self:
		# 	#print i.x()+x
		# 	#print i.y() + y
		# 	i.setX(i.x() + y)
		# 	i.setY(i.y() + x)

		#self.computePointMap()\
	def rotate(self,angle):
		x,y = self.computeMassCenter()
		mat = np.array([[cos(angle),-sin(angle)],[sin(angle),cos(angle)]])
		for i,p in enumerate(self):
			v = np.array([p.x() - x, p.y() - y]).astype(np.float)
			v1= np.dot(mat,v) + np.array([x,y])
			self.setPoint(i,QPoint(int(round(v1[0])),int(round(v1[1]))))

	def scale(self,factor=1):
		for i,p in enumerate(self):
			self.setPoint(i,QPoint(int(round(p.x()*factor)),int(round(p.y()*factor))))

	def isPointInRoi(self,point):
		pt = QPoint(point[0],point[1])
		return self.containsPoint(pt,Qt.OddEvenFill)

	def computeMassCenter(self):
		x = 0.0
		y = 0.0
		
		if self.size() < 1:
			return x,y
		
		for i in xrange(0, self.size()):
			p = self.point(i)
			x = x + p.x()
			y = y + p.y()
			
		x = x / self.size()
		y = y / self.size()
		
		return x,y
		


class RoisList(list):
	def __init__(self):
		super(RoisList, self).__init__()
		
		#self.color = QColor(Qt.green)
		#self.ordinal = -1
		self.roiNumbers = []
	def append(self,roi,number=None):
		self.append(roi)
		if number == None:
			number = len(self)

		self.roiNumbers.append(number)
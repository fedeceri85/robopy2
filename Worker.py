import PyQt4
from PyQt4.QtCore import QThread
import sys


class Worker(QThread):
	def __init__(self, parent = None, cb=None):
		QThread.__init__(self, parent)
		
		self.cb = cb
		
	def run(self):
		if self.cb != None:
			self.cb()
		


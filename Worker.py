import PyQt4
from PyQt4.QtCore import QThread


class Worker(QThread):
	def __init__(self, parent = None, cb=None, data=None, withSignals=False):
		QThread.__init__(self, parent)
		
		self.cb = cb
		self.data = data
		self.withSignals = withSignals
		
	def run(self):
		if self.cb != None and self.withSignals==True:
			if self.data != None:
				self.cb(self.data)
			else:
				self.cb()
		else:
			exec()
			
			
	def startJob(self):
		
		if self.cb != None:
			if self.data != None:
				self.cb(self.data)
			else:
				self.cb()
			
			self.emit(PyQt4.QtGui.SIGNAL("jobDone()"))


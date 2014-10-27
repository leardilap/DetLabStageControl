import sys
from PyQt4 import QtGui, QtCore, uic
import PyTango

class Ymove(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
 
		self.ui = uic.loadUi('Ymove.ui')
		self.ui.show()
		
		self.ym = PyTango.DeviceProxy("anka/motor_detlab/ysample")
		
		self.connect(self.ui.Yplus, QtCore.SIGNAL("clicked()"), self.YplusButton)
		self.connect(self.ui.Yminus, QtCore.SIGNAL("clicked()"), self.YminusButton)
		self.connect(self.ui.Yplus, QtCore.SIGNAL("pressed()"), self.jogPosStart)
		self.connect(self.ui.Yplus, QtCore.SIGNAL("released()"), self.jogStop)
		self.timer = QtCore.QTimer()
		self.timer.start(100)
		self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.updateState)
		
	def YplusButton(self):
	      pass
	      #x = self.ym.state()
	      #self.ui.YmoveLabel.setText(str(x))
	
	def YminusButton(self):
	      pass
	      #x = self.ym.state()
	      #self.ui.YmoveLabel.setText(str(x))
	      
	def jogPosStart(self):
		self.ym.forward()
	    
	def jogStop(self):
	    self.ym.stop()
	    
	def updateState(self):
	    x = self.ym.state()
	    self.ui.YmoveLabel.setText(str(x))
	
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	win = Ymove()
	sys.exit(app.exec_())

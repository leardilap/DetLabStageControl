import sys
from PyQt4 import QtGui, QtCore, uic
import PyTango

class YSampleMove(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
 
		self.ui = uic.loadUi('GUI_DetLabStage.ui')
		self.ui.show()
		
		self.ym = PyTango.DeviceProxy("anka/motor_detlab/ysample")
		
		self.connect(self.ui.YSamplePlus, QtCore.SIGNAL("clicked()"), self.YSamplePlusButton)
		self.connect(self.ui.YSampleMinus, QtCore.SIGNAL("clicked()"), self.YSampleMinusButton)
		self.connect(self.ui.YSamplePlus, QtCore.SIGNAL("pressed()"), self.jogPosStart)
		self.connect(self.ui.YSamplePlus, QtCore.SIGNAL("released()"), self.jogStop)
		self.timer = QtCore.QTimer()
		self.timer.start(100)
		self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.updateState)
		
	def YSamplePlusButton(self):
	      pass
	      #x = self.ym.state()
	      #self.ui.YmoveLabel.setText(str(x))
	
	def YSampleMinusButton(self):
	      pass
	      #x = self.ym.state()
	      #self.ui.YmoveLabel.setText(str(x))
	      
	def jogPosStart(self):
		self.ym.forward()
	    
	def jogStop(self):
	    self.ym.stop()
	    
	def updateState(self):
	    x = self.ym.state()
	    self.ui.YSampleMoveLabel.setText(str(x))
	
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	win = YSampleMove()
	sys.exit(app.exec_())

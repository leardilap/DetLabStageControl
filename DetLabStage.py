import sys
from PyQt4 import QtGui, QtCore, uic
import PyTango

class DetLabStage(QtGui.QMainWindow):
	def __init__(self, Device, uiFile):
		QtGui.QMainWindow.__init__(self)
 
		self.ui = uic.loadUi(uiFile)
		self.ui.show()
		
		#####################################################
		# Y SAMPLE
		
		#Declaring Device
		self.axis = PyTango.DeviceProxy(Device)
				
		#Jogging Plus
		self.connect(self.ui.YSampleJogPlus, QtCore.SIGNAL("pressed()"), self.JogPlus)
		self.connect(self.ui.YSampleJogPlus, QtCore.SIGNAL("released()"), self.Stop)
		
		#Jogging Minus
		self.connect(self.ui.YSampleJogMinus, QtCore.SIGNAL("pressed()"), self.JogMinus)
		self.connect(self.ui.YSampleJogMinus, QtCore.SIGNAL("released()"), self.Stop)
		
		#Home
		self.connect(self.ui.YSampleHome, QtCore.SIGNAL("clicked()"), self.Home)
		
		#Move
		self.connect(self.ui.YSampleMove, QtCore.SIGNAL("clicked()"), self.Move)
		
		#Scroll
		self.connect(self.ui.YSampleScroll, QtCore.SIGNAL("valueChanged(int)"), self.UpdateDesiredPosScroll)
		
		#Updating State - Position
		self.timer = QtCore.QTimer()
		self.timer.start(100)
		self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.UpdateState)
		self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.CurrentPosition)
		
		self.UpdateDesiredPos()
		
	      
	def JogPlus(self):
		self.axis.forward()
		
	def JogMinus(self):
		self.axis.backward()
		
	def Home(self):
		self.axis.initializeReferencePosition()	
	    
	def Stop(self):
		self.axis.stop()
		self.UpdateDesiredPos()
		
	def Move(self):
		pos = self.ui.YSampleDesirePos.value()
		self.axis.position = pos			
		
	def UpdateDesiredPosScroll(self):
		pos = self.ui.YSampleScroll.value()
		self.ui.YSampleDesirePos.setValue(-1*pos)	#-1 is for positive values the slider goes left
	
	def UpdateDesiredPos(self):
		pos = self.axis.position
		self.ui.YSampleDesirePos.setValue(pos)
		self.ui.YSampleScroll.setValue(-1*pos)		#-1 is for positive values the slider goes left
	     
	def CurrentPosition(self):
		pos = self.axis.position
		self.ui.YSampleCurrentPos.display(pos)
	    
	def UpdateState(self):
		state = self.axis.state()
		self.ui.YSampleStatusLabel.setText(str(state))
	
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	uiFile = "YSample.ui" #"GUI_DetLabStage.ui"
	Device = "anka/motor_detlab/ysample"
	win = DetLabStage(Device, uiFile)
	sys.exit(app.exec_())

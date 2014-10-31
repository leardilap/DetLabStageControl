import sys
from PyQt4 import QtGui, QtCore, uic
import PyTango

class Axis(QtGui.QMainWindow):
	def __init__(self, Device, uiFile, Invert):
		QtGui.QMainWindow.__init__(self)
 
		self.ui = uic.loadUi(uiFile)
		self.ui.show()
		
		#####################################################
		# Y SAMPLE
		
		#Declaring Device
		self.axis = PyTango.DeviceProxy(Device)
				
		#Jogging Plus
		self.connect(self.ui.JogPlus, QtCore.SIGNAL("pressed()"), self.JogPlus)
		self.connect(self.ui.JogPlus, QtCore.SIGNAL("released()"), self.Stop)
		
		#Jogging Minus
		self.connect(self.ui.JogMinus, QtCore.SIGNAL("pressed()"), self.JogMinus)
		self.connect(self.ui.JogMinus, QtCore.SIGNAL("released()"), self.Stop)
		
		#Home
		self.connect(self.ui.Home, QtCore.SIGNAL("clicked()"), self.Home)
		
		#Move
		self.connect(self.ui.Move, QtCore.SIGNAL("clicked()"), self.Move)
		
		#Scroll
		self.connect(self.ui.Scroll, QtCore.SIGNAL("valueChanged(int)"), self.UpdateDesiredPosScroll)
		
		#Updating State - Position
		#self.timer = QtCore.QTimer()
		#self.timer.start(100)
		#self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.UpdateState)
		#self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.CurrentPosition)
		
		#self.UpdateDesiredPos()
		
		self.ui.Scroll.setInvertedAppearance(Invert)
		
	      
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
		pos = self.ui.DesirePos.value()
		self.axis.position = pos			
		
	def UpdateDesiredPosScroll(self):
		pos = self.ui.Scroll.value()
		self.ui.DesirePos.setValue(pos)
	
	def UpdateDesiredPos(self):
		pos = self.axis.position
		self.ui.DesirePos.setValue(pos)
		self.ui.DesirePos.setValue(pos)	
	     
	def CurrentPosition(self):
		pos = self.axis.position
		self.ui.CurrentPos.display(pos)
	    
	def UpdateState(self):
		state = self.axis.state()
		self.ui.StatusLabel.setText(str(state))
	
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	uiFile = "YWidget.ui" #"GUI_DetLabStage.ui"
	Device = "anka/motor_detlab/ysample"
	Invert = True
	win = Axis(Device, uiFile, Invert)
	sys.exit(app.exec_())

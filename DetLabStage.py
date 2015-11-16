#! /usr/bin/env python

# Luis Ardila 	leardilap@unal.edu.co 	22/03/15
import sys
from PyQt4 import QtGui, QtCore, uic

tangoEnable = True
if tangoEnable:
	import PyTango

class Axis(QtGui.QWidget):
	def __init__(self, parent, Title, Device, uiFile):
		super(Axis, self).__init__(parent)
 
		self.ui = uic.loadUi(uiFile)		
		
		#Declaring Device
		if tangoEnable:
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
		self.connect(self.ui.MoveAB, QtCore.SIGNAL("clicked()"), self.MoveAB)
		self.connect(self.ui.MoveRE, QtCore.SIGNAL("clicked()"), self.MoveRE)
		
		##Stop
		self.connect(self.ui.Stop, QtCore.SIGNAL("clicked()"), self.Stop)
		
		##Limits
		self.connect(self.ui.Limits, QtCore.SIGNAL("clicked()"), self.Limits)
		
		#Scroll
		self.connect(self.ui.Scroll, QtCore.SIGNAL("valueChanged(int)"), self.UpdateDesiredPosScroll)
		
		#Updating State - Position
		self.timer = QtCore.QTimer()
		self.timer.start(100)
		self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.UpdateState)
		self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.CurrentPosition)
	
		#####################
		# Initializing Widget
		self.UpdateDesiredPos()
		self.ui.setWindowTitle(Title)
		
		# Var
		self.currentPos = 0
		self.Title = Title
		self.lenght = self.ui.DesirePos.maximum()
			   
	def JogPlus(self):
		if tangoEnable:
			self.axis.forward()
		else:
			self.ui.StatusLabel.setText("JogPlus")
		
	def JogMinus(self):
		if tangoEnable:
			self.axis.backward()
		else:
			self.ui.StatusLabel.setText("JogMinus")
		
	def Home(self):
		ret = QtGui.QMessageBox.warning(self, "Homming",
				"Please Check the setup!\n\nAre you sure you really want\nto Home the motor?",
				QtGui.QMessageBox.Yes, QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Escape )
		if ret == QtGui.QMessageBox.Yes:
			if tangoEnable:
				self.axis.initializeReferencePosition()	
			else:
				self.ui.StatusLabel.setText("Home")
				
	def Stop(self):
		if tangoEnable:
			self.axis.stop()
		else:
			self.ui.StatusLabel.setText("")
			
		self.UpdateDesiredPos()
		
	def Limits(self):
		self.Limits = Limits(self)
		
	def MoveAB(self):
		pos = self.ui.DesirePos.value()
		if tangoEnable:
			self.axis.position = pos	
		else:
			self.ui.StatusLabel.setText(str(pos))	
			self.currentPos = self.ui.DesirePos.value()
			self.ui.CurrentPos.display(self.currentPos)
			
		self.ui.Scroll.setValue(pos)
		
	def MoveRE(self):
		movement = self.ui.RelativePos.value()
		UpperLimit = self.ui.DesirePos.maximum()
		LowerLimit = self.ui.DesirePos.minimum()
		
		if self.currentPos + movement > UpperLimit:
			movement = UpperLimit - self.currentPos
		elif self.currentPos + movement < LowerLimit:
			movement = LowerLimit - self.currentPos
			
		if tangoEnable:
			self.axis.MoveMotorRelative(movement)
		else:
			self.ui.StatusLabel.setText(str(movement))
			self.currentPos = self.currentPos + movement
			self.ui.CurrentPos.display(self.currentPos)
			
		self.UpdateDesiredPos()
	
	def UpdateDesiredPosScroll(self):
		pos = self.ui.Scroll.value()
		self.ui.DesirePos.setValue(pos)
	
	def UpdateDesiredPos(self):
		if tangoEnable:
			pos = self.axis.position
			self.ui.DesirePos.setValue(pos)
			self.ui.Scroll.setValue(pos)
	     
	def CurrentPosition(self):
		if tangoEnable:
			self.currentPos = self.axis.position
			self.ui.CurrentPos.display(self.currentPos)
	    
	def UpdateState(self):
		if tangoEnable:
			state = self.axis.state()
			self.ui.StatusLabel.setText(str(state))
	
	def run(self):
		self.ui.show()

class Limits(QtGui.QDialog):
	def __init__(self, parent):
		QtGui.QDialog.__init__(self, parent)
				
		# Declaring GUI 
		self.ui = uic.loadUi('Limits.ui')
		self.ui.show()
		self.connect(self.ui.ButtonBox, QtCore.SIGNAL("accepted()"), lambda: self.Accepted(parent))
		self.connect(self.ui.UpperLimit, QtCore.SIGNAL("valueChanged(double)"), lambda: self.UpdateUpperLimit(parent))
		self.connect(self.ui.LowerLimit, QtCore.SIGNAL("valueChanged(double)"), lambda: self.UpdateLowerLimit(parent))
		self.ui.setWindowTitle(str(parent.Title + " Limits"))
		self.ui.UpperLimit.setMaximum(parent.lenght*2)
		self.ui.LowerLimit.setMaximum(parent.lenght*2)
		self.ui.UpperLimit.setMinimum(-parent.lenght*2)
		self.ui.LowerLimit.setMinimum(-parent.lenght*2)
		self.ui.UpperLimit.setValue(parent.ui.DesirePos.maximum())
		self.ui.LowerLimit.setValue(parent.ui.DesirePos.minimum())
	
	def UpdateUpperLimit(self, parent):
		self.UpperLimit = self.ui.UpperLimit.value()
		self.LowerLimit = self.ui.LowerLimit.value()
		if self.UpperLimit - self.LowerLimit > parent.lenght:
			self.ui.LowerLimit.setValue(self.UpperLimit - parent.lenght)
		elif self.UpperLimit <= self.LowerLimit:
			self.ui.LowerLimit.setValue(self.UpperLimit - 1)
    
	def UpdateLowerLimit(self, parent):
		self.UpperLimit = self.ui.UpperLimit.value()
		self.LowerLimit = self.ui.LowerLimit.value()
		if self.LowerLimit + parent.lenght < self.UpperLimit:
			self.ui.UpperLimit.setValue(self.LowerLimit + parent.lenght)
		elif self.LowerLimit >= self.UpperLimit:
			self.ui.UpperLimit.setValue(self.LowerLimit + 1)
			
	def Accepted(self, parent):
		parent.ui.DesirePos.setMaximum(self.ui.UpperLimit.value())
		parent.ui.DesirePos.setMinimum(self.ui.LowerLimit.value())
		parent.ui.Scroll.setMaximum(self.ui.UpperLimit.value())
		parent.ui.Scroll.setMinimum(self.ui.LowerLimit.value())
		
class MainWidget(QtGui.QWidget):
	def __init__(self, parent=None):
		super(MainWidget, self).__init__(parent)

		self.stack = QtGui.QStackedWidget()
		layout = QtGui.QVBoxLayout(self)
		layout.addWidget(self.stack)

		#############################################################
		# SAMPLE
		# X Sample
		XS_Title = "X Sample"
		XS_Device = "anka/motor_detlab/xsample"
		XS_uiFile = "XWidget.ui"
		self.XSample = Axis(self, XS_Title, XS_Device, XS_uiFile)

		# Y Sample
		YS_Title = "Y Sample"
		YS_Device = "anka/motor_detlab/ysample"
		YS_uiFile = "YWidget.ui"
		self.YSample = Axis(self, YS_Title, YS_Device, YS_uiFile)

		##############################################################
		# DETECTOR
		# X Detector
		XD_Title = "X Detector"
		XD_Device = "anka/motor_detlab/xdet"
		XD_uiFile = "XWidget.ui"
		self.XDetector = Axis(self, XD_Title, XD_Device, XD_uiFile)

		# Y Detector
		YD_Title = "Y Detector"
		YD_Device = "anka/motor_detlab/ydet"
		YD_uiFile = "YWidget.ui"
		self.YDetector = Axis(self, YD_Title, YD_Device, YD_uiFile)

		# Z Detector
		ZD_Title = "Z Detector"
		ZD_Device = "anka/motor_detlab/zdet"
		ZD_uiFile = "ZWidget.ui"
		self.ZDetector = Axis(self, ZD_Title, ZD_Device, ZD_uiFile)
		
		################################################################
		# MAIN WINDOW
		self.stack.addWidget(self.YSample)
		self.stack.addWidget(self.XSample)
		self.stack.addWidget(self.YDetector)
		self.stack.addWidget(self.XDetector)
		self.stack.addWidget(self.ZDetector)
		
		self.XSample.run()
		self.YSample.run()
		self.XDetector.run()
		self.YDetector.run()
		self.ZDetector.run()


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	
	win = MainWidget()

	sys.exit(app.exec_())

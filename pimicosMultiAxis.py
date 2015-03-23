#! /usr/bin/env python

# Luis Ardila 	leardilap@unal.edu.co 	22/03/15

import sys
from PyQt4 import QtGui, QtCore, uic

class pimicosMultiAxis(QtGui.QWidget):
	def __init__(self):
		QtGui.QWidget.__init__(self)

		self.tangoEnable = False
		
		if self.tangoEnable:
			import PyTango
		
		# Declaring GUI 
		self.ui = uic.loadUi('pimicosMultiAxis.ui')
		self.ui.show()
		
		self.pimicosY = pimicosY(self)
		self.pimicosZ = pimicosZ(self)
		self.pimicosRoll = pimicosRoll(self)
		self.pimicosPitch = pimicosPitch(self)
		self.pimicosYaw = pimicosYaw(self)
		
		self.connect(self.ui.Home, QtCore.SIGNAL("clicked()"), self.Home)
	
	def Home(self):
		if self.tangoEnable:
			self.axis = PyTango.DeviceProxy("anka/pimicos/G0_Y")
			self.axis.InitializeReferencePosition()
		else:
			print "Home"
			
class pimicosY(QtGui.QWidget):
	def __init__(self, parent):
		QtGui.QWidget.__init__(self, parent)
		
		#Declaring Device
		if parent.tangoEnable:
			self.axis = PyTango.DeviceProxy("anka/pimicos/G0_Y")

		#Move
		parent.connect(parent.ui.Move_Y, QtCore.SIGNAL("clicked()"), lambda: self.Move(parent))
		
		#Scroll
		parent.connect(parent.ui.Scroll_Y, QtCore.SIGNAL("valueChanged(int)"), lambda: self.UpdateDesiredPos(parent))
		parent.connect(parent.ui.Scroll_Y, QtCore.SIGNAL("actionTriggered(int)"), lambda: self.UpdateDesiredPosEnable(parent))
		#Spiner 
		parent.connect(parent.ui.DesirePos_Y, QtCore.SIGNAL("valueChanged(double)"), lambda: self.UpdateScroll(parent))
		
		#Updating State - Position
		self.timer = QtCore.QTimer()
		self.timer.start(100)
		self.connect(self.timer, QtCore.SIGNAL("timeout()"), lambda: self.CurrentPosition(parent))
		
		self.Init(parent)
		
	def Move(self, parent):
		pos = parent.ui.DesirePos_Y.value()
		if parent.tangoEnable:
			self.axis.write_attribute('Position',pos)	
		else:
			parent.ui.CurrentPos_Y.display(pos)	
		
	def UpdateDesiredPos(self, parent):
		if self.UpdateDesiredPosFlag:
			pos = parent.ui.Scroll_Y.value()
			self.UpdateDesiredPosFlag = False
			parent.ui.DesirePos_Y.setValue(pos)
		
	def UpdateDesiredPosEnable(self, parent):
		self.UpdateDesiredPosFlag = True
	
	def UpdateScroll(self, parent):
		self.UpdateDesiredPosFlag = False
		pos = parent.ui.DesirePos_Y.value()
		parent.ui.Scroll_Y.setValue(pos)
		
	def Init(self, parent):
		self.UpdateDesiredPosFlag = False
		if parent.tangoEnable:
			pos = self.axis.read_attribute('Position')
		else:
			pos = 23
		parent.ui.DesirePos_Y.setValue(pos)
		parent.ui.Scroll_Y.setValue(pos)
	     
	def CurrentPosition(self, parent):
		if parent.tangoEnable:
			pos = self.axis.read_attribute('Position')
			parent.ui.CurrentPos_Y.display(pos)

class pimicosZ(QtGui.QWidget):
	def __init__(self, parent):
		QtGui.QWidget.__init__(self, parent)
		
		#Declaring Device
		if parent.tangoEnable:
			self.axis = PyTango.DeviceProxy("anka/pimicos/G0_Z")

		#Move
		parent.connect(parent.ui.Move_Z, QtCore.SIGNAL("clicked()"), lambda: self.Move(parent))
		
		#Scroll
		parent.connect(parent.ui.Scroll_Z, QtCore.SIGNAL("valueChanged(int)"), lambda: self.UpdateDesiredPos(parent))
		parent.connect(parent.ui.Scroll_Z, QtCore.SIGNAL("actionTriggered(int)"), lambda: self.UpdateDesiredPosEnable(parent))
		
		#Spiner 
		parent.connect(parent.ui.DesirePos_Z, QtCore.SIGNAL("valueChanged(double)"), lambda: self.UpdateScroll(parent))
		
		#Updating State - Position
		self.timer = QtCore.QTimer()
		self.timer.start(100)
		self.connect(self.timer, QtCore.SIGNAL("timeout()"), lambda: self.CurrentPosition(parent))
		
		self.Init(parent)
		
	def Move(self, parent):
		pos = parent.ui.DesirePos_Z.value()
		if parent.tangoEnable:
			self.axis.write_attribute('Position',pos)	
		else:
			parent.ui.CurrentPos_Z.display(pos)	
		
	def UpdateDesiredPos(self, parent):
		if self.UpdateDesiredPosFlag:
			pos = parent.ui.Scroll_Z.value()
			self.UpdateDesiredPosFlag = False
			parent.ui.DesirePos_Z.setValue(pos)
		
	def UpdateDesiredPosEnable(self, parent):
		self.UpdateDesiredPosFlag = True
		
	def UpdateScroll(self, parent):
		self.UpdateDesiredPosFlag = False
		pos = parent.ui.DesirePos_Z.value()
		parent.ui.Scroll_Z.setValue(pos)
		
	def Init(self, parent):
		self.UpdateDesiredPosFlag = False
		if parent.tangoEnable:
			pos = self.axis.read_attribute('Position')
		else:
			pos = 23
		parent.ui.DesirePos_Z.setValue(pos)
		parent.ui.Scroll_Z.setValue(pos)
	     
	def CurrentPosition(self, parent):
		if parent.tangoEnable:
			pos = self.axis.read_attribute('Position')
			parent.ui.CurrentPos_Z.display(pos)

class pimicosRoll(QtGui.QWidget):
	def __init__(self, parent):
		QtGui.QWidget.__init__(self, parent)
		
		#Declaring Device
		if parent.tangoEnable:
			self.axis = PyTango.DeviceProxy("anka/pimicos/G0_roll")

		#Move
		parent.connect(parent.ui.Move_Roll, QtCore.SIGNAL("clicked()"), lambda: self.Move(parent))
		
		#Scroll
		parent.connect(parent.ui.Scroll_Roll, QtCore.SIGNAL("valueChanged(int)"), lambda: self.UpdateDesiredPos(parent))
		parent.connect(parent.ui.Scroll_Roll, QtCore.SIGNAL("actionTriggered(int)"), lambda: self.UpdateDesiredPosEnable(parent,0))
		
		#Dial
		parent.connect(parent.ui.Dial_Roll, QtCore.SIGNAL("valueChanged(int)"), lambda: self.UpdateDesiredPos(parent))
		parent.connect(parent.ui.Dial_Roll, QtCore.SIGNAL("sliderPressed()"), lambda: self.UpdateDesiredPosEnable(parent,1))
		
		#Spiner 
		parent.connect(parent.ui.DesirePos_Roll, QtCore.SIGNAL("valueChanged(double)"), lambda: self.UpdateScroll(parent))
		
		#Updating State - Position
		self.timer = QtCore.QTimer()
		self.timer.start(100)
		self.connect(self.timer, QtCore.SIGNAL("timeout()"), lambda: self.CurrentPosition(parent))
		
		self.Init(parent)
		
	def Move(self, parent):
		pos = parent.ui.DesirePos_Roll.value()
		if parent.tangoEnable:
			self.axis.write_attribute('Position',pos)	
		else:
			parent.ui.CurrentPos_Roll.display(pos)	
		
	def UpdateDesiredPos(self, parent):
		if self.UpdateDesiredPosFlag:
			if self.SliderDial == 0:
				pos = parent.ui.Scroll_Roll.value()
				self.UpdateDesiredPosFlag = False
				parent.ui.Dial_Roll.setValue(pos)
			elif self.SliderDial == 1:
				pos = parent.ui.Dial_Roll.value()
				self.UpdateDesiredPosFlag = False
				parent.ui.Scroll_Roll.setValue(pos)
			parent.ui.DesirePos_Roll.setValue(pos)
	
	def UpdateDesiredPosEnable(self, parent, SliderDial):
		self.UpdateDesiredPosFlag = True
		self.SliderDial = SliderDial
		
	def UpdateScroll(self, parent):
		self.UpdateDesiredPosFlag = False
		pos = parent.ui.DesirePos_Roll.value()
		parent.ui.Scroll_Roll.setValue(pos)
		parent.ui.Dial_Roll.setValue(pos)
		
	def Init(self, parent):
		self.UpdateDesiredPosFlag = False
		if parent.tangoEnable:
			pos = self.axis.read_attribute('Position')
		else:
			pos = 2
		parent.ui.DesirePos_Roll.setValue(pos)
		parent.ui.Scroll_Roll.setValue(pos)
		parent.ui.Dial_Roll.setValue(pos)
	     
	def CurrentPosition(self, parent):
		if parent.tangoEnable:
			pos = self.axis.read_attribute('Position')
			parent.ui.CurrentPos_Roll.display(pos)
			
class pimicosPitch(QtGui.QWidget):
	def __init__(self, parent):
		QtGui.QWidget.__init__(self, parent)
		
		#Declaring Device
		if parent.tangoEnable:
			self.axis = PyTango.DeviceProxy("anka/pimicos/G0_pth")

		#Move
		parent.connect(parent.ui.Move_Pitch, QtCore.SIGNAL("clicked()"), lambda: self.Move(parent))
		
		#Scroll
		parent.connect(parent.ui.Scroll_Pitch, QtCore.SIGNAL("valueChanged(int)"), lambda: self.UpdateDesiredPos(parent))
		parent.connect(parent.ui.Scroll_Pitch, QtCore.SIGNAL("actionTriggered(int)"), lambda: self.UpdateDesiredPosEnable(parent,0))
		
		#Dial
		parent.connect(parent.ui.Dial_Pitch, QtCore.SIGNAL("valueChanged(int)"), lambda: self.UpdateDesiredPos(parent))
		parent.connect(parent.ui.Dial_Pitch, QtCore.SIGNAL("sliderPressed()"), lambda: self.UpdateDesiredPosEnable(parent,1))
		
		#Spiner 
		parent.connect(parent.ui.DesirePos_Pitch, QtCore.SIGNAL("valueChanged(double)"), lambda: self.UpdateScroll(parent))
		
		#Updating State - Position
		self.timer = QtCore.QTimer()
		self.timer.start(100)
		self.connect(self.timer, QtCore.SIGNAL("timeout()"), lambda: self.CurrentPosition(parent))
		
		self.Init(parent)
		
	def Move(self, parent):
		pos = parent.ui.DesirePos_Pitch.value()
		if parent.tangoEnable:
			self.axis.write_attribute('Position',pos)	
		else:
			parent.ui.CurrentPos_Pitch.display(pos)	
		
	def UpdateDesiredPos(self, parent):
		if self.UpdateDesiredPosFlag:
			if self.SliderDial == 0:
				pos = parent.ui.Scroll_Pitch.value()
				self.UpdateDesiredPosFlag = False
				parent.ui.Dial_Pitch.setValue(pos)
			elif self.SliderDial == 1:
				pos = parent.ui.Dial_Pitch.value()
				self.UpdateDesiredPosFlag = False
				parent.ui.Scroll_Pitch.setValue(pos)
			parent.ui.DesirePos_Pitch.setValue(pos)
	
	def UpdateDesiredPosEnable(self, parent, SliderDial):
		self.UpdateDesiredPosFlag = True
		self.SliderDial = SliderDial
		
	def UpdateScroll(self, parent):
		self.UpdateDesiredPosFlag = False
		pos = parent.ui.DesirePos_Pitch.value()
		parent.ui.Scroll_Pitch.setValue(pos)
		parent.ui.Dial_Pitch.setValue(pos)
		
	def Init(self, parent):
		self.UpdateDesiredPosFlag = False
		if parent.tangoEnable:
			pos = self.axis.read_attribute('Position')
		else:
			pos = 2
		parent.ui.DesirePos_Pitch.setValue(pos)
		parent.ui.Scroll_Pitch.setValue(pos)
		parent.ui.Dial_Pitch.setValue(pos)
	     
	def CurrentPosition(self, parent):
		if parent.tangoEnable:
			pos = self.axis.read_attribute('Position')
			parent.ui.CurrentPos_Pitch.display(pos)

class pimicosYaw(QtGui.QWidget):
	def __init__(self, parent):
		QtGui.QWidget.__init__(self, parent)
		
		#Declaring Device
		if parent.tangoEnable:
			self.axis = PyTango.DeviceProxy("anka/pimicos/G0_yaw")

		#Move
		parent.connect(parent.ui.Move_Yaw, QtCore.SIGNAL("clicked()"), lambda: self.Move(parent))
		
		#Dial
		parent.connect(parent.ui.Dial_Yaw, QtCore.SIGNAL("valueChanged(int)"), lambda: self.UpdateDesiredPos(parent))
		parent.connect(parent.ui.Dial_Yaw, QtCore.SIGNAL("sliderPressed()"), lambda: self.UpdateDesiredPosEnable(parent))
		
		#Spiner 
		parent.connect(parent.ui.DesirePos_Yaw, QtCore.SIGNAL("valueChanged(int)"), lambda: self.UpdateScroll(parent))
		
		#Updating State - Position
		self.timer = QtCore.QTimer()
		self.timer.start(100)
		self.connect(self.timer, QtCore.SIGNAL("timeout()"), lambda: self.CurrentPosition(parent))
		self.Init(parent)
		
	def Move(self, parent):
		pos = parent.ui.DesirePos_Yaw.value()
		if parent.tangoEnable:
			self.axis.write_attribute('Position',pos)	
		else:
			parent.ui.CurrentPos_Yaw.display(pos)	
		
	def UpdateDesiredPos(self, parent):
		if self.UpdateDesiredPosFlag:
			pos = parent.ui.Dial_Yaw.value()
			self.UpdateDesiredPosFlag = False
			parent.ui.DesirePos_Yaw.setValue(pos)
	
	def UpdateDesiredPosEnable(self, parent):
		self.UpdateDesiredPosFlag = True
		
	def UpdateScroll(self, parent):
		self.UpdateDesiredPosFlag = False
		pos = parent.ui.DesirePos_Yaw.value()
		parent.ui.Dial_Yaw.setValue(pos)
		
	def Init(self, parent):
		self.UpdateDesiredPosFlag = False
		if parent.tangoEnable:
			pos = self.axis.read_attribute('Position')
		else:
			pos = 2
		parent.ui.DesirePos_Yaw.setValue(pos)
		parent.ui.Dial_Yaw.setValue(pos)
	     
	def CurrentPosition(self, parent):
		if parent.tangoEnable:
			pos = self.axis.read_attribute('Position')
			parent.ui.CurrentPos_Yaw.display(pos)
			
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	win = pimicosMultiAxis()
	sys.exit(app.exec_())

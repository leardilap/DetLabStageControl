#! /usr/bin/env python

# Luis Ardila 	leardilap@unal.edu.co 	22/03/15

import sys
from PyQt4 import QtGui, QtCore, uic
import PyTango
from time import sleep

class pimicosMultiAxis(QtGui.QWidget):
	def __init__(self):
		QtGui.QWidget.__init__(self)

		self.tangoEnable = True
				
		# Declaring GUI 
		self.ui = uic.loadUi('pimicosMultiAxis.ui')
		self.ui.show()
		
		self.pimicosY = pimicosY(self)
		self.pimicosZ = pimicosZ(self)
		self.pimicosRoll = pimicosRoll(self)
		self.pimicosPitch = pimicosPitch(self)
		self.pimicosYaw = pimicosYaw(self)
		
		self.connect(self.ui.Home, QtCore.SIGNAL("clicked()"), self.Home)
		self.connect(self.ui.Stop, QtCore.SIGNAL("clicked()"), self.Stop)
		
		#Updating Status
		self.timer = QtCore.QTimer()
		self.timer.start(100)
		self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.Status)
		
		self.InitFlag = True
	       
	def Home(self):
		if self.tangoEnable:
			self.pimicosY.axis.InitializeReferencePosition()
		else:
			print "Home"
		sleep(1)
		self.InitFlag = True
		
	def Stop(self):
		if self.tangoEnable:
			
			self.pimicosY.axis.Stop()
		else:
			print "Stop"
		sleep(1)
		self.InitFlag = True	
		
	def Status(self):
		if self.tangoEnable:
			if (self.pimicosY.Status == "ok" and self.pimicosZ.Status == "ok" and
			  self.pimicosRoll.Status == "ok" and self.pimicosPitch.Status == "ok" and 
			  self.pimicosYaw.Status == "ok"):
				self.ui.Status.setStyleSheet("background-color: green")
				self.ui.Move_Y.setEnabled(True)
				self.ui.Move_Z.setEnabled(True)
				self.ui.Move_Pitch.setEnabled(True)
				self.ui.Move_Roll.setEnabled(True)
				self.ui.Move_Yaw.setEnabled(True)
				
				if self.InitFlag:
					self.pimicosY.Init(self)
					self.pimicosZ.Init(self)
					self.pimicosRoll.Init(self)
					self.pimicosPitch.Init(self)
					self.pimicosYaw.Init(self)
					self.InitFlag = False
			else:
				self.ui.Status.setStyleSheet("background-color: red")
				self.ui.Move_Y.setEnabled(False)
				self.ui.Move_Z.setEnabled(False)
				self.ui.Move_Pitch.setEnabled(False)
				self.ui.Move_Roll.setEnabled(False)
				self.ui.Move_Yaw.setEnabled(False)
		else:
			self.ui.Status.setStyleSheet("background-color: green")
			
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
		pos = round(parent.ui.DesirePos_Y.value(),4)
		if parent.tangoEnable:
			self.axis.write_attribute('Position',pos)	
		else:
			parent.ui.CurrentPos_Y.display(pos)	
		
	def UpdateDesiredPos(self, parent):
		if self.UpdateDesiredPosFlag:
			self.UpdateDesiredPosFlag = False
			pos = parent.ui.Scroll_Y.value()
			parent.ui.DesirePos_Y.setValue(-pos)
		
	def UpdateDesiredPosEnable(self, parent):
		self.UpdateDesiredPosFlag = True
	
	def UpdateScroll(self, parent):
		self.UpdateDesiredPosFlag = False
		pos = parent.ui.DesirePos_Y.value()
		parent.ui.Scroll_Y.setValue(-pos)
		
	def Init(self, parent):
		self.UpdateDesiredPosFlag = False
		if parent.tangoEnable:
			self.pos = self.axis.read_attribute('Position')
		else:
			pos = 23
		parent.ui.DesirePos_Y.setValue(self.pos.value)
		parent.ui.Scroll_Y.setValue(-self.pos.value)
	     
	def CurrentPosition(self, parent):
		if parent.tangoEnable:
			self.pos = self.axis.read_attribute('Position')
			parent.ui.CurrentPos_Y.display(self.pos.value)
			self.Status = self.axis.Status()

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
		pos = round(parent.ui.DesirePos_Z.value(),4)
		if parent.tangoEnable:
			self.axis.write_attribute('Position',pos)	
		else:
			parent.ui.CurrentPos_Z.display(pos)	
		
	def UpdateDesiredPos(self, parent):
		if self.UpdateDesiredPosFlag:
			self.UpdateDesiredPosFlag = False
			pos = parent.ui.Scroll_Z.value()
			parent.ui.DesirePos_Z.setValue(-pos)
		
	def UpdateDesiredPosEnable(self, parent):
		self.UpdateDesiredPosFlag = True
		
	def UpdateScroll(self, parent):
		self.UpdateDesiredPosFlag = False
		pos = parent.ui.DesirePos_Z.value()
		parent.ui.Scroll_Z.setValue(-pos)
		
	def Init(self, parent):
		self.UpdateDesiredPosFlag = False
		if parent.tangoEnable:
			self.pos = self.axis.read_attribute('Position')
		else:
			pos = 23
		parent.ui.DesirePos_Z.setValue(self.pos.value)
		parent.ui.Scroll_Z.setValue(-self.pos.value)
	     
	def CurrentPosition(self, parent):
		if parent.tangoEnable:
			self.pos = self.axis.read_attribute('Position')
			parent.ui.CurrentPos_Z.display(self.pos.value)
			self.Status = self.axis.Status()

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
		pos = round(parent.ui.DesirePos_Roll.value(),4)
		if parent.tangoEnable:
			self.axis.write_attribute('Position',pos)	
		else:
			parent.ui.CurrentPos_Roll.display(pos)	
		
	def UpdateDesiredPos(self, parent):
		if self.UpdateDesiredPosFlag:
			if self.SliderDial == 0:
				self.UpdateDesiredPosFlag = False
				pos = parent.ui.Scroll_Roll.value()
				parent.ui.Dial_Roll.setValue(pos)
			elif self.SliderDial == 1:
				self.UpdateDesiredPosFlag = False
				pos = parent.ui.Dial_Roll.value()
				parent.ui.Scroll_Roll.setValue(pos)
			parent.ui.DesirePos_Roll.setValue(-float(pos)/10)
	
	def UpdateDesiredPosEnable(self, parent, SliderDial):
		self.UpdateDesiredPosFlag = True
		self.SliderDial = SliderDial
		
	def UpdateScroll(self, parent):
		self.UpdateDesiredPosFlag = False
		pos = parent.ui.DesirePos_Roll.value()
		parent.ui.Scroll_Roll.setValue(-pos*10)
		parent.ui.Dial_Roll.setValue(-pos*10)
		
	def Init(self, parent):
		self.UpdateDesiredPosFlag = False
		if parent.tangoEnable:
			self.pos = self.axis.read_attribute('Position')
		else:
			pos = 2
		parent.ui.DesirePos_Roll.setValue(self.pos.value)
		parent.ui.Scroll_Roll.setValue(-self.pos.value*10)
		parent.ui.Dial_Roll.setValue(-self.pos.value*10)
	     
	def CurrentPosition(self, parent):
		if parent.tangoEnable:
			self.pos = self.axis.read_attribute('Position')
			parent.ui.CurrentPos_Roll.display(self.pos.value)
			self.Status = self.axis.Status()
			
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
		pos = round(parent.ui.DesirePos_Pitch.value(),4)
		print pos
		if parent.tangoEnable:
			self.axis.write_attribute('Position',pos)	
		else:
			parent.ui.CurrentPos_Pitch.display(pos)	
		
	def UpdateDesiredPos(self, parent):
		if self.UpdateDesiredPosFlag:
			if self.SliderDial == 0:
				self.UpdateDesiredPosFlag = False
				pos = -parent.ui.Scroll_Pitch.value()
				parent.ui.Dial_Pitch.setValue(pos)
			elif self.SliderDial == 1:
				self.UpdateDesiredPosFlag = False
				pos = parent.ui.Dial_Pitch.value()
				parent.ui.Scroll_Pitch.setValue(-pos)
			parent.ui.DesirePos_Pitch.setValue(float(pos)/10)
	
	def UpdateDesiredPosEnable(self, parent, SliderDial):
		self.UpdateDesiredPosFlag = True
		self.SliderDial = SliderDial
		
	def UpdateScroll(self, parent):
		self.UpdateDesiredPosFlag = False
		pos = parent.ui.DesirePos_Pitch.value()
		parent.ui.Scroll_Pitch.setValue(-pos*10)
		parent.ui.Dial_Pitch.setValue(pos*10)
		
	def Init(self, parent):
		self.UpdateDesiredPosFlag = False
		if parent.tangoEnable:
			self.pos = self.axis.read_attribute('Position')
		else:
			pos = 2
		parent.ui.DesirePos_Pitch.setValue(self.pos.value)
		parent.ui.Scroll_Pitch.setValue(-self.pos.value*10)
		parent.ui.Dial_Pitch.setValue(self.pos.value*10)
	     
	def CurrentPosition(self, parent):
		if parent.tangoEnable:
			self.pos = self.axis.read_attribute('Position')
			parent.ui.CurrentPos_Pitch.display(self.pos.value)
			self.Status = self.axis.Status()

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
		pos = round(parent.ui.DesirePos_Yaw.value(),4)
		if parent.tangoEnable:
			self.axis.write_attribute('Position',pos)	
		else:
			parent.ui.CurrentPos_Yaw.display(pos)	
		
	def UpdateDesiredPos(self, parent):
		if self.UpdateDesiredPosFlag:
			self.UpdateDesiredPosFlag = False
			pos = parent.ui.Dial_Yaw.value()
			parent.ui.DesirePos_Yaw.setValue(float(pos)/10)
	
	def UpdateDesiredPosEnable(self, parent):
		self.UpdateDesiredPosFlag = True
		
	def UpdateScroll(self, parent):
		self.UpdateDesiredPosFlag = False
		pos = parent.ui.DesirePos_Yaw.value()
		parent.ui.Dial_Yaw.setValue(pos*10)
		
	def Init(self, parent):
		self.UpdateDesiredPosFlag = False
		if parent.tangoEnable:
			self.pos = self.axis.read_attribute('Position')
		else:
			pos = 2
		parent.ui.DesirePos_Yaw.setValue(self.pos.value)
		parent.ui.Dial_Yaw.setValue(self.pos.value*10)
	     
	def CurrentPosition(self, parent):
		if parent.tangoEnable:
			self.pos = self.axis.read_attribute('Position')
			parent.ui.CurrentPos_Yaw.display(self.pos.value)
			self.Status = self.axis.Status()
			
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	win = pimicosMultiAxis()
	sys.exit(app.exec_())

import sys
from PyQt4 import QtGui, QtCore, uic

tangoEnable = False
if tangoEnable:
	import PyTango

class Axis(QtGui.QWidget):
	def __init__(self, Title, Device, uiFile, Invert):
		QtGui.QWidget.__init__(self)
 
		self.ui = uic.loadUi(uiFile)
		self.ui.show()		
		
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
		self.connect(self.ui.Move, QtCore.SIGNAL("clicked()"), self.Move)
		
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
		self.ui.Box.setTitle(Title)

		if Invert:
			if uiFile == "XWidget.ui":
				self.ui.JogPlus.setGeometry(40,150,51,41)
				self.ui.JogMinus.setGeometry(40,80,51,41)
				self.ui.Scroll.setInvertedAppearance(not Invert)
			elif (uiFile == "YWidget.ui") or (uiFile == "ZWidget.ui"):
				self.ui.JogPlus.setGeometry(110,50,51,41)
				self.ui.JogMinus.setGeometry(160,50,51,41)
				self.ui.Scroll.setInvertedAppearance(Invert)
		else:
			if uiFile == "XWidget.ui":
				self.ui.JogPlus.setGeometry(40,80,51,41)
				self.ui.JogMinus.setGeometry(40,150,51,41)
				self.ui.Scroll.setInvertedAppearance(not Invert)
			elif (uiFile == "YWidget.ui") or (uiFile == "ZWidget.ui"):
				self.ui.JogPlus.setGeometry(160,50,51,41)
				self.ui.JogMinus.setGeometry(110,50,51,41)
				self.ui.Scroll.setInvertedAppearance(Invert)
	   
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
		
	def Move(self):
		pos = self.ui.DesirePos.value()
		if tangoEnable:
			self.axis.position = pos	
		else:
			self.ui.StatusLabel.setText(str(pos))		
		
	def UpdateDesiredPosScroll(self):
		pos = self.ui.Scroll.value()
		self.ui.DesirePos.setValue(pos)
	
	def UpdateDesiredPos(self):
		if tangoEnable:
			pos = self.axis.position
			self.ui.DesirePos.setValue(pos)
	     
	def CurrentPosition(self):
		if tangoEnable:
			pos = self.axis.position
			self.ui.CurrentPos.display(pos)
	    
	def UpdateState(self):
		if tangoEnable:
			state = self.axis.state()
			self.ui.StatusLabel.setText(str(state))
	
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	
	#############################################################
	# X Sample
	XS_Title = "X Sample"
	XS_Device = "anka/motor_detlab/xsample"
	XS_uiFile = "XWidget.ui"
	XS_Invert = True
	XSample = Axis(XS_Title, XS_Device, XS_uiFile, XS_Invert)
	
	# Y Sample
	YS_Title = "Y Sample"
	YS_Device = "anka/motor_detlab/ysample"
	YS_uiFile = "YWidget.ui"
	YS_Invert = True
	YSample = Axis(YS_Title, YS_Device, YS_uiFile, YS_Invert)
	
	# Z Sample
	ZS_Title = "Z Sample"
	ZS_Device = "anka/motor_detlab/zsample"
	ZS_uiFile = "ZWidget.ui"
	ZS_Invert = True
	ZSample = Axis(ZS_Title, ZS_Device, ZS_uiFile, ZS_Invert)

	##############################################################
	# X Detector
	XD_Title = "X Detector"
	XD_Device = "anka/motor_detlab/xdet"
	XD_uiFile = "XWidget.ui"
	XD_Invert = False
	XDetector = Axis(XD_Title, XD_Device, XD_uiFile, XD_Invert)

	# Y Detector
	YD_Title = "Y Detector"
	YD_Device = "anka/motor_detlab/ydet"
	YD_uiFile = "YWidget.ui"
	YD_Invert = False
	YDetector = Axis(YD_Title, YD_Device, YD_uiFile, YD_Invert)

	# Z Detector
	ZD_Title = "Z Detector"
	ZD_Device = "anka/motor_detlab/zdet"
	ZD_uiFile = "ZWidget.ui"
	ZD_Invert = False
	ZDetector = Axis(ZD_Title, ZD_Device, ZD_uiFile, ZD_Invert)

	sys.exit(app.exec_())

#!/usr/bin/env python2.7
#-*-python-2.7-
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal
from phone import *


class Aria_Call(object):
	def __init__(self):
		self.win = QtGui.QMainWindow()
		self.setup_ui()
		self.state=False;
		self.win.show()
		self.phone_setup()
	def setup_ui(self):
		self.setup()
		self.win.setWindowTitle("ARIA Calling")
		self.win.resize(435, 201)
		self.win.setMenuBar(self.menubar)
		self.statusbar = QtGui.QStatusBar(self.win)
		self.win.setStatusBar(self.statusbar)
		self.win.setCentralWidget(self.centralwidget)
		self.setactions()

	def setup(self):
		self.centralwidget = QtGui.QWidget(self.win)
		self.MsgArea = QtGui.QLabel(self.centralwidget)
		self.MsgArea.setText("")
		
		self.PhoneLabel = QtGui.QLabel(self.centralwidget)
		self.PhoneNo = QtGui.QLineEdit(self.centralwidget)

		self.formLayout = QtGui.QFormLayout()
		self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.PhoneLabel)
		self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.PhoneNo)

		self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
		self.gridLayout_2.addWidget(self.MsgArea, 0, 0, 1, 1)
		self.gridLayout_2.addLayout(self.formLayout, 1, 0, 1, 1)

		self.BtnLayout = QtGui.QHBoxLayout()


		self.callBtn = QtGui.QPushButton(self.centralwidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.callBtn.sizePolicy().hasHeightForWidth())
		self.callBtn.setSizePolicy(sizePolicy)

		self.BtnLayout.addWidget(self.callBtn)

		self.gridLayout_2.addLayout(self.BtnLayout, 2, 0, 1, 1)

		self.menubar = QtGui.QMenuBar(self.win)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 435, 22))
		self.menuFile = QtGui.QMenu(self.menubar)

		self.actionRegister = QtGui.QAction(self.win)
		self.menuFile.addAction(self.actionRegister)
		self.menubar.addAction(self.menuFile.menuAction())

		
		self.PhoneLabel.setText("Phone No:")
		self.callBtn.setText("Call")
		self.menuFile.setTitle("File")
		self.actionRegister.setText("Unregister")

	def setactions(self):
		
		QtCore.QObject.connect(self.callBtn, QtCore.SIGNAL("clicked()"),self.click)
		QtCore.QObject.connect(self.actionRegister, QtCore.SIGNAL("triggered()"),self.unregister)
		QtCore.QMetaObject.connectSlotsByName(self.win)

	def setmsg(self,msgstr=""):
		self.MsgArea.setText(msgstr)
	def click(self):
		self.statusbar.clearMessage()
		if(self.state):
			self.endcall(1)
		else:
			t=str(self.PhoneNo.text())
			if t.isdigit():
				self.state=True
				print t
				current_call = self.ph.call(t,msgfn=self.setmsg,stfn=self.endcall)
				self.callBtn.setText("End")
			else:
				return

	def unregister(self):
		self.ph.destroy()
		self.ph=None

	def phone_setup(self):
		self.ph=Phone(5080)     
	    	self.ph.register("127.0.0.1:5060","blaine")
		self.ph.printstatus(self.statusbar.showMessage)

	def endcall(self,t):
		if t==0:
			try:
				current_call=calllist.pop()
				current_call = None
			except IndexError:
				pass
				self.state=False
				self.callBtn.setText("Call")
		if t==1:
			try:
				current_call=calllist.pop()
				current_call.hangup()
			except pjsua.Error, e:
				pass 
			except IndexError:
				pass


if __name__ == "__main__":
	import sys
	calllist=list()
	app = QtGui.QApplication(sys.argv)
	ui=Aria_Call()
	QtCore.QObject.connect(app, QtCore.SIGNAL("lastWindowClosed()"),ui.unregister)
	#app.connect(app, SIGNAL(),app, SLOT("quit()"))
	#app.exec_loop()
	app.exec_()
#	ui.unregister()
#	sys.exit()

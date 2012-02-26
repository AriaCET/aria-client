#!/usr/bin/env python2.7
#-*-python-2.7-
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

class Aria_Call(object):
	def __init__(self,argv=''):
		app = QtGui.QApplication(argv)
		self.win = QtGui.QMainWindow()
		self.setup_ui()
		self.win.show()
		sys.exit(app.exec_())

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

		self.cancelBtn = QtGui.QPushButton(self.centralwidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.cancelBtn.sizePolicy().hasHeightForWidth())

		self.cancelBtn.setSizePolicy(sizePolicy)

		self.BtnLayout.addWidget(self.cancelBtn)

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
		self.cancelBtn.setText("Cancel")
		self.callBtn.setText("Call")
		self.menuFile.setTitle("File")
		self.actionRegister.setText("Register")

	def setactions(self):
		
		QtCore.QObject.connect(self.cancelBtn, QtCore.SIGNAL("clicked()"), self.win.close)
		#QtCore.QObject.connect(self.callBtn, QtCore.SIGNAL("clicked()"),call)
		#QtCore.QObject.connect(self.actionRegister, QtCore.SIGNAL("triggered()"),register)
		QtCore.QMetaObject.connectSlotsByName(self.win)

	def setmsg(msgstr=""):
		self.MsgArea.setText(msgstr)

if __name__ == "__main__":
	import sys
	ui=Aria_Call(sys.argv)


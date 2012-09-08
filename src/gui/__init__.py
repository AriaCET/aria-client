#!/usr/bin/env python2.7
#-*-python-2.7-
# -*- coding: utf-8 -*-
from PySide import QtGui
from login import Login
from mainWindow import MainWindow

if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	ui = Login()
	ui.show()
	ui2 = MainWindow()
	ui2.hide()
	sys.exit(app.exec_())
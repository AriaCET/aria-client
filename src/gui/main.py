#!/usr/bin/env python2.7
#-*-python-2.7-
# -*- coding: utf-8 -*-

from PySide import QtGui
from mainWindow import MainWindow

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())
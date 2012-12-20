#!/usr/bin/env python2.7
#-*-python-2.7-
# -*- coding: utf-8 -*-
try:
	from PySide import QtGui ,QtCore
except Exception, e:
	from PyQt4 import QtGui

from speakerManagement import SpeakerManagement
from passwordChange import passwordChange
from configDialog import configDialog
import config as config

class MainSettings(QtGui.QDialog):
    def __init__(self,parent = None):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint)
        self.password()

    def password(self):
        firstTime = not config.isPassWordOk()
        self.passwordDialog = passwordChange(firstTime=firstTime,isContinue=True)
        QtCore.QObject.connect(self.passwordDialog, QtCore.SIGNAL("accepted()"),self.config)
        QtCore.QObject.connect(self.passwordDialog, QtCore.SIGNAL("rejected()"),self.cancel)

    def speaker(self):
        self.speakerDialog = SpeakerManagement(isContinue=True)
        QtCore.QObject.connect(self.speakerDialog, QtCore.SIGNAL("accepted()"),self.ok)
        QtCore.QObject.connect(self.speakerDialog, QtCore.SIGNAL("rejected()"),self.cancel)

    def config(self):
        self.configUi = configDialog(isContinue=True)
        QtCore.QObject.connect(self.configUi, QtCore.SIGNAL("accepted()"),self.speaker)
        QtCore.QObject.connect(self.configUi, QtCore.SIGNAL("rejected()"),self.cancel)

    def ok(self):
        QtGui.QMessageBox.information(self, "ARIA ","Settings Saved")
    def cancel(self):
        pass
        

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = MainSettings()
    sys.exit(app.exec_())

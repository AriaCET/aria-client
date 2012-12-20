# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'changePassword.ui'
#
# Created: Wed Dec 12 22:51:10 2012
#      by: pyside-uic 0.2.14 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class passwordChange(QtGui.QDialog):
    def __init__(self,parent = None, firstTime=False, isContinue=False):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint)
        self.firstTime = firstTime
        self.setupUi(isContinue)
        self.show()

    def setupUi(self, isContinue):

        self.resize(391, 226)
        self.setWindowTitle( "Change Password")        

        self.gridLayout = QtGui.QGridLayout(self)

        self.opassBox = QtGui.QLineEdit(self)
        self.opassBox.setEchoMode(QtGui.QLineEdit.Password)
        self.gridLayout.addWidget(self.opassBox, 0, 1, 1, 1)

        self.rpasslbl = QtGui.QLabel("Repet", self)
        self.gridLayout.addWidget(self.rpasslbl, 3, 0, 1, 1)
        
        self.npassBox = QtGui.QLineEdit(self)
        self.npassBox.setEchoMode(QtGui.QLineEdit.Password)
        self.gridLayout.addWidget(self.npassBox, 2, 1, 1, 1) 

        self.rpassBox = QtGui.QLineEdit(self)
        self.rpassBox.setEchoMode(QtGui.QLineEdit.Password)
        self.gridLayout.addWidget(self.rpassBox, 3, 1, 1, 1)

        self.opasslbl = QtGui.QLabel("Old Password", self)
        self.gridLayout.addWidget(self.opasslbl, 0, 0, 1, 1)

        if self.firstTime:
            self.opassBox.setEnabled(False)

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        if isContinue:
            self.buttonBox.addButton("Next", QtGui.QDialogButtonBox.AcceptRole)
        else:
            self.buttonBox.addButton("Change", QtGui.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton("Cancel", QtGui.QDialogButtonBox.RejectRole)
        self.gridLayout.addWidget(self.buttonBox, 5, 1, 1, 1)

        self.npasslbl = QtGui.QLabel("New Password", self)
        self.gridLayout.addWidget(self.npasslbl, 2, 0, 1, 1)


        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.change)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def change(self):
        oldPass = self.opassBox.text()
        newPass = self.npassBox.text()
        repetPass = self.rpassBox.text()
        self.deleteErrorMsg()

        from ConfigParser import NoSectionError
        import config as config
        try:
            auth = config.auth(oldPass)
        except NoSectionError :
            auth = True
        if not auth and not self.firstTime:
            self.err = QtGui.QLabel("<font color=\"red\"> Authentication failure</font>")
            self.gridLayout.addWidget(self.err, 4, 1, 1, 1)
            return
        elif newPass != repetPass :
            self.err = QtGui.QLabel("<font color=\"red\"> Password did not match </font>")
            self.gridLayout.addWidget(self.err, 4, 1, 1, 1)
            return
        config.setPassword(newPass)    
        self.accept()

    def deleteErrorMsg(self):
        try:
            self.err.close()
        except AttributeError:
            pass

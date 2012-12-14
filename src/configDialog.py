# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config.ui'
#
# Created: Wed Dec 12 23:37:29 2012
#      by: pyside-uic 0.2.14 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class configDialog(QtGui.QDialog):
    def __init__(self,parent = None,isContinue=False):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(isContinue)
        self.setValues()
        self.show()
    
    def setupUi(self,isContinue):

        self.resize(400, 300)
        self.setWindowTitle( "Dialog")
        
        self.gridLayout = QtGui.QGridLayout(self)
        
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        if isContinue:
            self.buttonBox.addButton("Next", QtGui.QDialogButtonBox.AcceptRole)
        else:
            self.buttonBox.addButton("Update", QtGui.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton("Cancel", QtGui.QDialogButtonBox.RejectRole)
        self.gridLayout.addWidget(self.buttonBox, 5, 1, 1, 1)
        
        self.domainlbl = QtGui.QLabel("Domain")
        self.gridLayout.addWidget(self.domainlbl, 0, 0, 1, 1)

        self.passBox = QtGui.QLineEdit(self)
        self.passBox.setEchoMode(QtGui.QLineEdit.Password)
        self.gridLayout.addWidget(self.passBox, 2, 1, 1, 1)

        self.domainBox = QtGui.QLineEdit()
        self.domainBox.setText("127.0.0.1:5060")
        self.gridLayout.addWidget(self.domainBox, 0, 1, 1, 1)

        self.usernameBox = QtGui.QLineEdit()
        self.gridLayout.addWidget(self.usernameBox, 1, 1, 1, 1)

        self.portBox = QtGui.QLineEdit()
        self.portBox.setText("5080")
        self.gridLayout.addWidget(self.portBox, 3, 1, 1, 1)

        self.usernamelbl = QtGui.QLabel("Username")
        self.gridLayout.addWidget(self.usernamelbl, 1, 0, 1, 1)

        self.passlbl = QtGui.QLabel("Password")
        self.gridLayout.addWidget(self.passlbl, 2, 0, 1, 1)

        self.portlbl = QtGui.QLabel("Bind Port")
        self.gridLayout.addWidget(self.portlbl, 3, 0, 1, 1)


        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.ok)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)
        
    def ok(self):
        domain = self.domainBox.text()
        username = self.usernameBox.text() 
        password = self.passBox.text()
        port = self.portBox.text()
        if domain == "":
            self.errorMsg("Domain should not empty")
            return   
        if username == "":
            self.errorMsg("Username should not empty")
            return
        if port == "":
            self.errorMsg("Bind Port should not empty")
            return
        import config as config
        config.setPhoneSettings(domain,username,password,port)
        self.accept()

    def errorMsg(self, str):
        self.deleteErrorMsg()
        self.err = QtGui.QLabel("<font color=\"red\"> " + str + "</font>")
        self.gridLayout.addWidget(self.err, 4, 1, 1, 1)

    def deleteErrorMsg(self):
        try:
            self.err.close()
        except AttributeError:
            pass
    def setValues(self):
        from ConfigParser import NoSectionError
        import config as config
        try:
            config.init()
            self.domainBox.setText(config.domain)
            self.usernameBox.setText(config.username)
            self.passBox.setText(config.password)
            self.portBox.setText(config.bindport)
        except NoSectionError, e:
            print e
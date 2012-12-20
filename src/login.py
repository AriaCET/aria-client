# -*- coding: utf-8 -*-
#-*-python-2.7-
try:
    from PySide import QtCore, QtGui
except:
    from PyQt4 import QtCore, QtGui

import config

class Login(QtGui.QDialog):
    def __init__(self,parent = None):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi()
        try:
            config.auth("") # to check Password is in Config File
        except Exception, e:
            QtGui.QMessageBox.critical(self,"Configuration Error"," \n Run ariasetup")
            self.close()
            exit()
        self.show()

    def setupUi(self):
        
        self.resize(375, 169)
        self.setWindowTitle("ARIA")

        self.mainlayout = QtGui.QVBoxLayout(self)
        self.mainlayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.mainlayout.setContentsMargins(12, -1, 12, 27)
        
        spacerItem = QtGui.QSpacerItem(20, 19, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.mainlayout.addItem(spacerItem)
        
        self.verticalLayout = QtGui.QVBoxLayout()
        
        self.textboxLayout = QtGui.QHBoxLayout()
        
        self.passLabel = QtGui.QLabel("password:",self)
        self.textboxLayout.addWidget(self.passLabel)
        
        self.passBox = QtGui.QLineEdit(self)
        self.passBox.setEchoMode(QtGui.QLineEdit.Password)
        self.textboxLayout.addWidget(self.passBox)
        self.verticalLayout.addLayout(self.textboxLayout)
        
        spacer = QtGui.QSpacerItem(20, 28, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer)
        
        self.buttonLayout = QtGui.QHBoxLayout()
        self.buttonLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.buttonLayout.setContentsMargins(150, -1, 5, -1)
        
        self.buttonSpliter = QtGui.QSplitter(self)
        self.buttonSpliter.setOrientation(QtCore.Qt.Horizontal)
        
        self.cancelButton = QtGui.QPushButton("Cancel",self.buttonSpliter)
        self.okButton = QtGui.QPushButton("Ok",self.buttonSpliter)
        self.okButton.setDefault(True)
        self.okButton.setEnabled(True)
        
        self.buttonLayout.addWidget(self.buttonSpliter)
        self.verticalLayout.addLayout(self.buttonLayout)
        self.mainlayout.addLayout(self.verticalLayout)

        self.cancelButton.clicked.connect(self.reject)
        self.okButton.clicked.connect(self.login)
        
        self.setTabOrder(self.passBox, self.cancelButton)
        self.setTabOrder(self.cancelButton, self.okButton)

    def login(self):
        password = self.passBox.text()
        if config.auth(password) :
            self.accept()
        self.passBox.setText("")
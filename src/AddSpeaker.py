# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'speakerAdd.ui'
#
# Created: Tue Dec 11 13:21:37 2012
#      by: pyside-uic 0.2.14 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
from PySide.QtCore import QThread

class AddSpeaker(QtGui.QDialog):
    def __init__(self,parent = None):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi()
        self.show()
    
    def setupUi(self):

        self.resize(418, 192)
        self.gridLayout = QtGui.QGridLayout(self)
        self.setWindowTitle("Add Speaker")

        spacerItem = QtGui.QSpacerItem(20, 6, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 56, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 6, 0, 1, 1)

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.addButton("Cancel", QtGui.QDialogButtonBox.RejectRole)
        self.buttonBox.addButton("Add", QtGui.QDialogButtonBox.AcceptRole)
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 2)

        self.nameLabel= QtGui.QLabel("Name", self)
        self.gridLayout.addWidget(self.nameLabel, 2, 0, 1, 1)

        self.nameBox = QtGui.QLineEdit(self)
        self.gridLayout.addWidget(self.nameBox, 2, 1, 1, 1)
        
        self.numberLabel = QtGui.QLabel("Number", self)
        self.gridLayout.addWidget(self.numberLabel, 4, 0, 1, 1)
        
        self.numberBox = QtGui.QLineEdit(self)
        self.gridLayout.addWidget(self.numberBox, 4, 1, 1, 1)
        

        self.mainLabel = QtGui.QLabel("Enter Details :\n", self)
        self.gridLayout.addWidget(self.mainLabel, 1, 0, 1, 2)


        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.add)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def add(self):
        number = self.numberBox.text().strip()
        name = self.nameBox.text().strip()
        if name == '' :
            self.deleteNumErrorMsg()
            self.nameError = QtGui.QLabel("<font color=\"red\"> Name should not be blank</font>")
            self.gridLayout.addWidget(self.nameError, 3, 1, 1, 1)
            return
        if not number.isdigit() or number =='':
            self.deleteNameErrorMsg()
            self.numError = QtGui.QLabel("<font color=\"red\">Number is blank or not digits</font>")
            self.gridLayout.addWidget(self.numError, 5, 1, 1, 1)
            return
        self.emit(QtCore.SIGNAL('add(const QString& ,const QString& )'),name,number)
        self.accept()

    def deleteNameErrorMsg(self):
        try:
            self.nameError.close()
        except AttributeError:
            pass

    def deleteNumErrorMsg(self):
        try:
            self.nameError.close()
        except AttributeError:
            pass

# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui

class Login(QtGui.QDialog):
    def __init__(self,parent = None):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi()
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
        print password
        if password == "test":
            self.accept()
        self.passBox.setText("")      


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = Login()
    sys.exit(app.exec_())
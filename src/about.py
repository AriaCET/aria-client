# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created: Fri Dec 21 14:19:39 2012
#      by: pyside-uic 0.2.14 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

try:
    from PySide import QtCore, QtGui
except Exception, e:
    from PyQt4 import QtCore, QtGui


class About(QtGui.QDialog):
    def __init__(self,parent = None):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi()
        self.show()
        self.setinfo()

    def setupUi(self):

        self.resize(300, 200)
        self.gridLayout = QtGui.QGridLayout(self)

        self.info = QtGui.QLabel(self)

        self.gridLayout.addWidget(self.info, 0, 0, 1, 3)
        self.Credits = QtGui.QPushButton("Credits", self)
        self.Credits.setCheckable(True)

        self.gridLayout.addWidget(self.Credits, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(197, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.Ok = QtGui.QPushButton("Ok", self)

        self.gridLayout.addWidget(self.Ok, 1, 2, 1, 1)

        self.setWindowTitle("About")

        self.Credits.clicked.connect(self.toggleCredits)
        self.Ok.clicked.connect(self.accept)
        QtCore.QMetaObject.connectSlotsByName(self)
    
    def setinfo(self):
        aboutmsg = """<p><h3>Asterisk RadIo Architecture</h3></p>
        <p>An public addressing system based on the Asterisk VoIP network</p>"""
        self.info.setText(aboutmsg)

    def setCredits(self):
        credits = """
        <h3 align=\"center\">credits</h3>
        <div align=\"center\">
        Abil N George<br/>
        Dhananjay M Balan<br/>
        Deepak Krishnan<br/>
        Melwin Jose<br/>
        Thomas Abraham<br/>
        Sujith G<br/>
        </div>
        """
        self.info.setText(credits) 

    def toggleCredits(self):
        if self.sender().isChecked():
            self.setCredits()
        else :
            self.setinfo()

# -*- coding: utf-8 -*-


from PySide import QtCore, QtGui


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.speakerBtns = []
        self.selectedSpeaker = None
        self.setupUi()
        self.show()

    def setupUi(self):
        self.setWindowTitle("ARIA")
        self.resize(678, 341)
        self.centralwidget = QtGui.QWidget(self)
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)

        self.mainVerticalLayout = QtGui.QVBoxLayout()

        self.label = QtGui.QLabel("Select speaker : \n",self.centralwidget)
        self.mainVerticalLayout.addWidget(self.label)
        
        self.horizontalLayout = QtGui.QHBoxLayout()

        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.adjustSize()

        self.speakerBtnLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        #set spaker buttons        
        self.setSpeakerBtns(self.speakerBtnLayout)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)

        self.btnLayout = QtGui.QVBoxLayout()
        self.okBtn = QtGui.QPushButton("Ok")

        self.okBtn.clicked.connect(self.okAct)
        
        self.okBtn.setEnabled(False)
        self.btnLayout.addWidget(self.okBtn)
        self.cancelBtn = QtGui.QPushButton("Cancel")
        self.cancelBtn.setEnabled(False)
        self.cancelBtn.clicked.connect(self.cancelAct)
        self.btnLayout.addWidget(self.cancelBtn)
        self.horizontalLayout.addLayout(self.btnLayout)

        self.mainVerticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.mainVerticalLayout, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 678, 30))
        self.menuFile = QtGui.QMenu("&File",self.menubar)
        self.menuHelp = QtGui.QMenu("&Help",self.menubar)
        self.setMenuBar(self.menubar)
        self.actionQuit = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",triggered=self.close)
        self.actionAbout = QtGui.QAction("&About", self, triggered=self.about)

        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())


        self.statusbar = QtGui.QStatusBar(self)
        self.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(self)

    def setSpeakerBtns(self,layout):
        #size = QtCore.QSize(30,20)
        for i in range(0,10):
            pushButton = QtGui.QPushButton("Name"+str(i),self.scrollAreaWidgetContents)
            pushButton.setAutoFillBackground(False)
            pushButton.setCheckable(True)
            pushButton.clicked.connect(self.speakerSelect)
            #pushButton.setAutoExclusive(True)
            #pushButton.resize(size)
            layout.addWidget(pushButton)
            self.speakerBtns.append(pushButton)

    def speakerSelect(self):
        btn = self.sender()
        if self.selectedSpeaker != None:
            self.selectedSpeaker.setChecked(False)
        if btn.isChecked():
            self.selectedSpeaker = btn
            self.okBtn.setEnabled(True)
            self.cancelBtn.setEnabled(True)
            self.statusbar.message("Selected Speaker :"
                +str(btn.text()),0)
        else:
            self.selectedSpeaker = None
            self.okBtn.setEnabled(False)
            self.cancelBtn.setEnabled(False)
            self.statusbar.clear()

    def cancelAct(self):
        if self.cancelBtn.text() == "Cancel":
            self.selectedSpeaker.setChecked(False)
            self.selectedSpeaker = None
            self.okBtn.setEnabled(False)
            self.cancelBtn.setEnabled(False)

    def okAct(self):
        index = self.speakerBtns.index(self.selectedSpeaker)
        print index
        #TODO Call
        self.okBtn.setEnabled(False)
        self.cancelBtn.setText("End")

    def about(self):
        QtGui.QMessageBox.about(self, "About ARIA",
            "<p><b>Asterisk RadIo Architecture</b></p>"
            "<p>An public addressing system based on the Asterisk VoIP network</p>")



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())
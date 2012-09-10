# -*- coding: utf-8 -*-
#-*-python-2.7-

from PySide import QtCore, QtGui
from login import Login
import config as config
import pjsua
from phone import Phone

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.speakerBtns = list()
        self.selectedSpeaker = None
        config.init()
        login = Login(self)
        QtCore.QObject.connect(login, QtCore.SIGNAL("accepted()"),self.loginSucess)
        QtCore.QObject.connect(login, QtCore.SIGNAL("reject()"),self.loginFailed)

    def loginSucess(self):
        self.setupUi()
        self.setEnabled(False)
        self.show()
        if self.phone_setup() :
            self.calllist = list()
            self.setEnabled(True)   

    def loginFailed(self):
        print "Bye...."
        self.close()       

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
        self.scrollArea.setLayout(QtGui.QGridLayout())
        
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.adjustSize()

        #self.speakerBtnLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.speakerBtnLayout = QtGui.QGridLayout(self.scrollAreaWidgetContents)
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
        i = 0
        for speaker in config.getSpeakers():
            pushButton = Speaker(speaker['Name'],speaker['Number'],self.layout)
            #QtGui.QPushButton("\nName"+str(i)+"\n",self.scrollAreaWidgetContents)
            pushButton.setAutoFillBackground(False)
            pushButton.setCheckable(True)
            #pushButton.setAutoExclusive(True)
            #pushButton.resize(size)
            pushButton.clicked.connect(self.speakerSelect)
            layout.addWidget(pushButton, i / 3, i % 3)
            i = i + 1
            self.speakerBtns.append(pushButton)

    def speakerSelect(self,clear=True):
        btn = self.sender()
        if self.selectedSpeaker != None:
            self.selectedSpeaker.setChecked(False)
        if btn.isChecked():
            self.selectedSpeaker = btn
            self.okBtn.setEnabled(True)
            self.cancelBtn.setEnabled(True)
            self.statusbar.message("Selected Speaker :"
                +str(btn) ,0)
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
            self.statusbar.clear()
        if self.cancelBtn.text() == "End":
            self.endcall(1)
            #self.okBtn.setEnabled(True)
            #self.cancelBtn.setText("Cancel")
            #self.scrollArea.setEnabled(True)

    def okAct(self):
        number = self.selectedSpeaker.getNumber()
        #print number
        #TODO Call
        self.scrollArea.setEnabled(False)
        self.okBtn.setEnabled(False)
        self.cancelBtn.setText("End")
        current_call = self.ph.call(number,msgfn=self.setmsg,stfn=self.endcall)
        self.calllist.append(current_call)

    def about(self):
        QtGui.QMessageBox.about(self, "About ARIA",
            "<p><b>Asterisk RadIo Architecture</b></p>"
            "<p>An public addressing system based on the Asterisk VoIP network</p>")

    def endcall(self,t):
        if t==0:
            try:
                current_call=self.calllist.pop()
                print(current_call.is_valid())
                current_call = None
            except IndexError:
                pass
        if t==1:
            try:
                current_call=self.calllist.pop()
                print(current_call.is_valid())
                current_call.hangup()
                #self.statusbar.showMessage(str(current_call.info().state_text),1000)
            except pjsua.Error, e:
                print ("e"+str(e))
                #pass 
            except IndexError ,e:
                print ("e"+str(e))
                #pass
        self.okBtn.setEnabled(True)
        self.cancelBtn.setText("Cancel")
        self.scrollArea.setEnabled(True)
        #self.selectedSpeaker.click()
        #self.statusbar.message("Disconnected",0)

    def phone_setup(self):
        print config.domain
        print config.username
        print config.password
        print type(config.bindport)
        self.ph = Phone(int(config.bindport))
        status = self.ph.register(domain=config.domain,
            username=config.username, password=config.password)
        if status != 200: #200 is OK
            errorBox = QtGui.QMessageBox.critical(self,"","Registation Failed")
            self.close()
            return False
        else :
            return True

    def setmsg(self,message,time=1000):
        self.statusbar.clear()
        self.statusbar.message(message,time)

class Speaker(QtGui.QPushButton):
    """ Speaker"""
    def __init__(self, name,number,parent=None):
        super(Speaker,self).__init__()
        self.setText("\n"+name+"\n")
        self.__name__ = name
        self.__number__ = number
    
    def __str__(self):
        return (str(self.__name__) + 
            " ["+str(self.__number__)+"]")

    def getNumber(self):
        return self.__number__

    def getName(self):
        return self.__name__
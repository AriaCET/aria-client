# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'self.ui'
#
# Created: Tue Dec 11 14:14:51 2012
#      by: pyside-uic 0.2.14 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class SpeakerManagement(QtGui.QDialog):
    def __init__(self,parent = None,isContinue=False):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(isContinue)
        self.setSpeakers()
        self.show()

    def setupUi(self,isContinue):
        self.resize(400, 300)
        self.setWindowTitle("Speaker Management")


        self.addBtn = QtGui.QPushButton("Add", self)
        self.addBtn.setGeometry(QtCore.QRect(290, 50, 101, 32))
        self.addBtn.clicked.connect(self.AddSpeaker)

        self.delBtn = QtGui.QPushButton("Delete", self)
        self.delBtn.setGeometry(QtCore.QRect(290, 90, 101, 32))
        self.delBtn.setEnabled(False)
        self.delBtn.clicked.connect(self.deleteSpeaker)

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(210, 250, 176, 32))
        if isContinue:
            self.buttonBox.addButton("Next", QtGui.QDialogButtonBox.AcceptRole)
        else:
            self.buttonBox.addButton("Apply", QtGui.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton("Cancel", QtGui.QDialogButtonBox.RejectRole)

        self.rowcount=0

        self.tableWidget = QtGui.QTableWidget(self.rowcount, 2, self)
        self.tableWidget.setGeometry(QtCore.QRect(10, 20, 271, 191))
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)       
        self.tableWidget.verticalHeader().setCascadingSectionResizes(True)
        self.tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows) 
        self.tableWidget.setHorizontalHeaderLabels(['Name','Number']) #'Extension Number'])

        self.connect(self.tableWidget, QtCore.SIGNAL("itemSelectionChanged()"), self.enableDelButton)
        self.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.saveSpeakers)
        QtCore.QMetaObject.connectSlotsByName(self)

    def AddSpeaker(self):
        from AddSpeaker import AddSpeaker
        popup = AddSpeaker(self)
        QtCore.QObject.connect(popup, QtCore.SIGNAL('add(const QString& ,const QString& )'), self.addRow)

    def addRow(self, name, number):
        if not number.isdigit():
            return
        if name == '' or number =='':
            return
        #print name
        #print number
        self.tableWidget.insertRow(self.rowcount)
        self.rowcount = self.rowcount + 1
        self.setValue(self.rowcount -1,name,number)

    def getValue(self,row):
        try:
            name = self.tableWidget.item(row, 0).text()
            number = self.tableWidget.item(row, 1).text()
        except Exception, e:
            name = number = None
        return (name, number)

    def setValue(self,row,name,number):
        newItem1 = QtGui.QTableWidgetItem(name)
        flag = newItem1.flags() ^(QtCore.Qt.ItemIsEditable)
        newItem1.setFlags(flag)
        self.tableWidget.setItem(row, 0, newItem1)

        newItem2 = QtGui.QTableWidgetItem(number)
        newItem2.setFlags(flag)
        self.tableWidget.setItem(row, 1, newItem2)
        
    def deleteSpeaker(self):
        row = self.tableWidget.selectedIndexes()[0].row()
        #print row
        self.rowcount = self.rowcount - 1
        self.tableWidget.removeRow(row)

    def enableDelButton(self):
            self.delBtn.setEnabled(True)

    def setSpeakers(self):
        from ConfigParser import NoSectionError
        import config as config
        try:
            for speaker in config.getSpeakers():
                self.addRow(speaker['Name'],speaker['Number'])
        except NoSectionError :
            pass

    def saveSpeakers(self):
        speakers = []
        for index in xrange(0,self.rowcount):
            (name,number) = self.getValue(index)
            speaker = {'Name':name ,'Number':number}
            speakers.append(speaker)
        from ConfigParser import NoSectionError
        import config as config
        config.setSpeakers(speakers)
        self.accept()
#-*-python-2.7-
# -*- coding: utf-8 -*-
#File:phone.py
#Implementing functions for phone.

import pjsua
from CallConfig import PhoneCallCallback
from AccountConfig import PhoneAccountCallback
from cmdlinefunctions import debugMessage
try:
    from PySide import QtCore, QtGui
    from PySide.QtCore import QThread
except:
    from PyQt4 import QtCore, QtGui
    from PyQt4.QtCore import QThread

class Phone(QThread):
    def __init__(self,port=0, bound_addr='', public_addr='',Sound_rate=44100):
        super(Phone, self).__init__() 
        self.exiting = False
        self.lib = pjsua.Lib()
        self.Sound_rate=Sound_rate
        self.media_cfg = pjsua.MediaConfig()
        self.media_cfg.clock_rate = self.Sound_rate
        #self.media_cfg.no_vad = True
        self.lib.init(media_cfg=self.media_cfg)
        #pass log_cfg = pjsua.LogConfig(level=4, =log_cb)) for debuging
        self.TransConfig=pjsua.TransportConfig(port,bound_addr,public_addr)
        self.transport=self.lib.create_transport(pjsua.TransportType.UDP,self.TransConfig)
        self.lib.start()

    def register(self,domain='', username='', password='', display='', registrar='', proxy=''):
        try:
            self.domain=domain
            self.AccConfig=pjsua.AccountConfig(domain, username, password, display,registrar,proxy)
            self.account = self.lib.create_account(self.AccConfig)
            self.callbackAccount = PhoneAccountCallback(self.account)
            self.account.set_callback(self.callbackAccount)
            self.callbackAccount.wait()
        except pjsua.Error, e:
            debugMessage ("Exception: " + str(e))
            self.lib.destroy()
        self.signalStatus()

    def signalStatus(self):
        #print "hgfgfg"
        status = self.account.info().reg_status
        self.emit(QtCore.SIGNAL('regStatus(int )'),status)
        print (status)

    def printstatus(self):
        my_sip_uri = "sip:" + self.transport.info().host + \
            ":" + str(self.transport.info().port)
        msg = "SIP URI is"+ my_sip_uri
        self.printMessage(msg)
        msg = "Registration status ="+str(self.account.info().reg_status)+ \
            "(" + self.account.info().reg_reason+")"
        self.printMessage(msg)

    def deregister(self):
        self.account.set_registration(False)
        self.lib.destroy()
        del self.lib
        debugMessage ("Bye..............")
        self.signalStatus()
        

    def printMessage(self,msg,signal=True):
        debugMessage (msg)
        if signal:
            self.emit(QtCore.SIGNAL('phoneMessage(const QString& )'),msg)

    def statechanged(self,state):
        self.emit(QtCore.SIGNAL('statechanged(int )'),state)

    def call(self,phoneno,domain=''):
        try:
            if domain=='':
                domain=self.domain
            uri="<sip:"+str(phoneno)+"@"+domain+">"
            debugMessage ("Making call to"+ str(uri))
            self.callbackSetting = PhoneCallCallback(self.printMessage,self.statechanged);
            lck = self.lib.auto_lock()
            current_call=self.account.make_call(uri,cb=self.callbackSetting)
            del lck
            return current_call
        except pjsua.Error, e:
            msg = "Exception: "+ str(e)
            self.printMessage(msg)
            return

    def __del__(self):
        self.deregister()
        super.__del__()

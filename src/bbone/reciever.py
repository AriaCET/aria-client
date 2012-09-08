#!/usr/bin/env python2
import config
import sys
import pjsua as pj
import threading
from datetime import datetime

logfile = open(config.log, "a")
current_call = None

def log_actions(messege):
    tp = str(datetime.now())+":"
    if config.debug:
        print tp+messege
    logfile.write(tp+messege)

def log_cb(level, str, len):
    log_actions(str)

class MyAccountCallback(pj.AccountCallback):
    sem = None

    def __init__(self, account):
        pj.AccountCallback.__init__(self, account)

    def wait(self):
        self.sem = threading.Semaphore(0)
        self.sem.acquire()

    def on_reg_state(self):
        if self.sem:
            if self.account.info().reg_status >= 200:
                self.sem.release()

    def on_incoming_call(self, call):
        global current_call
        if current_call:
            call.answer(486, "Busy")
            return

        log_actions("Incoming call from "+str(call.info().remote_uri))

        current_call = call

        call_cb = MyCallCallback(current_call)
        current_call.set_callback(call_cb)

        current_call.answer()

class MyCallCallback(pj.CallCallback):

    def __init__(self, call=None):
        pj.CallCallback.__init__(self, call)

    # Notification when call state has changed
    def on_state(self):
        global current_call
        log_actions("Call with "+str(self.call.info().remote_uri)+"is"+ str(self.call.info().state_text)+"last code ="+str(self.call.info().last_code)+"(" + str(self.call.info().last_reason) + ")")

        if self.call.info().state == pj.CallState.DISCONNECTED:
            current_call = None
            log_actions('Current call is'+str(current_call))

    # Notification when call's media state has changed.
    def on_media_state(self):
        if self.call.info().media_state == pj.MediaState.ACTIVE:
            # Connect the call to sound device
            call_slot = self.call.info().conf_slot
            pj.Lib.instance().conf_connect(call_slot, 0)
            pj.Lib.instance().conf_connect(0, call_slot)
            print "Media is now active"
        else:
            print "Media is inactive"

lib = pj.Lib()

try:
    lib.init(log_cfg = pj.LogConfig(level=config.LEVEL, callback=log_cb))
    lib.create_transport(pj.TransportType.UDP, pj.TransportConfig(5080))
    lib.start()

    acc = lib.create_account(pj.AccountConfig(config.server, config.username, config.password))

    acc_cb = MyAccountCallback(acc)
    acc.set_callback(acc_cb)
    acc_cb.wait()

    log_actions("Registration complete, status="+str(acc.info().reg_status)+ "(" + str(acc.info().reg_reason) + ")")
    sys.stdin.readline()

except pj.Error, e:
    log_actions("Exception: " + str(e))
    lib.destroy()
    lib = None

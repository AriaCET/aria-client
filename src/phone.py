import sys
import pjsua
import threading


#def log_cb(level, str, len):   #for loging debuging
#    print str,

class MyAccountCallback(pjsua.AccountCallback):
    sem = None
    def __init__(self, account):
        pjsua.AccountCallback.__init__(self, account)

    def wait(self):
        self.sem = threading.Semaphore(0)
        self.sem.acquire()

    def on_reg_state(self):
        if self.sem:
            if self.account.info().reg_status >= 200:
                self.sem.release()
    def on_incoming_call(self, call):
        call.hangup(501, "Sorry, not ready to accept calls yet")

class MyCallCallback(pjsua.CallCallback):

    def __init__(self, call=None):
        pjsua.CallCallback.__init__(self, call)

    # Notification when call state has changed
    def on_state(self):
        #global current_call
        print "Call with", self.call.info().remote_uri,
        print "is", self.call.info().state_text,
        print "last code =", self.call.info().last_code, 
        print "(" + self.call.info().last_reason + ")"
        
        if self.call.info().state == pjsua.CallState.DISCONNECTED:
            current_call = None
            try:
                 self.call.hangup()
            except pjsua.Error, e:
                 pass #print "Exception: "+ str(e)
            print 'Current call is', current_call
            

    # Notification when call's media state has changed.
    def on_media_state(self):
        if self.call.info().media_state == pjsua.MediaState.ACTIVE:
            # Connect the call to sound device
            call_slot = self.call.info().conf_slot
            pjsua.Lib.instance().conf_connect(call_slot, 0)
            pjsua.Lib.instance().conf_connect(0, call_slot)
            print "Media is now active"
        else:
            print "Media is inactive"


class Phone():
    def __init__(self,port=0, bound_addr='', public_addr='',Sound_rate=44100):
        self.lib = pjsua.Lib()
        self.Sound_rate=Sound_rate
        self.media_cfg = pjsua.MediaConfig()
        self.media_cfg.clock_rate = self.Sound_rate
        #self.media_cfg.no_vad = True
        self.lib.init(media_cfg=self.media_cfg)#pass log_cfg = pjsua.LogConfig(level=4, callback=log_cb)) for debuging
	self.TransConfig=pjsua.TransportConfig(port,bound_addr,public_addr)
        self.transport=self.lib.create_transport(pjsua.TransportType.UDP,self.TransConfig)
        self.lib.start()
    def register(self,domain='', username='', password='', display='', registrar='', proxy=''):
        try:
            self.domain=domain
            self.AccConfig=pjsua.AccountConfig(domain, username, password, display,registrar,proxy)
            self.acc = self.lib.create_account(self.AccConfig)
            self.acc_cb = MyAccountCallback(self.acc)
            self.acc.set_callback(self.acc_cb)
            self.acc_cb.wait()
        except pjsua.Error, e:
            print "Exception: " + str(e)
            lib.destroy()

    def printstatus(self):
        my_sip_uri = "sip:" + self.transport.info().host + \
                 ":" + str(self.transport.info().port)
        print "My SIP URI is", my_sip_uri
        print("Registration status="+str(self.acc.info().reg_status)+"(" + self.acc.info().reg_reason+")")
        print("Press ENTER")
        sys.stdin.readline()
    def destroy(self):
	global current_call
        self.acc.delete()
        del current_call   ##############
        self.lib.destroy()
        self.lib = None
    def call(self,phoneno,domain=''):
        try:
            if domain=='':
                domain=self.domain
            uri="<sip:"+str(phoneno)+"@"+domain+">"
            print "Making call to", uri
            self.my_cb = MyCallCallback();
            current_call=self.acc.make_call(uri,cb=self.my_cb)
            return current_call
        except pjsua.Error, e:
            print "Exception: "+ str(e)
            return
    def __del__(self):
        self.destroy()
	super.__del__()

def end_call():
    try:
        current_call.hangup()
    except pjsua.Error, e:
        pass #print "Exception: "+ str(e)


if __name__ == "__main__":
    current_call=None
    ph=Phone(5080)     
    ph.register("127.0.0.1:5060","blaine")
    ph.printstatus()
    current_call=ph.call("1000")
    while raw_input('press q to quit')!='q':
        pass
    end_call()
    #del current_call
    ph.destroy()



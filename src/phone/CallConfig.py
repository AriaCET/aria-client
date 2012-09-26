from pjsua import CallCallback ,CallState
from pjsua import Error as pjsuaException
from pjsua import Lib ,MediaState
from cmdlinefunctions import debugMessage
class PhoneCallCallback(CallCallback):
    """
    Class to receive event notification from Call objects. 
    """
    def __init__(self,msgfn,stfn, call=None):
        CallCallback.__init__(self, call)
        self.msgfn = msgfn
        self.statefn = stfn

    # Notification when call state has changed
    def on_state(self):
        """
        Called when state of a 'call' changed
        """
        debugMessage ("Call with"+ str(self.call.info().remote_uri)+"is ")
        self.msgfn (str(self.call.info().state_text))
        debugMessage ("last code ="+ str(self.call.info().last_code)) 
        if self.call.info().state == CallState.DISCONNECTED:
            self.statefn(0)
            try:
                 self.call.hangup()
            except pjsuaException, e:
                debugMessage ("Exception: "+ str(e))
            
    # Notification when call's media state has changed.
    def on_media_state(self):
        """
        set function to be called when the call is ready
        (media is active)
        """
        if self.call.info().media_state == MediaState.ACTIVE:
            # Connect the call to sound device
            call_slot = self.call.info().conf_slot
            Lib.instance().conf_connect(call_slot, 0)
            Lib.instance().conf_connect(0, call_slot)
            debugMessage ("Media is now active")
        else:
            debugMessage ("Media is inactive")


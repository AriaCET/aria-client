from pjsua import AccountCallback
import threading

class PhoneAccountCallback(AccountCallback):
    """
    Class that Set Account setting :
        on_incoming_call:-reject
    """
    sem = None
    def __init__(self, account):
        AccountCallback.__init__(self, account)

    def wait(self):
        self.sem = threading.Semaphore(0)
        self.sem.acquire()

    def on_reg_state(self):
        if self.sem:
            if self.account.info().reg_status >= 200:
                self.sem.release()

    def on_incoming_call(self, call):
        call.hangup(501, "Sorry, not ready to accept calls yet")


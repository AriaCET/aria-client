"""
Functions used by Phone for general Cmd line message
"""
def debugMessage(message):
    """
    for debuging
    TODO: print messages to a log file
    """
    print (str(message))

def end_call(current_call):
    """
    To end a call 
    """
    try:
        current_call.hangup()
    except pjsua.Error, e:
        pass #debugMessage "Exception: "+ str(e)

def statechange(t):
    if t==0:
        current_call = None
    debugMessage ('Current call is'+str(current_call))

def getCallStatus(call):
    try:
        callInfo = call.info()
        debugMessage (callInfo.state_text)
        return callInfo.state
    except pjsua.Error, e:
        debugMessage ("NULL")
        return 0

from phone import * 
import time
if __name__ == "__main__":
    current_call=None
    ph=Phone(5070)     
    ph.register("127.0.0.1:5060","blaine")
    ph.printstatus(debugMessage)
    current_call=ph.call("1000")
#    while ():
#	time.sleep(1)
    while getCallStatus(current_call) == 5 and raw_input('press q to quit')!='q':
        pass
    end_call(current_call)
    #del current_call
    ph.destroy()


"""
A simple example of hooking the keyboard on Linux using pyxhook

Any key pressed prints out the keys values, program terminates when spacebar is pressed
"""

#Libraries we need
import pythoncom
import pyHook
import time
import pyperclip
import socket
import traceback
import threading
import time

ctrl_press = 0


class copy_server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print "server init"

    def run(self):
        host = ''
        port = 10086

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))

        while 1:
            try:
                message, addr = s.recvfrom(8192)
                pyperclip.copy(message)
            except:
                traceback.print_exc()


class send_copy_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        v = pyperclip.paste();
        if v != None and v != "":
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("10.9.3.245", 10086))
                s.sendall(v.encode("utf-8"))
                s.close();
            except:
                traceback.print_exc()    
				
def send_copy():
    v = pyperclip.paste();
        if v != None and v != "":
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("10.9.3.245", 10086))
            s.sendall(v.encode("utf-8"))
            s.close();
        except:
            traceback.print_exc()  
    return

def key_all_event(event):
    global ctrl_press
    if (event.MessageName == "key down"):
        if event.ScanCode == 29:
            ctrl_press = 1
    if (event.MessageName == "key up"):
        if event.ScanCode == 29:
            ctrl_press = 0
        if event.ScanCode == 46:
            if ctrl_press == 1:
                send_copy();
    return True
        
        
if __name__ == '__main__':
    ctrl_press = 0
    serv = copy_server()
    serv.start()
    
    print "key listening"
    #Create hookmanager
    hookman = pyHook.HookManager()
    #Define our callback to fire when a key is pressed down
    #hookman.KeyDown = key_down_event
    hookman.KeyAll = key_all_event
    #Hook the keyboard
    hookman.HookKeyboard()
    #Start our listener
    pythoncom.PumpMessages()

    #Create a loop to keep the application running
    running = True
    while running:
        time.sleep(0.1)

    #Close the listener when we are done
    hookman.cancel()

#!/usr/bin/python
"""
A simple example of hooking the keyboard on Linux using pyxhook

Any key pressed prints out the keys values, program terminates when spacebar is pressed
"""

#Libraries we need
import pyxhook
import time
import pyperclip
import socket
import traceback
import threading

ctrl_press = 0


class copy_server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print "server run"
        host = ''
        port = 10086

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))

        while 1:
            try:
                message, addr = s.recvfrom(81920)
                pyperclip.copy(str(message))
            except:
                traceback.print_exc()



def send_copy():
    v = pyperclip.paste();
    if v != None and v != "":
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("10.9.3.244", 10086))
            s.sendall(v.decode("utf-8").encode("gbk"))
            s.close();
        except:
            traceback.print_exc()

#This function is called every time a key is presssed
def kbevent( event ):
    global ctrl_press
    if event.ScanCode == 37:
        ctrl_press = 1
    if event.ScanCode == 54:
        if ctrl_press == 1:
            send_copy()

def key_up_event( event ):
    global ctrl_press
    if event.ScanCode == 37:
        ctrl_press = 0

if __name__ == '__main__':
    ctrl_press = 0
    serv = copy_server()
    serv.start()


    print "keyboard listening"
    #Create hookmanager
    hookman = pyxhook.HookManager()
    #Define our callback to fire when a key is pressed down
    hookman.KeyDown = kbevent
    hookman.KeyUp = key_up_event
    #Hook the keyboard
    hookman.HookKeyboard()
    #Start our listener
    hookman.start()

    #Create a loop to keep the application running
    running = True
    while running:
        time.sleep(0.1)

    #Close the listener when we are done
    hookman.cancel()

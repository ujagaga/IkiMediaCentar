#!/usr/bin/env python3

'''
This script is intended to output the current IP address to the LCD display.
'''
import socket
import time
import os
import subprocess


LastIP = ""
logFile = "/tmp/display"


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


while True:
    # Check IP address
    ipAddr = ""
    if os.path.isfile(logFile):
        # Only do this if the display is initialized. Otherwise we may be going for a shutdown.
        ipAddr = get_ip()
        if ipAddr != LastIP:
            LastIP = ipAddr

            file = open(logFile, 'w')
            file.write(LastIP)
            file.close()
    else:
        LastIP = ""
   

    time.sleep(5)

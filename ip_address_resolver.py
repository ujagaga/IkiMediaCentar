#!/usr/bin/env python3

import socket
import time

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
    ipAddr = get_ip()
    if ipAddr != LastIP:
        LastIP = ipAddr
        file = open(logFile, 'w')
        file.write(LastIP)
        file.close()

    time.sleep(5)
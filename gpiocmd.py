#!/usr/bin/env python3

'''
Orange PI GPIO module
sudo apt install python3-dev
pip3 install OrangePi.GPIO
'''

import OPi.GPIO as GPIO
import time
import subprocess
import os

BTN_NEXT = 22
BTN_PREV = 8
BTN_PAUSE = 18
LED_PIN = 7

btn_timestamp = 0
led_timestamp = 0
play_active = False
get_current_timestamp = 0


def run_process(command_list):
    result = subprocess.run(command_list, stdout=subprocess.PIPE)
    #print("Running: {}".format(command_list))
    return [str(result.stdout, 'utf-8'), result.returncode]


def setup():
    GPIO.setboard(GPIO.ZERO)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BTN_NEXT, GPIO.IN,
               pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BTN_PREV, GPIO.IN,
               pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BTN_PAUSE, GPIO.IN,
               pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LED_PIN, GPIO.OUT) 
    GPIO.output(LED_PIN, 1) 


def get_current():
    global play_active
    global get_current_timestamp

    get_current_timestamp = time.time()
    current = 0
    total = 1
    cmd = ['mpc']
    status = run_process(cmd)[0].split('\n')

    try:
        play_active = False
        for i in range(0, len(status)):
            if '[playing]' in status[i]:
                data = status[i].split('#')[1].split(' ')[0].split('/')
                current = int(data[0])
                total = int(data[1])
                play_active = True  

    except Exception as e:
        print('get_current() ERROR:', e)

    return current, total


def next_station():
    current, total = get_current()
    current += 1
    if current > total:
        current = 1

    cmd = ['mpc', 'play', str(current)]
    result = run_process(cmd)[1]
    
    if result != 0:
        # Try one more time
        current += 1
        if current > total:
            current = 1
        cmd = ['mpc', 'play', str(current)]
        run_process(cmd)


def previous_station():
    current, total = get_current()
    current -= 1
    if current < 1:
        current = total

    cmd = ['mpc', 'play', str(current)]
    result = run_process(cmd)[1]
    
    if result != 0:
        # Try one more time
        current -= 1
        if current < 1:
            current = total
        cmd = ['mpc', 'play', str(current)]
        run_process(cmd)


def stop_mpc():
    cmd = ['mpc', 'stop']
    run_process(cmd)


def play_mpc():
    cmd = ['mpc', 'play']
    run_process(cmd)


def play_mpc_number(number):
    cmd = ['mpc', 'play', str(number)]
    run_process(cmd)


def tgl_mpc():
    global play_active

    current, total = get_current()

    if current == 0:
        play_mpc()
        play_active = True
    else:
        stop_mpc()
        play_active = False


setup()
time.sleep(10)
get_current()

try:
    while True:
        if not GPIO.input(BTN_NEXT):
            btn_timestamp = time.time()

            longPressFlag = False
            while not GPIO.input(BTN_NEXT):
                time.sleep(0.1)
                if time.time() - btn_timestamp > 2:
                    # Long press. Play last.
                    longPressFlag = True
                    play_mpc_number(1)
                    time.sleep(0.1)
                    previous_station()
                    while not GPIO.input(BTN_NEXT):
                        pass

            if not longPressFlag:
                # Short press
                next_station()

        elif not GPIO.input(BTN_PREV):
            btn_timestamp = time.time()

            longPressFlag = False
            while not GPIO.input(BTN_PREV):
                time.sleep(0.1)
                if time.time() - btn_timestamp > 2:
                    # Long press. Play first.
                    longPressFlag = True
                    play_mpc_number(1)
                    while not GPIO.input(BTN_NEXT):
                        pass

            if not longPressFlag:
                # Short press
                previous_station()

        elif not GPIO.input(BTN_PAUSE):
            btn_timestamp = time.time()

            while not GPIO.input(BTN_PAUSE):
                time.sleep(0.1)
                if time.time() - btn_timestamp > 3:
                    # Long press.Shutdown. Remove the display file so the LCD will go blank.
                    try:
                        os.remove("/tmp/display")
                        time.sleep(3.5)
                    except:
                        pass
                    GPIO.output(LED_PIN, 0) 

                    cmd = ['/usr/sbin/poweroff']
                    run_process(cmd)
                    exit(0)


            # Short press
            tgl_mpc()

        if play_active:
            if (time.time() - led_timestamp) > 2:
                GPIO.output(LED_PIN, 0) 
                led_timestamp = time.time();
            elif (time.time() - led_timestamp) > 1:
                GPIO.output(LED_PIN, 1) 
        else:
            GPIO.output(LED_PIN, 1) 

        if (time.time() - get_current_timestamp) > 2:
            get_current()
        
        time.sleep(0.1)

finally:                        # this block will run no matter how the try block exits
    GPIO.cleanup()              # clean up after yourself


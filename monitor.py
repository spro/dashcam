#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import subprocess
import os

cmd='python3 /home/map7/code/dashcam/dashcam.py'

GPIO.setwarnings(False) # Ignore warning for now

GPIO.setmode(GPIO.BCM) # BCM is the GPIO PINS
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button Start Recording
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button Shutdown
GPIO.setup(19, GPIO.OUT)        # LED

state=0
proc=""

while True:

    shutdown_state=GPIO.input(5)

    if (shutdown_state == False):
        print("SHUTDOWN")
        os.system("sudo shutdown -h now")
        time.sleep(1)
    
    input_state=GPIO.input(13)
    
    if (state == 0 and input_state == False):
        print('Button Pressed')
        print("Starting ", cmd)
        # os.system(cmd)
        proc = subprocess.Popen(cmd,shell=True)
        print("PID: ", proc.pid)
        GPIO.output(19, GPIO.HIGH)
        state = 1
        time.sleep(1)
        
    elif (state == 1 and input_state == False):
        GPIO.output(19, GPIO.LOW)
        state = 0
        print("KILL PID: ", proc.pid)
        #cmd="kill " + str(proc.pid)
        #print(cmd)
        #os.system(cmd)
        os.system("pkill -f dashcam")
        time.sleep(1)

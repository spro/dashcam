#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import subprocess
import os

# Command to run dashcam script
script_dir = os.path.dirname(os.path.abspath(__file__))
cmd = f"python3 {script_dir}/dashcam.py"

# Pin definitions
RECORD_BUTTON_PIN = 33
SHUTDOWN_BUTTON_PIN = 29
STATUS_LED_PIN = 35

GPIO.setwarnings(False)  # Ignore warning for now

GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
GPIO.setup(
    RECORD_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP
)  # Button Start Recording
GPIO.setup(SHUTDOWN_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button Shutdown
GPIO.setup(STATUS_LED_PIN, GPIO.OUT)  # LED

state = 0
proc = ""

while True:
    shutdown_state = GPIO.input(SHUTDOWN_BUTTON_PIN)

    if shutdown_state == False:
        print("SHUTDOWN")
        os.system("sudo shutdown -h now")
        time.sleep(1)

    input_state = GPIO.input(RECORD_BUTTON_PIN)

    if state == 0 and input_state == False:
        print("Button Pressed")
        print("Starting ", cmd)
        # os.system(cmd)
        proc = subprocess.Popen(cmd, shell=True)
        print("PID: ", proc.pid)
        GPIO.output(STATUS_LED_PIN, GPIO.HIGH)
        state = 1
        time.sleep(1)

    elif state == 1 and input_state == False:
        GPIO.output(STATUS_LED_PIN, GPIO.LOW)
        state = 0
        print("KILL PID: ", proc.pid)
        # cmd="kill " + str(proc.pid)
        # print(cmd)
        # os.system(cmd)
        os.system("sudo pkill -f dashcam.py")
        time.sleep(1)

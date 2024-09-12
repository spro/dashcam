#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # BCM is the GPIO PINS
GPIO.setup(19, GPIO.OUT)

while(1):
    GPIO.output(19, GPIO.LOW)
    time.sleep(1)
    GPIO.output(19, GPIO.HIGH)
    time.sleep(1)

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for using adafruit_motorkit with a stepper motor"""
import time
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import motor

kit = MotorKit()

kit.motor3.throttle = 0.0
kit.motor4.throttle = 0.0


while True:
    usrInput = input("Enter a throttle position from 0-100% or ctrl-c to exit: ")
    throttle = float(usrInput) / 100.0
    throttle = min(1.0, throttle)
    throttle = max(-1.0, throttle)
    print(f'Throttle at {throttle}')
    kit.motor3.throttle = throttle
    kit.motor4.throttle = throttle

#time.sleep(timeStep)


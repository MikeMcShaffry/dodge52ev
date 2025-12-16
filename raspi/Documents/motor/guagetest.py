# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for using adafruit_motorkit with a stepper motor"""
import time
import math
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import motor


PON_MIN_POSITION = 0.60
PON_MAX_POSITION = 0.9

B3B_MIN_POSITION = 0.60
B3B_MAX_POSITION = 0.9

kit = MotorKit()
kit.motor3.throttle = 0.0
kit.motor4.throttle = 0.0

beginTime = time.time()
now = time.time()
finishTime = beginTime + 60

while now < finishTime:
    runTime = now - beginTime
    throttle3 = PON_MIN_POSITION + ( (PON_MAX_POSITION - PON_MIN_POSITION) * 0.5 * (1.0 + math.sin(runTime)) )
    kit.motor3.throttle = throttle3

    throttle4 = B3B_MIN_POSITION + ( (B3B_MAX_POSITION - B3B_MIN_POSITION) * 0.5 * (1.0 + math.sin(runTime*2.0)) )
    kit.motor4.throttle = throttle4
    now = time.time()
    print(f'Throttle3 = {throttle3}    Throttle4 = {throttle4}', end="\r")

kit.motor3.throttle = 0.0

#time.sleep(timeStep)


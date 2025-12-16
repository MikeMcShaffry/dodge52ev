# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for using adafruit_motorkit with a stepper motor"""
import time
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

mystyle = stepper.SINGLE
kit = MotorKit(i2c=board.I2C())
timeStep = 0.02
loops = 5
distance = 200

for j in range(loops):
   for i in range(distance):
       kit.stepper1.onestep(style=mystyle)
       #kit.stepper1.release();
       time.sleep(timeStep)

   for i in range(distance):
       kit.stepper1.onestep(direction=stepper.BACKWARD, style=mystyle)
       #kit.stepper1.release();
       time.sleep(timeStep)

kit.stepper1.release();

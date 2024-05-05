# SSH

* Don't be on the VPN
* ssh 192.168.1.102
* PWD ST 



# Start Up Notes for the Motor Bonnet

Tried
sudo pip3 install adafruit-blinka

but got "This environment is externally managed" error

Then
sudo pip3 install adafruit-blinka --break-system-packages
sudo pip3 install adafruit-circuitpython-motorkit --break-system-packages

```
dtparam=i2c_arm=on
```

```
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
```

# Setup Notes for the PICAN2

Follwed instructions here: https://copperhilltech.com/blog/pican2-pican3-and-picanm-driver-installation-for-raspberry-pi/

Added this to /boot/config.txt

```
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25
dtoverlay=spi-bcm2835-overlay 
```

Then
```
sudo reboot
sudo /sbin/ip link set can0 up type can bitrate 500000                    <<< no errors!
sudo apt-get install can-utils

cansend can0 7DF#0201050000000000                                         <<< no errors

sudo pip3 install python-can --break-system-packages


```

Try putting this in /etc/network/interfaces

```
auto can0
iface can0 inet manual
   pre-up /sbin/ip link set can0 type can bitrate 500000 triple-sampling on
   up /sbin/ifconfig can0 up
   down /sbin/ifconfig can0 down
```
   
Now I can see can0 on ifconfig...
But no data.

Then I saw that post on soldering the jumpers on the PiCAN. NOW I SEE DATA!

But, I couldn't import the data into SavvyCan until I ran candump with the -t 



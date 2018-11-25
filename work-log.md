# Work Log
This document describes how I created the project.

## Hardware

### Parts
* Raspberry Pi Zero W
* CSN-A2 Thermal Printer
* Rotary encoder + button
* Seven segment display with I<sup>2</sup>C backpack

### Setup
#### CSN-A2 Thermal Printer
Connect the RXD pin on the printer to the TXD pin on the Raspberry Pi. Connect the TXD pin on the printer to the RXD pin on the Raspberry Pi.

#### Setting up the rotary encoder
Connect the channel A and B pins on the rotary encoder to any available GPIO pin on the Raspberry Pi and make note of the pin numbers. Then add the following to /boot/config.txt:

> dtoverlay=rotary-encoder,pin_a=23,pin_b=24,relative_axis=1

#### Setting up the button
Connect the 

> dtoverlay=gpio-key,gpio=16,keycode=28,label=KEY_ENTER

## Software
Raspbian

Python
* evdev
* pillow
* python-escpos

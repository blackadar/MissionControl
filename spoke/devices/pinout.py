"""
Defines physical devices connected to the running computer.
This file should be modified as needed to enable interaction with available devices.
"""

# Connect an LED to Pin 14 and to Ground.
from spoke.devices.led import led
led_14 = led(14)

# Connect a Unicorn pHAT to Pi Zero header.
from spoke.devices.hat import hat

pi_hat = hat()

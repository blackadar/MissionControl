"""
Functions to control a physical LED attached to a Raspberry Pi
"""
try:
    from gpiozero import LED
except:
    print("Running on incompatible platform!")


class led:

    def __init__(self, pin: int):
        try:
            self.led = LED(pin)
        except NameError:
            print("Couldn't initialize an LED...")
        self.tasked = False

    def set_pin(self, pin):
        self.led = LED(pin)

    def on(self):
        self.led.on()

    def off(self):
        self.led.off()

    def is_on(self):
        return self.led.is_active

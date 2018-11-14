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
            self.led = simulationLED(pin)
        self.tasked = False

    def set_pin(self, pin):
        self.led = LED(pin)

    def on(self):
        self.led.on()

    def off(self):
        self.led.off()

    def is_on(self):
        return self.led.is_active


class simulationLED:

    def __init__(self, pin):
        self.pin = pin
        self.is_on = False

    def on(self):
        print("ON")
        self.is_on = True

    def off(self):
        print("OFF")
        self.is_on = False

    def is_active(self):
        return self.is_on

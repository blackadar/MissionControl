"""
Blink a device with an encoded message
"""

from spoke.devices import led

device = led.led(14)


def do(client, text):
    text = text[0].lower()
    if text == "true":
        device.on()
        client.okay(client)
    elif text == "false":
        device.off()
        client.okay(client)
    else:
        client.error(client)


def discover():
    return 'boolean'


def status():
    if device.is_on():
        return "ON"
    else:
        return "OFF"

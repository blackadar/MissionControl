"""
Blink a device with an encoded message
"""

from spoke.devices.pinout import led_14

device = led_14


def do(client, text):
    text = text[0].lower()
    if text == "true":
        if not device.tasked:
            device.on()
            client.okay(client)
        else:
            client.error(client)
            client.tell(client, "Device or resource is in use.")
    elif text == "false":
        if not device.tasked:
            device.off()
            client.okay(client)
        else:
            client.error(client)
            client.tell(client, "Device or resource is in use.")
    else:
        client.error(client)
        client.tell(client, "Invalid option '" + text + "'.")


def discover():
    return 'boolean'


def status():
    if device.is_on():
        return "ON"
    else:
        return "OFF"

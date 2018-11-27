"""
Control a simple LED
"""

from spoke.devices.pinout import pi_led_15

device = pi_led_15


def do(client, text):
    text = text[0].lower()
    if text == "on":
        if not device.tasked:
            device.on()
            client.okay(client)
        else:
            client.error(client)
            client.tell(client, "Device or resource is in use.")
    elif text == "off":
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
    return 'on, off'


def status():
    if device.is_on():
        return "ON"
    else:
        return "OFF"

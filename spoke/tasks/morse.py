"""
Blink a device with an encoded message
"""
from time import sleep

from spoke.devices.pinout import pi_led

led = pi_led
time_unit = 0.25  # Seconds for a 'dot'


def do(client, text):
    if led is None:
        client.error(client)
        client.tell(client, "Device or resource is not available.")
        return
    build = ""
    for word in text:
        build = build + encode(word)
    if not led.tasked:
        client.okay(client)
        led.tasked = True
        perform(build, led)
        led.tasked = False
    else:
        client.error(client)
        client.tell(client, "Device or resource is in use.")
    # print(client.addrport() + ": " + build)


def discover():
    return 'text'


def status():
    if led is None:
        return "UNAVAILABLE"
    if led.tasked:
        return "DEVICE BUSY"
    else:
        return "READY"


def encode(word):
    word = word.upper()
    build = ""
    for c in word:
        switcher = {
            'A': ".- ",
            'B': "-... ",
            'C': "-.-. ",
            'D': "-.. ",
            'E': ". ",
            'F': "..-. ",
            'G': "--. ",
            'H': ".... ",
            'I': ".. ",
            'J': ".--- ",
            'K': "-.- ",
            'L': ".-.. ",
            'M': "-- ",
            'N': "-. ",
            'O': "--- ",
            'P': ".--. ",
            'Q': "--.- ",
            'R': ".-. ",
            'S': "... ",
            'T': "- ",
            'U': "..- ",
            'V': "...- ",
            'W': ".-- ",
            'X': "-..- ",
            'Y': "-.-- ",
            'Z': "--.. ",
            '1': ".---- ",
            '2': "..--- ",
            '3': "...-- ",
            '4': "....- ",
            '5': "..... ",
            '6': "-.... ",
            '7': "--... ",
            '8': "---.. ",
            '9': "----. ",
            '0': "----- ",
            '.': ".-.-.-\n",
            '!': "-.-.--\n",
            '?': "..--..\n",
            ',': "--..-- ",
            ' ': "/",
        }
        char = switcher.get(c, "")
        if char is not None:
            build = build + char
    # build = build + ".-.-."
    return build


def perform(encoded_phrase: str, dev):
    for c in encoded_phrase:
        switch = {
            '.': dot,
            '-': dash,
            ' ': letter,
            '/': word
        }
        fun = switch.get(c)
        fun(dev)


def dot(dev):
    dev.on()
    sleep(time_unit * 1)
    dev.off()
    sleep(time_unit * 1)


def dash(dev):
    dev.on()
    sleep(time_unit * 3)
    dev.off()
    sleep(time_unit * 1)


def letter(dev):
    # dev.off()
    sleep(time_unit * 3)


def word(dev):
    # dev.off()
    sleep(time_unit * 7)

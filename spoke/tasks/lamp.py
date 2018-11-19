"""
Control a Unicorn pHAT 'Light Bulb'
"""

from spoke.devices.pinout import pi_hat

hat = pi_hat


def do(client, text):
    if hat is None:
        client.error(client)
        client.tell(client, "Device or resource is not available.")
        return
    if len(text) < 1:
        client.error(client)
        client.tell(client, "No arguments received.")
    else:
        target = str(text[0]).lower()
        if target == 'clear':
            hat.loop = False
            client.okay(client)
        elif target == 'on':
            if not check_tasked(client):
                hat.tasked = True
                hat.on()
                hat.tasked = False
                client.okay(client)
        elif target == 'off':
            if not check_tasked(client):
                hat.tasked = True
                hat.off()
                hat.tasked = False
                client.okay(client)
        elif target == 'mood':
            if not check_tasked(client):
                hat.mood()
                client.okay(client)
        elif target == 'pulse':
            if not check_tasked(client):
                if len(text) > 1:
                    try:
                        times = int(text[1])
                    except ValueError:
                        client.tell(client("Invalid parameter. Using default."))
                        times = 1
                else:
                    times = 1
                hat.tasked = True
                hat.pulse(times)
                hat.tasked = False
                client.okay(client)
        elif target == 'rainbow':
            if not check_tasked(client):
                hat.rainbow()
                client.okay(client)
        elif target == 'blink':
            if not check_tasked(client):
                if len(text) < 2:
                    client.error(client)
                    client.tell(client, "Blink requires a frequency argument.")
                else:
                    try:
                        freq = int(text[1])
                    except ValueError:
                        client.tell(client("Invalid parameter. Using default."))
                        freq = 1
                    hat.blink(freq)
                    client.okay(client)
        elif target == 'color':
            if not check_tasked(client):
                if len(text) < 4:
                    client.error(client)
                    client.tell(client, "Color requires 3 integers for R(ed), (G)reen, (B)lue.")
                else:
                    try:
                        red = int(text[1])
                        green = int(text[2])
                        blue = int(text[3])
                    except ValueError:
                        client.error(client)
                        client.tell(client, "Color requires 3 integers for R(ed), (G)reen, (B)lue.")
                        return
                    hat.color(red, green, blue)
                    client.okay(client)
        elif target == 'dim':
            if len(text) < 2:
                client.error(client)
                client.tell(client, "Dim requires a float intensity 0.0 - 1.0.")
            else:
                try:
                    level = float(text[1])
                except ValueError:
                    client.error(client)
                    client.tell(client, "Dim requires a float intensity 0.0 - 1.0.")
                    return
                hat.dim(level)
                client.okay(client)
        else:
            client.error(client)
            client.tell(client, "Light does not support '" + target + "'.")


def check_tasked(client):
    if hat.tasked:
        client.error(client)
        client.tell(client, "Device or resource is in use.")
        return True
    else:
        return False


def discover():
    return 'blink, pulse, dim, on, off, color, mood, rainbow, clear'


def status():
    if hat is None:
        return "UNAVAILABLE"
    return ("R: " + str(hat.red) +
            ", G: " + str(hat.green) +
            ", B: " + str(hat.blue) +
            ", BRIGHT: " + str(hat.brightness))

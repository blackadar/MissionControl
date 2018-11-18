"""
Controls a Pi Zero 'Unicorn' Hat
"""
import colorsys
import math
import threading
import time
from random import randint

import unicornhat as uh


class hat:

    def __init__(self):
        uh.set_layout(uh.PHAT)
        uh.brightness(1.0)

        self.tasked = False
        self.loop = False
        self.min_val = 43  # The hat seems to ignore values <= this
        self.min_bright = 0.25
        self.red = self.min_val
        self.green = self.min_val
        self.blue = self.min_val
        self.brightness = 1.0

    def rainbow(self):
        spacing = 360.0 / 16.0

        def worker():
            self.loop = True
            self.tasked = True
            while self.loop:
                hue = int(time.time() * 100) % 360
                for x in range(8):
                    offset = x * spacing
                    h = ((hue + offset) % 360) / 360.0
                    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
                    for y in range(4):
                        uh.set_pixel(x, y, r, g, b)
                uh.show()
                time.sleep(0.05)
            self.tasked = False
            self.color(self.red, self.green, self.blue)

        thread = threading.Thread(target=worker)
        thread.start()

    def mood(self):
        def worker():
            self.loop = True
            self.tasked = True
            while self.loop:
                wait = randint(2, 20)
                length = randint(1, 6)
                red = randint(100, 255)
                green = randint(100, 255)
                blue = randint(0, 255)
                self.color(red, green, blue, write=False, length=length)
                time.sleep(wait)
            self.color(self.red, self.green, self.blue)
            self.tasked = False

        thread = threading.Thread(target=worker)
        thread.start()

    def color(self, red, green, blue, write=True, length=1):
        distance = 255
        resolution = 60
        max_movement = round(distance / resolution)

        if red < self.min_val:
            red = self.min_val
        if green < self.min_val:
            green = self.min_val
        if blue < self.min_val:
            blue = self.min_val

        if write:
            self.red = red
            self.green = green
            self.blue = blue

        grid = uh.get_pixels()
        max_distance = 1
        for y in grid:
            for x in y:
                r_dist = abs(x[0] - red)
                g_dist = abs(x[1] - green)
                b_dist = abs(x[2] - blue)

                if r_dist > max_distance:
                    max_distance = r_dist
                if g_dist > max_distance:
                    max_distance = g_dist
                if b_dist > max_distance:
                    max_distance = b_dist

        steps = [[[math.ceil((abs(x[0] - red) / max_distance) * max_movement),
                   math.ceil((abs(x[1] - green) / max_distance) * max_movement),
                   math.ceil((abs(x[2] - blue) / max_distance) * max_movement)] for x in y] for y in grid]

        self.tasked = True
        loop = True

        while loop:
            work = False
            for x in range(8):
                for y in range(4):
                    r, g, b = uh.get_pixel(x, y)
                    red_step = steps[y][x][0]
                    red_dist = abs(red - r)
                    green_step = steps[y][x][1]
                    green_dist = abs(green - g)
                    blue_step = steps[y][x][2]
                    blue_dist = abs(blue - b)

                    if red_dist < red_step:
                        r = red
                    elif r < red:
                        r = r + red_step
                        work = True
                    elif r > red:
                        r = r - red_step
                        work = True

                    if green_dist < green_step:
                        g = green
                    elif g < green:
                        g = g + green_step
                        work = True
                    elif g > green:
                        g = g - green_step
                        work = True

                    if blue_dist < blue_step:
                        b = blue
                    elif b < blue:
                        b = b + blue_step
                        work = True
                    elif b > blue:
                        b = b - blue_step
                        work = True

                    uh.set_pixel(x, y, r, g, b)
            if not work:
                loop = False
            uh.show()
            time.sleep(length / resolution)
        self.tasked = False

    def on(self):
        if self.red == self.min_val and self.green == self.min_val and self.blue == self.min_val:
            self.red = 255
            self.green = 255
            self.blue = 255
        self.color(self.red, self.green, self.blue, write=False)

    def off(self):
        self.color(0, 0, 0, write=False)

    def dim(self, brightness):
        step = 0.01

        if brightness < self.min_bright:
            brightness = self.min_bright

        def worker():
            work = True
            while work:
                if abs(brightness - self.brightness) < step:
                    self.brightness = brightness
                    work = False
                elif self.brightness < brightness:
                    self.brightness = self.brightness + step
                elif self.brightness > brightness:
                    self.brightness = self.brightness - step
                uh.brightness(self.brightness)
                uh.show()
                time.sleep(.01)

        thread = threading.Thread(target=worker)
        thread.start()

    def pulse(self, times=1):
        r_dist = 255 - self.red
        g_dist = 255 - self.green
        b_dist = 255 - self.blue
        pulse_dist = min(r_dist, g_dist, b_dist, 50)
        if pulse_dist < 50:
            pulse_dist = -50
        for x in range(times):
            self.color(self.red + pulse_dist, self.green + pulse_dist, self.blue + pulse_dist, write=False)
            time.sleep(0.1)
            self.color(self.red, self.green, self.blue)

    def blink(self, rate, red=-1, green=-1, blue=-1):
        if red == -1:
            red = self.red
        if green == -1:
            green = self.green
        if blue == -1:
            blue = self.blue

        def worker():
            self.loop = True
            self.tasked = True
            while self.loop:
                self.off()
                time.sleep(rate)
                self.color(red, green, blue, write=False)
            self.color(self.red, self.green, self.blue)
            self.tasked = False

        thread = threading.Thread(target=worker)
        thread.start()

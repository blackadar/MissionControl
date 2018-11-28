import telnetlib as tl
import threading
import time
import tkinter as tk
from tkinter import *
from tkinter.colorchooser import *


class Application(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.e = Entry()
        self.clear = Button(text='Clear the light', state=DISABLED, command=self.clear_light)
        self.clear.place(x=280, y=180)
        self.rainbow = Button(text='Rainbow', state=NORMAL, command=self.send_rainbow)
        self.rainbow.place(x=170, y=180)
        self.blink = Button(text='Blink the Light', state=NORMAL, command=self.send_blink)
        self.blink.place(x=345, y=135)
        self.pulse = Button(text='Send a Pulse', state=NORMAL, command=self.send_pulse)
        self.pulse.place(x=220, y=135)
        self.color = Button(text='Select Color', state=NORMAL, command=self.get_color)
        self.color.place(x=100, y=135)
        self.lights = Button(text='Turn light on or off', state=NORMAL, command=self.light_status)
        self.lights.place(x=205, y=60)
        self.zero_indicator = canvas.create_oval(68, 42, 78, 52, fill='red')
        self.orion_indicator = canvas.create_oval(310, 42, 320, 52, fill='red')
        canvas.pack()
        self.v = IntVar()
        self.v.set(2)
        self.light_zero = False
        self.light_orion = False
        self.master = master
        self.place()
        self.reception = tl.Telnet('10.8.0.1', 9090, timeout=5)
        self.reception.write('tell zero light clear\n'.encode('ascii'))
        time.sleep(1.5)
        self.reception.write('tell network light off\n'.encode('ascii'))
        self.run = True
        self.widgets(master)
        self.reader = threading.Thread(target=self.read)
        self.reader.start()

    def read(self):
        while self.run:
            try:
                out = str(self.reception.read_very_eager())
            except EOFError:
                return
            if out != "b''":
                print(out)
            time.sleep(1)
        return

    def widgets(self, master):
        Label(master, text='Welcome to Mission Control').place(x=185, y=10)
        counter = 160
        for vector, val in BRANCHES:
            Radiobutton(root, text=vector, variable=self.v, value=val).place(x=counter, y=35)
            counter = counter + 80
        Label(text='Morse Code: ').place(x=100, y=100)
        self.e.place(x=199, y=100)
        Button(text='Submit Morse', command=self.morse_code).place(x=345, y=95)

    def light_status(self):
        command = ''
        if self.v.get() == 1:
            if self.light_zero:
                command = 'tell zero light off\n'
                self.light_zero = False
                canvas.itemconfig(self.zero_indicator, fill='red')
            elif not self.light_zero:
                command = 'tell zero light on\n'
                canvas.itemconfig(self.zero_indicator, fill='lime green')
                self.light_zero = True
        if self.v.get() == 2:
            if self.light_zero and self.light_orion:
                command = 'tell network light off\n'
                canvas.itemconfig(self.orion_indicator, fill='red')
                canvas.itemconfig(self.zero_indicator, fill='red')
                self.light_orion = False
                self.light_zero = False
            elif (not self.light_zero) and (not self.light_orion):
                command = 'tell network light on\n'
                canvas.itemconfig(self.orion_indicator, fill='lime green')
                canvas.itemconfig(self.zero_indicator, fill='lime green')
                self.light_orion = True
                self.light_zero = True
            else:
                if self.light_orion:
                    command = 'tell orion light off\n'
                    canvas.itemconfig(self.orion_indicator, fill='red')
                    self.light_orion = False
                else:
                    command = 'tell orion light on\n'
                    canvas.itemconfig(self.orion_indicator, fill='lime green')
                    self.light_orion = True

                if self.light_zero:
                    command = command + 'tell zero light off\n'
                    canvas.itemconfig(self.zero_indicator, fill='red')
                    self.light_zero = False
                else:
                    command = command + 'tell zero light on\n'
                    canvas.itemconfig(self.zero_indicator, fill='lime green')
                    self.light_zero = True
        if self.v.get() == 3:
            if self.light_orion:
                command = 'tell orion light off\n'
                canvas.itemconfig(self.orion_indicator, fill='red')
                self.light_orion = False
            elif not self.light_orion:
                command = 'tell orion light on\n'
                canvas.itemconfig(self.orion_indicator, fill='lime green')
                self.light_orion = True
        self.reception.write(command.encode('ascii'))
        self.refresh()

    def morse_code(self):
        command = 'tell orion morse ' + self.e.get() + '\n'
        self.reception.write(command.encode('ascii'))

    def get_color(self):
        color = askcolor()
        red, green, blue = [int(i) for i in color[0]]
        command = 'tell zero lamp color ' + str(red) + ' ' + str(green) + ' ' + str(blue) + '\n'
        canvas.itemconfig(self.zero_indicator, fill='lime green')
        self.reception.write(command.encode('ascii'))

    def send_pulse(self):
        self.light_zero = True
        command = 'tell zero lamp pulse\n'
        canvas.itemconfig(self.zero_indicator, fill='lime green')
        self.reception.write(command.encode('ascii'))

    def send_blink(self):
        command = 'tell zero lamp blink 1\n'
        self.reception.write(command.encode('ascii'))
        canvas.itemconfig(self.zero_indicator, fill='lime green')
        self.color.config(state='disabled')
        self.rainbow.config(state='disabled')
        self.blink.config(state='disabled')
        self.pulse.config(state='disabled')
        self.clear.config(state='normal')
        self.refresh()

    def send_rainbow(self):
        command = 'tell zero lamp rainbow\n'
        self.reception.write(command.encode('ascii'))
        canvas.itemconfig(self.zero_indicator, fill='lime green')
        self.color.config(state='disabled')
        self.rainbow.config(state='disabled')
        self.blink.config(state='disabled')
        self.pulse.config(state='disabled')
        self.clear.config(state='normal')
        self.refresh()

    def clear_light(self):
        command = 'tell zero lamp clear\n'
        self.reception.write(command.encode('ascii'))
        canvas.itemconfig(self.zero_indicator, fill='lime green')
        self.color.config(state='normal')
        self.rainbow.config(state='normal')
        self.blink.config(state='normal')
        self.pulse.config(state='normal')
        self.clear.config(state='disabled')
        self.refresh()

    def refresh(self):
        self.update()
        self.update_idletasks()
        canvas.pack()


BRANCHES = [
    ('zero', 1),
    ('both', 2),
    ('orion', 3),
]

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Mission Control")
    root.geometry('530x260')
    canvas = tk.Canvas(root)
    app = Application(master=root)
    app.mainloop()
    app.reception.close()
    app.run = False

import sys
for path in sys.path:
    print(path)

import os
os.system("pip list")
import PySimpleGUI as sg

# layout
sg.set_options(font='Default 18', keep_on_top=True)
layout = [
        [sg.Text("Hello world")],
        [sg.Button("ok")]


]


# window

window = sg.window("Title", layout)


# event handlers
event, value = window.read()


# close
window.close()
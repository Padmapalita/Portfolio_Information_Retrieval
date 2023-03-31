# import sys
# for path in sys.path:
#     print(path)

# import os
# os.system("pip list")
import PySimpleGUI as sg
sg.theme('DarkGrey2') 
# layout
sg.set_options(font='Default 18', keep_on_top=True)
layout = [
    [sg.Text('Please enter your Name, Age, Phone')],
    [sg.Text('Name', size =(15, 1)), sg.InputText()],
    [sg.Text('Age', size =(15, 1)), sg.InputText()],
    [sg.Text('Phone', size =(15, 1)), sg.InputText()],
    [sg.Submit(), sg.Cancel()]
]


# window

window = sg.Window("Title", layout)


# event handlers
event, values = window.read()

# The input data looks like a simple list 
# when automatic numbered
print(event, values[0], values[1], values[2])

# close
window.close()

  

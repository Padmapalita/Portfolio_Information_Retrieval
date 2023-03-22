import PySimpleGUI as sg
#import PySimpleGUIQt as sg

# layout
sg.set_options(font='Default 18', keep_on_top=True)
layout = [
        [sg.Text("Hello world")],
        [sg.Button("ok")]


]


# window
#window = sg.window("Title", layout)
window = sg.Window("Title", layout)


# event handlers
event, value = window.read()


# close
window.close()

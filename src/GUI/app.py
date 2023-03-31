# import sys
# for path in sys.path:
#     print(path)

# import os
# os.system("pip list")

import PySimpleGUI as sg
from search import Search

searcher = Search()
num_results = 20

show_title = '--SHOW_title--'
show_value = '--SHOW_value--'
duration_title = '--DURATION_title--'
duration_value = '--DURATION_value--'
episode_title = '--EPISODE_tile--'
episode_value = '--EPISODE_value--'
       





sg.theme('DarkGrey2') 
# layout
sg.set_options(font='Default 18', keep_on_top=True)
basic_output = sg.Text('', key="output")# size=(40,4))


basic_show = [sg.Text('', key="--empty--")]
#basic_episode = [sg.Text('', key="--EPISODEtext--"), sg.Text('', key="--EPISODE--") ]
basic_element = [[sg.Text('basic', key="--SHOWtext--"), sg.Text('element', key="--SHOW--"), sg.Text('', key="--DURATIONtext--"),sg.Text('', key="--DURATION--") ],[sg.Text('', key="--EPISODEtext--"),  ],[sg.Text('', key="--EPISODE--")]]
basic_element = []
empty = sg.Column(basic_element,key='LIST', scrollable=False,  vertical_scroll_only=True, size=(850,1))



column_contents = [basic_show]
for i in range(num_results):
    #print('creation before', show_title)
    #print("show_title[:-1]", show_title[:-1])
    #set the string values for the elements 
    show_title = show_title+str(i)
    show_value = show_value+str(i)
    duration_title = duration_title+str(i)
    duration_value = duration_value+str(i)
    episode_title = episode_title+str(i)
    episode_value = episode_value+str(i)
    #print('creation after', show_title)

    #append the elements to the layout

    #column_contents.append([[sg.Text('', key=show_title), sg.Text('', key=show_value), sg.Text('', key=duration_title),sg.Text('', key=duration_value) ],[sg.Text('', key=episode_title),  ],[sg.Text('', key=episode_value)]])
    # layout.append([sg.Text('', key=show_title), sg.Text('', key=show_value), sg.Text('', key=duration_title),sg.Text('', key=duration_value) ])
    # layout.append([sg.Text('', key=episode_title),])
    # layout.append([sg.Text('', key=episode_value),])
    column_contents.append([sg.Text('', key=show_title), sg.Text('', key=show_value), sg.Text('', key=duration_title),sg.Text('', key=duration_value) ])
    column_contents.append([sg.Text('', key=episode_title),])
    column_contents.append([sg.Text('', key=episode_value, size=(65, 4))])

    #reset the string for the elements
    show_title = show_title[:-1]
    show_value = show_value[:-1]
    duration_title = duration_title[:-1]
    duration_value = duration_value[:-1]
    episode_title = episode_title[:-1]
    episode_value = episode_value[:-1]
    if i>9:
        show_title = show_title[:-1]
        show_value = show_value[:-1]
        duration_title = duration_title[:-1]
        duration_value = duration_value[:-1]
        episode_title = episode_title[:-1]
        episode_value = episode_value[:-1]

print(column_contents)

column = [sg.Column(column_contents, key='blah',scrollable=True,  vertical_scroll_only=True, size=(850,550))]
#layout = layout.append([column])
# print(column)
# print(column[0])
# layout = layout.append(column)
# window.extend_layout(window['-Column-'], new_layout(i))
# window
layout = [
    [sg.Text('Please Enter your search query')],
    [sg.Text('Query', size =(15, 1)), sg.InputText(key="query")],
    [sg.Submit(), sg.Cancel()],
    [empty],
    [column],
    #[sg.Column([basic_show,], key='LIST', size=(850,200))],
    #[basic_show],
    #[basic_episode],
    #basic_element, 
    # the loop below appends num_results to the bottom of the screen

   
]


window = sg.Window("Title", layout, size=(850,650), resizable=False)

#window.extend_layout(window['LIST'], [column])
# event handlers


while True:
    event, values = window.read()
    #print(event, values['query'], )
    if event=="Submit":
        user_query = values['query']
        print("I have created an event driven output ",values['query'])
        result = searcher.retrieve_ranking(user_query)
        #print(result)
        readable_result = searcher.lookup_metadata(result)
        print(readable_result[0])
        #print(readable_result)
        
        for i in range(num_results):
            #print('event before', show_title)
            #set the string values for the elements 
            show_title = show_title+str(i)
            show_value = show_value+str(i)
            duration_title = duration_title+str(i)
            duration_value = duration_value+str(i)
            episode_title = episode_title+str(i)
            episode_value = episode_value+str(i)
            #print('event after', show_title)

            #append the elements to the layout

            window[show_title].update("Show name: ")
            window[show_value].update("{text}".format(text=readable_result[i]['Show name']))
            window[duration_title].update("Length: ")
            window[duration_value].update("{text} minutes".format(text=readable_result[i]['Episode duration (minutes)']))
            window[episode_title].update("Description: ")
            window[episode_value].update("{text}".format(text=readable_result[i]['Episode title']))

            #reset the string for the elements
            show_title = show_title[:-1]
            show_value = show_value[:-1]
            duration_title = duration_title[:-1]
            duration_value = duration_value[:-1]
            episode_title = episode_title[:-1]
            episode_value = episode_value[:-1]
            if i>9:
                show_title = show_title[:-1]
                show_value = show_value[:-1]
                duration_title = duration_title[:-1]
                duration_value = duration_value[:-1]
                episode_title = episode_title[:-1]
                episode_value = episode_value[:-1]
            
        

       
    if event=="Cancel":
        break
    if event==None:
        break

# The input data looks like a simple list 
# when automatic numbered


# close
window.close()

  

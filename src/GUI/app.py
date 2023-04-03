import PySimpleGUI as sg
import webbrowser
import feedparser

from search import Search


searcher = Search()
num_results = 5

show_title = '--SHOW_title--'
show_value = '--SHOW_value--'
duration_title = '--DURATION_title--'
duration_value = '--DURATION_value--'
episode_title = '--EPISODE_tile--'
episode_value = '--EPISODE_value--'
button_title = '--Button_tile--'
       
sg.theme('DarkGrey') 
#sg.set_options(font='Default 18', keep_on_top=True)
sg.set_options(font=("Calibri",14), element_padding=(5, 5), keep_on_top=False)
basic_show = [sg.Text('', key="--HOLDER--")]
basic_element = []
empty = sg.Column([],key='LIST', scrollable=False, vertical_scroll_only=True, size=(850,1))
column_contents = [basic_show]

for i in range(num_results):
    # modify the keys for the list elements
    show_title = show_title+str(i)
    show_value = show_value+str(i)
    duration_title = duration_title+str(i)
    duration_value = duration_value+str(i)
    episode_title = episode_title+str(i)
    episode_value = episode_value+str(i)
    button_title = button_title+str(i)

    # This is the structure of a search result element
    column_contents.append([sg.Text('', key=show_title, font=("bold"), text_color='light grey'), sg.Text('', key=show_value, font=(25,), text_color='light grey', size=(50,2)), sg.Text('', key=duration_title,font=(25), text_color='light grey'),sg.Text('', key=duration_value) ])
    column_contents.append([sg.Text('', key=episode_title,  font=(25), text_color='light grey'),])
    column_contents.append([sg.Text('', key=episode_value, size=(50, 2),  font=(25), text_color='light grey')])
    column_contents.append([sg.Button('', key=i,  font=(25), )])

    #reset the string for the elements
    show_title = show_title[:-1]
    show_value = show_value[:-1]
    duration_title = duration_title[:-1]
    duration_value = duration_value[:-1]
    episode_title = episode_title[:-1]
    episode_value = episode_value[:-1]
    button_title = button_title[:-1]
    if i>9:
        show_title = show_title[:-1]
        show_value = show_value[:-1]
        duration_title = duration_title[:-1]
        duration_value = duration_value[:-1]
        episode_title = episode_title[:-1]
        episode_value = episode_value[:-1]
        button_title = button_title[:-1]

# put the 
column = [sg.Column(column_contents, key='--COLUMN--',scrollable=True, visible=False,  vertical_scroll_only=True, size=(850,550), )]

layout = [
    [sg.Text('Please Enter your search query')],
    [sg.Text('Query', size =(15, 1)), sg.InputText(key="query")],
    [sg.Submit(), sg.Cancel()],
    # is a holder
    [empty],
    # results column
    [column],
]


window = sg.Window("Spotify Transcript Search Engine", layout, size=(850,650), resizable=False)
readable_result = []
# This is the event stream 
while True:
    event, values = window.read()
    
    if event=="Submit":
        user_query = values['query']
        result = searcher.retrieve_ranking(user_query)
        readable_result = searcher.lookup_metadata(result)
        window['--COLUMN--'].update(visible=True)
        
        # This loops through the results elements and updates them
        for i in range(num_results):
            show_title = show_title+str(i)
            show_value = show_value+str(i)
            duration_title = duration_title+str(i)
            duration_value = duration_value+str(i)
            episode_title = episode_title+str(i)
            episode_value = episode_value+str(i)
            button_title = button_title+str(i)
            
            
            #append the elements to the layout
            window[show_title].update("Show name: ")
            window[show_value].update("{text}".format(text=readable_result[i]['Show name']))
            window[duration_title].update("Length: ")
            window[duration_value].update("{text} minutes".format(text=readable_result[i]['Episode duration (minutes)']))
            window[episode_title].update("Description: ")
            window[episode_value].update("{text}".format(text=readable_result[i]['Episode title']))
            window[i].update('View Podcast')
            # NewsFeed = feedparser.parse(readable_result[i]['rss_link'])
            # value = ""
            # for entry in NewsFeed.entries:
            #     if entry['title'] == readable_result[i]['Episode title']:
            #         print(entry['title'])
            #         print(len(entry))
            #         print(entry.keys())
            #         print(entry['link'])

            
            
            # #webbrowser.open_new(url)
            # #reset the string for the elements
            show_title = show_title[:-1]
            show_value = show_value[:-1]
            duration_title = duration_title[:-1]
            duration_value = duration_value[:-1]
            episode_title = episode_title[:-1]
            episode_value = episode_value[:-1]
            button_title = button_title[:-1]
            if i>9:
                show_title = show_title[:-1]
                show_value = show_value[:-1]
                duration_title = duration_title[:-1]
                duration_value = duration_value[:-1]
                episode_title = episode_title[:-1]
                episode_value = episode_value[:-1]
                button_title = button_title[:-1]
    for i in range(num_results):
        if event==i:
            NewsFeed = feedparser.parse(readable_result[i]['rss_link'])
            
            for entry in NewsFeed.entries:
                if entry['title'] == readable_result[i]['Episode title']:
                    print(entry['title'])
                    print(len(entry))
                    print(entry.keys())
                    for key in entry.keys():
                        
                        if key=='link':
                            webbrowser.open_new(entry['link'])
                    else:
                        links = entry['links']
                        link = links[0]

                      
                        # link = group_link[0]
                        print(link['href'])
                        webbrowser.open_new(link['href'])

            
            
            
            #reset the string for the elements

               
    if event=="Cancel":
        break
    if event==None:
        break

# closes the app after the while loop breaks 
window.close()

  

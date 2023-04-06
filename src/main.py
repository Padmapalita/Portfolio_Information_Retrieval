import PySimpleGUI as sg
import webbrowser as web
import feedparser
from urllib import request
import re
from app_search import AppSearch


searcher = AppSearch()
num_results = 20

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
empty = sg.Column([],key='LIST', scrollable=False, vertical_scroll_only=True, size=(650,1))
column_contents = [basic_element]

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
    column_contents.append([sg.Text('', key=show_title, font=("bold"), text_color='light grey',size=(11, 1)), sg.Text('', key=show_value, font=(25,), text_color='light grey', size=(30,1)), sg.Text('', key=duration_title,font=(25), text_color='light grey',  size=(8,1)),sg.Text('', key=duration_value,  size=(16,1)) ])
    column_contents.append([sg.Text('', key=episode_title,  font=("bold"), text_color='light grey', size=(11, 1)),sg.Text('', key=episode_value, size=(48, 1),  font=(25), text_color='light grey')])
    column_contents.append([sg.Button('', key=i,  font=(25), )])
    column_contents.append([sg.Text('', key="blank{i}", size=(30, 2),  font=(25), text_color='light grey')])

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


def podcast_modal(entry):
    print([(entry[key], key) for key in entry.keys()])
    summary = ''
    if 'summary' in entry:
        summary = entry['summary']
    
    # as per recommendation from @freylis, compile once only
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    new_summary = re.sub(CLEANR, '', summary)
    
    author = '' 
    if 'author' in entry:
        author = entry['author']
    title = ''
    if 'title' in entry:
        author = entry['title']

    layout = [
        [sg.Text(title)],
        [sg.Text(author)],
        [sg.Multiline(new_summary,size=(40,10), key="WORK")],
        [sg.Button('PODCAST AVAILABLE',key="--PODCASTLINK--")],
        [sg.Button('OK')],
    ]
    
    modalWindow = sg.Window('Podcast Details', layout, modal=False)
    if "link" not in entry.keys():
        if "links" not in entry.keys():
            window["--PODCASTLINK--"].update(visible=False)


    while True:
          event, values = modalWindow.read()
          if event == "--PODCASTLINK--":
            if 'link' in entry.keys():
                web.open_new(entry['link'])
                break
            if 'link' not in entry.keys():
                if 'links' in entry.keys():
                    links = entry['links']
                    link = links[0]
                    web.open_new(link['href'])
                    break
                if "links" not in entry.keys():
                    print("")
          if event == "OK":
              modalWindow.close()
              break
          if event == sg.WIN_CLOSED:
              modalWindow.close()
              break
    modalWindow.close()
                

# put the search contents into a column
column = [sg.Column(column_contents, key='--COLUMN--',scrollable=True, visible=False,  vertical_scroll_only=True, size=(650,450), )]

layout = [
    
    [sg.Text('What would you like to listen to today?', font=("Calibri",20, 'bold'), pad=(10, (5, 5)))],
    [sg.Text("Search for: ", size =(8, 1),font=("Calibri",17, 'bold'), pad=(10, (5, 5))), sg.InputText(key="query", font=("Calibri",17), pad=(10, (5, 5)))],
    [sg.Submit(font=("Calibri",17), pad=(10, (5, 10)))],
   
    [column],
]


window = sg.Window("Spotify Transcript Search Engine", layout, size=(650,580), resizable=False)
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
            window[i].update('Check for podcast details')

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
            print(readable_result[i]['rss_link'])
            link = readable_result[i]['rss_link']
            newsFeed = feedparser.parse(link)
            if len(newsFeed.entries) < 1 or newsFeed.entries == None:
                print("no news feed entries")
            for entry in newsFeed.entries:
                if 'title' in entry.keys():
                    print("Title is in entry.keys")

                    if entry['title'] == readable_result[i]['Episode title']:
                        print(entry['title'])
                        print(len(entry))
                        print(entry.keys())
                        if 'link' in entry.keys():
                            print("podcast Link FOUND")
                            podcast_modal(entry)
                            # web.open_new(entry['link'])
                        if 'link' not in entry.keys():
                            print("podcast Link not in  entry.keys()")
                            if 'links' in entry.keys():
                                links = entry['links']
                                link = links[0]
                                podcast_modal(entry)
                                # web.open_new(link['href'])
                                print("href links FOUND")
                            if "links" not in entry.keys():
                                print("href Links not found in entry.keys()")
                else:
                    print("Title is NOT in entry.keys")
             
    if event=="Cancel":
        break
    if event==None:
        break

# closes the app after the while loop breaks 
window.close()

  

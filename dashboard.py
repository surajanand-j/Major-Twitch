from os import link
import streamlit as st
import pandas as pd
import numpy as np
import json
import requests
from pandas.io.json import json_normalize
import time
import Fetch
import Footer
import config
import Insert
from itertools import cycle
import dateutil.parser as dp

import threading
from datetime import timedelta


import viewcount_create
from pymongo import MongoClient



#Request for the access code using requests library
# access_code = requests.post('https://id.twitch.tv/oauth2/token?client_id='+str(config.client_id)+'&client_secret='+str(config.client_secret)+'&grant_type=client_credentials')

#access token response is a JSON-encoded app access token
access_token = json.loads(config.access_code.text)
access_token = access_token['access_token']

    # st.write(access_token)
st.sidebar.write('MENU')
Menu=['Channels','Games', 'Search Channel', 'Know Twitch Better']
option=st.sidebar.selectbox("Look Into",Menu,0)

def loading_bar():
    # displays a loading bar that shows how much the page has loaded.
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1)

def header_print():
    st.markdown("<h1 style='text-align: center; color: ;'>Metrics Twitchify</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: ;'>Welcome to Metrics Twitchify.<br> This website was created as a final year project as CS students. <br>We hope you find it useful!</p>", unsafe_allow_html=True)
    
    # st.header("Metrics Twitchify")
    # st.write("Welcome to Metrics Twitchify. This website was created as a final year project as CS students. We hope you find it useful!")

#Page 1 Top Games
if option=='Games':
    header_print()
    loading_bar()

    @st.cache(ttl=60*2)
    def insert_games():
        Insert.exec()
    insert_games()
    # @st.cache
    def twitch():
        # threading.Timer(100.0, twitch).start()
        
        st.subheader('Top 15 Categories/Games On twitch Right Now')

        # Top Games
        headers = {
            'Client-ID' : config.client_id,
            'Authorization' : 'Bearer '+str(access_token),
        }
        
        # topgames_data = games_response_json['data']
        topgames_data_t=Fetch.games_data()
        # st.write(topgames_data_t)
        topgames_data=topgames_data_t['data']
        # topgames_data=json.loads(topgames_data_t.text)
        for message in topgames_data:
            game_name=message['name']
            st.write('Game Name - ',game_name)
            col1, col2 = st.columns([1,3])
            with col1:
                img=message['box_art_url'].replace("{width}", "150").replace("{height}", "200")
                st.image(img)
                clips_response=requests.get('https://api.twitch.tv/helix/clips?first=4&game_id='+message['id'],headers=headers)
                clips_response_json=json.loads(clips_response.text)
                clips_data=clips_response_json['data']
                # st.write(clips_response_json)
            with col2:
                with st.expander('Show Popular Streamers of -> '+game_name):
                    tempo=message['id']
                    st.write(message['name'])
                    URL='https://api.twitch.tv/helix/streams?game_id={}'
                    final_url=URL.format(tempo)
                    stream_response = requests.get(final_url, headers=headers)
                    stream_response_json = json.loads(stream_response.text)
                    topstreamers_data=stream_response_json['data']
                    
                    count=1
                    for i in topstreamers_data:
                        st.write(count,')',i['user_name'])
                        count+=1
                    # st.write(stream_response_json)
            st.write('Popular clips of: '+game_name)
            filteredImages = []
            clips_link=[] 
            for ths in clips_data:
                filteredImages.append(ths['thumbnail_url'])
                clips_link.append(ths['url'])
            # caption = [] # your caption here
            idx = 0 
            for _ in range(len(filteredImages)-1): 
                cols = st.columns(4) 

                if idx < len(filteredImages): 
                    cols[0].image(filteredImages[idx], width=150)
                    with cols[0]:
                        st.warning('[open in twitch](%s)'%clips_link[idx])
                    idx+=1

                if idx < len(filteredImages):
                    cols[1].image(filteredImages[idx], width=150)
                    with cols[1]:
                        st.warning('[open in twitch](%s)'%clips_link[idx])
                    idx+=1

                if idx < len(filteredImages):
                    cols[2].image(filteredImages[idx], width=150)
                    with cols[2]:
                        st.warning('[open in twitch](%s)'%clips_link[idx])
                    idx+=1 
                if idx < len(filteredImages): 
                    cols[3].image(filteredImages[idx], width=150)
                    with cols[3]:
                        st.warning('[open in twitch](%s)'%clips_link[idx])
                    idx = idx + 1
                else:
                    break
                # st.write("[Open in Twitch](filteredImage['url'])")

        # topgames_df = pd.DataFrame.from_dict(json_normalize(topgames_data), orient='columns')
        # export_topgames_csv = topgames_df.to_csv (r'C:/Users/suraj_gjnx4vc/Desktop/Major Twitch/topgames.csv', index = None, header=True)
    twitch()

#Page 2 Channels/Streamers
elif option=='Channels':
    header_print()
    loading_bar()
    
    @st.cache(ttl=60*2)
    def insert_stream():
        Insert.exec1()
    # def repeat():
    #     threading.Timer(1000.0, repeat).start()
    #     insert_stream()
    insert_stream()


    def twitch1():
        # threading.Timer(100.0, twitch1).start()
        st.subheader("Top Active Stream on Twitch Right Now")
        headers = {
        'Client-ID' : config.client_id,
        'Authorization' : 'Bearer '+str(access_token),
        }

        Streamers_data=Fetch.stream_data()
        # print(Streamers_data.keys())
        Streamers_data=Streamers_data["data"]
        # display data save
        idx = 0 
        Imag=[]
        Type=[]
        game_name=[]
        title=[]
        viewer_count=[]
        started_at=[]
        user_name=[]
        stream_url = []

        for ths in Streamers_data:
                Imag.append(ths['thumbnail_url'].replace("{width}", "400").replace("{height}", "250"))
                Type.append(ths['type'])
                game_name.append(ths['game_name'])
                title.append(ths['title'])
                viewer_count.append(ths['viewer_count'])
                started_at.append(ths['started_at'])
                user_name.append(ths['user_name'])

                stream_url.append('https://www.twitch.tv/'+ths['user_name'])

        # Printing Sreamer Data on Channels Page
        for _ in range(len(Streamers_data)-1):  
            cols = st.columns(2)
            if user_name[idx]=='Amouranth':
                idx+=1
            if idx < len(Streamers_data): 
                with cols[0]:
                    st.image(Imag[idx])
                    #watch on twitch hyperlink
                    st.warning('[Watch '+user_name[idx]+' on Twitch](%s)'%stream_url[idx])
                    
                
            if idx < len(Streamers_data):
                with cols[1]:
                    
                    st.success('User : '+user_name[idx])
                    st.error('Viewers : '+str(viewer_count[idx]))
                    st.info("Stream Category : "+game_name[idx])
                


            if idx < len(Streamers_data):

                # Here goes Viewercount Data Per Streamer (in the same order as the Top Streamer List)
                st.markdown("<p style='text-align: center; color: white;'>Viewcount Trend</p>", unsafe_allow_html=True)

                # Processing Viewer count data from database
                viewcount_create.viewcount_data_create()

                # get sreamer viewcount data
                def fetch_viewcount(name, filepath):
                    newdf = pd.read_csv(filepath)
                    newdf = newdf.loc[newdf['user_name'] == name]

                    # converting time into seconds (int)
                
                    # if not newdf.empty:
                    #     newdf['time'] = int(np.ceil(dp.parse(newdf['time'].values[0]).timestamp()))
                      
                    newdf.reset_index(inplace = True)
                    # newdf.set_index('time', drop=True)
                    return newdf[['viewer_count', 'time']]
                    # return newdf

                chart_data = fetch_viewcount(user_name[idx], 'streams_processed.csv')

                
                if not chart_data.empty:
                    chart_data['time'] =  pd.to_datetime(chart_data['time'])+timedelta(hours=5,minutes=30)
                    # st.write(chart_data)
                    chart_data = chart_data.rename(columns={'time':'index'}).set_index('index')
                    st.line_chart(chart_data)
                else:
                    st.write('Insufficient Data')
                idx+=1 
            else:
                break
    twitch1()
        
    

elif option=='Search Channel':
    header_print()
    loading_bar()

    headers = {
        'Client-ID' : config.client_id,
        'Authorization' : 'Bearer '+str(access_token),
    }
    
    # Search Bar
    st.subheader('Search Channels')
    with st.form(key='my_form'):
        text_input = st.text_input(label='Enter Channel')
        submit_button = st.form_submit_button(label='Find')
    if text_input:
        channel_response=requests.get('https://api.twitch.tv/helix/search/channels?query='+text_input,headers=headers)
        channel_response_json=json.loads(channel_response.text)
        # st.write(channel_response_json)
        
        channel_data=channel_response_json['data']
        num_of_results = len(channel_data)
        st.subheader("Showing {} Channels".format(num_of_results))
        for temp in channel_data:
            col1, col2 = st.columns([1,3])
            with col1:
                image1=temp['thumbnail_url'].replace("{width}", "100").replace("{height}", "100")
                st.write('Channel Name :',temp['display_name'])
                st.image(image1)
            with col2:
                channel_live=temp['is_live']
                Emote_response=requests.get('https://api.twitch.tv/helix/chat/emotes?broadcaster_id='+temp['id'],headers=headers)
                Emote_response_json=json.loads(Emote_response.text)
                Emote_Data=Emote_response_json['data']
                
                # filteredImages = [] # your images here
                # caption = [] # your caption here
                
                        
                # st.write(Emote_response_json)
                if(channel_live):
                    st.success("Channel is LIVE right now")
                    st.write("Current Stream Name -->>",temp['title'])
                    
                    # st.write(temp['id'])
                    video_response=requests.get('https://api.twitch.tv/helix/streams?user_id='+temp['id'],headers=headers)
                    video_response_json=json.loads(video_response.text)
                    
                    # st.info('Viewers  ',temp[])
                    if(video_response_json['data']):
                        st.info('Viewers Count -->'+str(video_response_json['data'][0]["viewer_count"]))
                    
                else:
                    st.error("Channel is Not LIVE right now.")
            if(Emote_Data):
                st.write('Emotes of this Channel are:')
                cols = cycle(st.columns(10)) 
                for idx, filteredImage in enumerate(Emote_Data):
                    next(cols).image(filteredImage['images']['url_1x'])



elif option=='Know Twitch Better':
#else:
    header_print()
    loading_bar()
    st.header("What is Twitch?")
    st.write("Twitch is a popular online service used to watch and stream digital video broadcasts. It originally focused almost entirely on video games but has since expanded to include streams dedicated to artwork creation, music, talk shows, and the occasional TV series.")
    st.header("Where Can I Watch Twitch?")
    st.write("Twitch streams can be viewed on the official Twitch website - Twitch.tv and via one of the many official Twitch apps. Watching broadcasts and videos on Twitch is completely free and doesn't require viewers to log in. Creating an account, however, does allow users to add their favorite channels to a follow list and participate in each stream's unique chatroom. Hosting is a popular way for Twitch streamers to broadcast another channel's live stream to their own audience.")
    st.header("How Can I Find Twitch Streamers to Watch?")
    st.write("Twitch recommends streams on the front page of its website and its apps. Another popular way to discover new Twitch channels to watch is by browsing the Games category. This option is available on all of the apps and the Twitch website and is an easy way to find a live stream relating to a specific video game title or series.")
    st.write("Alternatively, you can use our website - Metrics Twitchify, for browsing the popular streams or browse the popular streams based on which game category.")
    st.write("You can go to the Channels page to see the top active streams on the whole website right and see if you like anything.")
    st.write("You can go to the Games page to browse active streams that are in that particular game category and live at the moment.")
    st.write("Finally, you can use the Search page to search for any streamer using a name that you will enter.")
    st.write("Additionally We have provided details about Twitch in the Know Twitch Better page where we have talked about the basics about twitch and how our website can be utilized.")
    st.header("What are Emotes?")
    st.write("When words just aren’t enough, there’s Emotes: Twitch-specific emoticons that viewers and streamers use to express a number of feelings in chat. Emotes are the <3 of Twitch culture. They’re a language of their own. They’re also a way for Partners and Affiliates to reinforce their branding and personalities, and give fans ways to celebrate epic moments, poke fun at fails, spread love in chat, and become active members of your community.")

Footer.footer()

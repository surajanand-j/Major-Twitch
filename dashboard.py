from os import link
import streamlit as st;
import pandas as pd;
import numpy as np;
import json
import requests
from pandas.io.json import json_normalize
import time
import threading
import Fetch
import Footer
import config
import Insert
from itertools import cycle

from pymongo import MongoClient



#Request for the access code using requests library
access_code = requests.post('https://id.twitch.tv/oauth2/token?client_id='+str(config.client_id)+'&client_secret='+str(config.client_secret)+'&grant_type=client_credentials')

#access token response is a JSON-encoded app access token
access_token = json.loads(access_code.text)
access_token = access_token['access_token']

    # st.write(access_token)
st.sidebar.write('MENU')
Menu=['Games','Channels','Know Twitch Better']
option=st.sidebar.selectbox("Look Into",Menu,1)
st.header(option)

if option=='Games':
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1)

    @st.cache
    def insert_games():
        Insert.exec()

    
    # def twitch():
    #     threading.Timer(100.0, twitch).start()
        
    st.subheader('Top 15 Games On twitch Right Now')

    # Top Games
    headers = {
        'Client-ID' : config.client_id,
        'Authorization' : 'Bearer '+str(access_token),
    }
    insert_games()
    # topgames_data = games_response_json['data']
    topgames_data_t=Fetch.res
    # st.write(topgames_data_t)
    topgames_data=topgames_data_t['data']
    # topgames_data=json.loads(topgames_data_t.text)
    for message in topgames_data:
        game_name=message['name']
        st.write('Game Name - ',game_name)
        col1, col2 = st.columns([1,3])
        with col1:
            img=message['box_art_url'].replace("{width}", "100").replace("{height}", "100")
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
                    st.write('[open in twitch](%s)'%clips_link[idx])
                idx+=1
    
            if idx < len(filteredImages):
                cols[1].image(filteredImages[idx], width=150)
                with cols[1]:
                    st.write('[open in twitch](%s)'%clips_link[idx])
                idx+=1

            if idx < len(filteredImages):
                cols[2].image(filteredImages[idx], width=150)
                with cols[2]:
                    st.write('[open in twitch](%s)'%clips_link[idx])
                idx+=1 
            if idx < len(filteredImages): 
                cols[3].image(filteredImages[idx], width=150)
                with cols[3]:
                    st.write('[open in twitch](%s)'%clips_link[idx])
                idx = idx + 1
            else:
                break
                # st.write("[Open in Twitch](filteredImage['url'])")

        # topgames_df = pd.DataFrame.from_dict(json_normalize(topgames_data), orient='columns')
        # export_topgames_csv = topgames_df.to_csv (r'C:/Users/suraj_gjnx4vc/Desktop/Major Twitch/topgames.csv', index = None, header=True)
    # twitch()

elif option=='Channels':
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1)
    
    
    headers = {
        'Client-ID' : config.client_id,
        'Authorization' : 'Bearer '+str(access_token),
    }
    @st.cache(ttl=600)
    def insert_stream():
        Insert.exec1()
    # def repeat():
    #     threading.Timer(1000.0, repeat).start()
    #     insert_stream()
    insert_stream()

    st.subheader("Top 20 Active Streamers on Twitch")
    Streamers_data=Fetch.report
    Streamers_data=Streamers_data["data"]
    idx = 0 
    Imag=[]
    Type=[]
    game_name=[]
    title=[]
    viewer_count=[]
    started_at=[]
    user_name=[]
    for ths in Streamers_data:
            Imag.append(ths['thumbnail_url'].replace("{width}", "150").replace("{height}", "200"))
            Type.append(ths['type'])
            game_name.append(ths['game_name'])
            title.append(ths['title'])
            viewer_count.append(ths['viewer_count'])
            started_at.append(ths['started_at'])
            user_name.append(ths['user_name'])
           
    for _ in range(len(Streamers_data)-1): 
        cols = st.columns(4) 

        if idx < len(Streamers_data): 
            with cols[0]:
                st.image(Imag[idx])
            

        if idx < len(Streamers_data):
            with cols[1]:
                st.error('User :'+user_name[idx])
                st.info('Viewers :'+str(viewer_count[idx]))
                st.success("Game Name :"+game_name[idx])
            idx+=1
        if idx < len(Streamers_data): 
            with cols[2]:
                st.image(Imag[idx])
            

        if idx < len(Streamers_data):
            with cols[3]:
                st.error('User :'+user_name[idx])
                st.info('Viewers :'+str(viewer_count[idx]))
                st.success("Game Name :"+game_name[idx])
            idx+=1
            
        else:
            break
    
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
                    st.info('Viewers Count -->'+str(video_response_json['data'][0]["viewer_count"]))
                    
                else:
                    st.error("Channel is Not LIVE right now.")
            if(Emote_Data):
                st.write('Emotes of this Channel are:')
                cols = cycle(st.columns(10)) # st.columns here since it is out of beta at the time I'm writing this
                for idx, filteredImage in enumerate(Emote_Data):
                    next(cols).image(filteredImage['images']['url_1x'])
elif option=='Know Twitch Better':
    st.subheader('TO DO')
Footer.footer()

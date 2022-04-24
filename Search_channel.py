import streamlit as st
import config
import requests
import json
from itertools import cycle

def search_channel():
    headers = {
            'Client-ID' : config.client_id,
            'Authorization' : 'Bearer '+str(config.access_token),
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


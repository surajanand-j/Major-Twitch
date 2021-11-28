import streamlit as st;
import pandas as pd;
import numpy as np;
import json
import requests
from pandas.io.json import json_normalize
import time
import threading

client_id= 'kfdicyd8nct8dwqd8vy7zrc8jn5sfw'
client_secret= 'o77rnssqevendjf22z2sb21erif5n9'

#Request for the access code using requests library
access_code = requests.post('https://id.twitch.tv/oauth2/token?client_id='+str(client_id)+'&client_secret='+str(client_secret)+'&grant_type=client_credentials')

#access token response is a JSON-encoded app access token
access_token = json.loads(access_code.text)
access_token = access_token['access_token']

    # st.write(access_token)
st.sidebar.write('MENU')
Menu=['Games','Channels']
option=st.sidebar.selectbox("Look Into",Menu,1)
st.header(option)

if option=='Games':
    def twitch():
        threading.Timer(1000.0, twitch).start()
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1)
        st.subheader('Top 15 Games On twitch Right Now')
    
        # Top Games
        headers = {
            'Client-ID' : client_id,
            'Authorization' : 'Bearer '+str(access_token),
        }
        games_response = requests.get('https://api.twitch.tv/helix/games/top?first=15', headers=headers)
    
        games_response_json = json.loads(games_response.text)
        # st.write(games_response_json)
        topgames_data = games_response_json['data']
        for message in topgames_data:
            game_name=message['name']
            st.write('--',game_name)
            col1, col2 = st.columns([1,3])
            with col1:
                img=message['box_art_url'].replace("{width}", "100").replace("{height}", "100")
                st.image(img)
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
            # st.write('Analytics on '+game_name )
            # URLt='https://api.twitch.tv/helix/analytics/games?game_id={}'
            # final_urlt=URLt.format(message['id'])
            # Analytics = requests.get(final_urlt, headers=headers)
            # Analytics_json = json.loads(Analytics.text)
            # # Analytics_data=Analytics_json['data']
            # st.write(Analytics_json)


        # topgames_df = pd.DataFrame.from_dict(json_normalize(topgames_data), orient='columns')
        # export_topgames_csv = topgames_df.to_csv (r'C:/Users/suraj_gjnx4vc/Desktop/Major Twitch/topgames.csv', index = None, header=True)
    twitch()

elif option=='Channels':
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1)
    st.subheader('See all the Analytics of Streams on Twitch')
    
    headers = {
        'Client-ID' : client_id,
        'Authorization' : 'Bearer '+str(access_token),
    }
    with st.form(key='my_form'):
        text_input = st.text_input(label='Enter Channel')
        submit_button = st.form_submit_button(label='Submit')
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
                st.write(temp['display_name'])
                st.image(image1)
            with col2:
                channel_live=temp['is_live']
                if(channel_live):
                    st.success("Channel is LIVE right now")
                    st.write("Current Stream Name -->>",temp['title'])
                    
                    # st.write(temp['id'])
                    video_response=requests.get('https://api.twitch.tv/helix/streams?user_id='+temp['id'],headers=headers)
                    video_response_json=json.loads(video_response.text)
                    # st.write(video_response_json['data'][0]["viewer_count"])
                    # st.info('Viewers  ',temp[])
                    st.info('Viewers Count -->'+str(video_response_json['data'][0]["viewer_count"]))
                    
                else:
                    st.error("Channel is Not LIVE right now.")


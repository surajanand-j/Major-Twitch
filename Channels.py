import config
import Fetch
import streamlit as st
# import Youtube
import viewcount_create
import pandas as pd
from datetime import timedelta
from viewcount_create import Fetch_all_docs
all_docs_channels=Fetch_all_docs()

def parse_datetime(dt_str):
    try:
        return pd.to_datetime(dt_str, utc=True, format='%Y-%m-%dT%H:%M:%S.%f%z')
    except ValueError:
        return pd.to_datetime(dt_str, utc=True, format='%Y-%m-%dT%H:%M:%S.%f')


def twitch1():
    # 
    # threading.Timer(100.0, twitch1).start()
    st.subheader("Top Active Stream on Twitch Right Now")
    headers = {
    'Client-ID' : config.client_id,
    'Authorization' : 'Bearer '+str(config.access_token),
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
    Number=0

 


    for _ in range(len(Streamers_data)-1):  
        cols = st.columns(2)
        
        if user_name[idx]=='Amouranth':
            idx+=1
        Number+=1
        if idx < len(Streamers_data): 
            with cols[0]:
                st.image(Imag[idx])
                #watch on twitch hyperlink
                st.warning('[Watch '+user_name[idx]+'](%s)'%stream_url[idx])
                        
            
        if idx < len(Streamers_data):
            with cols[1]:
                # st.markdown("<p style='text-align: center; color: white;'>Twitch Info</p>", unsafe_allow_html=True)
                
                st.success(str(Number)+') '+'User : '+user_name[idx])
                st.success('Viewers : '+str(viewer_count[idx]))
                st.success("Stream Category : "+game_name[idx])
        #  Adding Youtube info   
        # if idx < len(Streamers_data):
        #     with cols[2]:
        #         Youtube.channel(user_name[idx])


        if idx < len(Streamers_data):

            # Here goes Viewercount Data Per Streamer (in the same order as the Top Streamer List)
            st.markdown("<p style='text-align: center; color: white;'>Viewcount Trend</p>", unsafe_allow_html=True)

            # Processing Viewer count data from database
            
            streams_processed=viewcount_create.viewcount_data_create(all_docs_channels)

            # get sreamer viewcount data
            def fetch_viewcount(name, filepath):
                newdf = streams_processed
                newdf = newdf.loc[newdf['user_name'] == name]

                # converting time into seconds (int)
            
                # if not newdf.empty:
                #     newdf['time'] = int(np.ceil(dp.parse(newdf['time'].values[0]).timestamp()))
                    
                newdf.reset_index(inplace = True)
                # newdf.set_index('time', drop=True)
                return newdf[['viewer_count', 'time']]
                # return newdf

            chart_data = fetch_viewcount(user_name[idx], streams_processed)

            
            if not chart_data.empty:

                chart_data['time'] = chart_data['time'].apply(parse_datetime)

# Convert from UTC to desired timezone (+05:30)
                chart_data['time'] = chart_data['time'].dt.tz_convert('Asia/Kolkata')
                chart_data['time'] =  pd.to_datetime(chart_data['time'])+timedelta(hours=5,minutes=30)
                # st.write(chart_data)
                chart_data = chart_data.rename(columns={'time':'index'}).set_index('index')
                st.line_chart(chart_data)
            else:
                st.write('Insufficient Data')
            idx+=1 
        else:
            break
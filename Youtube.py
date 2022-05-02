import googleapiclient.discovery
import streamlit as st
import random
# API information
api_service_name = "youtube"
api_version = "v3"
developer_key=[]
DEVELOPER_KEY1 = 'AIzaSyBZcdVS9CnU08k1VvAUph47BkY6lhK8CFQ'
DEVELOPER_KEY2 = 'AIzaSyA0DvUPENuoYgUnaXnFFAQ0mWjCLzOkUbk'
DEVELOPER_KEY3 = 'AIzaSyAHddqbcSENsC5hyfXcK6gOrcxwsgJJLb4'
developer_key.append(DEVELOPER_KEY1)
developer_key.append(DEVELOPER_KEY2)
developer_key.append(DEVELOPER_KEY3)



# Notice that nextPageToken now is requested in 'fields' parameter
def channel(arg_1):
    #Request for the first channel with this name
    key_num=random.randint(0,2)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = developer_key[key_num])
    
    request = youtube.search().list(
            part="snippet",
            q=arg_1,
            type="channel",
            maxResults=1
    )
    response = request.execute()
    channel_id=response["items"][0]["id"]["channelId"]
    
    #Request for channel info with channel_id
    # st.write(channel_id)
    Youtube_url="https://www.youtube.com/channel/"+channel_id
    request1=youtube.channels().list(
        part="statistics",
        id=channel_id
    )
    response_1=request1.execute()
    print(response_1)
    st.markdown("<p style='text-align: center; color: white;'>YouTube Info</p>", unsafe_allow_html=True)
    youtube_stats=response_1["items"][0]["statistics"]
    # st.write(youtube_stats)
    st.warning('[Open YouTube Channel](%s)'%Youtube_url)
    st.error('Views on Youtube: '+youtube_stats["viewCount"])
    if(youtube_stats["hiddenSubscriberCount"]==True):
        st.warning("Subscribers Count is hidden")
    else:
        st.error('Subscribers: '+youtube_stats["subscriberCount"])
    st.error('Number of Videos: '+youtube_stats["videoCount"])


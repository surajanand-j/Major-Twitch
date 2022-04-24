import googleapiclient.discovery
import streamlit as st
# API information
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = 'AIzaSyBZcdVS9CnU08k1VvAUph47BkY6lhK8CFQ'
# API client
youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

# Notice that nextPageToken now is requested in 'fields' parameter
def channel(arg_1):
    #Request for the first channel with this name
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


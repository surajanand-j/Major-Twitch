import googleapiclient.discovery
import streamlit as st
import random
# API information
api_service_name = "youtube"
api_version = "v3"
developer_key=[]


developer_key.append('AIzaSyA0DvUPENuoYgUnaXnFFAQ0mWjCLzOkUbk')
developer_key.append('AIzaSyAHddqbcSENsC5hyfXcK6gOrcxwsgJJLb4')
developer_key.append('AIzaSyBZcdVS9CnU08k1VvAUph47BkY6lhK8CFQ')
developer_key.append('AIzaSyBqh7alvQs4KVf9xp_C4-Uapf8JzH49bJw')
developer_key.append('AIzaSyCg3rUiRNxAgbuLMI58IU0wttE0Kw1jrsA')
developer_key.append('AIzaSyBOcJn10VzXgtpBSuhd1R-8yCD1CRecVog')


# Notice that nextPageToken now is requested in 'fields' parameter
def channel(arg_1):
    #Request for the first channel with this name
    key_num=random.randint(0,5)
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
    response1=request1.execute()
    print(response1)
    st.markdown("<p style='text-align: center; color: white;'>YouTube Info</p>", unsafe_allow_html=True)
    youtube_stats=response1["items"][0]["statistics"]
    # st.write(youtube_stats)
    st.warning('[Open YouTube Channel](%s)'%Youtube_url)
    st.error('Views on Youtube: '+youtube_stats["viewCount"])
    if(youtube_stats["hiddenSubscriberCount"]==True):
        st.warning("Subscribers Count is hidden")
    else:
        st.error('Subscribers: '+youtube_stats["subscriberCount"])
    st.error('Number of Videos: '+youtube_stats["videoCount"])


def games(arg_2,video_url,yt_thumbnail):
    st.markdown("<p style='text-align: center; color: white;'>Popular YT Channel(Video)</p>", unsafe_allow_html=True)
    key_num=random.randint(0,2)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = developer_key[key_num])
    # Request for video from game name
    request2 = youtube.search().list(
            part="snippet",
            q=arg_2,
            type="video",
            maxResults=5
    )
    response2 = request2.execute()
    search_data=response2["items"]
    # st.write(response2["items"])
    with st.expander('On Youtube'):        
        count=1
        for i in search_data:
            st.error(str(count)+') '+i["snippet"]["channelTitle"]+"\n"+"("+i["snippet"]["title"]+")")
            yt_thumbnail.append(i["snippet"]["thumbnails"]["default"]["url"])
            temp="https://www.youtube.com/watch?v="
            video_url.append(temp+i["id"]["videoId"])
            count+=1


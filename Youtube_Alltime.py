import youtube_channels_helper
import streamlit as st
playlist_fetch=youtube_channels_helper.get_all_video_details_by_playlist_search()
res=youtube_channels_helper.top_videos_of_channel(playlist_fetch,amount=50)
def alltime_display():
    col0,col2,col3,col4,col5 =st.columns([4,4,4,3,2])
    with col0:
        st.markdown("<p style='text-align: center; color: white;'>Thumbnails</p>", unsafe_allow_html=True)
    with col2:
        st.markdown("<p style='text-align: center; color: white;'>Title</p>", unsafe_allow_html=True)
    with col3:
        st.markdown("<p style='text-align: center; color: white;'>Channel Name</p>", unsafe_allow_html=True)
    with col4:
        st.markdown("<p style='text-align: center; color: white;'>Views</p>", unsafe_allow_html=True)
    with col5:
        st.markdown("<p style='text-align: center; color: white;'>Likes</p>", unsafe_allow_html=True)
    
    for i in range(len(res['channelTitle'])):
        col1=st.columns([4,4,4,3,2])
        with col1[0]:
            st.image(res['thumbnails'].values[i]['url'])
        with col1[1]:
            st.write(res['title'].values[i])          
        with col1[2]:
            st.write(res['channelTitle'].values[i])
        with col1[3]:
            st.write(str(res['viewCount'].values[i]))
        with col1[4]:
            st.write(str(res['likeCount'].values[i]))
         


    
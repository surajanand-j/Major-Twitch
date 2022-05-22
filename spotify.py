import Fetch
import streamlit as st


def spotify_display(Result):
    # rank=Result['rank']
    # album_name=[]
    # artist_name=[]
    # track_name=[]	
    # track_popularity=[]
    # id=[]	
    # preview_url=[]	
    # track_url=[]	
    # album_thumbnail=[]
    col0,col2,col3,col4,col5,col6 =st.columns([4,2,5,4,4,3])
    with col0:
        st.markdown("<p style='text-align: center; color: white;'>Thumbnail</p>", unsafe_allow_html=True)
    with col2:
        st.markdown("<p style='text-align: center; color: white;'>Track</p>", unsafe_allow_html=True)
    with col3:
        st.markdown("<p style='text-align: center; color: white;'>Track Name</p>", unsafe_allow_html=True)
    with col4:
        st.markdown("<p style='text-align: center; color: white;'>Artist</p>", unsafe_allow_html=True)
    with col5:
        st.markdown("<p style='text-align: center; color: white;'>Album</p>", unsafe_allow_html=True)
    with col6:
        st.markdown("<p style='text-align: center; color: white;'>Listen</p>", unsafe_allow_html=True)
        
    for i in range(len(Result['rank'])):
        col1=st.columns([4,2,5,4,4,3])
        with col1[0]:
            st.image(Result['album_thumbnail'][i][1]['url'])
        with col1[1]:
            st.write(Result['rank'][i])
        with col1[2]:
            st.write(Result['track_name'][i])
        with col1[3]:
            st.write(Result['artist_name'][i])
        with col1[4]:
            st.write(Result['album_name'][i])
        with col1[5]:
            st.write('[Listen On Spotify](%s)'%Result['track_url'][i])

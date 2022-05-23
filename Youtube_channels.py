import streamlit as st
import youtube_channels_helper

def Youtube_display(Result):
    channel_dict=youtube_channels_helper.get_channel_details_by_search(Result)
    col=st.columns([4,5,3,3,2])
    with col[0]:
        st.markdown("<p style='text-align: center; color: white;'>Thumbnail</p>", unsafe_allow_html=True)
    with col[1]:
        st.markdown("<p style='text-align: left; color: white;'>Channel Name</p>", unsafe_allow_html=True)
    with col[2]:
        st.markdown("<p style='text-align: center; color: white;'>Subscribers</p>", unsafe_allow_html=True)
    with col[3]:
        st.markdown("<p style='text-align: center; color: white;'>Views</p>", unsafe_allow_html=True)
    with col[4]:
        st.markdown("<p style='text-align: center; color: white;'>totalVideos</p>", unsafe_allow_html=True)

    col1=st.columns([4,5,3,3,2])
    with col1[0]:
        st.image(channel_dict['thumbnails']['url'])
    with col1[1]:
        st.write(channel_dict['channelName'])
    with col1[2]:
        st.write(channel_dict['subscribers'])
    with col1[3]:
        st.write(channel_dict['views'])
    with col1[4]:
        st.write(channel_dict['totalVideos'])

    st.info('Top Videos of this Channel')
    video_detail=youtube_channels_helper.get_all_video_details_by_channel_search(Result)
    top_vids=youtube_channels_helper.top_videos_of_channel(video_detail,amount=10)
    # st.table(top_vids)
    # Thumbnails channelTitle	title	publishedAt	viewCount	likeCount	commentCount	duration
    col0,col2,col3,col4,col5,col7 =st.columns([4,4,3,3,2,2])
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
   
    with col7:
        st.markdown("<p style='text-align: center; color: white;'>Duration(s)</p>", unsafe_allow_html=True)
    
    for i in range(len(top_vids['channelTitle'])):
        col1=st.columns([4,4,3,3,2,2])
        with col1[0]:
            st.image(top_vids['thumbnails'].values[i]['url'])
        with col1[1]:
            st.write(top_vids['title'].values[i])          
        with col1[2]:
            st.write(top_vids['channelTitle'].values[i])
        with col1[3]:
            st.write(str(top_vids['viewCount'].values[i]))
        with col1[4]:
            if(str(top_vids['likeCount'].values[i]))=='nan':
                st.write('Not Provided')
            st.write(str(top_vids['likeCount'].values[i]))
        with col1[5]:
            st.write(str(top_vids['duration'].values[i]))
         
    st.info('Video Viewcount analysis')
    st.pyplot(youtube_channels_helper.violinplot(video_detail))
    st.success('This plot shows the viewcount in the y axis and the width of the plot which is the x axis corresponds to the amount of videos that possess that viewcount. This graph is useful in analyzing the performance of the videos of the channel.')
    st.write('Interpretation:')
    st.write('If a very long graph is obtained, it means that the variability in video performance is high. There are videos with very low view count and some videos with very high viewcount.')
    st.write('The point where the graph is the widest signifies the general performance of the videos.')
    
    st.info('Correlation Analysis')
    st.pyplot(youtube_channels_helper.stat_analysis_fig(video_detail))
    st.success('This scatter plot shows if there is any corelation between the three metrics of a video, that is, the view count, like count, and the comment count.')
    st.write('Interpretation:')
    st.write('If a strong corelation between the metrics is present, the scatter plot will signify a positive slope line. ')
    
    st.info('Duration Analysis')
    st.pyplot(youtube_channels_helper.duration_analysis(video_detail))
    st.success('This plot provides a correlation analysis between the duration of a video and how much views or likes the video gets as the duration increases.')
    st.write('Interpretation:')
    st.write('The points being lower and closer to the x axis after a point shows that as the duration of the videos increases, the amount of views and likes the video gets keeps declining. This shows a general trend in people wanting to consume short form video content on youtube.')
    





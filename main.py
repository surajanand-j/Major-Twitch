import streamlit as st
from pandas.io.json import json_normalize
import time
import Footer
import Insert
import Search_channel
import Channels
import Games
import spotify 
import Fetch
from top_50_for_today import Top_tracks_all_time

import Youtube_channels 
import Youtube_Alltime

    # st.write(access_token)
st.sidebar.write('MENU')
Fields=st.sidebar.radio(
     "Choose Any one",
     ('Spotify', 'Twitch', 'Youtube'))
Menu=['Channels','Categories', 'Search Channel', 'Know Twitch Better']
Menu1=['Spotify\'s Today\'s Hits','Know Spotify Better','Spotify\'s All Time Hits']
Menu2=['Search in Youtube','Youtube\'s All Time Hits','Know Youtube Better']
if Fields=='Twitch':
    option=st.sidebar.selectbox("Look into Twitch",Menu,3)
elif Fields=='Spotify':
    option1=st.sidebar.selectbox("Look into Spotify",Menu1,1)
elif Fields=='Youtube':
    option2=st.sidebar.selectbox("Look into Youtube",Menu2,2)
# Menu2=['Spotify']
# option2=st.sidebar.selectbox("Look into Spotify",Menu2)


def loading_bar():
    # displays a loading bar that shows how much the page has loaded.
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1)

def header_print():
    st.markdown("<h1 style='text-align: center; color: ;'>Metrics YouTwitchify</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: ;'>Leaderboards and Metrics of Internet's Video, Livestream and Music Content All-In-One place </h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: ;'>Welcome to Metrics YouTwitchify.<br> This website was created as a final year project as CS students. <br>We hope you find it useful!</p>", unsafe_allow_html=True)
    
    # st.header("Metrics Twitchify")
    # st.write("Welcome to Metrics Twitchify. This website was created as a final year project as CS students. We hope you find it useful!")

#Page 1 Top Games
if Fields=='Twitch' and option=='Categories':
    header_print()
    loading_bar()

    def insert_games():
        Insert.exec()
    insert_games()
    # @st.cache
    
    Games.twitch()

#Page 2 Channels/Streamers
elif Fields=='Twitch' and option=='Channels':
    header_print()
    loading_bar()
       
    def insert_stream():
        Insert.exec1()
    # def repeat():
    #     threading.Timer(1000.0, repeat).start()
    #     insert_stream()
    insert_stream()
    Channels.twitch1()
        
    

elif Fields=='Twitch' and option=='Search Channel':
    header_print()
    loading_bar()
    Search_channel.search_channel()

elif Fields=='Twitch' and option=='Know Twitch Better':
#else:
    header_print()
    loading_bar()
    st.header("What is Twitch?")
    st.write("Twitch is a popular online service used to watch and stream digital video broadcasts. It originally focused almost entirely on video games but has since expanded to include streams dedicated to artwork creation, music, talk shows, and the occasional TV series.")
    st.header("Where Can I Watch Twitch?")
    st.write("Twitch streams can be viewed on the official Twitch website - Twitch.tv and via one of the many official Twitch apps. Watching broadcasts and videos on Twitch is completely free and doesn't require viewers to log in. Creating an account, however, does allow users to add their favorite channels to a follow list and participate in each stream's unique chatroom. Hosting is a popular way for Twitch streamers to broadcast another channel's live stream to their own audience.")
    st.header("How Can I Find Twitch Streamers to Watch?")
    st.write("Twitch recommends streams on the front page of its website and its apps. Another popular way to discover new Twitch channels to watch is by browsing the Games category. This option is available on all of the apps and the Twitch website and is an easy way to find a live stream relating to a specific video game title or series.")
    st.write("Alternatively, you can use our website - Metrics Twitchify, for browsing the popular streams or browse the popular streams based on which game category.")
    st.write("You can go to the Channels page to see the top active streams on the whole website right and see if you like anything.")
    st.write("You can go to the Games page to browse active streams that are in that particular game category and live at the moment.")
    st.write("Finally, you can use the Search page to search for any streamer using a name that you will enter.")
    st.write("Additionally We have provided details about Twitch in the Know Twitch Better page where we have talked about the basics about twitch and how our website can be utilized.")
    st.header("What are Emotes?")
    st.write("When words just aren’t enough, there’s Emotes: Twitch-specific emoticons that viewers and streamers use to express a number of feelings in chat. Emotes are the <3 of Twitch culture. They’re a language of their own. They’re also a way for Partners and Affiliates to reinforce their branding and personalities, and give fans ways to celebrate epic moments, poke fun at fails, spread love in chat, and become active members of your community.")
elif Fields=='Spotify' and option1=='Spotify\'s Today\'s Hits':
    header_print()
    loading_bar()
    st.subheader('Today\'s Top Hits')
    Result=Fetch.Spotify_data()
    spotify.spotify_display(Result)
    Insert.insert_spotify_data()
elif Fields=='Spotify' and option1=='Spotify\'s All Time Hits':
    header_print()
    loading_bar()
    st.subheader('All Time Top Hits')
    spotify.spotify_display(Top_tracks_all_time)


elif Fields=='Spotify' and option1=='Know Spotify Better':
    header_print()
    loading_bar()
    st.header("What is Spotify?")
    st.write("Spotify is a digital music, podcast, and video service that gives you access to millions of songs and other content from creators all over the world.")
    st.write("Basic functions such as playing music are totally free, but you can also choose to upgrade to Spotify Premium.")
    st.header("Where can I use Spotify?")
    st.write("Spotify is available across a range of devices, including computers, phones, tablets, speakers, TVs, and cars, and you can easily transition from one to another with Spotify Connect.")
    st.header("Can I keep music from Spotify?")
    st.write("Spotify only gives access to music and podcasts through our apps. Our licensing means there's no way to export our content outside of the app.")

elif Fields=='Youtube' and option2=='Search in Youtube':
    header_print()
    loading_bar()
    st.subheader('Search Channel On Youtube')
    with st.form(key='my_form'):
        text_input = st.text_input(label='Enter')
        submit_button = st.form_submit_button(label='Find')   
    if text_input:
        Youtube_channels.Youtube_display(text_input)
    

    # Spotify_analysis.display()
elif Fields=='Youtube' and option2=='Youtube\'s All Time Hits':
    header_print()
    loading_bar()
    st.subheader('Top 50 Videos of all time')
    Youtube_Alltime.alltime_display()
elif Fields=='Youtube' and option2=='Know Youtube Better':
    header_print()
    loading_bar()
    st.header("What Is YouTube?")

    st.write("YouTube is an American online video sharing and social media platform. it is a free video sharing website that makes it easy to watch online videos. You can even create and upload your own videos to share with others. Owned by Google, it is the second most visited website, right after Google itself.")
    st.header("Why use YouTube?")

    st.write("One reason YouTube is so popular is the sheer number of videos you can find. On average, 100 hours of video are uploaded to YouTube every minute, so there's always something new to watch! And you'll find all kinds of videos on YouTube, quite literally anything you feel like watching content on will be found on YouTube. Film and television companies maintain a tight control over their own content and block illegal sharing of their content. With user generated content, it can cater to any niche. Many use it for entertainment purposes, for learning how to do something (tutorials), for keeping up with their favorite artists' latest music videos, and more.")

    st.header("Where can I watch videos on YouTube?")

    st.write("Navigating to youtube.com and watching a suggested video or searching for one. or you can download the YouTube mobile app for iOS or Android and do the same there. You can watching a YouTube video that was embedded into a post on a social network (like Facebook or Twitter). You can Watch a YouTube video that was embedded into a web page or blog post.")



Footer.footer()



from pymongo import MongoClient
import streamlit as st
import config
import pymongo
client = MongoClient(config.CONNECTION_STRING)
db=client['Twitch']
def games_data():
    col=db['Games']
    res=col.find_one(sort=[( 'Time', -1 )])
    return res
# st.write(res)

def stream_data():
    col1=db['Streams']
    report = col1.find_one(sort=[( 'Time', -1 )])
    return report
# st.write(report)
def Spotify_data():
    col2=db['Spotify Data']
    res2=col2.find
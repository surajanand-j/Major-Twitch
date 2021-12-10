from pymongo import MongoClient
import streamlit as st
import config
import pymongo
client = MongoClient(config.CONNECTION_STRING)
db=client['Twitch']
col=db['Games']
#games
res=col.find_one(sort=[( 'Time', -1 )])
# st.write(res)


col1=db['Streams']
#streamers
report = col1.find_one(sort=[( 'Time', -1 )])
# st.write(report)

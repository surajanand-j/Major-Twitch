from pymongo import MongoClient
import streamlit as st
import config
import pymongo
client = MongoClient(config.CONNECTION_STRING)
db=client['Twitch']
col=db['Games']
res=col.find_one()

col1=db['Streams']
report = col1.find_one(
  
#   sort=[( '_id', -1 )]
)

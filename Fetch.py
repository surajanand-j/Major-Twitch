from pymongo import MongoClient
import config
client = MongoClient(config.CONNECTION_STRING)
db=client['Twitch']
col=db['Games']
res=col.find_one()
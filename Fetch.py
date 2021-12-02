from pymongo import MongoClient
CONNECTION_STRING = "mongodb+srv://suraj:wtcsproject@wtcs.sweig.mongodb.net/wtcsproject?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db=client['Twitch']
col=db['Games']
res=col.find_one()
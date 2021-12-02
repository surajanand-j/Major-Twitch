
from pymongo import collection
import json
import requests
client_id= 'kfdicyd8nct8dwqd8vy7zrc8jn5sfw'
client_secret= 'o77rnssqevendjf22z2sb21erif5n9'

#Request for the access code using requests library
access_code = requests.post('https://id.twitch.tv/oauth2/token?client_id='+str(client_id)+'&client_secret='+str(client_secret)+'&grant_type=client_credentials')

#access token response is a JSON-encoded app access token
access_token = json.loads(access_code.text)
access_token = access_token['access_token']



from pymongo import MongoClient

headers = {
            'Client-ID' : client_id,
            'Authorization' : 'Bearer '+str(access_token),
        }
def exec():
    CONNECTION_STRING = "mongodb+srv://suraj:wtcsproject@wtcs.sweig.mongodb.net/wtcsproject?retryWrites=true&w=majority"
 
    client = MongoClient(CONNECTION_STRING)
    games_response = requests.get('https://api.twitch.tv/helix/games/top?first=15', headers=headers)
    
    games_response_json = json.loads(games_response.text)
    dbname = client['Twitch']
    if games_response.status_code != 500:
        if('Games' in dbname.list_collection_names()):
            dbname['Games'].drop()

    collection_name = dbname["Games"]

    if isinstance(games_response_json, list):
        collection_name.insert_many(games_response_json)  
    else:
        collection_name.insert_one(games_response_json)
# print(collection_name)
# print(games_response_json)



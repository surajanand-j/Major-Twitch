
from pymongo import collection
import json
import requests
import config
from datetime import datetime

#Request for the access code using requests library
access_code = requests.post('https://id.twitch.tv/oauth2/token?client_id='+str(config.client_id)+'&client_secret='+str(config.client_secret)+'&grant_type=client_credentials')

#access token response is a JSON-encoded app access token
access_token = json.loads(access_code.text)
access_token = access_token['access_token']



from pymongo import MongoClient

headers = {
            'Client-ID' : config.client_id,
            'Authorization' : 'Bearer '+str(access_token),
        }
def exec():
 
    client = MongoClient(config.CONNECTION_STRING)
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
def exec1():
    client = MongoClient(config.CONNECTION_STRING)
    stream_response = requests.get('https://api.twitch.tv/helix/streams', headers=headers)
    stream_response_json = json.loads(stream_response.text)
    now=datetime.now()
    formatted_datetime =now.isoformat()
    dict={"Time":formatted_datetime}
    # json_datetime = json.loads(json.dumps(formatted_datetime))
    stream_response_json.update(dict)
    dbname = client['Twitch']
    collection_name = dbname["Streams"]

    if isinstance(stream_response_json, list):
        collection_name.insert_many(stream_response_json)  
    else:
        collection_name.insert_one(stream_response_json)



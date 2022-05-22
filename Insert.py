
from pymongo import collection
import json
import requests
import config
from datetime import datetime
from pytz import timezone
import top_50_for_today
#Request for the access code using requests library
# access_code = requests.post('https://id.twitch.tv/oauth2/token?client_id='+str(config.client_id)+'&client_secret='+str(config.client_secret)+'&grant_type=client_credentials')

#access token response is a JSON-encoded app access token
access_token = json.loads(config.access_code.text)
access_token = access_token['access_token']



from pymongo import MongoClient

headers = {
            'Client-ID' : config.client_id,
            'Authorization' : 'Bearer '+str(access_token),
        }
        
def exec():
 
    client = MongoClient(config.CONNECTION_STRING)
    games_response = requests.get('https://api.twitch.tv/helix/games/top?first=6', headers=headers)
    games_response_json = json.loads(games_response.text)


    #adding time to top games
    now=datetime.now(timezone("Asia/Kolkata"))
    formatted_datetime =now.isoformat()
    dict={"Time":formatted_datetime}
    games_response_json.update(dict)

    dbname = client['Twitch']
    # if games_response.status_code != 500:
    #     if('Games' in dbname.list_collection_names()):
    #         dbname['Games'].drop()

    collection_name = dbname["Games"]

    if isinstance(games_response_json, list):
        collection_name.insert_many(games_response_json)  
    else:
        collection_name.insert_one(games_response_json)
# print(collection_name)
# print(games_response_json)

def exec1():
    client = MongoClient(config.CONNECTION_STRING)
    stream_response = requests.get('https://api.twitch.tv/helix/streams?first=11', headers=headers)
    stream_response_json = json.loads(stream_response.text)

    now=datetime.now(timezone("Asia/Kolkata"))
    formatted_datetime =now.isoformat()
    dict={"Time":formatted_datetime}
    # json_datetime = json.loads(json.dumps(formatted_datetime))
    stream_response_json.update(dict)
    dbname = client['Twitch']
    collection_name = dbname["Streams"]
    collection_name.delete_many({'error':"Unauthorized"})
    if isinstance(stream_response_json, list):
        collection_name.insert_many(stream_response_json)  
    else:
        collection_name.insert_one(stream_response_json)

def insert_spotify_data():
    client = MongoClient(config.CONNECTION_STRING)
    dbname=client['Twitch']
    collection_name=dbname['Spotify Data']
    # Top_tracks_today.reset_index(inplace=True)
    # # now=datetime.now(timezone("Asia/Kolkata"))
    # # formatted_datetime =now.isoformat()
    # # dict={"Time":formatted_datetime}
    # data_dict = Top_tracks_today
    # data_dict.update(dict)
    collection_name.insert_one(top_50_for_today.get_playlist_track_info())


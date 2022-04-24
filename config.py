import requests
import json
CONNECTION_STRING = "mongodb+srv://suraj:wtcsproject@wtcs.sweig.mongodb.net/wtcsproject?retryWrites=true&w=majority"
client_id= 'kfdicyd8nct8dwqd8vy7zrc8jn5sfw'
client_secret= 'o77rnssqevendjf22z2sb21erif5n9'
access_code = requests.post('https://id.twitch.tv/oauth2/token?client_id='+str(client_id)+'&client_secret='+str(client_secret)+'&grant_type=client_credentials')
access_token = json.loads(access_code.text)
access_token = access_token['access_token']
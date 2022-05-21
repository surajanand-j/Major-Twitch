import requests
import datetime
from urllib.parse import urlencode
import pandas as pd
import base64
import requests
import pandas as pd

# from skimage import io
import matplotlib.pyplot as plt


client_id = '08e04f879f8f47bcbd25377aec2133f4'
client_secret = '7e78874a40d342c3889e0c82bfd6b6fa'
redirect = 'http://localhost:7777/callback'

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"
    
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    
    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }
    
    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        } 
    
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True
        
    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token() 
        return token
    
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    def search(self, query, search_type='artist' ): # type artist
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        data = urlencode({"q": query, "type": search_type.lower()})
        lookup_url = f"{endpoint}?{data}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):  
            return {}
        return r.json()

    def search_generic(self, query, search_type, limit=1): # type mention
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        data = urlencode({"q": query, "type": search_type.lower(), "limit": int(limit)})
        lookup_url = f"{endpoint}?{data}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):  
            return {}
        return r.json()

    def get_playlist_tracks(self, playlist_id):
        headers = self.get_resource_header()
        lookup_url = 'https://api.spotify.com/v1/playlists/'+playlist_id+'/tracks'
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):  
            return {}
        return r.json()

    def get_track(self, track_id):
        headers = self.get_resource_header()
        lookup_url = 'https://api.spotify.com/v1/tracks/'+track_id
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):  
            return {}
        return r.json()

spotify = SpotifyAPI(client_id, client_secret)

def get_playlist_track_info(search_q = 'Global Top', type_q='playlist'):
    top_50_playlist = spotify.search_generic(search_q, type_q)
    playlist_tracks_request = spotify.get_playlist_tracks(top_50_playlist['playlists']['items'][0]['id'])

    rank = []
    album_name = []
    artist_name = []
    track_name = []
    track_popularity = []
    id = []
    preview_url = []
    track_url = []
    album_thumbnail = []

    for i, track in enumerate(playlist_tracks_request['items']): #looping through all tracks in playlist
        rank.append(i+1)
        album_name.append(track['track']['album']['name'])
        artist_name.append(track['track']['artists'][0]['name'])
        track_name.append(track['track']['name'])
        track_popularity.append(track['track']['popularity'])
        id.append(track['track']['id'])
        preview_url.append(track['track']['preview_url'])
        track_url.append(track['track']['external_urls']['spotify'])
        album_thumbnail.append(track['track']['album']['images'])


    track_dict = {'rank': rank, 
    'album_name': album_name, 
    'artist_name': artist_name, 
    'track_name': track_name, 
    'track_popularity': track_popularity, 
    'id': id, 
    'preview_url': preview_url, 
    'track_url': track_url, 
    'album_thumbnail': album_thumbnail}

    return track_dict


Top_tracks_today = get_playlist_track_info()

    


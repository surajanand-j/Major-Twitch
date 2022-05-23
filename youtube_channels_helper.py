from googleapiclient.discovery import build
from dateutil import parser
import pandas as pd
from IPython.display import JSON

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import random
import isodate

# %matplotlib inline


# Helper functions

def build_youtube():
    api_service_name = "youtube"
    api_version = "v3"
    developer_key=[]

    developer_key.append('AIzaSyA0DvUPENuoYgUnaXnFFAQ0mWjCLzOkUbk')
    developer_key.append('AIzaSyAHddqbcSENsC5hyfXcK6gOrcxwsgJJLb4')
    developer_key.append('AIzaSyBZcdVS9CnU08k1VvAUph47BkY6lhK8CFQ')
    developer_key.append('AIzaSyBqh7alvQs4KVf9xp_C4-Uapf8JzH49bJw')
    developer_key.append('AIzaSyCg3rUiRNxAgbuLMI58IU0wttE0Kw1jrsA')
    developer_key.append('AIzaSyBOcJn10VzXgtpBSuhd1R-8yCD1CRecVog')
    
    key_num = random.randint(0,len(developer_key)-1)
    youtube = build(api_service_name, api_version, developerKey = developer_key[key_num])
    return youtube

def search_channel_id(search_text):

    youtube = build_youtube()

    response = youtube.search().list(
                part= "snippet",
                q = search_text,
                type="channel",
                maxResults = 1
        ).execute()
    
    channel_id = response['items'][0]['id']['channelId']
    return channel_id

def get_channel_details(search_id):

    youtube = build_youtube()
    request = youtube.channels().list(
            part = "snippet,contentDetails,statistics",
            id = search_id
        )

    response = request.execute()

    try:
        for i in range(len(response['items'])):
            data = dict(channelName = response['items'][i]['snippet']['title'],
                        id = response['items'][i]['id'],
                        thumbnails = response['items'][i]['snippet']['thumbnails']['medium'],
                        subscribers = response['items'][i]['statistics']['subscriberCount'],
                        views = response['items'][i]['statistics']['viewCount'],
                        totalVideos = response['items'][i]['statistics']['videoCount'],
                        playlistId = response['items'][i]['contentDetails']['relatedPlaylists']['uploads']
                        )
    except:
        print('error in searching channel by this name')
        return {}

    return data

def get_video_ids(playlist_id):
    
    video_ids = []
    youtube = build_youtube()

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id,
        maxResults = 50
    )
    response = request.execute()
    
    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])
        
    next_page_token = response.get('nextPageToken')
    while next_page_token is not None:
        request = youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId = playlist_id,
                    maxResults = 50,
                    pageToken = next_page_token)
        response = request.execute()

        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = response.get('nextPageToken')
        
    return video_ids

def get_video_details(video_ids):

    youtube = build_youtube()
    all_video_info = []
    
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute() 

        for video in response['items']:
            stats_to_keep = {'snippet': ['channelTitle', 'title', 'publishedAt', 'thumbnails'],
                             'statistics': ['viewCount', 'likeCount', 'commentCount'],
                             'contentDetails': ['duration']
                            }
            video_info = {}
            video_info['video_id'] = video['id']

            for k in stats_to_keep.keys():
                for v in stats_to_keep[k]:
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info[v] = None

            #converting duration into seconds
            video_info['duration'] = isodate.parse_duration(video_info['duration'])
            video_info['duration'] = video_info['duration'].total_seconds()

            video_info['publishedAt'] = parser.parse(video_info['publishedAt'])
            video_info['thumbnails'] = video_info['thumbnails']['medium']

            all_video_info.append(video_info)
    
    all_video_info = pd.DataFrame(all_video_info)
    numeric_cols = ['viewCount', 'likeCount', 'commentCount']
    all_video_info[numeric_cols] = all_video_info[numeric_cols].apply(pd.to_numeric, errors = 'coerce', axis = 1)

    return all_video_info

def search_playlist_id(search_text = 'Most Viewed Videos of All Time'):

    youtube = build_youtube()

    response = youtube.search().list(
                part= "snippet",
                q = search_text,
                type="playlist",
                maxResults = 1
        ).execute()
    
    playlist_id = response['items'][0]['id']['playlistId']
    return playlist_id



# ALL ENCOMPASSING FUNCTIONS BELOW

def get_all_video_details_by_channel_search(search_text):
    id = search_channel_id(search_text)
    channel_data = get_channel_details(id)
    video_df = get_video_details(get_video_ids(channel_data['playlistId']))
    return video_df

def get_channel_details_by_search(search_text):
    return get_channel_details(search_channel_id(search_text))

def get_all_video_details_by_playlist_search(search_text='Most Viewed Videos of All Time'):
    id = search_playlist_id(search_text)
    video_df = get_video_details(get_video_ids(id))
    return video_df

# Analysis functions

def top_videos_of_channel(df, parameter='viewCount', amount = 5):
    # parameter = 'viewCount' or 'likeCount' or 'commendCount' or 'duration'
    return df.sort_values(parameter, ascending=False)[:amount]

def violinplot(df):
    fig = plt.figure(figsize=(8,6))
    sns.violinplot(df['channelTitle'], df['viewCount'])
    return fig

def stat_analysis_fig(df):
    fig, ax = plt.subplots(1,3, figsize=(16,7))
    sns.scatterplot(data = df, x = 'commentCount', y = 'viewCount', ax = ax[0])
    sns.scatterplot(data = df, x = 'likeCount', y = 'viewCount', ax = ax[1])
    sns.scatterplot(data = df, x = 'likeCount', y = 'commentCount', ax = ax[2])

    return fig

def durationplot(df):
    fig = plt.figure(figsize=(8,6))
    sns.distplot(df['duration'])

    return fig
def duration_analysis(df):
    fig, ax = plt.subplots(1,2, figsize=(16,5))
    sns.scatterplot(data = df, x = 'duration', y = 'viewCount', ax = ax[0])
    sns.scatterplot(data = df, x = 'duration', y = 'likeCount', ax = ax[1])

    return fig
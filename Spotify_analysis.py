# import streamlit as st
# import seaborn as sns
# import matplotlib.pyplot as plt
# import pandas as pd
# from pymongo import MongoClient

# def years_vs_duration(df_tracks):
#     years = df_tracks.dates.dt.year.values
#     fig2, ax = plt.subplots(figsize=(18,6))
#     plt.xticks(rotation=90)
#     sns.barplot(x = years, y = df_tracks.duration_s, ax = ax, errwidth = False).set(title='Years vs Duration')

#     return fig2
# def duration_vs_genre(genres):
#     fig = plt.figure(figsize=(12,6))
#     plt.title('Duration of songs in different Genres')
#     sns.color_palette('rocket')
#     sns.barplot(y='genre', x='duration_ms', data=genres)
#     plt.xlabel('Duration in milliseconds')
#     plt.ylabel('Genres')

#     return fig


# def fetch_spotify_analysis():
#     CONNECTION_STRING = "mongodb+srv://suraj:wtcsproject@wtcs.sweig.mongodb.net/wtcsproject?retryWrites=true&w=majority"
#     client = MongoClient(CONNECTION_STRING)
#     db=client['Twitch']
#     col=db['Streams']
#     cursor=col.find()
#     mongo_docs = list(cursor)
#     col=db['Streams']
#     cursor=col.find()
#     mongo_docs = list(cursor)
#     docs = pd.DataFrame(columns=["_id","release_date","dates","duration_s"])
#     for num, doc in enumerate( mongo_docs ):
#         # convert ObjectId() to str
#         doc["_id"] = str(doc["_id"])
#         # get document _id from dict
#         doc_id = doc["_id"]
#         # create a Series obj from the MongoDB dict
#         series_obj = pd.Series(doc, name=doc_id)
#         # append the MongoDB Series obj to the DataFrame obj
#         docs = docs.append( series_obj )
#     return docs
# def fetch_spotify_analysis2():
#     CONNECTION_STRING = "mongodb+srv://suraj:wtcsproject@wtcs.sweig.mongodb.net/wtcsproject?retryWrites=true&w=majority"
#     client = MongoClient(CONNECTION_STRING)
#     db=client['Twitch']
#     col=db['Spotify Analysis Genre']
#     cursor=col.find()
#     mongo_docs = list(cursor)
#     docs = pd.DataFrame(columns=["_id","genre","artist_name","track_name","track_id","popularity","acousticness","danceability","duration_ms",
#                                 "energy","instrumentalness","key","liveness","loudness","mode","speechiness","tempo","time_signature","valence"])
    
#     for num, doc in enumerate( mongo_docs ):
#         # convert ObjectId() to str
#         doc["_id"] = str(doc["_id"])
#         # get document _id from dict
#         doc_id = doc["_id"]
#         # create a Series obj from the MongoDB dict
#         series_obj = pd.Series(doc, name=doc_id)
#         # append the MongoDB Series obj to the DataFrame obj
#         docs = docs.append( series_obj )
#     return docs 
# # st.pyplot(years_vs_duration(tracks)) 


# # tracks = pd.read_csv('spotify_tracks_data.csv')
# def display():
#     # docs=fetch_spotify_analysis()
#     # docs2=fetch_spotify_analysis2()
#     # # st.pyplot(years_vs_duration(docs))
#     # st.pyplot(duration_vs_genre(docs2))

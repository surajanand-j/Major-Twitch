import pandas as pd
import json
import pandas as pd
from pymongo import MongoClient
import json


import pandas as pd
from pymongo import MongoClient

def Fetch_all_docs():
    CONNECTION_STRING = "mongodb+srv://suraj:wtcsproject@wtcs.sweig.mongodb.net/wtcsproject?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    db = client['Twitch']
    col = db['Streams']
    cursor = col.find()
    mongo_docs = list(cursor)
    
    # Initialize an empty list to hold the Series objects
    series_list = []

    for num, doc in enumerate(mongo_docs):
        # Convert ObjectId() to str
        doc["_id"] = str(doc["_id"])
        # Get document _id from dict
        doc_id = doc["_id"]
        # Create a Series obj from the MongoDB dict
        series_obj = pd.Series(doc, name=doc_id)
        # Append the MongoDB Series obj to the list
        series_list.append(series_obj)

    # Concatenate all Series objects into a DataFrame
    docs = pd.concat(series_list, axis=1).T

    # Ensure columns are in the desired order
    docs = docs.reindex(columns=["Time", "_id", "data", "pagination.cursor"])

    return docs

# # Example usage
# docs = Fetch_all_docs()
# print(docs)


# def Fetch_all_docs():
#     CONNECTION_STRING = "mongodb+srv://suraj:wtcsproject@wtcs.sweig.mongodb.net/wtcsproject?retryWrites=true&w=majority"
#     client = MongoClient(CONNECTION_STRING)
#     db=client['Twitch']
#     col=db['Streams']
#     cursor=col.find()
#     mongo_docs = list(cursor)
#     col=db['Streams']
#     cursor=col.find()
#     mongo_docs = list(cursor)
#     docs = pd.DataFrame(columns=["Time","_id","data","pagination.cursor"])

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
    

# def viewcount_data_create(df):
#     dict_format = {'time': [], 'user_name': [], 'viewer_count': []}
#     for r in df[['Time', 'data']].values:
#         for entry in r[1]:
#             dict_format['time'].append(r[0])
#             dict_format['user_name'].append(entry['user_name'])
#             dict_format['viewer_count'].append(entry['viewer_count'])
#     return pd.DataFrame.from_dict(dict_format)

def viewcount_data_create(df):
    dict_format = {'time': [], 'user_name': [], 'viewer_count': []}
    
    # Use pandas' explode method to simplify the nested iteration
    exploded_df = df.explode('data')
    
    # Extract values from exploded 'data' column
    dict_format['time'] = exploded_df['Time'].tolist()
    dict_format['user_name'] = exploded_df['data'].apply(lambda x: x['user_name']).tolist()
    dict_format['viewer_count'] = exploded_df['data'].apply(lambda x: x['viewer_count']).tolist()
    
    return pd.DataFrame(dict_format)




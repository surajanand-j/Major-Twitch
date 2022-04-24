import pandas as pd
import json

def viewcount_data_create():
    file_path = 'Streams.csv'
    df = pd.read_csv(file_path)
    df.dropna(inplace=True)

    dict_format = {'time': [], 'user_name': [], 'viewer_count': []}

    for r in df[['Time', 'data']].values:
        for entry in json.loads(r[1]):
            dict_format['time'].append(r[0])
            dict_format['user_name'].append(entry['user_name'])
            dict_format['viewer_count'].append(entry['viewer_count'])
    dict_format_1 = sorted(dict_format.items(), key=lambda x: x[0])

    pd.DataFrame(dict_format).to_csv('streams_processed.csv')



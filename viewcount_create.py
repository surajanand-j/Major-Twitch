import pandas as pd
import json


file_path = 'E:\Code dump\Major Project\Exported Data\Streams.csv'
df = pd.read_csv(file_path)
df.dropna(inplace=True)

dict_format = {'time': [], 'user_name': [], 'viewer_count': []}

for r in df[['Time', 'data']].values:
    for entry in json.loads(r[1]):
        dict_format['time'].append(r[0])
        dict_format['user_name'].append(entry['user_name'])
        dict_format['viewer_count'].append(entry['viewer_count'])

pd.DataFrame(dict_format).to_csv('E:\Code dump\Major Project\Exported Data\streams_processed.csv')

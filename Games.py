import streamlit as st
import config
import Fetch
import requests
import json
import Youtube

def twitch():
        # threading.Timer(100.0, twitch).start()
        
        st.subheader('Top Categories/Games On twitch Right Now')

        # Top Games
        headers = {
            'Client-ID' : config.client_id,
            'Authorization' : 'Bearer '+str(config.access_token),
        }
        
        # topgames_data = games_response_json['data']
        topgames_data_t=Fetch.games_data()
        # st.write(topgames_data_t)
        topgames_data=topgames_data_t['data']
        # topgames_data=json.loads(topgames_data_t.text)
        for message in topgames_data:
            game_name=message['name']
            # youtube
            video_url=[]
            yt_thumbnail=[]
            ##
            st.write('Game Name - ',game_name)
            col1, col2,col3 = st.columns(3)
            with col1:
                img=message['box_art_url'].replace("{width}", "150").replace("{height}", "200")
                st.image(img)
                clips_response=requests.get('https://api.twitch.tv/helix/clips?first=2&game_id='+message['id'],headers=headers)
                clips_response_json=json.loads(clips_response.text)
                clips_data=clips_response_json['data']
                # st.write(clips_response_json)
            with col2:
                st.markdown("<p style='text-align: center; color: white;'>Popular Streamers</p>", unsafe_allow_html=True)
                with st.expander('On Twitch'):
                    tempo=message['id']
                   
                    URL='https://api.twitch.tv/helix/streams?first=5&game_id={}'
                    final_url=URL.format(tempo)
                    stream_response = requests.get(final_url, headers=headers)
                    stream_response_json = json.loads(stream_response.text)
                    topstreamers_data=stream_response_json['data']
                    
                    count=1
                    for i in topstreamers_data:
                        st.success(str(count)+') '+i['user_name'])
                        count+=1
            with col3:
                Youtube.games(game_name,video_url,yt_thumbnail)

                    # st.write(stream_response_json)
            st.write('Popular clips of: '+game_name)
            filteredImages = []
            clips_link=[] 
            for ths in clips_data:
                filteredImages.append(ths['thumbnail_url'])
                clips_link.append(ths['url'])
            # caption = [] # your caption here
           
            cols = st.columns(4) 
            cols[0].image(filteredImages[0], width=150)
            with cols[0]:
                st.warning('[open in twitch](%s)'%clips_link[0])
            cols[1].image(filteredImages[1], width=150)
            with cols[1]:
                    st.warning('[open in twitch](%s)'%clips_link[1]) 
            cols[2].image(yt_thumbnail[0], width=150)
            with cols[2]:
                    st.warning('[open in Youtube](%s)'%video_url[0])
            cols[3].image(yt_thumbnail[1], width=150)
            with cols[3]:
                    st.warning('[open in Youtube](%s)'%video_url[1])     
            
                # st.write("[Open in Twitch](filteredImage['url'])")

        # topgames_df = pd.DataFrame.from_dict(json_normalize(topgames_data), orient='columns')
        # export_topgames_csv = topgames_df.to_csv (r'C:/Users/suraj_gjnx4vc/Desktop/Major Twitch/topgames.csv', index = None, header=True)
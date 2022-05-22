import streamlit as st

def search_spotify():
    st.subheader('Search Spotify Playlists')
    with st.form(key='my_form'):
        text_input = st.text_input(label='Enter')
        submit_button = st.form_submit_button(label='Find')
    if text_input:
        # use text_imput
        pass
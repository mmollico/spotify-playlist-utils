import pandas as pd
import streamlit as st
import spotipy
from spotipy import util

def spotify_auth():
    scope = 'user-library-read user-library-modify'
    redirect_uri = 'http://127.0.0.1:8080/'
    token = util.prompt_for_user_token(scope=scope, redirect_uri=redirect_uri)
    client = spotipy.Spotify(auth=token)
    return client

@st.cache
def get_user_playlists(client):

    playlists = client.current_user_playlists()

    playlists_list = []
    for playlist in playlists['items']:
        playlists_list.append([playlist['id'], playlist['name']])
    playlist_df = pd.DataFrame(playlists_list, columns=['id', 'name'])

    return playlist_df

@st.cache
def get_playlist(client, id):

    playlist = client.playlist_tracks(id)

    track_list = []
    for track in playlist['items']:
        artists = []
        for artist in track['track']['artists']:
            artists.append(artist['name'])

        id = track['track']['id']
        name = track['track']['name']
        artist = ", ".join(artists)
        track_list.append([id, name, artist])

    columns = ['id', 'song_name', 'artists']
    tracks_df = pd.DataFrame(track_list, columns=columns)
    return tracks_df

def like_all_playlist_tracks(client, tracks_df):
    client.current_user_saved_tracks_add(tracks=tracks_df['id'].tolist())
    return None

def main():
    
    # Setup
    st.set_page_config("Spotify Playlist Utils", page_icon="🎧")
    st.sidebar.image('static/images/spotify_banner_white.png')
    st.title('Spotify Playlist Utils')
    
    # Spotify
    client = spotify_auth()
    playlists = get_user_playlists(client)

    selected_playlist = st.sidebar.selectbox('Playlists', playlists.name)
    selected_playlist_id = playlists[playlists['name'] == selected_playlist]['id'].item()

    if selected_playlist_id is not None:
        playlist = get_playlist(client, str(selected_playlist_id))
        st.table(playlist)

    st.button(
        'Like All Playlist Tracks',
        on_click=lambda : like_all_playlist_tracks(client, playlist))

if __name__ == '__main__':
    main()

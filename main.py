import pandas as pd
import streamlit as st
import spotipy
from spotipy import util

def spotify_auth():
    scope = 'user-library-read'
    redirect_uri = 'http://127.0.0.1:8080/'
    token = util.prompt_for_user_token(scope=scope, redirect_uri=redirect_uri)
    client = spotipy.Spotify(auth=token)
    return client

@st.cache
def get_user_playlists(client):

    playlists = client.current_user_playlists()

    playlists_list = []
    for playlist in playlists['items']:
        playlists_list.append([playlist['name'], playlist['id']])
    playlist_df = pd.DataFrame(playlists_list, columns=['name', 'id'])

    return playlist_df

def get_playlist(client, id):

    playlist = client.playlist_tracks(id)

    track_list = []
    for track in playlist['items']:
        artists = []
        for artist in track['track']['artists']:
            artists.append(artist['name'])

        track = track['track']['name']
        artist = ", ".join(artists)
        track_list.append([track, artist])

    tracks_df = pd.DataFrame(track_list, columns=['song_name', 'artists'])
    return tracks_df

def main():
    
    # Setup
    st.sidebar.image('static/images/spotify_banner_white.png')
    st.sidebar.title('Spotify Playlist Utils')
    
    # Spotify
    client = spotify_auth()
    playlists = get_user_playlists(client)

    selected_playlist = st.selectbox('Playlists', playlists.name)
    selected_playlist_id = playlists[playlists['name'] == selected_playlist]['id'].item()

    if selected_playlist_id is not None:
        playlist = get_playlist(client, str(selected_playlist_id))
        st.table(playlist)

if __name__ == '__main__':
    main()

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd


client_id = ''
client_secret = ''
redirect_uri = ''
scope = 'playlist-modify-public playlist-modify-private'
user_id = ''

secrets_path = 'secrets.txt'
input_csv = 'top_50_recommendations.csv'

playlist_name = 'AutoEncoder RecSys'
description = 'Top 50 songs recommended by AutoEncoder Model'
public = 'True'


# setups for Spotify API useage
with open('secrets.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    client_id = lines[0][:-1]
    client_secret = lines[1][:-1]
    redirect_uri = lines[2][:-1]
    user_id = lines[3][:-1]


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope
))

# Get several Tracks to get uris
df = pd.read_csv(input_csv)

ids = df['id'].tolist()

tracks = sp.tracks(ids)
uris = []
for track in tracks['tracks']:
    uris.append(track['uri'])
    
# Create a playlist for the user
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=public, description=description)
playlist_id = playlist['id']

# Add songs to the playlist
sp.playlist_add_items(playlist_id, uris)

print(f"Added {len(uris)} tracks to playlist {playlist_name}")
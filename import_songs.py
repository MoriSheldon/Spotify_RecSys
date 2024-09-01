import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import csv

with open('secret.txt') as f:
    secret_ls = f.readlines()
    client_id = secret_ls[0][:-1]
    client_secret = secret_ls[1][:-1]
    redirect_uri = secret_ls[2][:-1]


scope = 'user-library-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

limit = 50
offset = 0
out_file = 'liked_songs.csv'

def main():
    liked_songs = get_liked_songs(sp, limit=limit, offset=offset)
    ids_string = ','.join(liked_songs)

    with open(out_file, mode='w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([ids_string])
    
    print(f"Audio features have been saved to {out_file}")


def get_liked_songs(sp, limit=20, offset=0):
    liked_songs = []
    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        
        if not results['items']:
            break
        
        for item in results['items']:
            track = item['track']
            liked_songs.append(
                track['id']
            )
        
        offset += limit
        time.sleep(0.1)
        if len(results['items']) < limit:
            break
        
    return liked_songs

main()
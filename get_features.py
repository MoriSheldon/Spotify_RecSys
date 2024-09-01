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

limit = 100
file_path = 'liked_songs.csv'
out_file = 'audio_features.csv'

def main():
    audio_features = get_audio_features(file_path, chunk_size=limit)

    with open(out_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=audio_features[0].keys())
        writer.writeheader()
        for feature in audio_features:
            writer.writerow(feature)

    print(f"Audio features have been saved to {out_file}")



def get_audio_features(file_path, chunk_size=100):
    all_features = []

    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        ids = next(reader)[0].split(',')

        for i in range(0, len(ids), chunk_size):
            chunk = ids[i:i + chunk_size]
            features = sp.audio_features(tracks=chunk)
            all_features.extend(features)
            time.sleep(0.1)

    return all_features

main()
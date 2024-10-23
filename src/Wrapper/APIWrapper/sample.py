
import sys
import pprint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Oath2
client_id      = "cf50f232d7384d6a94297f0130d64bc6"
client_secret  = "c4ae85dc52bb4f318a57cc2477fd3c13"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                           client_secret=client_secret))
# 検索
# search_str = sys.argv[1]

results = sp.search(q="冬の落ち着いた曲", limit=20, type='track', market = None)
for idx, track in enumerate(results['tracks']['items']):
    print(f"{idx:02d}\t{track['name']}\t")
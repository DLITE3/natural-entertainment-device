from dotenv import load_dotenv
load_dotenv()
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyWebAPIHandler:
    def __init__(self):
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
    
    def get_client_id(self):
        return self.client_id
    
    def get_client_secret(self):
        return self.client_secret

    def connected_to_spotify_web_api(client_id , client_secret):
       client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret) 
       spotify = spotipy.Spotify(client_credentials_managerclient_credentials_manager = client_credentials_manager)
       if(client_credentials_manager == True ):
         return ("success")
     
    def search_track_function(spotify=spotipy.Spotify):
         #search_str = sometext #chatGPTからのテキストを挿入する#
         results = spotify.search(q="冬の景色", limit=20, type='track', market ='JP')  #qにはキーワードを入れる。
         for idx, track in enumerate(results['tracks']['items']):
            print(f"{idx:03d}\t{track['name']}\t")


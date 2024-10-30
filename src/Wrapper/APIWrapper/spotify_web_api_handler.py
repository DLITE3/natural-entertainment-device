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
       
         

       
    #    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
    
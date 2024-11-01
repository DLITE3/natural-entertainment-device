from dotenv import load_dotenv
load_dotenv()
import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
class SpotifyWebAPIHandler:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self._req = requests   #リクエストを入れるもの
    
    def get_client_id(self):
        return self.client_id
    
    def get_client_secret(self):
        return self.client_secret


    # def connected_to_spotify_web_api(self, client_id , client_secret):
    #    client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret) 
    #    spotify = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    #    if(client_credentials_manager == True ):
    #     return ("success")
  
       
    #    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
    
    def connected_to_spotify_web_api( self ):    
        client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(SpotifyWebAPIHandler.get_client_id(self) , SpotifyWebAPIHandler.get_client_secret(self))
        sp = spotipy.Spotify(client_credentials_manager,status_forcelist = 200 )
        # 正常にクライアントが作成できたか確認
        response = self._req.get(sp.status_forcelist)
        return response.status_code 




import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pytest
import os
import sys
sys.path.append(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../APIWrapper')))
from  src.Wrapper.APIWrapper.spotify_web_api_handler import * #テストするファイルを参照
import requests



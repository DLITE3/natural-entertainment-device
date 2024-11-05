from dotenv import load_dotenv

class ImageToSongAPIWrapper():
    def __init__(self):
        self.image_to_song_api_url = load_dotenv("IMAGE_TO_SONG_API_URL")
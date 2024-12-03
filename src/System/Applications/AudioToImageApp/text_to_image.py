from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent.parent))

from src.Wrapper.APIWrapper.stable_diffusion_api_wrapper import StableDiffusionWrapper

import os
import base64
import time

class TextToImage:
    def __init__(self):
        self.stable_diffusion_api_wrapper = StableDiffusionWrapper()
          
    def generate_image(self, query: str) -> None:
        prompt = self.stable_diffusion_api_wrapper.text_to_image(query + "Watercolor style art.")
        image = self.stable_diffusion_api_wrapper.text_to_image(prompt)
        if image:
            self.stable_diffusion_api_wrapper.save_generate_image(image.get("image"))
            time.sleep(0.5)
        
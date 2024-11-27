import sys
import os
sys.path.append(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from src.Wrapper.APIWrapper.stable_diffusion_api_wrapper import StableDiffusionWrapper

class ConvertTexrToImage:
    def none():
     return None
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.Wrapper.APIWrapper.stable_diffusion_api_wrapper import StableDiffusionWrapper

def main():
    stable_diffusion_wrapper = StableDiffusionWrapper()
    prompt = "A beautiful sunset over the city."
    image = stable_diffusion_wrapper.text_to_image(prompt)
    stable_diffusion_wrapper.save_generate_image(image.get("image"))

if __name__ == "__main__":
    main()
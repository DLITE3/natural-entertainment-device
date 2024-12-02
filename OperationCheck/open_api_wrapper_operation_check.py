from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.Wrapper.APIWrapper.openai_api_wrapper import OpenAIAPIWrapper

def main():
    openai_api_wrapper = OpenAIAPIWrapper()
    response = openai_api_wrapper.post_request("空はなぜ青いのですか？")
    print(response.text)

if __name__ == "__main__":
    main()
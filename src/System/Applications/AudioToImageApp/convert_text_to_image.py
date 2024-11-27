import sys
import os
import base64
sys.path.append(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from src.Wrapper.APIWrapper.stable_diffusion_api_wrapper import StableDiffusionWrapper

class ConvertTexrToImage:
     def __init__(self):
          self.api_handler = StableDiffusionWrapper()


          
     def send_to_stable_diffusion( self , response):
         generate = self.api_handler.post_data(self, response)
         base64_image = generate.get("image")
         if base64_image:
                # Base64文字列をバイナリデータに変換
                image_data = base64.b64decode(base64_image)

                # 画像ファイルとして保存
                with open("output_image.jpeg", "wb") as f:
                    f.write(image_data)
                print("画像が保存されました: output_image.jpeg")
         else:
                print("画像データがレスポンスに含まれていません。")

         
         
        
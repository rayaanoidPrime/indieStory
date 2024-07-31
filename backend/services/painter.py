import torch
import requests
from io import BytesIO
from PIL import Image
from config import IndieStoryConfig

class PainterService:
    def __init__(self, config: IndieStoryConfig):
        self.config = config
        self.url = config.cf_host + config.painter
        self.headers = {
            'Authorization': f'Bearer {config.cf_token}',
        }
        self.data = {
            "prompt": ""
        }

    def paint(self, prompt: str) -> Image.Image:
        self.data["prompt"] = prompt
        response = requests.post(self.url, headers=self.headers, json=self.data)
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        return img
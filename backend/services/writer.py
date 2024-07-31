import torch
import requests
from config import IndieStoryConfig

class WriterService:
    def __init__(self, config: IndieStoryConfig):
        self.config = config
        self.url = config.cf_host + config.writer
        self.headers = {
            'Authorization': f'Bearer {config.cf_token}',
            'Content-Type': 'application/json'
        }
        self.data = {
            "messages": [
                {"role": "system", "content": "You are an expert scriptwriting assistant for children's short stories based on ancient Indian myths like the Mahabharata. You can only answer questions in the form of a short story."},
            ]
        }

    @torch.inference_mode()
    def write(self, prompt: str) -> str:
        self.data["messages"].append({"role": "user", "content": prompt})
        response = requests.post(self.url, headers=self.headers, json=self.data)
        response = response.json()
        return response["result"]["response"].split('<|im_end|>')[0]
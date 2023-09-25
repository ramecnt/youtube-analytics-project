import json
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()


class Channel:
    """Класс для ютуб-канала"""
    API_key = os.getenv("API_key")

    def __init__(self, channel_id: str) -> None:
        self.channel_id = channel_id
        self.youtube = build('youtube', 'v3', developerKey=self.API_key)
        self.channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

    def print_info(self) -> None:
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

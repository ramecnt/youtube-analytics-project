import json
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
from typing import Any, Optional, Dict

load_dotenv()


class Channel:
    """Класс для ютуб-канала"""
    __API_key = os.getenv("API_key")
    __youtube = build('youtube', 'v3', developerKey=__API_key)

    def __init__(self, channel_id: str) -> None:
        self._channel_id = channel_id
        self._channel = self.__youtube.channels().list(id=self._channel_id, part='snippet,statistics').execute()
        self.__items = self._channel.get('items')[0]
        self._title = self.__items['snippet']['title']
        self._description = self.__items['snippet']['description']
        self._url = self.__items['snippet']['customUrl']
        self._subscriber_count = self.__items['statistics']['subscriberCount']
        self._video_count = self.__items['statistics']['videoCount']
        self._view_count = self.__items['statistics']['viewCount']

    def __str__(self) -> str:
        return f'{self.title} ({self.url})'

    def __add__(self, other) -> int:
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count
    
    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def url(self) -> str:
        return "https://www.youtube.com/" + self._url

    @property
    def subscriber_count(self) -> int:
        return int(self._subscriber_count)

    @property
    def video_count(self) -> int:
        return int(self._video_count)

    @property
    def view_count(self) -> int:
        return int(self._view_count)

    @classmethod
    def get_service(cls) -> Any:
        return cls.__youtube

    @property
    def channel_id(self) -> str:
        return self._channel_id

    def print_info(self) -> None:
        print(json.dumps(self._channel, indent=2, ensure_ascii=False))

    def to_json(self, fp) -> None:
        with open(fp, 'w', encoding='utf-8') as f:
            js = {
                "id": self._channel_id,
                "title": self.title,
                "description": self.description,
                "url": self.url,
                "subscriber_count": self.subscriber_count,
                "video_count": self.video_count,
                "view_count": self.view_count
            }
            json.dump(js, f, indent=2, ensure_ascii=False)

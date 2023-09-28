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

    def __get_items(self) -> Optional[Dict]:
        return self._channel.get('items')[0]

    @property
    def title(self) -> str:
        return self.__get_items()['snippet']['title']

    @property
    def description(self) -> str:
        return self.__get_items()['snippet']['description']

    @property
    def url(self) -> str:
        return "https://www.youtube.com/" + self.__get_items()['snippet']['customUrl']

    @property
    def subscriber_count(self) -> int:
        return int(self.__get_items()['statistics']['subscriberCount'])

    @property
    def video_count(self) -> int:
        return int(self.__get_items()['statistics']['videoCount'])

    @property
    def view_count(self) -> int:
        return int(self.__get_items()['statistics']['viewCount'])

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
            json.dump(self._channel, f, indent=2, ensure_ascii=False)

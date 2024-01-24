import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
from typing import Dict

load_dotenv()


class Video:
    __API_key = os.getenv("API_key")
    __youtube = build('youtube', 'v3', developerKey=__API_key)

    def __init__(self, id: int):
        self._video: Dict = self.__youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=id).execute()
        self.__items: Dict = self._video.get('items')[0]
        self._id: int = id
        self._title: str = self.__items['snippet']['title']
        self._link: str = f"https://www.youtube.com/watch?v={id}"
        self._views: str = self.__items['statistics']['viewCount']
        self._likes: str = self.__items['statistics']['likeCount']

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._title

    @property
    def link(self) -> str:
        return self._link

    @property
    def views(self) -> int:
        return int(self._views)

    @property
    def likes(self) -> int:
        return int(self._likes)

    def __str__(self) -> str:
        return self._title



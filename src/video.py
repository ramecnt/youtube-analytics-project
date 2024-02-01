import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
from typing import Dict, Optional

load_dotenv()


class Video:
    __API_key = "AIzaSyCyuQKNvYVgQWxg3obGZV4qoA_O-qdzvrk"
    __youtube = build('youtube', 'v3', developerKey=__API_key)

    def __init__(self, id: int):
        self._id: int = id
        self._video: Dict = self.__youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=self.id).execute()
        try:
            self.__items: Dict = self._video.get('items')[0]
        except IndexError:
            self._title: None = None
            self._link: None = None
            self._views: None = None
            self._likes: None = None
        else:
            self._title: str = self.__items['snippet']['title']
            self._link: str = f"https://www.youtube.com/watch?v={id}"
            self._views: int = int(self.__items['statistics']['viewCount'])
            self._likes: int = int(self.__items['statistics']['likeCount'])

    @property
    def id(self) -> int:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def link(self) -> str:
        return self._link

    @property
    def views(self) -> Optional[int]:
        return self._views

    @property
    def like_count(self) -> Optional[int]:
        return self._likes

    def __str__(self) -> str:
        return self._title



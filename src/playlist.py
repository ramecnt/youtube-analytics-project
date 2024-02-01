import datetime
import json
import os
from pprint import pprint

import requests
import isodate

from dotenv import load_dotenv
from googleapiclient.discovery import build
from typing import Any, Optional, Dict

load_dotenv()


class PlayList:
    __API_key = os.getenv("API_key")
    __youtube = build('youtube', 'v3', developerKey=__API_key, )

    def __init__(self, playlist_id: int):
        self._playlist_id = playlist_id
        self._playlist = self.__youtube.playlistItems().list(playlistId=self._playlist_id,
                                                             part='snippet, contentDetails').execute()
        self._video_ids: list[str] = [video['contentDetails']['videoId'] for video in self._playlist['items']]
        self._video_response = self.__youtube.videos().list(part='contentDetails,statistics',
                                                            id=','.join(self._video_ids)).execute()
        self.title = requests.get(
            f"https://www.googleapis.com/youtube/v3/playlists?part=snippet%2Clocalizations&id={self._playlist_id}"
            f"&fields=items(localizations%2Csnippet%2Flocalized%2Ftitle)&key={self.__API_key}").json().get('items')[
            0].get('snippet').get('localized').get('title')
        self.url = f"https://www.youtube.com/playlist?list={self._playlist_id}"

    @property
    def total_duration(self):
        total_duration = datetime.timedelta()
        for video in self._video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        best_video = ''
        likes_max = 0
        for video in self._video_response['items']:
            if int(video['statistics']['likeCount']) > likes_max:
                best_video = video['id']
                likes_max = int(video['statistics']['likeCount'])
        return 'https://youtu.be/' + best_video

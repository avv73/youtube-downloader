import googleapiclient.discovery
import json
from urllib.parse import parse_qs, urlparse
from pytube import YouTube
import os

__api_key__ = ''

class VideoPlaylist:
    
    @property
    def video_count(self) -> int:
        return len(self.__list_objects)

    def __initialize_object_list(self):
        youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey = __api_key__, cache_discovery=False)
        request = youtube.playlistItems().list(
            part = 'snippet',
            playlistId = self.id,
            maxResults = 50
        )

        response = request.execute()
        
        playlist_items = []
        while request is not None:
            response = request.execute()
            playlist_items += response['items']
            request = youtube.playlistItems().list_next(request, response)

        for item in playlist_items:
            current_obj = YouTube('https://youtube.com/watch?v={}'.format(item['snippet']['resourceId']['videoId']))
            self.__list_objects.append(current_obj)

    def __read_api_key(self):
        path = os.path.dirname(__file__)
        file_path = os.path.join(path, 'secret.json')
        file_decode = json.load(open(file_path))
        global __api_key__
        __api_key__ = file_decode['API_Key']

    def __fetch_info(self):
        youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey = __api_key__, cache_discovery=False)

        request = youtube.playlists().list(
            part = 'snippet',
            id = self.id
        )

        response = request.execute()

        total_length = sum(obj.length for obj in self.__list_objects)

        return [response['items'][0]['snippet']['title'], response['items'][0]['snippet']['channelTitle'], total_length]

    def __init__(self, url):
        self.url = url
        self.id = parse_qs(urlparse(url).query, keep_blank_values=True)['list'][0]
        self.__list_objects = []
        self.__read_api_key()
        self.__initialize_object_list()
        self.__notify_func = lambda : True

        info_list = self.__fetch_info()
        self.title = info_list[0]
        self.author = info_list[1]
        self.length = info_list[2]

    def register_on_progress_callback(self, progress_func):
        for obj in self.__list_objects:
            obj.register_on_progress_callback(progress_func)
    
    def register_on_complete_callback(self, notify_func):
        self.__notify_func = notify_func

    def fetch_available_streams(self, is_audio_only):
        res_list = []
        if is_audio_only:
            res_list.append('[2] Audio Only')
            self.__selected_stream = 2
        else:
            res_list.append('[1] Highest possible resolution w/ audio')
            self.__selected_stream = 1
        
        return res_list

    def download(self, stream_option, save_path):
        #  stream options: 0 Highest definition with audio, 1 audio only
        streams_list = []

        for yt_inst in self.__list_objects:
            selected_stream = ''

            if stream_option == 0:
                selected_stream = yt_inst.streams.filter(progressive=True).order_by('resolution').desc()[0]
            elif stream_option == 1:
                selected_stream = yt_inst.streams.filter(only_audio=True)[0]
       
            streams_list.append(selected_stream)

        for stream in streams_list:
            stream.download(save_path)
        
        anon = type('', (object,), {'title':self.title})()

        self.__notify_func(anon, save_path)


if __name__ == '__main__':
    print('This is a library class and cannot be executed')

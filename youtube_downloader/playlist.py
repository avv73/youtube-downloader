import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse
from pytube import YouTube

class VideoPlaylist:
    __api_key = ''

    @property
    def video_count(self) -> int:
        return len(self.__list_objects)

    def __initialize_object_list(self):
        #API Calls
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = __api_key)
        request = youtube.playlistItems().list(
            part = "snippet",
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

    def __init__(self, url):
        self.url = url
        self.id = parse_qs(urlparse(url).query, keep_blank_values=True)['list'][0]
        self.__list_objects = []
        self.__initialize_object_list()
    


pl = VideoPlaylist('https://www.youtube.com/playlist?list=PLiPrjSGafY76oh0A4vpwxQ7nQ_vMiNYSk')
print(pl.video_count)
print(pl)


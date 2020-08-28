import request_exceptions
import googleapiclient.errors
import oauthlib.oauth2
#import importlib
import pytube.exceptions
import threading
from pytube import Playlist
from pytube import YouTube
from playlist import VideoPlaylist

class RequestHandler:
    def __init__(self, link_address, link_type):
        self.__requester_obj = None
        self.__streams_list = []

        try:
            if link_type == 'Video':
                self.__requester_obj = YouTube(link_address)
            else:
                self.__requester_obj = VideoPlaylist(link_address)
        except pytube.exceptions.RegexMatchError as e:
            raise request_exceptions.InvalidVideoURLException('Provided video URL is invalid!')
        except googleapiclient.errors.HttpError as e:
            raise request_exceptions.InvalidPlaylistURLException('Provided playlist URL is invalid!')

    def fetchResolutionOptions(self, is_audio_only):
        res_list = []
        
        if isinstance(self.__requester_obj, YouTube):
            if is_audio_only:
                self.__streams_list = self.__requester_obj.streams.filter(only_audio = True)
            else:
                self.__streams_list = self.__requester_obj.streams.order_by('resolution').desc()

            i = 0
            for stream in self.__streams_list:
                res_list.append('[{}] Resolution: {}, Type: {}, FPS: {}, Audio:{}, Video:{}'
                                .format(i+1, stream.resolution, stream.mime_type, stream.fps, 
                                stream.includes_audio_track, stream.includes_video_track))
                i += 1
            
        else:
            if is_audio_only:
                res_list.append('[2] Audio Only')
            else:
                res_list.append('[1] Highest possible resolution w/ audio')
            
        
        return res_list
    
    def fetchInfo(self):
        return 'Title: {}\nAuthor: {}\nDuration:{:02}:{:02}'.format(
            self.__requester_obj.title, self.__requester_obj.author, 
            self.__requester_obj.length//60, self.__requester_obj.length-60*(self.__requester_obj.length//60)
        )
    
    def downloadResource(self, stream_option, save_path, progress_func, notify_func):
        self.__requester_obj.register_on_progress_callback(progress_func)
        self.__requester_obj.register_on_complete_callback(notify_func)
        self.__streams_list[stream_option].download(save_path)
        #TODO: Create wrapper class for YouTube object.

if __name__ == '__main__':
    print('This is a library class and cannot be executed')

#rq = RequestHandler('https://www.youtube.com/watch?v=VsZLFqE_iLc', 'Video')
#list_stream = rq.fetchResolutionOptions()
#print(list_stream)
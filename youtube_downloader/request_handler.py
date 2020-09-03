import request_exceptions
import googleapiclient.errors
import oauthlib.oauth2
import pytube.exceptions
import threading
from playlist import VideoPlaylist
from video import Video

class RequestHandler:
    def __init__(self, link_address, link_type):
        self.__requester_obj = None

        try:
            if link_type == 'Video':
                self.__requester_obj = Video(link_address)
            elif link_type == 'Playlist':
                self.__requester_obj = VideoPlaylist(link_address)
            else:
                raise request_exceptions.InvalidResourceType('RequestHandler received unexpected link type. Expected: \'Video\' or \'Playlist\'')
        except pytube.exceptions.RegexMatchError as e:
            raise request_exceptions.InvalidVideoURLException('Provided video URL is invalid!')
        except googleapiclient.errors.HttpError as e:
            raise request_exceptions.InvalidPlaylistURLException('Provided playlist URL is invalid!')

    def fetchResolutionOptions(self, is_audio_only):
        res_list = self.__requester_obj.fetch_available_streams(is_audio_only)
    
        return res_list
    
    def fetchInfo(self):
        return 'Title: {}\nAuthor: {}\nDuration:{:02}:{:02}\nVideo Count:{}'.format(
            self.__requester_obj.title, self.__requester_obj.author, 
            self.__requester_obj.length//60, self.__requester_obj.length-60*(self.__requester_obj.length//60),
            self.__requester_obj.video_count
        )
    
    def downloadResource(self, stream_option, save_path, progress_func, notify_func):
        self.__requester_obj.register_on_progress_callback(progress_func)
        self.__requester_obj.register_on_complete_callback(notify_func)
        self.__requester_obj.download(stream_option, save_path)

if __name__ == '__main__':
    print('This is a library class and cannot be executed')

#rq = RequestHandler('https://www.youtube.com/watch?v=VsZLFqE_iLc', 'Video')
#list_stream = rq.fetchResolutionOptions()
#print(list_stream)
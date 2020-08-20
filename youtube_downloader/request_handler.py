import request_exceptions
import importlib
import pytube.exceptions
import threading
from pytube import Playlist
from pytube import YouTube

class RequestHandler:
    requester_obj = None

    def __init__(self, link_address, link_type):
        link_type = 'YouTube' if link_type == 'Video' else link_type
        SubstClass = getattr(importlib.import_module('pytube'), link_type)

        try:
            self.requester_obj = SubstClass(link_address)
        except pytube.exceptions.RegexMatchError:
            raise request_exceptions.InvalidVideoURLException('Provided video URL is invalid!', None)
        
        if isinstance(self.requester_obj, Playlist): # This needs addressing...
            if len(self.requester_obj.video_urls) == 0:
                raise request_exceptions.InvalidPlaylistURLException('Provided playlist URL is invalid!', None)

    def fetchResolutionOptions(self):
        res_list = []
        
        if isinstance(self.requester_obj, YouTube):
            streams_list = self.requester_obj.streams.order_by('resolution').desc()

            i = 0
            for stream in streams_list:
                res_list.append('[{}] Resolution: {}, Type: {}, FPS: {}, Audio:{}, Video:{}'
                                .format(i+1, stream.resolution, stream.mime_type, stream.fps, 
                                stream.includes_audio_track, stream.includes_video_track))
                i += 1
            
        else: #WIP
            pass
        
        return res_list
    
    def fetchInfo(self):
        if isinstance(self.requester_obj, YouTube):
            return 'Title: {}\nAuthor: {}\nDuration:{:02}:{:02}'.format(
                self.requester_obj.title, self.requester_obj.author, 
                self.requester_obj.length//60, self.requester_obj.length-60*(self.requester_obj.length//60)
            )
    
    def downloadResource(self, stream_option, save_path, progress_func):
        if isinstance(self.requester_obj, YouTube):
            self.requester_obj.register_on_progress_callback(progress_func)
            self.requester_obj.streams[stream_option].download(save_path)

if __name__ == '__main__':
    print('This is a library class and cannot be executed')

#rq = RequestHandler('https://www.youtube.com/watch?v=VsZLFqE_iLc', 'Video')
#list_stream = rq.fetchResolutionOptions()
#print(list_stream)

#rq = YouTube('https://www.youtube.com/watch?v=VsZLFqE_iLc')
#rq.streams[0].title()
from pytube import YouTube

class Video:
    def __init__(self, video_url):
        self.__yt_object = YouTube(video_url)
        self.__streams_list = []
    
        self.title = self.__yt_object.title
        self.author = self.__yt_object.author
        self.length = self.__yt_object.length

    def register_on_progress_callback(self, progress_func):
        self.__yt_object.register_on_progress_callback(progress_func)

    def register_on_complete_callback(self, notify_func):
        self.__yt_object.register_on_complete_callback(notify_func)

    @property
    def video_count(self) -> int:
        return 1

    def fetch_available_streams(self, is_audio_only):
        if is_audio_only:
            self.__streams_list = self.__yt_object.streams.filter(only_audio = True)
        else:
            self.__streams_list = self.__yt_object.streams.order_by('resolution').desc()
        
        res_list = []
        i = 0
        for stream in self.__streams_list:
            res_list.append('[{}] Resolution: {}, Type: {}, FPS: {}, Audio:{}, Video:{}'
                            .format(i+1, stream.resolution, stream.mime_type, stream.fps, 
                            stream.includes_audio_track, stream.includes_video_track))
            i += 1
        
        return res_list

    def download(self, stream_option, save_path):
        self.__streams_list[stream_option].download(save_path)

if __name__ == '__main__':
    print('This is a library class and cannot be executed')

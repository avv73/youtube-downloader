import pytube

def show_progress_bar(chunk, file_handle, bytes_remaining):
    percentage = (bytes_remaining * 1.0 / chunk.filesize * 100) - 99.99
    percentage = -percentage
    print('Download in progress... [{0:.3g}%]'.format(percentage))


youtube_link = input('Please input YouTube video link: ')

yt = pytube.YouTube(youtube_link)

available_streams_list = yt.streams
# menu and stuff....

print('Available resolutions:')
i = 0

for stream_str in available_streams_list:
    print('[{}] Resolution: {}, type: {}, fps: {}, audio: {}, video: {}'.format(
        i+1, stream_str.resolution, stream_str.mime_type, stream_str.fps, 
        stream_str.includes_audio_track, stream_str.includes_video_track))
    i += 1

stream_index = -1
while True:
    stream_index = int(input('Please select option: '.format(len(available_streams_list))))
    if stream_index not in range(1, len(available_streams_list) + 1):
        print('Provided option is invalid.')
    else:
        break


yt.register_on_progress_callback(show_progress_bar)
yt.streams[stream_index].download()

print('Download completed!')

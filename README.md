# YouTube Downloader
Simple GUI program for downloading YouTube videos and playlists

## Installation

### Required libraries:
* [pytube](https://github.com/nficano/pytube)
* [googleapiclient](https://github.com/googleapis/google-api-python-client)
* [AppJar](https://github.com/jarvisteach/appJar/)

In order to work, the program requires Youtube Data v3 API key. [Here](https://rapidapi.com/blog/how-to-get-youtube-api-key/#how-do-you-get-a-youtube-api-key) you can find instructions on how to acquire one for yourself.


Simply execute the main.py with the Python interpeter (version >= 3.0 recommended). On first run, the program will require 
the API key from the user. API Key is stored in the .json file in the program directory.

## Features

* Different resolution options can be selected for a single video. 
* Playlists can be downloaded.
* Audio only can be downloaded from a video or a playlist.

## To-do

* Simplify the installation process
* Enhance the UI
* Expand playlist features (for now only limited number of videos can be downloaded, also the check link process is a bit slow)



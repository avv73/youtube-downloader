import appJar
from request_handler import RequestHandler
import request_exceptions
import re

# Develop video download feature, with resolution select, download path and progress bar.
# Then focus on playlist implementation, library class is broken? Use Youtube API to fetch 
# URLs from a playlist and then download them one by one?
handler = None

def changeProgressBar(app, chunk, file_handle, bytes_remaining):
    percentage = (bytes_remaining * 1.0 / chunk.filesize * 100) - 99.99
    percentage = -percentage
    if percentage == 100:
        app.setMeter('progress', percentage, text='Download complete!')
    else:
        app.setMeter('progress', percentage, text='Download in progress...')

    

def downloadResource(app):
    file_path = app.getEntry('savepath')
    stream_option_raw = app.getOptionBox('Resolution options')
    stream_option = int(re.match(r"\[(\d+)\]", stream_option_raw).groups()[0]) - 1

    if file_path == '':
        app.errorBox('Error', 'Please provide download directory!')
        return

    handler.downloadResource(stream_option, file_path, lambda ch, fh, by_r : changeProgressBar(app, ch, fh, by_r))

def refreshInfo(app):
    app.changeOptionBox('Resolution options', handler.fetchResolutionOptions())
    app.setMessage('resourceInfo', handler.fetchInfo())  
    app.setButtonState('Download', 'active')

def updateInfo(app):
    link_type = app.getRadioButton('type')
    link_address = app.getEntry('Link')

    try:
        global handler
        handler = RequestHandler(link_address, link_type)
        refreshInfo(app)
    except request_exceptions.InvalidVideoURLException as e:
        app.errorBox('Error', 'An error occured: ' + e.message)
    except request_exceptions.InvalidPlaylistURLException as e:
        app.errorBox('Error', 'An error occured: ' + e.message)
    except Exception as e:
        app.errorBox('Fatal error', 'Unknown fatal error occured: ' + e.message)

def main():
    app = appJar.gui('Youtube Downloader', '600x400', showIcon=False)
    app.setLogLevel('CRITICAL')
    app.setFont(10)
    app.setIcon('icon.gif')

    app.addLabel('title', 'Youtube Downloader')
    app.setLabelBg('title', 'red')
    app.addWebLink('Make sure to check out this project at Github!', 'https://github.com/avv73/...')

    app.addRadioButton('type', 'Video')
    app.addRadioButton('type', 'Playlist')

    app.addLabelEntry('Link')
    app.addLabel('Directory to save file:')
    app.addDirectoryEntry('savepath')

    app.addLabelOptionBox('Resolution options', [])
    app.addMessage('resourceInfo', 'Waiting for input...')
    
    app.addButtons(['Check Link', 'Download'], [lambda : updateInfo(app), lambda : downloadResource(app)])
    app.setButtonState('Download', 'disabled')

    app.addMeter('progress')
    app.setMeterFill('progress', 'green')
    app.setMeter('progress', 0.0, 'Waiting for download...')
    app.go()

if __name__ == '__main__':
    main()
from request_handler import RequestHandler
import request_exceptions
import re
import time
import json.decoder

_handler = None

def changeProgressBar(app, chunk, file_handle, bytes_remaining):
    percentage = round((bytes_remaining * 1.0 / chunk.filesize * 100) - 99.99)
    percentage = -percentage

    if app.getMeter('progress')[1] != '{} %'.format(percentage) and percentage % 20 == 0: #fix this... dont update on 12.1 12.2 12.3 etc.. but on 12 24 ...
        app.setMeter('progress', percentage, text='{} %'.format(percentage))
        time.sleep(0.00001)

def notifyCompletedDownload(app, stream):    
    #while not app.eventQueue.empty():
    #    app.eventQueue.get()
    app.setMeter('progress', 100.0, text='Download complete!')
    app.infoBox('Download complete', 'The video {} has been successfully downloaded!'.format(stream.title))

def downloadResource(app):
    file_path = app.getEntry('savepath')
    stream_option_raw = app.getOptionBox('Resolution options')
    stream_option = int(re.match(r"\[(\d+)\]", stream_option_raw).groups()[0]) - 1

    if file_path == '':
        app.errorBox('Error', 'Please provide download directory!')
        return

    # Check if below code works...
    #app.thread(_handler.downloadResource, stream_option, file_path, 
    #    lambda ch, fh, by_r : app.queueFunction(changeProgressBar, app, ch, fh, by_r), 
    #    lambda strm, pth : notifyCompletedDownload(app, strm))   

    app.thread(_handler.downloadResource, stream_option, file_path, 
        lambda ch, fh, by_r : changeProgressBar(app, ch, fh, by_r),
        lambda strm, pth : notifyCompletedDownload(app, strm))

def _refreshInfo(app):
    app.changeOptionBox('Resolution options', _handler.fetchResolutionOptions())
    app.setMessage('resourceInfo', _handler.fetchInfo())  
    app.setButtonState('Download', 'active')

def updateInfo(app):
    link_type = app.getRadioButton('type')
    link_address = app.getEntry('Link')

    try:
        global _handler
        _handler = RequestHandler(link_address, link_type)
        _refreshInfo(app)
    except request_exceptions.InvalidVideoURLException as e:
        app.errorBox('Error', 'An error occured: ' + e.message)
    except request_exceptions.InvalidPlaylistURLException as e:
        app.errorBox('Error', 'An error occured: ' + e.message)
    except AttributeError as e: # Should fix attribute error exception? 'message unknown' ?s
        pass
    except KeyError as e:
        pass
    except json.decoder.JSONDecodeError as e:
        pass
    except Exception as e:
        app.errorBox('Fatal error', 'Unknown fatal error occured: ' + e.message)

if __name__ == '__main__':
    print('This is a library class and cannot be executed')
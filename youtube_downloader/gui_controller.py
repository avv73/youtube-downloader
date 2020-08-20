from request_handler import RequestHandler
import request_exceptions
import re

handler = None

def changeProgressBar(app, chunk, file_handle, bytes_remaining):
    percentage = (bytes_remaining * 1.0 / chunk.filesize * 100) - 99.99
    percentage = -percentage
    app.setMeter('progress', percentage, text='{:.1f}%'.format(percentage)) # remove enqueue? Queue gets full by this call maybe? ...

def downloadResource(app):
    file_path = app.getEntry('savepath')
    stream_option_raw = app.getOptionBox('Resolution options')
    stream_option = int(re.match(r"\[(\d+)\]", stream_option_raw).groups()[0]) - 1

    if file_path == '':
        app.errorBox('Error', 'Please provide download directory!')
        return

    # See if below code works...
    app.thread(handler.downloadResource, stream_option, file_path, lambda ch, fh, by_r : app.queueFunction(changeProgressBar, app, ch, fh, by_r))   
   #app.thread(handler.downloadResource, stream_option, file_path, lambda ch, fh, by_r : changeProgressBar(app, ch, fh, by_r))
    #app.setMeter('progress', 100.0, text='Download complete!')

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
    except AttributeError as e: # Should fix attribute error exception? 'message unknown' ?s
        pass
    except Exception as e:
        app.errorBox('Fatal error', 'Unknown fatal error occured: ' + e.message)
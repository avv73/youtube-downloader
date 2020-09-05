from request_handler import RequestHandler
import request_exceptions
import re
import time
import os
import json.decoder

_handler = None

def changeProgressBar(app, chunk, file_handle, bytes_remaining):
    percentage = round((bytes_remaining * 1.0 / chunk.filesize * 100) - 99.99)
    percentage = -percentage

    if app.getMeter('progress')[1] != '{} %'.format(percentage) and percentage % 20 == 0: 
        app.setMeter('progress', percentage, text='{} %'.format(percentage))
        time.sleep(0.00001)

def notifyCompletedDownload(app, stream):   
    app.setMeter('progress', 100, text='Download complete!')
    app.infoBox('Download complete', 'The resource {} has been successfully downloaded!'.format(stream.title))

    app.setButtonState('Download', 'active')
    app.setButtonState('Check Link', 'active')

    app.setStopFunction(lambda : True)

def confirmExitOnDownload(app):
    return app.yesNoBox('Confirm Exit', 'Download is still in progress. Are you sure you want to exit the application?')

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

    app.setButtonState('Download', 'disabled')
    app.setButtonState('Check Link', 'disabled')

    app.setStopFunction(lambda : confirmExitOnDownload(app))

    app.thread(_handler.downloadResource, stream_option, file_path, 
        lambda ch, fh, by_r : changeProgressBar(app, ch, fh, by_r),
        lambda strm, pth : notifyCompletedDownload(app, strm))

def _refreshInfo(app):
    app.changeOptionBox('Resolution options', _handler.fetchResolutionOptions(app.getCheckBox('Audio Only')))
    app.setMessage('resourceInfo', _handler.fetchInfo())  
    app.setButtonState('Download', 'active')

def checkAPIKey(app):
    path = os.path.dirname(__file__)
    file_path = os.path.join(path, 'secret.json')
    file_decode = json.load(open(file_path))
    api_readed = file_decode['API_Key']

    if api_readed != '' and api_readed != None:
        return
    
    while api_readed == '' or api_readed == None:
        api_readed = app.stringBox('API Key Required', 'Please provide Youtube Data v3 API key. Check the instructions in the Github repository on obtaining API key.')
        data = {}
        data['API_Key'] = api_readed

    with open(file_path, 'w') as output:
        json.dump(data, output)

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
        app.errorBox('Fatal error', 'Unknown fatal error occured! Please contact developer!')

if __name__ == '__main__':
    print('This is a library class and cannot be executed')
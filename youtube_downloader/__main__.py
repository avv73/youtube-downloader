import appJar
import gui_controller

# Develop video download feature, with resolution select, download path and progress bar.
# Then focus on playlist implementation, library class is broken? Use Youtube API to fetch 
# URLs from a playlist and then download them one by one?

def main():
    app = appJar.gui('Youtube Downloader', '600x400', showIcon=False)
    app.setLogLevel('CRITICAL')
    app.setFont(10)
    app.setIcon('icon.gif')
    app.addLabel('title', 'Youtube Downloader')
    app.setLabelBg('title', 'red')
    app.addWebLink('Make sure to check out this project at Github!', 'https://github.com/avv73/youtube-downloader')
    
    app.addRadioButton('type', 'Video')
    app.addRadioButton('type', 'Playlist')

    app.addLabelEntry('Link')
    app.addLabel('Directory to save file:')
    app.addDirectoryEntry('savepath')

    app.addLabelOptionBox('Resolution options', [])
    app.addMessage('resourceInfo', 'Waiting for input...')
    app.addButtons(['Check Link', 'Download'], [lambda : gui_controller.updateInfo(app), lambda : gui_controller.downloadResource(app)])
    app.setButtonState('Download', 'disabled')

    app.addMeter('progress')
    app.setMeterFill('progress', 'green')
    app.setMeter('progress', 0.0, 'Waiting for download...')

    app.go()

if __name__ == '__main__':
    main()
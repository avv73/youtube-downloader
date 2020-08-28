class InvalidVideoURLException(Exception):
    def __init__(self, message):
        super().__init__(message, None)
        self.errors = None
        self.message = message
        
class InvalidPlaylistURLException(Exception):
    def __init__(self, message):
        super().__init__(message, None)
        self.errors = None
        self.message = message

if __name__ == '__main__':
    print('This is a library class and cannot be executed')

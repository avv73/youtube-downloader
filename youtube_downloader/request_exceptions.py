class InvalidVideoURLException(Exception):
    def __init__(self, message, errors):
        super().__init__(message, errors)
        self.errors = errors
        self.message = message
        
class InvalidPlaylistURLException(Exception):
    def __init__(self, message, errors):
        super().__init__(message, errors)
        self.errors = errors
        self.message = message

if __name__ == '__main__':
    print('This is a library class and cannot be executed')

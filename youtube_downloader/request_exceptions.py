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

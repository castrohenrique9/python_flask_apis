# encoding: utf-8

class GenericException(Exception):
    """Exception to assist in throwing errors"""

    def __init__(self, message):
        self.message = {"error": message}
        super().__init__(self.message)


class DataNotFoundException(GenericException):
    """Exception when data not found on external resources"""

    def __init__(self, message):
        super().__init__(message)

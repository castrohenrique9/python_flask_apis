# encoding: utf-8


class GenericException(Exception):
    """Exception to assist in throwing errors"""

    def __init__(self, message: str):
        self.message = {"error": message}
        super().__init__(self.message)


class DataNotFoundException(GenericException):
    """Exception when data not found on external resources"""

    def __init__(self, message: str):
        super().__init__(message)


class ParameterException(GenericException):
    """Exception when parameter is wrong"""

    def __init__(self, message: str):
        super().__init__(message)


class UnauthorizedException(GenericException):
    """Exception when do not have permission"""

    def __init__(self, message: str):
        super().__init__(message)

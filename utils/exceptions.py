class AppException(BaseException):
    """Base application exception"""


class QuietException(AppException):
    """Exception that should not be traced"""


class LoudException(AppException):
    """Exception that should be traced"""

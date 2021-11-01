class CommunicationError(Exception):
    pass


class NetworkError(CommunicationError):
    pass


class ResponseError(CommunicationError):
    pass


class AuthError(ResponseError):
    pass


class PageLoadError(ResponseError):
    pass

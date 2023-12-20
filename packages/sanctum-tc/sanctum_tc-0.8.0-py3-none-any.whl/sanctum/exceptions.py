__all__ = ("HTTPException", "NotFound", "DataConflict")

class HTTPException(Exception):
    def __init__(self, status_code, data) -> None:
        self.status_code = status_code
        self.data = data
        super().__init__(f"Got {status_code} with message {data}")


class NotFound(HTTPException):
    """
    An exception that is raised when a 404 status code occurs.
    """
    pass


class DataConflict(HTTPException):
    """
    An exception that is raised when a 409 status code occurs.
    """
    pass

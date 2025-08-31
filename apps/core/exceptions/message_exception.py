from fastapi import HTTPException


class MessageException(Exception):
    def __init__(self, message_id: str, status_code: int = 400, kwargs: dict = None):
        super().__init__()
        self.message_id = message_id
        self.status_code = status_code
        self.kwargs = kwargs


class MMLException(HTTPException):
    def __init__(self, detail: str, status_code: int = 500):
        super().__init__(status_code=status_code, detail=detail)

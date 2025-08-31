class MessageException(Exception):
    def __init__(self, message_id: str, status_code: int = 400, kwargs: dict = None):
        super().__init__()
        self.message_id = message_id
        self.status_code = status_code
        self.kwargs = kwargs

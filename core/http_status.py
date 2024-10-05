from enum import Enum
class HTTP_STATUS(Enum):
    OK = (200, "OK")
    NOT_FOUND = (404, "Not Found")

    def __init__(self, code, message):
        self.code = code
        self.message = message



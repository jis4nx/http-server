from typing import Dict, Optional
import json
from .http_status import HTTP_STATUS
from abc import ABC, abstractmethod


class BaseResponse(ABC):
    def __init__(self, status: HTTP_STATUS):
        self.status = status

    def _response(self):
        response = f"HTTP/1.1 {self.status.code} {self.status.message}\r\n"
        return response

    def _build_headers(self, content_type, content_length):
        return (
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {content_length}\r\n\r\n"
        )

    @abstractmethod
    def get_response(self) -> str:
        pass


class Response(BaseResponse):
    def __init__(self, status: HTTP_STATUS, response_body: str):
        super().__init__(status)
        self.response_body = response_body

    def get_response(self) -> str:
        resp = self._response()

        headers = self._build_headers("text/html", len(self.response_body))
        resp += headers + self.response_body
        return resp

    def __repr__(self) -> str:
        return self.get_response()


class JsonResponse(BaseResponse):
    def __init__(self, status: HTTP_STATUS, data: Dict):
        super().__init__(status)
        self.status = status
        self.data = data

    def get_response(self):
        json_data = json.dumps(self.data)

        resp = self._response()
        headers = self._build_headers("application/json", len(json_data))
        resp += headers + json_data
        return resp

    def __repr__(self) -> str:
        return self.get_response()

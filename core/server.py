import asyncio
from typing import Any, Dict
from pathlib import Path
from .response import JsonResponse
import signal
import json
from .http_status import HTTP_STATUS



class HTTPServer:
    def __init__(self, host="127.0.0.1", port=8001):
        self.HOST = host
        self.PORT = port
        self.server_socket = None

        loop = asyncio.get_event_loop()
        loop.add_signal_handler(
            signal.SIGTERM, lambda: asyncio.create_task(self.shutdown())
        )
        loop.add_signal_handler(
            signal.SIGINT, lambda: asyncio.create_task(self.shutdown())
        )

    async def shutdown(self, *args):
        self.server_socket = None
        print("\nShutting Down")

    async def run_server(self) -> None:
        _server = await asyncio.start_server(
            self.handle_connection, self.HOST, self.PORT
        )
        self.server_socket = _server
        print(f"Started Serving at {self.HOST}:{self.PORT}")

        async with self.server_socket:
            while self.server_socket:
                await self.server_socket.start_serving()

    async def _response_serializer(self, writer: asyncio.StreamWriter, response):
        print(response)
        resp = response.get_response()

        writer.write(resp.encode())
        await writer.drain()

        writer.close()
        await writer.wait_closed()

    def check_path_param(self, path: str):
        return Path(path).resolve().exists()

    def _serialize_header(self, header_bytes: bytes) -> Dict:
        header: Dict[str, Any] = {}
        HTTP_METHODS = ["GET", "POST", "PUT", "PATCH"]

        request_headers = header_bytes.decode().splitlines()

        for line in request_headers:
            if any(method in line for method in HTTP_METHODS):
                parts = line.split()
                header["Method"] = parts[0]
                header["Path"] = parts[1]
                header["Ver"] = parts[2]
            elif line.startswith("Host:"):
                header["Host"] = line.split()[1]
            elif line.startswith("User-Agent:"):
                header["User-Agent"] = line.split()[1]
            elif line.startswith("Accept:"):
                header["Accept"] = line.split()[1]

        return header

    async def handle_connection(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        data = await reader.read(1024)
        header = self._serialize_header(data)
        path = header.get("Path", "/")
        status = HTTP_STATUS.OK

        if path != "/":
            is_path = self.check_path_param(path)
            if not is_path:
                status = HTTP_STATUS.NOT_FOUND
                response_body = json.dumps({"error": "Not Found"})
        json_resp = JsonResponse(status, data={"msg": "Noice"})
        await self._response_serializer(writer, json_resp)

import asyncio
from .server import HTTPServer


async def main():
    PORT = 8001
    server = HTTPServer(port=PORT)
    await server.run_server()


if __name__ == "__main__":
    asyncio.run(main())

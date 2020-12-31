import asyncio
import logging
import websockets
from websockets import WebSocketServerProtocol

logging.basicConfig(level=logging.INFO)


async def produce(message: str, host: str, port: int) -> None:
    async with websockets.connect(f"ws://{host}:{port}") as ws:
        await ws.send(message)
        print("RESULT" + await ws.recv())


async def consumer_handler(websocket: WebSocketServerProtocol) -> None:
    async for message in websocket:
        log_message(message)


async def consume(host: str, port: int) -> None:
    websocket_resource_url = f"ws://{host}:{port}"
    async with websockets.connect(websocket_resource_url) as websocket:
        await consumer_handler(websocket)


def log_message(message: str) -> None:
    logging.info(f"Message: {message}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        produce(host="localhost", port=5000, message="{\"method\":\"getSession\",\"parameters\":{\"sid\":1000}}"))

    loop.run_forever()

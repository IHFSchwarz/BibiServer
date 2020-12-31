import asyncio
import sys

import websockets


async def chat():
    async with websockets.connect('ws://localhost:5000') as websocket:
        while (True):
            print("Enter message to server (type 'q' to exit), str+z to eof:")
            sys.stdin.flush()
            msg = sys.stdin.readlines()
            print("received EOF")
            if msg == "q":
                break
            await websocket.send(msg)
            msg = await websocket.recv()
            print(f"From Server: {msg}")


asyncio.get_event_loop().run_until_complete(chat())

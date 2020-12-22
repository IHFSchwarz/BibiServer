import asyncio
import json
import logging
import websockets
from websockets import WebSocketServerProtocol


class Server:
    clients = set()
    sessions = set()

    async def register(self, ws: WebSocketServerProtocol) -> None:
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects.')

    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects.')

    async def send_to_clients(self, message: str) -> None:
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    async def ws_handler(self, ws: WebSocketServerProtocol, uri: str) -> None:
        await self.register(ws)
        try:
            await self.use_message(ws)
            # await self.distribute(ws)
        finally:
            await self.unregister(ws)

    async def getSession(self, ws: WebSocketServerProtocol, parameters):
        session_id = parameters["sid"]
        if session_id in self.sessions:
            await ws.send("Session already registered " + session_id)
            print("sent")
        else:
            await ws.send("Session registered " + session_id)
            print("sent")

        print(session_id)
        print("Lol")
        return "lol"


    async def use_message(self, ws: WebSocketServerProtocol) -> None:
        async for message in ws:
            messagejson = json.loads(message)
            method = messagejson["method"]
            parameters = messagejson["parameters"]
            func = getattr(self, method, print("invalid"))
            func(parameters, ws)
            #ws.send(message)

    async def distribute(self, ws: WebSocketServerProtocol) -> None:
        async for message in ws:
            await self.send_to_clients(message)


logging.basicConfig(level=logging.INFO)
server = Server()
start_server = websockets.serve(server.ws_handler, 'localhost', 5000)
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()
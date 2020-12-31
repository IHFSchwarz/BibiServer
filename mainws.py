import asyncio
import json
import logging
import websockets
import uuid
from websockets import WebSocketServerProtocol


class Server:
    clients = dict()
    sessions = dict()
    gamestate = dict()

    async def register(self, ws: WebSocketServerProtocol) -> None:
        self.clients[ws] = uuid.uuid4()
        logging.info(f'{ws.remote_address} connects.')

    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        del self.clients[ws]
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

    async def send_to_client(self, client, message: str) -> None:
        await asyncio.wait([client.send(message)])

    async def distribute(self, ws: WebSocketServerProtocol) -> None:
        async for message in ws:
            await self.send_to_clients(message)

    def __init__(self):
        self.gamestate["users"] = dict()
        self.gamestate["isBuzzerLocked"] = False

    async def use_message(self, ws: WebSocketServerProtocol) -> None:
        async for message in ws:
            try:
                messagejson = json.loads(message)
                method = messagejson["method"]
                parameters = messagejson["parameters"]
                func = getattr(self, method, print("invalid"))
                await func(ws, parameters)
            except json.JSONDecodeError:
                e = "JSON-Fehler, input: "
                print(e)
                await ws.send(e + message)
            # ws.send(message)

    async def distributeGamestate(self) -> None:
        msg = json.dumps(self.gamestate)
        send_to_clients(self, msg)

    async def getSession(self, ws: WebSocketServerProtocol, parameters):
        session_id = parameters["sid"]
        username = parameters["username"]

        if session_id in self.sessions: # Session already registered
            #await ws.send("Session already registered " + str(session_id))

        else:
            self.sessions.update({session_id: self.clients[ws]})
            await ws.send("Session registered " + str(session_id))
            print("sent")
        return "lol"


logging.basicConfig(level=logging.INFO)
server = Server()
start_server = websockets.serve(server.ws_handler, 'localhost', 5000)
loop = asyncio.get_event_loop()
print("Starting server")
loop.run_until_complete(start_server)
loop.run_forever()

from flask import Flask
from flask_sockets import Sockets
from flask.json import jsonify
import json

app = Flask(__name__)
sockets = Sockets(app)
def getSession(messagejson):
    print("GETSESSION")


@sockets.route('/ws')
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        messagejson = json.loads(message)
        method = messagejson["method"]
        switcher = {
            "getSession": getSession
        }
        func = switcher.get(method, lambda: "Invalid")
        func(messagejson)
        ws.send(message)

@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
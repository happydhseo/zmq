import os
import logging
import gevent
import zmq
import json
from flask import Flask, render_template
from flask_sockets import Sockets

gevent.monkey.patch_all()

app = Flask(__name__)
app.debug = 'DEBUG' in os.environ

sockets = Sockets(app)
context = zmq.Context()

ZMQ_LISTENING_PORT = 6557

class WebSocketBackend(object):
    """Interface for registering and updating WebSocket clients."""

    def __init__(self):
        self.clients = []

    def register(self, client):
        """Register a WebSocket connection for live updates."""
        self.clients.append(client)

    def send(self, client, data):
        """Send given data to the registered client.
        Automatically discards invalid connections."""
        try:
            client.send(data)
        except Exception:
            self.clients.remove(client)

    def run(self):
        """Listens for new messages in zmq, and sends them to clients."""
        """set up a zeromq context"""
        context = zmq.Context()

        """create a socket for receiving data from the zmq sink"""
        recv_socket = context.socket(zmq.SUB)
        recv_socket.connect("tcp://localhost:{PORT}".format(PORT=ZMQ_LISTENING_PORT))
        while True:
            gevent.sleep(0.1)
            data = recv_socket.recv()
            for client in self.clients:
                gevent.spawn(self.send, client, data)

    def start(self):
        """Maintains zmq  background."""
        gevent.spawn(self.run)

# websocks = WebSocketBackend()
# websocks.start()


@app.route('/')
def index():
    return render_template('index.html')


@sockets.route('/zeromq')
def send_data(ws):
    socket = context.socket(zmq.SUB)
    socket.connect('tcp://localhost:{PORT}'.format(PORT=ZMQ_LISTENING_PORT))
    socket.setsockopt(zmq.SUBSCRIBE, "")
    # ws.send(json.dumps([1, 2, 3]))
    while True:
        data = socket.recv_json()
        ws.send(json.dumps(data))
    gevent.sleep(0.1)

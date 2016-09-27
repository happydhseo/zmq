import os
import logging
import gevent
import zmq
from flask import Flask, render_template
from flask_sockets import Sockets

app = Flask(__name__)
app.debug = 'DEBUG' in os.environ

sockets = Sockets(app)
ZMQ_LISTENING_PORT = 9559


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
        """Listens for new messages in Redis, and sends them to clients."""
        """set up a zeromq context"""
        context = zmq.Context()

        """create a socket for receiving data from the zmq sink"""
        recv_socket = context.socket(zmq.SUB)
        recv_socket.connect("tcp://localhost:{PORT}".format(port=ZMQ_LISTENING_PORT))
        while True:
            data = recv_socket.recv()
            for client in self.clients:
                gevent.spawn(self.send, client, data)

    def start(self):
        """Maintains zmq  background."""
        gevent.spawn(self.run)

websocks = WebSocketBackend()
websocks.start()


@app.route('/')
def index():
    return render_template('index.html')


@sockets.route('/receive')
def send_data(ws):
    """Sends outgoing chat messages from WebSocketBackend."""
    websocks.register(ws)

    while not ws.closed:
        # Context switch while `ChatBackend.start` is running in the background.
        gevent.sleep(0.1)

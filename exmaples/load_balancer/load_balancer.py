from __future__ import print_function
from multiprocessing import Process
import zmq
import time
import uuid
import random

def client_task():
    """Basic request-reply client using REQ socket."""
    socket = zmq.Context().socket(zmq.REQ)
    socket.identity = str(uuid.uuid4())
    socket.connect("ipc://frontend.ipc")
    # Send request, get reply
    for i in range(100):
        print("SENDING: ", i)
        socket.send('WORK')
        msg = socket.recv()
        print(msg)

def worker_task():
    """Worker task, using a REQ socket to do load-balancing."""
    socket = zmq.Context().socket(zmq.REQ)
    socket.identity = str(uuid.uuid4())
    socket.connect("ipc://backend.ipc")
    # Tell broker we're ready for work
    socket.send(b"READY")
    while True:
        address, empty, request = socket.recv_multipart()
        time.sleep(random.randint(1, 4))
        socket.send_multipart([address, b"", b"OK : " + str(socket.identity)])


def broker():
    context = zmq.Context()
    frontend = context.socket(zmq.ROUTER)
    frontend.bind("ipc://frontend.ipc")
    backend = context.socket(zmq.ROUTER)
    backend.bind("ipc://backend.ipc")
    # Initialize main loop state
    workers = []
    poller = zmq.Poller()
    # Only poll for requests from backend until workers are available
    poller.register(backend, zmq.POLLIN)

    while True:
        sockets = dict(poller.poll())
        if backend in sockets:
            # Handle worker activity on the backend
            request = backend.recv_multipart()
            worker, empty, client = request[:3]
            if not workers:
                # Poll for clients now that a worker is available
                poller.register(frontend, zmq.POLLIN)
            workers.append(worker)
            if client != b"READY" and len(request) > 3:
                # If client reply, send rest back to frontend
                empty, reply = request[3:]
                frontend.send_multipart([client, b"", reply])

        if frontend in sockets:
            # Get next client request, route to last-used worker
            client, empty, request = frontend.recv_multipart()
            worker = workers.pop(0)
            backend.send_multipart([worker, b"", client, b"", request])
            if not workers:
                # Don't poll clients if no workers are available
                poller.unregister(frontend)

    # Clean up
    backend.close()
    frontend.close()
    context.term()

def main():
    NUM_CLIENTS = 1
    NUM_WORKERS = 10
    # Start background tasks
    def start(task, *args):
        process = Process(target=task, args=args)
        process.start()
    start(broker)

    for i in range(NUM_CLIENTS):
        start(client_task)

    for i in range(NUM_WORKERS):
        start(worker_task)

    
    # Process(target=broker).start()


    

if __name__ == "__main__":
    main()
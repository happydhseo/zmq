import zmq
import uuid
def run():
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    identity = str(uuid.uuid4())
    socket.identity = identity.encode('ascii')
    socket.connect('ipc://frontend')
    print 'Client %s started' % (identity)
    poll = zmq.Poller()
    poll.register(socket, zmq.POLLIN)
    reqs = 0
    while True:
        reqs = reqs + 1
        print('Req #%d sent..' % (reqs))
        socket.send_string(u'request #%d' % (reqs))
        sockets = dict(poll.poll(10))
        if socket in sockets:
            msg = socket.recv()
            print 'Client %s received: %s' % (identity, msg)

    socket.close()
    context.term()

if __name__ == '__main__':
    run()
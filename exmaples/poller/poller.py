import zmq

#  Prepare our context and sockets
context = zmq.Context()

rep = context.socket(zmq.REP)
rep.bind("tcp://*:15000")

sub = context.socket(zmq.SUB)
sub.connect("tcp://localhost:20000")

# Initialize poll set
poller = zmq.Poller()
poller.register(rep, zmq.POLLIN)
poller.register(sub, zmq.POLLIN)
while True:
    socks = dict(poller.poll())

    if socks.get(rep) == zmq.POLLIN:
        message = rep.recv()
        # do something with message
        rep.send(something)

    if socks.get(sub) == zmq.POLLIN:
        message = sub.recv()
        # do something with message

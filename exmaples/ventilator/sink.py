import zmq


def sink():
    """set up a zmq context"""
    context = zmq.Context()

    """create a pull socket for receiving results from the workers"""
    recv_socket = context.socket(zmq.PULL)
    recv_socket.bind("tcp://*:6001")

    while True:
        msg = recv_socket.recv()
        print msg

if __name__ == '__main__':
  sink()
import zmq
import time
import random

def run():
    context = zmq.Context()
    worker = context.socket(zmq.DEALER)
    worker.connect('ipc://backend')
    print 'Worker started'
    while True:
        ident, msg = worker.recv_multipart()
        print 'Worker received %s from %s' % (msg, ident)
        replies = random.randint(0, 4)
        for i in range(replies):
            time.sleep(random.random())
            worker.send_multipart([ident, msg])

    worker.close()
    context.term()

if __name__ == '__main__':
    run()

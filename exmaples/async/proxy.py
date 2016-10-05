import zmq

def run():
    context = zmq.Context()
    frontend = context.socket(zmq.ROUTER)
    frontend.bind('ipc://frontend')

    backend = context.socket(zmq.DEALER)
    backend.bind('ipc://backend')

    zmq.proxy(frontend, backend)

    # 
    # Clean up
    backend.close()
    frontend.close()
    context.term()
if __name__ == '__main__':
    run()
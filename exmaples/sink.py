import zmq
import time
 
"""set up a zmq context"""
context = zmq.Context()

"""create a pull socket for receiving results from the workers"""
recv_socket = context.socket(zmq.PULL)
recv_socket.connect("tcp://localhost:9556")

"""create a push socket for sending acknowledgements to the ventilator"""
send_socket = context.socket(zmq.PUSH)
send_socket.bind("tcp://127.0.0.1:9557")

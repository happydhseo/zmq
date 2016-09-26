package main

import zmq "github.com/alecthomas/gozmq"

func main() {
  context, _ := zmq.NewContext()
  socket, _ := context.NewSocket(zmq.REP)
  socket.Connect("tcp://127.0.0.1:5000")

  for {
    msg, _ := socket.Recv(0)
    println("Got", string(msg))
    socket.Send(msg, 0)
  }
}
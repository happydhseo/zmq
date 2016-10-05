package main

import (
	"fmt"
	zmq "github.com/pebbe/zmq4"
	"strconv"
	"time"
)

func main() {
	pull, _ := zmq.NewSocket(zmq.PULL)
	defer pull.Close()
	pull.Connect("tcp://localhost:6000")

	push, _ := zmq.NewSocket(zmq.PUSH)
	defer push.Close()
	push.Connect("tcp://localhost:6001")

	for {
		msg, _ := pull.Recv(0)
		fmt.Printf("golang got: '%s'\n", msg)
		delay, _ := strconv.ParseFloat(msg, 64)

		var out = "golang did work: " + msg
		// time.Sleep(time.Duration(strconv.ParseFloat(msg, 64)))
		time.Sleep(time.Duration(delay*1000) * time.Millisecond)
		push.Send(out, 0)

	}
}
